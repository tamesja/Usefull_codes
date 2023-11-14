import os
import rasterio
import numpy as np

'''
################################################
## Merge bands in a single Tiff with metadata ##
################################################
'''


def read_band(current_band):
    with rasterio.open(current_band) as dataset:
        data = dataset.read(
            out_shape=(
                dataset.count,
                dataset.height,
                dataset.width),
        )
        return data

# Define where the bands are (named as b1.tif, b2.tif...)
main_path = 'your_path'

bands = []
for band in range(1, 10):
    current_band = os.path.join(main_path, 'b' + str(band) + '.tif')
    bands.append(read_band(current_band))

# Save metadata from one band
source = rasterio.open(os.path.join(main_path, 'b2.tif'))
metadata = source.meta.copy()

# Update band number info
metadata.update(({'count': 9}))

# Build the multiband array
merged_im = np.squeeze(np.stack((bands[0], bands[0], bands[1], bands[2], bands[3], bands[4], bands[5], bands[6], bands[7], bands[8]), axis=0))

# Save to disk
save_name = 'merged.tif'
with rasterio.open(os.path.join(main_path, save_name), 'w', **metadata) as dst:
    dst.write(merged_im)
