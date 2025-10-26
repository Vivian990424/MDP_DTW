import multiprocessing
import os.path
import time
import numpy as np
try:
    from osgeo import gdal
except:
    import gdal
from scipy.signal import savgol_filter

from commons.all_common_infos import *
from mapping.mapping_func import (find_floods, find_matures, get_valid_arr,
                                  get_indexs_from_doy, get_latest_mature_index, read_VIs, make_VIs_npy,
                                  check_results, write_no_rice)
from mapping.compute_similarity import dtw_matching

from tools.file.files_process import is_fold_exist, delete_file
from tools.raster.raster_process import create_raster
from tools.time.time_process import get_year_daynum



def single_rice_mapping(year, tile, land_desc, crop_desc, threshold, ref,
                        flood_doy_range, flood_factor, grow_range, latest_mature, NDVI_ceiling,
                        para_region, rate=rate_daily, pool_num=20, wait=0):
    time.sleep(wait)

    start_time = time.time()
    method_info = get_method_desc(product_out_500m, para_region, purity, threshold, flood_doy_range, flood_factor, grow_range, NDVI_ceiling)

    if para_region in ['Australia', 'Brazil']:
        read_next_year, image_num = True, get_year_daynum(year) + get_year_daynum(year + 1)
    else:
        read_next_year, image_num = False, get_year_daynum(year)
    if year == 2000:
        image_num -= lack_daynum_2000

    # check: if output already exist
    flag, out_paths = check_results(year, tile, para_region, method_info)
    if flag:
        return 1

    # valid_positions
    flag, valid_positions, valid_arr, prj, trf = get_valid_arr(year, tile, land_desc, crop_desc, para_region, method_info)
    if flag != 0:
        return -1
    print(f"{year} {tile} {para_region} valid_positions={valid_positions.shape} valid_arr_shape={valid_arr.shape}")

    # potential floods
    flood_potential_indexs = get_indexs_from_doy(year, flood_doy_range)
    latest_mature_index = get_latest_mature_index(image_num, latest_mature)
    print(f"{year} {tile} {para_region} flood_potential_indexs={flood_potential_indexs}")

    pool_size = valid_positions.shape[0] // pool_num
    # single pool
    if pool_num < 2 or pool_size == 0:
        # read VIs
        f3, r3 = read_VIs(year, tile, next_year=read_next_year)
        if f3 < 0:
            return -2
        # NDVI_num, NDVI_images, LSWI_num, LSWI_images = r3
        if r3[0] != image_num or r3[2] != image_num:
            print(f"[ERROR] {year} {tile} image num error: image_num={image_num}, NDVI_num={r3[0]}, LSWI_num={r3[2]}")
            return -3
        print(f"{year} {tile} {para_region} shape of images: NDVI={r3[1].shape}, LSWI={r3[3].shape}")

        out_flood_arr = np.zeros(valid_arr.shape, dtype=np.int16)
        out_mature_arr = np.zeros(valid_arr.shape, dtype=np.int16)
        out_distance_arr = np.zeros(valid_arr.shape, dtype=np.float)
        for p in valid_positions:
            flood_index, mature_index, min_d = \
                single_rice(r3[1][:, p[0], p[1]], r3[3][:, p[0], p[1]], threshold, ref,
                            flood_potential_indexs, flood_factor,
                            grow_range, latest_mature_index, NDVI_ceiling, rate)

            out_distance_arr[p[0]][p[1]] = min_d
            if flood_index >= 0:
                out_flood_arr[p[0]][p[1]] = flood_index + 1  # 输出洪水日doy
                out_mature_arr[p[0]][p[1]] = mature_index + 1  # 输出成熟日doy

    # multi pool
    else:
        # caching
        NDVI_npy = get_VI_npy(year, tile, para_region, NDVI_npy_root)
        LSWI_npy = get_VI_npy(year, tile, para_region, LSWI_npy_root)
        flag3 = make_VIs_npy(year, tile, para_region, image_num, read_next_year, valid_arr, NDVI_npy, LSWI_npy)
        if flag3 < 0:
            print(f"[ERROR] {year} {tile} {para_region} make_VIs_npy")
            return -3

        print(f"{year} {tile} {para_region}: pool_num={pool_num} pool_size={pool_size}")
        son_paras = []
        for k in range(pool_num):
            pool_start = k * pool_size
            if k != (pool_num - 1):
                pool_end1 = (k + 1) * pool_size
                # pool_positions = valid_positions[pool_start:pool_end1]
            else:
                pool_end1 = valid_positions.shape[0]
                # pool_positions = valid_positions[pool_start:]
            son_paras.append([pool_start, pool_end1,
                              NDVI_npy, LSWI_npy, ref, threshold,
                              flood_factor, flood_potential_indexs,
                              NDVI_ceiling, grow_range, latest_mature_index, rate])
        pool = multiprocessing.Pool(pool_num)
        rs = pool.starmap(single_rice_mapping_positions, son_paras)
        pool.close()
        pool.join()

        # merge results in order
        flood_doys = []
        mature_doys = []
        distances = []
        for r in rs:
            flood_doys += r[0]
            mature_doys += r[1]
            distances += r[2]

        # write
        out_flood_arr = np.zeros(valid_arr.shape, dtype=np.int16)
        out_flood_arr[valid_arr == 1] = np.array(flood_doys)
        out_mature_arr = np.zeros(valid_arr.shape, dtype=np.int16)
        out_mature_arr[valid_arr == 1] = np.array(mature_doys)
        out_distance_arr = np.zeros(valid_arr.shape, dtype=np.float)
        out_distance_arr[valid_arr == 1] = np.array(distances)

    if year == 2000:
        out_flood_arr[out_flood_arr > 0] += lack_daynum_2000
        out_mature_arr[out_mature_arr > 0] += lack_daynum_2000

    out_distance_arr[out_distance_arr > 300] = 300  # prevent overflow: int16[-32768, 32767]
    out_distance_arr[out_distance_arr > 0] *= scale_dtw_distance
    out_distance_arr[valid_arr != 1] = -9

    if np.sum(out_flood_arr > 0) < 1:
        end_time = time.time()
        write_no_rice(year, tile, para_region, method_info)
        print(f"{year} {tile} {para_region} no rice, time={(end_time - start_time) / 60 / 60:.3f}h")
        return 2

    # create output
    out_flood_path, out_mature_path, out_distance_path = out_paths
    is_fold_exist(os.path.dirname(out_flood_path))
    create_raster(out_flood_path, out_flood_arr, trf[1], prj, trf, setnodata=True, nodata=0, datatype=gdal.GDT_Int16)
    create_raster(out_mature_path, out_mature_arr, trf[1], prj, trf, setnodata=True, nodata=0, datatype=gdal.GDT_Int16)
    create_raster(out_distance_path, out_distance_arr, trf[1], prj, trf, setnodata=False, datatype=gdal.GDT_Int16)

    # delete caches
    if pool_num >= 2 and pool_size != 0:
        delete_file(NDVI_npy)
        delete_file(LSWI_npy)

    end_time = time.time()
    print(f"{year} {tile} {para_region} time for single mapping is {(end_time - start_time) / 60 / 60:.3f}h: {method_info}")
    return 0


def single_rice_mapping_positions(start, end1,
                                  NDVI_npy, LSWI_npy, ref_series, threshold,
                                  flood_factor, flood_potential_indexs,
                                  NDVI_ceiling, grow_range, latest_mature_index, rate):
    st = time.time()
    flood_doys = []
    mature_doys = []
    distances = []
    all_NDVIs = np.load(NDVI_npy, mmap_mode='r')[start:end1]
    all_LSWIs = np.load(LSWI_npy, mmap_mode='r')[start:end1]
    print(f"{start}~{end1 - 1} single positions: NDVI={all_NDVIs.shape} LSWI={all_LSWIs.shape}")

    for k in range(end1 - start):  # range(start, end1):
        flood_index, mature_index, min_d = \
            single_rice(all_NDVIs[k], all_LSWIs[k], threshold, ref_series,
                        flood_potential_indexs, flood_factor,
                        grow_range, latest_mature_index, NDVI_ceiling, rate)

        distances.append(min_d)  # minimum distance (negative values indicate no rice)
        if flood_index >= 0:
            flood_doys.append(flood_index + 1)  # flood doy
            mature_doys.append(mature_index + 1)  # mature doy
        else:
            flood_doys.append(0)
            mature_doys.append(0)

    et = time.time()
    print(f"{start}~{end1-1} single positions: mapping time is {(et - st) / 60 / 60:.3f} h, flood_doy={np.min(flood_doys)}~{np.max(flood_doys)}, mature_doy={np.min(mature_doys)}~{np.max(mature_doys)}")
    return flood_doys, mature_doys, distances


def single_rice(NDVIs_raw, LSWIs_raw, threshold, ref, flood_potential_indexs, flood_factor, grow_range, latest_mature_index, NDVI_ceiling, rate):
    NDVIs_filtered = savgol_filter(NDVIs_raw, SG_win_length_daily, SG_poly_daily)
    flood_indexs = find_floods(NDVIs_filtered, LSWIs_raw, flood_potential_indexs, flood_factor, NDVI_ceiling)
    if len(flood_indexs) < 1:
        return -1, -1, -1

    potentials = []
    for flood_index in flood_indexs:
        mature_indexs = find_matures(NDVIs_filtered, flood_index, grow_range, latest_mature_index, rate, NDVI_ceiling)
        for mature_index in mature_indexs:
            align, d = dtw_matching(NDVIs_filtered[flood_index:mature_index+1], ref)
            potentials.append([d, flood_index, mature_index])
    if len(potentials) < 1:
        return -2, -2, -2

    min_d_index = np.argmin(np.array(potentials)[:, 0], axis=0)
    # if 0 <= potentials[min_d_index][0] <= threshold:
    #     return potentials[min_d_index][1], potentials[min_d_index][2], potentials[min_d_index][0]
    return potentials[min_d_index][1], potentials[min_d_index][2], potentials[min_d_index][0]
