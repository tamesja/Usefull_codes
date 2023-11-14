import os
import rasterio
from rasterio.enums import Resampling
import numpy as np
from rasterio.merge import merge
import MetaArray
import tifffile
from PIL import Image
from rasterio import CRS


def read_band(current_band):
    with rasterio.open(current_band) as dataset:
        # resample data to target shape using upscale_factor
        data = dataset.read(
            out_shape=(
                dataset.count,
                dataset.height,
                dataset.width),
        )
        return data

main_path = '/home/tamesja/aux'


bands = []
for band in range(1, 10):
    current_band = os.path.join(main_path, 'b' + str(band) + '.tif')
    bands.append(read_band(current_band))

# Save metadata from one band
source = rasterio.open(os.path.join(main_path, 'b2.tif'))
metadata = source.meta.copy()
metadata.update(({'count': 9}))

# Build the multiband array
merged_im = np.squeeze(np.stack((bands[0], bands[0], bands[1], bands[2], bands[3], bands[4], bands[5], bands[6], bands[7], bands[8]), axis=0))
save_name = 'f1_norm.tif'
with rasterio.open(os.path.join(main_path, save_name), 'w', **metadata) as dst:
    dst.write(merged_im)
