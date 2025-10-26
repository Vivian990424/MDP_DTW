import os.path
from commons.paths import *
from commons.products import *


def get_year_str(years):
    if len(years) > 1:
        return f'{min(years)}-{max(years)}'
    else:
        return str(years[0])


def get_res_from_scale(mosaic_scale):
    return int(mosaic_scale * 463.3127165)


def get_doy_start(year):
    if year == 2000:
        return 49  # 1+lack_daynum_2000
    else:
        return 1


def get_product(year, VI):
    # if year < 2000:
    #     print("!!! year not supported")
    #     return -1
    # if VI not in ['NDVI', 'LSWI']:
    #     print("!!! VI not supported")
    #     return -2
    type_prefix = 'M' if year > 2001 else 'MOD'
    type_suffix = 'Q1' if VI == 'NDVI' else 'A1'
    return type_prefix + '09' + type_suffix


def get_1km_ref(tile):
    return fr"E:\wwData\1km_ref\{tile}_dem.tif"


def get_500m_ref(tile):
    # return get_VI_tif(2021, tile, '0226', 'LSWI')
    return get_gtiff_path(2022, tile, day='0101')


def get_gtiff_path(year, tile, product=products_LC[0], day='0218', postfix='LC_Type1', tif_rt=tif_root):
    return os.path.join(tif_rt, str(year), product, tile, "{}{}_{}_{}.tif".format(year, day, tile, postfix))


def get_gtiff_fold(year, tile, product):
    return os.path.join(tif_root, str(year), product, tile)


def get_VI_tif(year, tile, day='0218', VI='NDVI'):
    rt = NDVI_8day_tif_root if VI == 'NDVI' else LSWI_8day_tif_root
    return os.path.join(rt, str(year), get_product(year, VI), tile, f'{year}{day}_{tile}_{VI}.tif')


def get_VI_daily_tif(year, tile, doy, VI_rt):
    doy_str = str(doy).zfill(3)
    VI = 'NDVI' if 'NDVI' in VI_rt else 'LSWI'
    return os.path.join(VI_rt, str(year), product_out_500m, tile, f'{year}{doy_str}_{tile}_{VI}.tif')


def get_VI_npy(year, tile, region, VI_rt):
    VI = 'NDVI' if 'NDVI' in VI_rt else 'LSWI'
    if region is not None and len(region) > 0:
        return os.path.join(VI_rt, region, f'{year}_{tile}_{region}_{VI}.npy')
    else:
        return os.path.join(VI_rt, f'{year}_{tile}_{VI}.npy')


def get_VI_fold(year, tile, VI='NDVI'):
    rt = NDVI_8day_tif_root if VI == 'NDVI' else LSWI_8day_tif_root
    return os.path.join(rt, str(year), get_product(year, VI), tile)


def get_VI_daily_fold(year, tile, VI_rt):
    return os.path.join(VI_rt, str(year), product_out_500m, tile)


def get_mask_path(tile, product, mask_type, year=None):
    if year is None:
        # rf'{Mask_root}\{mask_type}\{product}_{tile}.tif'
        return os.path.join(Mask_root, mask_type, f'{product}_{tile}.tif')
    else:
        return os.path.join(Mask_root, mask_type, str(year), f'{product}_{tile}.tif')


def get_mask_fold(mask_type, year=None):
    if year is None:
        # rf'{Mask_root}\{mask_type}'
        return os.path.join(Mask_root, mask_type)
    else:
        return os.path.join(Mask_root, mask_type, str(year))


def get_country_tif(country, tile, res, root=country_tile_root):
    return os.path.join(root, country, f'{country}_{tile}_{res}m.tif')


def get_country_tiles_csv(country, res, root=country_tile_root):
    return os.path.join(root, country, f'{country}_tiles_{res}m.csv')


def get_result_tif(year, tile, method_info, algorithm='single', data_type='flood-day'):
    return os.path.join(out_root, method_info, str(year), '{}_{}_{}_{}.tif'.format(year, tile, algorithm, data_type))


def get_result_tif_mosaic(year, mosaic_desc, method_desc, algorithm='mosaic', data_type=type_rice_area):
    return os.path.join(out_root, method_desc, 'mosaic', mosaic_desc,
                        f'{year}_{mosaic_desc}_{algorithm}_{data_type}.tif')


def get_result_tif_day(year, doy, tile, method_desc, algorithm=algorithm_mosaic, data_type=type_rice_area):
    day_str = str(doy).zfill(3)
    if algorithm == algorithm_mosaic:
        return os.path.join(out_root, method_desc, algorithm_mosaic, tile, str(year),
                            f'{year}_{day_str}_{tile}_{algorithm}_{data_type}.tif')
    else:
        return os.path.join(out_root, method_desc, str(year), f'{year}_{day_str}_{tile}_{algorithm}_{data_type}.tif')


def get_result_tif_block(year, tile, method_info, algorithm, data_type, block_num, block_index):
    return os.path.join(out_root, method_info, f'{block_num}_{block_index}', str(year),
                        f'{year}_{tile}_{algorithm}_{data_type}.tif')


def get_result_tif_country(year, tile, method_info, algorithm, data_type, country):
    return os.path.join(out_root, method_info, country, str(year),
                        f'{year}_{tile}_{algorithm}_{data_type}.tif')


def get_result_fold(method_info, year=None):
    if year is None:
        return os.path.join(out_root, method_info)
    return os.path.join(out_root, method_info, str(year))


def get_no_rice_csv(method_desc):
    return os.path.join(out_root, method_desc, 'no_rice.csv')


def get_no_rice_csv_country(method_desc, country):
    return os.path.join(out_root, method_desc, country, f'no_rice_{country}.csv')


def get_no_rice_csv_block(method_desc, block_num, block_index):
    return os.path.join(out_root, method_desc, f'no_rice_{block_num}_{block_index}.csv')


def get_method_desc(product, para_region, purity, threshold, flood_doy_range, flood_factor, grow_range, NDVI_ceiling):
    if flood_doy_range is None:
        return f"{product}_{para_region}_{purity}_{threshold}_DTW_all_{flood_factor}_{grow_range[0]}-{grow_range[1]}_{NDVI_ceiling}"
    else:
        return f"{product}_{para_region}_{purity}_{threshold}_DTW_{flood_doy_range[0]}-{flood_doy_range[1]}_{flood_factor}_{grow_range[0]}-{grow_range[1]}_{NDVI_ceiling}"
