import os
import rasterio
from rasterio.enums import Resampling
import numpy as np

'''
################################
## Compose S2 L2A single tiff ##
################################
'''

# resize upscales bands with lower resolution to 10m with nearest method
def resize(input_path, input_res):
    upscale_factor = int(input_res / 10)
    with rasterio.open(input_path) as dataset:
        # resample data to target shape using upscale_factor
        data = dataset.read(
            out_shape=(
                dataset.count,
                int(dataset.height * upscale_factor),
                int(dataset.width * upscale_factor)
            ),
            resampling=Resampling.nearest
        )
        dst_transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )

    return data


# get_sentinel_folders builds a list of sentinel images to process
def get_sentinel_folders(path):
    raw_list = os.listdir(path)
    folder_list = []
    for x in range(0, len(raw_list)):
        if raw_list[x][-5:] == '.SAFE':
            folder_list.append(raw_list[x])
    return folder_list


# main_path has some .SAFE S2L2A images inside
main_path = 'input_folder'
output_path = 'output_folder'

# Get the list of images to resize and merge
folders = get_sentinel_folders(main_path)

# Process images with different pixel sizes
for image in folders:

    # Going to jp2 files inside S2 folders
    images_path = os.listdir(os.path.join(main_path, image, 'GRANULE'))
    images_path = os.path.join(main_path, image, 'GRANULE', images_path[0], 'IMG_DATA')
    images_60m = os.listdir(os.path.join(images_path, 'R60m'))
    images_20m = os.listdir(os.path.join(images_path, 'R20m'))
    images_10m = os.listdir(os.path.join(images_path, 'R10m'))

    # Save path to different bands
    for current_image in images_60m:
        if current_image[-4:] == '.jp2':
            if current_image.count('B01') != 0:
                b1_path = os.path.join(images_path, 'R60m', current_image)
            if current_image.count('B09') != 0:
                b9_path = os.path.join(images_path,'R60m', current_image)
    for current_image in images_20m:
        if current_image[-4:] == '.jp2':
            if current_image.count('B05') != 0:
                b5_path = os.path.join(images_path, 'R20m', current_image)
            if current_image.count('B06') != 0:
                b6_path = os.path.join(images_path, 'R20m', current_image)
            if current_image.count('B07') != 0:
                b7_path = os.path.join(images_path, 'R20m', current_image)
            if current_image.count('B8A') != 0:
                b8a_path = os.path.join(images_path, 'R20m', current_image)
            if current_image.count('B11') != 0:
                b11_path = os.path.join(images_path, 'R20m', current_image)
            if current_image.count('B12') != 0:
                b12_path = os.path.join(images_path, 'R20m', current_image)
    for current_image in images_10m:
        if current_image[-4:] == '.jp2':
            if current_image.count('B02') != 0:
                b2_path = os.path.join(images_path, 'R10m', current_image)
            if current_image.count('B03') != 0:
                b3_path = os.path.join(images_path, 'R10m', current_image)
            if current_image.count('B04') != 0:
                b4_path = os.path.join(images_path, 'R10m', current_image)
            if current_image.count('B08') != 0:
                b8_path = os.path.join(images_path, 'R10m', current_image)

    # Resize all bands to 10m bands size
    b1 = resize(b1_path, 60)
    b2 = resize(b2_path, 10)
    b3 = resize(b3_path, 10)
    b4 = resize(b4_path, 10)
    b5 = resize(b5_path, 20)
    b6 = resize(b6_path, 20)
    b7 = resize(b7_path, 20)
    b8 = resize(b8_path, 10)
    b8a = resize(b8a_path, 20)
    b9 = resize(b9_path, 60)
    b11 = resize(b11_path, 20)
    b12 = resize(b12_path, 20)

    # Save metadata from one band to keep geo info
    source = rasterio.open(b2_path)
    metadata = source.meta.copy()
    metadata.update(({'count': 12}))

    # Build the multiband array
    merged_im = np.squeeze(np.stack((b1, b2, b3, b4, b5, b6, b7, b8, b8a, b9, b11, b12), axis=0))

    # Save tile and date in name
    save_name = 'S2_' + image[-54:-46] + '_' + image[-27:-21] + '.tiff'

    with rasterio.open(os.path.join(output_path, save_name), 'w', **metadata) as dst:
        dst.write(merged_im)

    print(str(image) + ' done.')
