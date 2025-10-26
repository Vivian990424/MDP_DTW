
products_reflectance = ['MOD09Q1', 'MYD09Q1', 'MOD09A1', 'MYD09A1']
products_reflectance_500m_8day = ['M09A1', 'MOD09A1', 'MYD09A1']
product_out_500m = 'M09A1D'

products_LC = ['MCD12Q1', 'MCD12Q2', 'MCD12C1']  # 500m, 1km, 0.05deg

desc_products = {
    'NDVI_8daily': product_out_500m,
    'LSWI_8daily': product_out_500m,

    'cropland': product_out_500m,

    'cropland_GlobalLand30_500m_50%': product_out_500m,
    'cropland_GlobalLand30': products_LC[0],

    'cropland_CDL_500m_50%': product_out_500m,

    'land_USA': product_out_500m,
    'land_ChinaDB': product_out_500m,
    'land_para_ChinaDB': product_out_500m,
    'land_Australia': product_out_500m,
    'land_KoreaJapan': product_out_500m,
    'land_Italy': product_out_500m,
    'land_para_Italy': product_out_500m,
    'land_para_SouthAsia': product_out_500m,
    'land_ChinaDN': product_out_500m,
    'land_para_Madagascar': product_out_500m,
    'land_para_Brazil': product_out_500m,
}


key_no_rice = 'no_rice'
key_pre = 'pre'
key_adjust = 'adjusted'

method_desc_final = 'Union'
method_desc_final_day = 'Union-day'

region_final = 'union'

algorithm_single = 'single'
algorithm_multi = 'multi'
algorithm_union = 'union'
algorithm_mosaic = 'mosaic'

type_flood = 'flood-day'
type_mature = 'mature-day'
type_distance = 'distance'
type_rice_area = 'rice-area'
type_flood_area = 'flood-area'

type_intensity = 'season-num'  # 复种指数
type_year_num = 'year_num'  # 存在水稻的年份数量
type_year_rate = 'rice-year-rate'  # 存在水稻的年份比例（有水稻的年数/年数）
type_vast = 'vast'
type_flood_month = 'flood_month'
type_long_series = 'long_series'   # 分析长时序的识别结果

head_year = 'year'
head_country = 'country'
head_tile = 'tile'
head_now_area = 'now_area'
head_base_area = 'base_area'
head_stat_area = 'stat_area'
head_now_threshold = 'now_threshold'
head_now_diff = 'now_diff(%)'

header_no_rice = [head_year, head_tile, 'para_region']
