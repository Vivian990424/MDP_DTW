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
                                  check_results, write_no_rice, get_no_rice_tiles)
from mapping.compute_similarity import dtw_matching

from tools.files_process import is_file_good, is_fold_exist, delete_file
from tools.raster_process import read_raster, create_raster
from tools.time_process import get_year_daynum


def get_multi_infos(year, para_region, purity, threshold, flood_doy_range, flood_factor, grow_range, NDVI_ceiling):
    method_info = get_method_desc(product_out_500m, para_region, purity, threshold, flood_doy_range, flood_factor, grow_range, NDVI_ceiling)

    if flood_doy_range is None:
        flood_doy_range = [1, get_year_daynum(year)]

    if para_region in ['ChinaDN', 'ChinaCJZXY']:  # SouthEast China
        read_next_year, image_num = False, get_year_daynum(year)
    else:
        read_next_year, image_num = True, get_year_daynum(year) + get_year_daynum(year + 1)

    if year == 2000:
        image_num -= lack_daynum_2000
    return method_info, flood_doy_range, read_next_year, image_num


def multi_rice_mapping(year, tile, land_desc, crop_desc, threshold, ref,
                       flood_doy_range, flood_factor, grow_range, latest_mature, NDVI_ceiling,
                       para_region, rate=rate_daily, pool_num=20, wait=0):
    """
    out: multi bands (.tif)
    distance: -9=non_mapping, -2=no_season, -1=no_flood
    """

    time.sleep(wait)

    start_time = time.time()
    method_info, flood_doy_range, read_next_year, image_num = \
        get_multi_infos(year, para_region, purity, threshold, flood_doy_range, flood_factor, grow_range, NDVI_ceiling)

    flag, out_paths = check_results(year, tile, para_region, method_info)
    if flag:
        return 1

    flag, valid_positions, valid_arr, prj, trf = get_valid_arr(year, tile, land_desc, crop_desc, para_region, method_info)
    if flag != 0:
        return -1
    print(f"{year} {tile} {para_region} valid_positions={valid_positions.shape} valid_arr_shape={valid_arr.shape}")

    # latest maturity day of the previous year (the flooding day of the current year must be later than this)
    if (year == 2000) or (tile in get_no_rice_tiles(year-1, method_info)):  # 起始年 / 上年无水稻， 则今年从 0 开始识别
        previous_mature_index_arr = np.zeros(valid_arr.shape)
    else:
        previous_mature_path = get_result_tif(year-1, tile, method_info=method_info, algorithm='multi', data_type='mature-day')
        if is_file_good(previous_mature_path, prt=True) != 0:
            print(f"[ERROR] {year} {tile} {para_region} previous year mature not exist: {previous_mature_path}")
            return -2
        previous_mature_index_arr = read_raster(previous_mature_path, 'arr')[0] % 1000 - 1 - get_year_daynum(year-1)
    print(f"{year} {tile} {para_region} latest previous_mature_index={np.max(previous_mature_index_arr)}")
    # starting flooding day of current year
    start_doy = get_doy_start(year)
    print(f"{year} {tile} {para_region} start_doy={start_doy}")

    flood_potential_indexs = get_indexs_from_doy(year, flood_doy_range)
    latest_mature_index = get_latest_mature_index(image_num, latest_mature)
    print(f"{year} {tile} {para_region} flood_potential_indexs={flood_potential_indexs}")

    pool_size = valid_positions.shape[0] // pool_num

    if pool_num < 2 or pool_size == 0:

        f3, r3 = read_VIs(year, tile, next_year=read_next_year)
        if f3 < 0:
            return -3
        # NDVI_num, NDVI_images, LSWI_num, LSWI_images = r4  # NDVI_images.shape= year_num * row * col
        if r3[0] != image_num or r3[2] != image_num:
            print(f"[ERROR] {year} {tile} image num error: image_num={image_num}, NDVI_num={r3[0]}, LSWI_num={r3[2]}")
            return -3
        print(f"{year} {tile} {para_region} shape of images: NDVI={r3[1].shape}, LSWI={r3[3].shape}")

        out_flood_arr = np.zeros(valid_arr.shape, dtype=np.int64)
        out_mature_arr = np.zeros(valid_arr.shape, dtype=np.int64)
        out_distance_arr = np.zeros(valid_arr.shape, dtype=np.int64)

        for p in valid_positions:
            d_str, flood_doy_str, mature_doy_str = \
                multi_rice(r3[1][:, p[0], p[1]], r3[3][:, p[0], p[1]], threshold, ref,
                           flood_potential_indexs, previous_mature_index_arr[p[0], p[1]], flood_factor,
                           grow_range, latest_mature_index, NDVI_ceiling, rate, start_doy)

            out_distance_arr[p[0]][p[1]] = int(d_str)
            out_flood_arr[p[0]][p[1]] = int(flood_doy_str)
            out_mature_arr[p[0]][p[1]] = int(mature_doy_str)

    else:
        NDVI_npy = get_VI_npy(year, tile, para_region, NDVI_npy_root)
        LSWI_npy = get_VI_npy(year, tile, para_region, LSWI_npy_root)
        flag3 = make_VIs_npy(year, tile, para_region, image_num, read_next_year, valid_arr, NDVI_npy, LSWI_npy)
        if flag3 < 0:
            print(f"[ERROR] {year} {tile} {para_region} make_VIs_npy")
            return -3

        NDVI_npy_arr = np.load(NDVI_npy, mmap_mode='r')
        NDVI_npy_length = NDVI_npy_arr.shape[0]
        LSWI_npy_arr = np.load(LSWI_npy, mmap_mode='r')
        LSWI_npy_length = LSWI_npy_arr.shape[0]
        if NDVI_npy_length != valid_positions.shape[0] or LSWI_npy_length != valid_positions.shape[0]:
            print(f"[ERROR] {year} {tile} {para_region} npy_length({NDVI_npy_length}, {LSWI_npy_length}) != valid_positions_num({valid_positions.shape[0]})")
            return -3

        previous_mature_indexs = previous_mature_index_arr[valid_arr == 1]
        pool_size = valid_positions.shape[0] // pool_num
        print(f"{year} {tile} {para_region}: pool_num={pool_num} pool_size={pool_size}")
        son_paras = []
        for k in range(pool_num):
            pool_start = k * pool_size
            if k != (pool_num - 1):
                pool_end1 = (k + 1) * pool_size
            else:
                pool_end1 = valid_positions.shape[0]
            son_paras.append([pool_start, pool_end1,
                              NDVI_npy, LSWI_npy, ref, threshold,
                              flood_factor, flood_potential_indexs, previous_mature_indexs[pool_start: pool_end1],
                              NDVI_ceiling, grow_range, latest_mature_index, rate, start_doy
                              ])
        # previous_mature_indexs = None
        pool = multiprocessing.Pool(pool_num)
        rs = pool.starmap(multi_rice_mapping_positions_new, tuple(son_paras))
        pool.close()
        pool.join()

        flood_doys = []
        mature_doys = []
        distances = []
        for r in rs:  # return distances, flood_doys, mature_doys
            distances += r[0]
            flood_doys += r[1]
            mature_doys += r[2]

        out_distance_arr = np.zeros(valid_arr.shape, dtype=np.int64)
        out_distance_arr[valid_arr == 1] = np.array(distances)
        out_flood_arr = np.zeros(valid_arr.shape, dtype=np.int64)
        out_flood_arr[valid_arr == 1] = np.array(flood_doys)
        out_mature_arr = np.zeros(valid_arr.shape, dtype=np.int64)
        out_mature_arr[valid_arr == 1] = np.array(mature_doys)

    # distance keeps two decimal places: int16[-32768, 32767]
    out_distance_arr[valid_arr != 1] = -9
    # prevent a single distance from being split into two (the maximum value for one distance is 99.99)
    out_distance_arr[(out_distance_arr > 9999) & (out_flood_arr < 999)] = 9999

    if np.sum(out_distance_arr >= 0) < 1:
        end_time = time.time()
        write_no_rice(year, tile, para_region, method_info)
        print(f"{year} {tile} {para_region} no rice, time={(end_time - start_time) / 60 / 60:.3f}h")
        return 2

    # stratified (layered)
    flood_arrs, mature_arrs, distance_arrs = [], [], []
    tmp_flood_arr, tmp_mature_arr, tmp_distance_arr = out_flood_arr, out_mature_arr, out_distance_arr
    while np.sum(tmp_flood_arr > 0) > 0:
        band_flood_arr = (tmp_flood_arr % 1000).astype(np.int16)
        band_mature_arr = (tmp_mature_arr % 1000).astype(np.int16)
        if np.sum(band_flood_arr == 0) != np.sum(band_mature_arr == 0):
            print(f"[ERROR] !!! {year} {tile} {para_region} flood_season != mature_season")
        band_distance_arr = (tmp_distance_arr % 10000).astype(np.int16)
        # pixels without seasons, change distance from 0 to 99.99
        band_distance_arr[(band_flood_arr == 0) & (band_distance_arr == 0)] = 9999
        # invalid values (not mapping)
        band_distance_arr[out_distance_arr < 0] = out_distance_arr[out_distance_arr < 0]

        flood_arrs.append(band_flood_arr)
        mature_arrs.append(band_mature_arr)
        distance_arrs.append(band_distance_arr)

        tmp_mature_arr //= 1000
        tmp_flood_arr //= 1000
        tmp_distance_arr //= 10000

    flood_arrs = np.array(flood_arrs).astype(np.int16)
    mature_arrs = np.array(mature_arrs).astype(np.int16)
    distance_arrs = np.array(distance_arrs).astype(np.int16)

    # create output rasters
    out_flood_path, out_mature_path, out_distance_path = out_paths
    is_fold_exist(os.path.dirname(out_flood_path))
    create_raster(out_flood_path, flood_arrs, trf[1], prj, trf, setnodata=True, nodata=0, datatype=gdal.GDT_Int16, band_num=flood_arrs.shape[0])
    create_raster(out_mature_path, mature_arrs, trf[1], prj, trf, setnodata=True, nodata=0, datatype=gdal.GDT_Int16, band_num=mature_arrs.shape[0])
    create_raster(out_distance_path, distance_arrs, trf[1], prj, trf, setnodata=True, nodata=-9, datatype=gdal.GDT_Int16, band_num=distance_arrs.shape[0])

    if pool_num >= 2 and pool_size != 0:
        delete_file(NDVI_npy)
        delete_file(LSWI_npy)

    end_time = time.time()
    print(f">>> {year} {tile} {para_region} time for multi mapping is {(end_time - start_time) / 60 / 60:.3f}h: {method_info}")


def multi_rice_mapping_positions_new(start, end1,
                                     NDVI_npy, LSWI_npy, ref_series, threshold,
                                     flood_factor, flood_potential_indexs, previous_mature_indexs,
                                     NDVI_ceiling, grow_range, latest_mature_index, rate, start_doy):
    """
    return: distances, flood_doys, mature_doys
    all returned values are integers with three digits
    """

    s = time.time()
    distances, flood_doys, mature_doys = [], [], []

    all_NDVIs = np.load(NDVI_npy, mmap_mode='r')[start:end1]
    all_LSWIs = np.load(LSWI_npy, mmap_mode='r')[start:end1]
    print(f"{start}~{end1-1} multi positions: NDVI={all_NDVIs.shape} LSWI={all_LSWIs.shape}")

    for k in range(end1 - start):
        d_str, flood_doy_str, mature_doy_str = \
            multi_rice(all_NDVIs[k], all_LSWIs[k], threshold, ref_series,
                       flood_potential_indexs, previous_mature_indexs[k], flood_factor,
                       grow_range, latest_mature_index, NDVI_ceiling, rate, start_doy)

        distances.append(int(d_str))
        flood_doys.append(int(flood_doy_str))
        mature_doys.append(int(mature_doy_str))

    e = time.time()
    print(f"{start}~{end1-1} multi positions: mapping time={(e - s) / 60 / 60:.3f}h, flood_doy={np.min(flood_doys)}~{np.max(flood_doys)}, mature_doy={np.min(mature_doys)}~{np.max(mature_doys)}")
    return distances, flood_doys, mature_doys


def multi_rice(NDVIs_raw, LSWIs_raw, threshold, ref,
               flood_potential_indexs, earliest_flood_index, flood_factor,
               grow_range, latest_mature_index, NDVI_ceiling, rate, start_doy):
    """
    return: d_str, flood_doy_str, mature_doy_str
    the returned distance values are all multiplied by 100 (to preserve two decimal places)
    only supports threshold < 99
    """

    NDVIs_filtered = savgol_filter(NDVIs_raw, SG_win_length_daily, SG_poly_daily)

    flood_indexs = find_floods(NDVIs_filtered, LSWIs_raw, flood_potential_indexs, flood_factor, NDVI_ceiling)
    if len(flood_indexs) < 1:
        return -1, 0, 0

    all_doys = []
    previous_mature_index = earliest_flood_index
    # Record multiple DOYs, for example: 110230355 represents110、230、355
    flood_doy_str, mature_doy_str, distance_str = '', '', ''
    for flood_index in flood_indexs:
        if flood_index <= previous_mature_index:  # current flooding date > previous maturity date
            continue
        mature_indexs = find_matures(NDVIs_filtered, flood_index, grow_range, latest_mature_index, rate, NDVI_ceiling)
        if mature_indexs.shape[0] < 1:
            continue

        now_indexs = []
        for mature_index in mature_indexs:
            align, d = dtw_matching(NDVIs_filtered[flood_index:mature_index + 1], ref)
            now_indexs.append([d, mature_index])
        d, min_mature_index = now_indexs[np.argmin(np.array(now_indexs)[:, 0], axis=0)]
        if d < threshold:
            previous_mature_index = min_mature_index
            flood_doy_str += str(flood_index + start_doy).zfill(3)
            mature_doy_str += str(min_mature_index + start_doy).zfill(3)
            distance_str += str(int(d * scale_dtw_distance)).zfill(4)  # 保留2位小数，d<100
        all_doys.append([d, flood_index + start_doy, min_mature_index + start_doy])

    if not all_doys:
        return -2, 0, 0

    if distance_str != '':
        return distance_str, flood_doy_str, mature_doy_str
    else:
        min_d_index = np.argmin(np.array(all_doys)[:, 0], axis=0)
        return all_doys[min_d_index][0] * scale_dtw_distance, all_doys[min_d_index][1], all_doys[min_d_index][2]
