from mapping.mapping_single import *


if __name__ == '__main__':

    parallel_num = 60   # number of parallel processes

    for year in range(2000, 2001 + 1):  # mapping years
        for tile in ['h26v04']:  # mapping tiles

            land_desc, crop_desc, threshold, ref, flood_doy_range, flood_factor, grow_range, latest_mature, NDVI_ceiling, para_region, rate = paras_ChinaDB
            single_rice_mapping(year, tile, land_desc, crop_desc, threshold, ref,
                                flood_doy_range, flood_factor, grow_range, latest_mature, NDVI_ceiling,
                                para_region, rate, parallel_num)

