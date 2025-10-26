# MDP_DTW

### Required Python Packages
The required Python packages and their tested versions are listed below:

| Package | Version | Description |
|----------|----------|-------------|
| dtw-python | 1.3.0 | Dynamic Time Warping implementation |
| gdal | 3.2.3 | Geospatial Data Abstraction Library |
| numpy | 1.19.1 | Fundamental package for numerical computing |
| multiprocess | 0.70.15 | Parallel computing library |
| scipy | 1.7.3 | Scientific computing and optimization tools |

> **Note:**  
> The listed package versions are tested examples based on **Windows 10 + Python 3.7**.  
> The code can also run on other operating systems (e.g., macOS, Linux) and Python versions,  
> but users may need to install compatible package versions according to their local environment.


### Hardware Requirements
No non-standard hardware is required.


### Installation Guide
It is recommended to use a virtual environment:

```bash
# Create a new environment
conda create -n mdp_dtw python=3.7
conda activate mdp_dtw

# Install dependencies
pip install dtw-python==1.3.0
pip install gdal==3.2.3
pip install numpy==1.19.1
pip install multiprocess==0.70.15
pip install scipy==1.7.3
```

The typical installation takes approximately **2–8 minutes** on a standard desktop computer.  
If GDAL requires compilation or the network connection is slow, the process may take **10–30 minutes or longer**.


### Demo
A working example is provided in `mapping_example.py`.

The sample dataset (~13 GB) is available at Zenodo: https://doi.org/xxxxxx

Before running the code, please modify the directory paths in  
`commons/paths.py` to match your **local data directories**.

After the program finishes running, three GeoTIFF files are generated **for each year and each tile**:

| File Name Pattern | Description |
|--------------------|-------------|
| `{year}_{tile}_{algorithm}_flood-area.tif` | **flooding day of year (DOY)** for each pixel |
| `{year}_{tile}_{algorithm}_mature-day.tif` | **harvest (mature) day of year (DOY)** for each pixel |
| `{year}_{tile}_{algorithm}_distance.tif` | **Dynamic Time Warping (DTW) distance** between the reference and observed time series |


### Expected Run Time
The runtime varies depending on the number of valid pixels within each tile (after masking).  
Processing can take as little as **a few minutes** for small tiles,  
but may extend to **several hours or even days** for larger areas with many valid pixels.
