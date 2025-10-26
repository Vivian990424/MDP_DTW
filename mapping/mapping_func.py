import time
import numpy as np

from commons.all_common_infos import *

from tools.raster_process import read_raster
from tools.time_process import get_year_daynum
from tools.files_process import is_file_good, is_dir_exist
from tools.csv_process import append_csv, write_csv, read_csv


def read_VIs(year, tile, next_year=True,
             NDVI_rt=NDVI_tif_root, LSWI_rt=LSWI_tif_root,
             next_NDVI_rt=None, next_LSWI_rt=None):
    NDVI_num, NDVI_images = read_VI_images_daily(year, tile, NDVI_rt, next_year, next_NDVI_rt)
    LSWI_num, LSWI_images = read_VI_images_daily(year, tile, LSWI_rt, next_year, next_LSWI_rt)

    if NDVI_num != LSWI_num:
        print(f"<read_VIs> [error] {year} {tile} NDVI_num != LSWI_num")
        return -1, []
    if min(NDVI_num, LSWI_num) < 1:
        print(f"<read_VIs> [error] {year} {tile} no image")
        return -2, []
    return 0, [NDVI_num, np.array(NDVI_images) / scale_VI_int16, LSWI_num, np.array(LSWI_images) / scale_VI_int16]


def read_VI_images_daily(year, tile, tif_rt, next_year, next_tif_rt=None):
    s = time.time()
    images = []

    # current year
    current_daynum = get_year_daynum(year)
    for doy in range(get_doy_start(year), current_daynum + 1):
        tif_path = get_VI_daily_tif(year, tile, doy, tif_rt)
        if is_file_good(tif_path) == 0:
            arr = read_raster(tif_path, mode='arr')[0]
            images.append(arr)
        else:
            print(f"<read_VI> [error] {year} {doy} {tile} read image failed", tif_path)
            return -1, []

    # next year
    if next_year:
        if next_tif_rt is None:
            next_tif_rt = tif_rt

        next_daynum = get_year_daynum(year + 1)
        for doy in range(1, next_daynum + 1):
            tif_path = get_VI_daily_tif(year + 1, tile, doy, next_tif_rt)
            if is_file_good(tif_path) == 0:
                arr = read_raster(tif_path, mode='arr')[0]
                images.append(arr)
            else:
                print(f"<read_VI> [info] {year + 1} {tile} end at {doy - 1}")
                break

    image_num = len(images)
    e = time.time()
    print(f"<read_VI> (success) {year} {tile} {tif_rt} : image_num={image_num}, time={(e - s)}s")
    return image_num, images


def get_indexs_from_doy(year, doy_range):
    year_end_doy = get_year_daynum(year)
    if doy_range[-1] <= year_end_doy:
        indexs = list(range(doy_range[0]-1, doy_range[1]))
    else:
        indexs1 = list(range(doy_range[0]-1, year_end_doy))  # index=doy-1
        indexs2 = list(range(0, doy_range[1]-year_end_doy))
        indexs = indexs2 + indexs1
    if year == 2000:
        indexs = np.array(indexs) - lack_daynum_2000
        indexs = indexs[indexs >= 0]
    return indexs


def get_latest_mature_index(image_num, end_num):
    if end_num is None:
        return image_num - 1
    return image_num - end_num - 1


def find_floods(NDVIs_filtered, LSWIs_raw, flood_potential_indexs, factor, NDVI_ceiling=0.5):
    """
    return: flood indexes
    """
    all_indexs = np.arange(0, len(NDVIs_filtered))
    flood_indexs = all_indexs[(NDVIs_filtered < LSWIs_raw + factor) &  # LSWI+F > NDVI  洪水判别
                              ((-1 < NDVIs_filtered) & (NDVIs_filtered < NDVI_ceiling))]  # -1 < NDVI < 0.5  NDVI不可过高
    return np.intersect1d(flood_indexs, flood_potential_indexs)


def find_matures(NDVIs_filtered, flood_index, grow_range, latest_mature_index=700, rate=0.02, end_Nceiling=0.5):
    NDVI_length = len(NDVIs_filtered)
    NDVIs_before_deriv = np.zeros(NDVI_length)
    NDVIs_before_deriv[1:] = NDVIs_filtered[1:] - NDVIs_filtered[:-1]  # current - before
    NDVIs_after_deriv = np.zeros(NDVI_length)
    NDVIs_after_deriv[:-1] = NDVIs_filtered[:-1] - NDVIs_filtered[1:]  # current - after
    all_indexs = np.arange(0, NDVI_length)
    mature_indexs = all_indexs[
        (NDVIs_before_deriv < 0) &
        (NDVIs_after_deriv < rate) &
        (NDVIs_filtered <= end_Nceiling) &
        (flood_index+grow_range[0] <= all_indexs) & (all_indexs <= flood_index+grow_range[1]) & (all_indexs <= latest_mature_index)
        ]
    return mature_indexs


def get_valid_arr(year, tile, land_desc, crop_desc, para_region, method_info):
    prdt = 'M09A1D'  # output product id

    # cropland
    if year == 2000:
        crop_tif = get_mask_path(tile, prdt, crop_desc, 2001)
    else:
        crop_tif = get_mask_path(tile, prdt, crop_desc, year)
    if is_file_good(crop_tif) != 0:  # 耕地必须存在
        print(f"[ERROR] {year} {tile} crop_tif not exist: {crop_tif}")
        return -1, 0, 0, 0, 0
    crop_arr, prj, trf, xsize, ysize, extent = read_raster(crop_tif, 'arr')

    # initiate
    valid_arr = np.ones(crop_arr.shape, dtype=np.int8)  # 1为需要运行算法的区域，0为无水稻区域
    valid_arr[crop_arr != 1] = 0
    crop_arr = None

    # land
    if land_desc is not None:  # mask可以不存在
        land_arr = read_raster(get_mask_path(tile, prdt, land_desc), 'arr')[0]
        if land_arr.shape != valid_arr.shape:
            print(f"[ERROR] {year} {tile} land_arr.shape != valid_arr.shape")
            return -2, 0, 0, 0, 0
        valid_arr[land_arr != 1] = 0
        land_arr = None

    valid_positions = np.argwhere(valid_arr == 1)
    if valid_positions.shape[0] < 1:
        write_no_rice(year, tile, para_region, method_info)
        print(f"{year} {tile} {para_region} no valid_positions")
        return -3, 0, 0, 0, 0
    return 0, valid_positions, valid_arr, prj, trf


def get_no_rice_tiles(year, method_desc, country=None):

    if country is None:
        no_rice_csv = get_no_rice_csv(method_desc)
    else:
        no_rice_csv = get_no_rice_csv_country(method_desc, country)

    if not os.path.exists(no_rice_csv):
        return []
    # print(no_rice_csv)
    header, content, _ = read_csv(no_rice_csv)
    year_col = content[:, header.index('year')].astype(int)
    tile_col = content[:, header.index('tile')]
    return tile_col[year_col == year]


def check_results(year, tile, para_region, method_desc, types=None, prt=True, country=None):

    types = types or [type_flood, type_mature, type_distance]
    algorithm = regions_algorithms[para_region]

    if tile in get_no_rice_tiles(year, method_desc, country):
        print(f"{year} {tile} {para_region} {algorithm} already no rice in /{method_desc}/({country})")
        return True, [key_no_rice]

    out_paths = []
    flag = True
    for t in types:
        if country is None:
            out_path = get_result_tif(year, tile, method_desc, algorithm, data_type=t)
        else:
            out_path = get_result_tif_country(year, tile, method_desc, algorithm, t, country)

        out_paths.append(out_path)
        if is_file_good(out_path, prt=prt) != 0:
            print(f"unmapping: {out_path}")
            flag = False
    if flag and prt:
        print(f"{year} {tile} {para_region} {algorithm} already exist")
    return flag, out_paths


def write_no_rice(year, tile, para_region, method_desc, country=None):
    if country is None:
        out_csv_path = get_no_rice_csv(method_desc)  # os.path.join(get_result_fold(method_desc, year=None), 'no_rice.csv')
    else:
        out_csv_path = get_no_rice_csv_country(method_desc, country)

    rows = [[year, tile, para_region]]
    if os.path.exists(out_csv_path):
        append_csv(out_csv_path, rows)
    else:
        header = ['year', 'tile', 'para_region']
        write_csv(out_csv_path, header, rows)


def make_VIs_npy(year, tile, para_region, image_num, next_year, valid_arr, NDVI_npy, LSWI_npy):
    if is_file_good(NDVI_npy, 1) == 0 and is_file_good(LSWI_npy, 1) == 0:
        NDVI_load = np.load(NDVI_npy)
        LSWI_load = np.load(LSWI_npy)
        if NDVI_load.shape != LSWI_load.shape or \
           NDVI_load.shape[0] != np.sum(valid_arr == 1) or \
           NDVI_load.shape[1] != image_num:
            print(f"[ERROR] {year} {tile} npy error")
            return -1
        print(f"[info] {year} {tile} {para_region} npy already exist")
        return 1

    flag, results = read_VIs(year, tile, next_year)
    if flag != 0:
        print(f"[ERROR] {year} {tile} read_images failed")
        return -1
    # NDVI_num, NDVI_images, LSWI_num, LSWI_images = results
    if results[0] != image_num or results[2] != image_num:
        print(f"[ERROR] {year} {tile} image num error: image_num={image_num}, NDVI_num={results[0]}, LSWI_num={results[2]}")
        return -2
    print(f"{year} {tile} {para_region} image_num={image_num}")

    # sereis是二维矩阵，每一行都是对应位置的NDVI曲线
    NDVI_series = np.transpose(results[1][:, valid_arr == 1], [1, 0])
    is_dir_exist(NDVI_npy)
    np.save(NDVI_npy, NDVI_series)
    if is_file_good(NDVI_npy, 1) == 0:
        print(f"(success) {year} {tile} {para_region} make NDVI series: {NDVI_npy}")
    else:
        print(f"[ERROR] {year} {tile} {para_region} make NDVI series: {NDVI_npy}")
        return -3

    LSWI_series = np.transpose(results[3][:, valid_arr == 1], [1, 0])
    is_dir_exist(LSWI_npy)
    np.save(LSWI_npy, LSWI_series)
    if is_file_good(LSWI_npy, 1) == 0:
        print(f"(success) {year} {tile} {para_region} make LSWI series: {LSWI_npy}")
    else:
        print(f"[ERROR] {year} {tile} {para_region} make LSWI series: {LSWI_npy}")
        return -4
    return 0
