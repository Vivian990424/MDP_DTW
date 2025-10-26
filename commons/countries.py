import os
from commons.paths import map_root


Asia_countries = [

    "Republic of Korea", "Democratic People's Republic of Korea", "Japan",

    "China",
    # 'ChinaXinJiang', 'ChinaYunNan', 'ChinaGuiZhou', 'ChinaChongQing', 'ChinaSiChuan', 'ChinaShaanXi', 'ChinaNingXia',
    # 'ChinaNeiMengGu', 'ChinaHeNan', 'ChinaHeBei', 'ChinaShanDong', 'ChinaLiaoNing', 'ChinaJiLin', 'ChinaHeiLongJiang',
    # 'ChinaBeiJing', 'ChinaTianJin', 'ChinaShanXi', 'ChinaXiZang', 'ChinaGanSu', 'ChinaQIngHai',

    'Türkiye', 'Azerbaijan', 'Iraq', 'Iran (Islamic Republic of)', 'Uzbekistan', 'Kazakhstan',
    'Kyrgyzstan', 'Tajikistan', 'Afghanistan', 'Pakistan',

    # 'ChinaJiangSu', 'ChinaShangHai', 'ChinaAnHui', 'ChinaZheJiang', 'ChinaJiangXi', 'ChinaHuBei', 'ChinaHuNan',
    # 'ChinaGuangXi', 'ChinaGuangDong', 'ChinaFuJian', 'ChinaTaiWan',

    # 'ChinaHaiNan',
    'India', 'Sri Lanka', 'Nepal', 'Bhutan', 'Bangladesh',
    'Myanmar', 'Thailand', "Lao People's Democratic Republic", "Cambodia", 'Viet Nam',
    'Malaysia', 'Brunei Darussalam', 'Indonesia', 'Timor-Leste', 'Philippines', 'Papua New Guinea'
]


Europe_countries = [
    'Russian Federation',
    'Italy', 'France', 'Portugal', 'Spain',
    'Greece', 'North Macedonia', 'Bulgaria', 'Romania', 'Ukraine',
    "Hungary",
]


Africa_countries = [
    'Morocco', 'Algeria', 'Egypt', 'Mauritania', 'Mali', 'Niger', 'Chad', 'Sudan', 'South Sudan',
    'Senegal', 'Gambia', 'Guinea-Bissau', 'Guinea', 'Sierra Leone', 'Liberia', "Côte d'Ivoire", 'Burkina Faso',
    'Ghana', 'Togo', 'Benin', 'Nigeria', 'Cameroon', 'Central African Republic',
    'Gabon', 'Congo', 'Democratic Republic of the Congo', 'Uganda', 'Rwanda', 'Burundi', 'Kenya', 'Somalia',
    'Malawi', 'Madagascar',
    "Ethiopia",
    'Angola', 'Zambia', 'United Republic of Tanzania', 'Zimbabwe', 'Mozambique', 'South Africa', 'Eswatini', 'Comoros'
]


NorthAmerica_countries = [
    'United States of America', 'Mexico',
    'Guatemala', 'Belize', 'El Salvador', 'Honduras', 'Nicaragua', 'Costa Rica', 'Panama',
    'Cuba', 'Haiti', 'Puerto Rico', 'Dominican Republic', 'Trinidad and Tobago',
]


SouthAmerica_countries = [
    'Chile', 'Argentina', 'Uruguay', 'Brazil', 'Paraguay', 'Bolivia (Plurinational State of)', 'Peru',
    'Ecuador', 'Colombia', 'Venezuela (Bolivarian Republic of)', 'Guyana', 'Suriname', 'French Guiana'
]


Americas_countries = NorthAmerica_countries + SouthAmerica_countries

Oceania_countries = [  # , shp checked
    'Australia', 'Fiji', 'Solomon Islands'
]



global_countries = Asia_countries + Europe_countries + Africa_countries + Oceania_countries + \
                   NorthAmerica_countries + SouthAmerica_countries

# checked shp
country_shps = {
    '1': os.path.join(map_root, 'Global_Rice', 'countries', '', '.shp'),
    '2': os.path.join(map_root, 'Global_NaturalEarth', '', '.shp'),

    # 欧洲
    'Italy': os.path.join(map_root, 'Global_Rice', 'countries', 'Italy_rice', 'Italy_rice_provinces.shp'),
    'Greece': os.path.join(map_root, 'Global_NaturalEarth', 'Greece', 'Greece.shp'),
    'Portugal': os.path.join(map_root, 'Global_NaturalEarth', 'Portugal', 'Portugal.shp'),
    'Spain': os.path.join(map_root, 'Global_Rice', 'countries', 'Spain_rice', 'Spain_rice_states.shp'),
    'France': os.path.join(map_root, 'Global_Rice', 'countries', 'France_rice', 'France_Europe_rice_states.shp'),
    'Ukraine': os.path.join(map_root, 'Global_Rice', 'countries', 'Ukraine_rice', 'Ukraine_rice_provinces.shp'),
    'Romania': os.path.join(map_root, 'Global_NaturalEarth', 'Romania', 'Romania.shp'),
    'Bulgaria': os.path.join(map_root, 'Global_Rice', 'countries', 'Bulgaria_rice', 'Bulgaria_rice_provinces.shp'),
    'North Macedonia': os.path.join(map_root, 'Global_NaturalEarth', 'NorthMacedonia', 'NorthMacedonia.shp'),
    'Hungary': os.path.join(map_root, 'Global_NaturalEarth', 'Hungary', 'Hungary.shp'),  # printer待补

    # 大洋洲
    'Australia': os.path.join(map_root, 'Global_Rice', 'countries', 'Australia_rice', 'Australia_rice_counties.shp'),
    'Fiji': os.path.join(map_root, 'Global_NaturalEarth', 'Fiji', 'Fiji.shp'),
    'Solomon Islands': os.path.join(map_root, 'Global_NaturalEarth', 'SolomonIslands', 'SolomonIslands.shp'),

    # 非洲
    # 多季
    'Ethiopia': os.path.join(map_root, 'Global_NaturalEarth', 'Ethiopia', 'Ethiopia.shp'),  # cluster待补
    'Morocco': os.path.join(map_root, 'Global_NaturalEarth', 'Morocco', 'Morocco.shp'),
    'Algeria': os.path.join(map_root, 'Global_NaturalEarth', 'Algeria', 'Algeria.shp'),
    'Egypt': os.path.join(map_root, 'Global_NaturalEarth', 'Egypt', 'Egypt.shp'),
    'Mauritania': os.path.join(map_root, 'Global_NaturalEarth', 'Mauritania', 'Mauritania.shp'),
    'Mali': os.path.join(map_root, 'Global_NaturalEarth', 'Mali', 'Mali.shp'),
    'Niger': os.path.join(map_root, 'Global_NaturalEarth', 'Niger', 'Niger.shp'),
    'Chad': os.path.join(map_root, 'Global_NaturalEarth', 'Chad', 'Chad.shp'),
    'Sudan': os.path.join(map_root, 'Global_NaturalEarth', 'Sudan', 'Sudan.shp'),
    'South Sudan': os.path.join(map_root, 'Global_NaturalEarth', 'SouthSudan', 'SouthSudan.shp'),
    'Senegal': os.path.join(map_root, 'Global_NaturalEarth', 'Senegal', 'Senegal.shp'),
    'Gambia': os.path.join(map_root, 'Global_NaturalEarth', 'Gambia', 'Gambia.shp'),
    'Guinea-Bissau': os.path.join(map_root, 'Global_NaturalEarth', 'GuineaBissau', 'GuineaBissau.shp'),
    'Guinea': os.path.join(map_root, 'Global_NaturalEarth', 'Guinea', 'Guinea.shp'),
    'Sierra Leone': os.path.join(map_root, 'Global_NaturalEarth', 'SierraLeone', 'SierraLeone.shp'),
    'Liberia': os.path.join(map_root, 'Global_NaturalEarth', 'Liberia', 'Liberia.shp'),
    "Côte d'Ivoire": os.path.join(map_root, 'Global_NaturalEarth', 'IvoryCoast', 'IvoryCoast.shp'),
    'Burkina Faso': os.path.join(map_root, 'Global_NaturalEarth', 'BurkinaFaso', 'BurkinaFaso.shp'),
    'Ghana': os.path.join(map_root, 'Global_NaturalEarth', 'Ghana', 'Ghana.shp'),
    'Togo': os.path.join(map_root, 'Global_NaturalEarth', 'Togo', 'Togo.shp'),
    'Benin': os.path.join(map_root, 'Global_NaturalEarth', 'Benin', 'Benin.shp'),
    'Nigeria': os.path.join(map_root, 'Global_NaturalEarth', 'Nigeria', 'Nigeria.shp'),
    'Cameroon': os.path.join(map_root, 'Global_NaturalEarth', 'Cameroon', 'Cameroon.shp'),
    'Central African Republic': os.path.join(map_root, 'Global_NaturalEarth', 'CentralAfricanRepublic', 'CentralAfricanRepublic.shp'),
    'Gabon': os.path.join(map_root, 'Global_NaturalEarth', 'Gabon', 'Gabon.shp'),
    'Congo': os.path.join(map_root, 'Global_NaturalEarth', 'Congo', 'Congo.shp'),
    'Democratic Republic of the Congo': os.path.join(map_root, 'Global_NaturalEarth', 'DemocraticCongo', 'DemocraticCongo.shp'),
    'Uganda': os.path.join(map_root, 'Global_NaturalEarth', 'Uganda', 'Uganda.shp'),
    'Rwanda': os.path.join(map_root, 'Global_NaturalEarth', 'Rwanda', 'Rwanda.shp'),
    'Burundi': os.path.join(map_root, 'Global_NaturalEarth', 'Burundi', 'Burundi.shp'),
    'Kenya': os.path.join(map_root, 'Global_NaturalEarth', 'Kenya', 'Kenya.shp'),
    'Somalia': os.path.join(map_root, 'Global_NaturalEarth', 'Somalia', 'Somalia.shp'),
    'Malawi': os.path.join(map_root, 'Global_NaturalEarth', 'Malawi', 'Malawi.shp'),
    'Madagascar': os.path.join(map_root, 'Global_NaturalEarth', 'Madagascar', 'Madagascar.shp'),

    # 单季
    'Angola': os.path.join(map_root, 'Global_NaturalEarth', 'Angola', 'Angola.shp'),
    'Zambia': os.path.join(map_root, 'Global_NaturalEarth', 'Zambia', 'Zambia.shp'),
    'United Republic of Tanzania': os.path.join(map_root, 'Global_NaturalEarth', 'Tanzania', 'Tanzania.shp'),
    'Zimbabwe': os.path.join(map_root, 'Global_NaturalEarth', 'Zimbabwe', 'Zimbabwe.shp'),
    'Mozambique': os.path.join(map_root, 'Global_NaturalEarth', 'Mozambique', 'Mozambique.shp'),
    'Comoros': os.path.join(map_root, 'Global_NaturalEarth', 'Comoros', 'Comoros.shp'),
    'South Africa': os.path.join(map_root, 'Global_NaturalEarth', 'SouthAfrica', 'SouthAfrica.shp'),
    'Eswatini': os.path.join(map_root, 'Global_NaturalEarth', 'Eswatini', 'Eswatini.shp'),

    # 北美洲
    'USA': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'USA_rice_counties.shp'),
    'United States of America': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'USA_rice_counties.shp'),
    'Mexico': os.path.join(map_root, 'Global_Rice', 'countries', 'Mexico_rice', 'Mexico_rice_states.shp'),
    'Guatemala': os.path.join(map_root, 'Global_NaturalEarth', 'Guatemala', 'Guatemala.shp'),
    'Belize': os.path.join(map_root, 'Global_NaturalEarth', 'Belize', 'Belize.shp'),
    'El Salvador': os.path.join(map_root, 'Global_NaturalEarth', 'ElSalvador', 'ElSalvador.shp'),
    'Honduras': os.path.join(map_root, 'Global_NaturalEarth', 'Honduras', 'Honduras.shp'),
    'Nicaragua': os.path.join(map_root, 'Global_NaturalEarth', 'Nicaragua', 'Nicaragua.shp'),
    'Costa Rica': os.path.join(map_root, 'Global_NaturalEarth', 'CostaRica', 'CostaRica.shp'),
    'Panama': os.path.join(map_root, 'Global_NaturalEarth', 'Panama', 'Panama.shp'),
    'Cuba': os.path.join(map_root, 'Global_NaturalEarth', 'Cuba', 'Cuba.shp'),
    'Haiti': os.path.join(map_root, 'Global_NaturalEarth', 'Haiti', 'Haiti.shp'),
    'Dominican Republic': os.path.join(map_root, 'Global_NaturalEarth', 'DominicanRepublic', 'DominicanRepublic.shp'),
    'Puerto Rico': os.path.join(map_root, 'Global_NaturalEarth', 'PuertoRico', 'PuertoRico.shp'),
    'Saint Vincent and the Grenadines': os.path.join(map_root, 'Global_NaturalEarth', 'SaintVincent_theGrenadines', 'SaintVincent_theGrenadines.shp'),
    'Trinidad and Tobago': os.path.join(map_root, 'Global_NaturalEarth', 'Trinidad_Tobago', 'Trinidad_Tobago.shp'),
    # 北美洲excluded country
    'Dominica': os.path.join(map_root, 'Global_NaturalEarth', 'Dominica', 'Dominica.shp'),
    'Saint Lucia': os.path.join(map_root, 'Global_NaturalEarth', 'SaintLucia', 'SaintLucia.shp'),
    'Barbados': os.path.join(map_root, 'Global_NaturalEarth', 'Barbados', 'Barbados.shp'),

    # 亚洲
    'Republic of Korea': os.path.join(map_root, 'Global_NaturalEarth', 'Korea', 'SouthKorea.shp'),
    "Democratic People's Republic of Korea": os.path.join(map_root, 'Global_NaturalEarth', 'Korea', 'NorthKorea.shp'),
    'Japan': os.path.join(map_root, 'Global_NaturalEarth', 'Japan', 'Japan.shp'),

    'Russian Federation': os.path.join(map_root, 'Global_Rice', 'countries', 'Russia_rice', 'Russia_rice_states.shp'),
    'Türkiye': os.path.join(map_root, 'Global_NaturalEarth', 'Turkey', 'Turkey.shp'),
    'Azerbaijan': os.path.join(map_root, 'Global_NaturalEarth', 'Azerbaijan', 'Azerbaijan.shp'),
    'Iraq': os.path.join(map_root, 'Global_NaturalEarth', 'Iraq', 'Iraq.shp'),
    'Iran (Islamic Republic of)': os.path.join(map_root, 'Global_NaturalEarth', 'Iran', 'Iran.shp'),
    'Turkmenistan': os.path.join(map_root, 'Global_NaturalEarth', 'Turkmenistan', 'Turkmenistan.shp'),
    'Uzbekistan': os.path.join(map_root, 'Global_Rice', 'countries', 'Uzbekistan_rice', 'Uzbekistan_rice_provinces.shp'),
    'Kazakhstan': os.path.join(map_root, 'Global_Rice', 'countries', 'Kazakhstan_rice', 'Kazakhstan_rice_provinces.shp'),
    'Kyrgyzstan': os.path.join(map_root, 'Global_NaturalEarth', 'Kyrgyzstan', 'Kyrgyzstan.shp'),
    'Tajikistan': os.path.join(map_root, 'Global_NaturalEarth', 'Tajikistan', 'Tajikistan.shp'),
    'Afghanistan': os.path.join(map_root, 'Global_NaturalEarth', 'Afghanistan', 'Afghanistan.shp'),
    'Pakistan': os.path.join(map_root, 'Global_NaturalEarth', 'Pakistan', 'Pakistan.shp'),

    # 中国省市
    'ChinaXinJiang': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'XinJiang_rice_cities.shp'),
    'ChinaYunNan': os.path.join(map_root, '2020China', 'YunNan.shp'),
    'ChinaGuiZhou': os.path.join(map_root, '2020China', 'GuiZhou.shp'),
    'ChinaChongQing': os.path.join(map_root, '2020China', 'ChongQing.shp'),
    'ChinaSiChuan': os.path.join(map_root, '2020China', 'SiChuan.shp'),
    'ChinaShaanXi': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'Shaanxi_rice_cities.shp'),
    'ChinaNingXia': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'NingXia_rice_cities.shp'),
    'ChinaNeiMengGu': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'NeiMengGu_rice_cities.shp'),
    'ChinaHeNan': os.path.join(map_root, '2020China', 'HeNan.shp'),
    'ChinaHeBei': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'HeBei_rice_cities.shp'),
    'ChinaShanDong': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'ShanDong_rice_cities.shp'),
    'ChinaLiaoNing': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'LiaoNing_rice_cities.shp'),
    'ChinaJiLin': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'JiLin_rice_cities.shp'),
    'ChinaHeiLongJiang': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'HeiLongJiang_rice_cities.shp'),

    'ChinaJiangSu': os.path.join(map_root, '2020China', 'JiangSu.shp'),
    'ChinaShangHai': os.path.join(map_root, '2020China', 'ShangHai.shp'),
    'ChinaAnHui': os.path.join(map_root, '2020China', 'AnHui.shp'),
    'ChinaZheJiang': os.path.join(map_root, '2020China', 'ZheJiang.shp'),
    'ChinaJiangXi': os.path.join(map_root, '2020China', 'JiangXi.shp'),
    'ChinaHuBei': os.path.join(map_root, '2020China', 'HuBei.shp'),
    'ChinaHuNan': os.path.join(map_root, '2020China', 'HuNan.shp'),
    'ChinaGuangXi': os.path.join(map_root, '2020China', 'GuangXi.shp'),
    'ChinaGuangDong': os.path.join(map_root, '2020China', 'GuangDong.shp'),
    'ChinaFuJian': os.path.join(map_root, '2020China', 'FuJian.shp'),
    'ChinaTaiWan': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'Taiwan_rice_counties.shp'),

    'ChinaHaiNan': os.path.join(map_root, 'Global_Rice', 'countries', 'China_rice', 'Hainan.shp'),

    # 南亚
    'India': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India.shp'),
    "India_TamilNadu": os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_TamilNadu.shp'),
    "India_Assam": os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Assam.shp'),
    # "India_No_TamilNadu_Assam": os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_No_TamilNadu_Assam.shp'),
    # 'India_patch': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_patch.shp'),
    "India_UttarPradesh": os.path.join(map_root, 'Global_NaturalEarth', 'India', "India_UttarPradesh.shp") ,
    'India_WestBengal': os.path.join(map_root, 'Global_NaturalEarth', 'India', "India_WestBengal.shp") ,
    'India_Jharkhand': r"C:\Users\dell\Nutstore\1\586_paper_maker\ww\Data\Global_NaturalEarth\India\India_Jharkhand.shp",
    'India_Odisha': r"C:\Users\dell\Nutstore\1\586_paper_maker\ww\Data\Global_NaturalEarth\India\India_Odisha.shp",
    'India_Chhattisgarh': r"C:\Users\dell\Nutstore\1\586_paper_maker\ww\Data\Global_NaturalEarth\India\India_Chhattisgarh.shp",

    'India_AndhraPradesh': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_AndhraPradesh.shp'),
    'India_Bihar': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Bihar.shp'),
    'India_Goa': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Goa.shp'),
    'India_Gujarat': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Gujarat.shp'),
    'India_Haryana': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Haryana.shp'),
    'India_HimachalPradesh': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_HimachalPradesh.shp'),
    'India_JammuKashmir': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_JammuKashmir.shp'),
    'India_Karnataka': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Karnataka.shp'),
    'India_Kerala': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Kerala.shp'),
    'India_MadhyaPradesh': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_MadhyaPradesh.shp'),
    'India_Maharashtra': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Maharashtra.shp'),
    'India_Manipur': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Manipur.shp'),
    'India_Meghalaya': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Meghalaya.shp'),
    'India_Mizoram': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Mizoram.shp'),
    'India_Nagaland': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Nagaland.shp'),
    'India_Punjab': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Punjab.shp'),
    'India_Rajasthan': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Rajasthan.shp'),
    'India_Sikkim': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Sikkim.shp'),
    'India_Telangana': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Telangana.shp'),
    'India_Tripura': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Tripura.shp'),
    'India_Uttarakhand': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_Uttarakhand.shp'),
    'India_': os.path.join(map_root, 'Global_NaturalEarth', 'India', 'India_.shp'),

    'Sri Lanka': os.path.join(map_root, 'Global_NaturalEarth', 'SriLanka', 'SriLanka.shp'),
    'Nepal': os.path.join(map_root, 'Global_NaturalEarth', 'Nepal', 'Nepal.shp'),
    'Bhutan': os.path.join(map_root, 'Global_NaturalEarth', 'Bhutan', 'Bhutan.shp'),
    'Bangladesh': os.path.join(map_root, 'Global_NaturalEarth', 'Bangladesh', 'Bangladesh.shp'),
    'Myanmar': os.path.join(map_root, 'Global_NaturalEarth', 'Myanmar', 'Myanmar.shp'),
    'Thailand': os.path.join(map_root, 'Global_NaturalEarth', 'Thailand', 'Thailand.shp'),
    "Lao People's Democratic Republic": os.path.join(map_root, 'Global_NaturalEarth', 'Lao', 'Lao.shp'),
    'Cambodia': os.path.join(map_root, 'Global_NaturalEarth', 'Cambodia', 'Cambodia.shp'),
    'Viet Nam': os.path.join(map_root, 'Global_NaturalEarth', 'Vietnam', 'Vietnam.shp'),
    'Malaysia': os.path.join(map_root, 'Global_NaturalEarth', 'Malaysia', 'Malaysia.shp'),
    'Brunei Darussalam': os.path.join(map_root, 'Global_NaturalEarth', 'Brunei', 'Brunei.shp'),
    'Indonesia': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'Indonesia_10m.shp'),
    'Timor-Leste': os.path.join(map_root, 'Global_NaturalEarth', 'TimorLeste', 'TimorLeste.shp'),
    'Philippines': os.path.join(map_root, 'Global_NaturalEarth', 'Philippines', 'Philippines.shp'),
    'Papua New Guinea': os.path.join(map_root, 'Global_NaturalEarth', 'PapuaNewGuinea', 'PapuaNewGuinea.shp'),

    # 美国
    'USAArkansas': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Arkansas_rice_counties.shp'),
    'USACalifornia': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'California_rice_counties.shp'),
    'USAFlorida': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Florida_rice_counties.shp'),
    'USALouisiana': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Louisiana_rice_counties.shp'),
    'USAMississippi': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Mississippi_rice_counties.shp'),
    'USAMissouri': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Missouri_rice_counties.shp'),
    'USATennessee': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Tennessee_rice_counties.shp'),
    'USATexas': os.path.join(map_root, 'Global_Rice', 'countries', 'USA_rice', 'Texas_rice_counties.shp'),

    # 南美洲
    'Chile': os.path.join(map_root, 'Global_Rice', 'countries', 'Chile_rice', 'Chile_rice_regions.shp'),
    'Argentina': os.path.join(map_root, 'Global_Rice', 'countries', 'Argentina_rice', 'Argentina_rice_provinces.shp'),
    'Uruguay': os.path.join(map_root, 'Global_Rice', '0ref_regions_v2', 'Uruguay.shp'),
    'Brazil': os.path.join(map_root, 'Global_Rice', 'countries', 'Brazil_rice', 'Brazil_rice_area.shp'),
    'Paraguay': os.path.join(map_root, 'Global_NaturalEarth', 'Paraguay', 'Paraguay.shp'),
    'Bolivia (Plurinational State of)': os.path.join(map_root, 'Global_Rice', 'countries', 'Bolivia_rice', 'Bolivia_rice_states.shp'),
    'Peru': os.path.join(map_root, 'Global_NaturalEarth', 'Peru', 'Peru.shp'),
    'Ecuador': os.path.join(map_root, 'Global_NaturalEarth', 'Ecuador', 'Ecuador__mailand_provinces.shp'),
    'Colombia': os.path.join(map_root, 'Global_Rice', 'countries', 'Colombia_rice', 'Colombia_rice_departments.shp'),
    'Venezuela (Bolivarian Republic of)': os.path.join(map_root, 'Global_NaturalEarth', 'Venezuela', 'Venezuela.shp'),
    'Guyana': os.path.join(map_root, 'Global_NaturalEarth', 'Guyana', 'Guyana.shp'),
    'Suriname': os.path.join(map_root, 'Global_NaturalEarth', 'Suriname', 'Suriname.shp'),
    'French Guiana': os.path.join(map_root, 'Global_Rice', 'countries', 'France_rice', 'Guyane_française.shp'),

    # 印尼省份
    'IndonesiaSumateraUtara': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'SumateraUtara.shp'),
    'IndonesiaSumateraSelatan': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'SumateraSelatan.shp'),
    'IndonesiaLampung': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'Lampung.shp'),
    'IndonesiaJawaBarat': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'JawaBarat.shp'),
    'IndonesiaJawaTimur': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'JawaTimur.shp'),
    'IndonesiaNusaTenggaraTimur': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'NusaTenggaraTimur.shp'),
    'IndonesiaKalimantanSelatan': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'KalimantanSelatan.shp'),
    'IndonesiaSulawesiSelatan': os.path.join(map_root, 'Global_NaturalEarth', 'Indonesia', 'SulawesiSelatan.shp'),
}

