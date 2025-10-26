import numpy as np
try:
    from osgeo import gdal, ogr, osr
except:
    import gdal, ogr, osr
from tools.files_process import is_dir_exist


def read_raster(in_tif, mode='info', b=1):
    ds = gdal.Open(in_tif)
    prj = ds.GetProjection()
    trf = ds.GetGeoTransform()
    xsize = ds.RasterXSize  # x轴的大小：高度/列数
    ysize = ds.RasterYSize  # y轴的大小：宽度/行数
    left, xres, _, top, _, yres = list(trf)
    right = left + xres * xsize
    bottom = top + yres * ysize
    extent = (left, right, bottom, top)
    if mode != 'info':
        band = ds.GetRasterBand(b)
        # nodata = band.GetNoDataValue()
        arr = band.ReadAsArray()
        return arr, prj, trf, xsize, ysize, extent
    else:
        return [], prj, trf, xsize, ysize, extent


def read_bands(in_tif, mode='info'):
    ds = gdal.Open(in_tif)
    prj = ds.GetProjection()
    trf = ds.GetGeoTransform()
    xsize = ds.RasterXSize  # x轴的大小：高度/列数
    ysize = ds.RasterYSize  # y轴的大小：宽度/行数
    left, xres, _, top, _, yres = list(trf)
    right = left + xres * xsize
    bottom = top + yres * ysize
    extent = (left, right, bottom, top)
    if mode != 'info':
        band_num = ds.RasterCount  # 波段数量
        arrs = []
        for k in range(1, band_num+1):
            band = ds.GetRasterBand(k)
            arr = band.ReadAsArray()
            arrs.append(arr)
        return np.array(arrs), prj, trf, xsize, ysize, extent
    else:
        return [], prj, trf, xsize, ysize, extent


def create_raster(out_tif, arr, res, prj, trf, setnodata=True, nodata=255, datatype=gdal.GDT_Float32, band_num=1):
    is_dir_exist(out_tif)
    h, w = arr.shape[-2:]
    tran_list = list(trf)
    tran_list[1] = res
    tran_list[5] = -res
    trf = tuple(tran_list)
    ds = gdal.GetDriverByName('GTiff').Create(out_tif, w, h, band_num, datatype, ['COMPRESS=LZW', 'BIGTIFF=YES'])

    if len(arr.shape) == 2:  # 单层数据
        band = ds.GetRasterBand(1)
        band.WriteArray(arr)
        ds.SetProjection(prj)
        ds.SetGeoTransform(trf)
        band.FlushCache()
        if setnodata:
            band.SetNoDataValue(nodata)
    else:  # 多波段：band_num * row_num * col_num
        for k in range(arr.shape[0]):
            band = ds.GetRasterBand(k+1)
            band.WriteArray(arr[k])
            ds.SetProjection(prj)
            ds.SetGeoTransform(trf)
            band.FlushCache()
            if setnodata:
                band.SetNoDataValue(nodata)

