import os
import rasterio
from rasterio.enums import Resampling
import numpy as np
from rasterio.merge import merge
import MetaArray
import tifffile
from PIL import Image
from rasterio import CRS

def resize(input_path, output_path, input_res):
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


# Get_sentinel_folders builds a list of sentinel images to process
def get_sentinel_folders(path):
    raw_list = os.listdir(path)
    folder_list = []
    for x in range(0, len(raw_list)):
        if raw_list[x][-5:] == '.SAFE':
            folder_list.append(raw_list[x])
    return folder_list


# Define input and output paths
main_path = '/home/tamesja/Projects/ESA_EO_AFRICA/Model/INPUTS/SENTINEL2'
output_path = '/home/tamesja/Projects/ESA_EO_AFRICA/Model/INPUTS/SENTINEL2/MERGED'

# Get the list of images to resize and merge
folders = get_sentinel_folders(main_path)

# Process images with different pixel sizes
for image in folders:
    images_path = os.listdir(os.path.join(main_path, image, 'GRANULE'))
    images_path = os.path.join(main_path, image, 'GRANULE', images_path[0], 'IMG_DATA')
    images_60m = os.listdir(os.path.join(images_path, 'R60m'))
    images_20m = os.listdir(os.path.join(images_path, 'R20m'))
    images_10m = os.listdir(os.path.join(images_path, 'R10m'))

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


    b1 = resize(b1_path, os.path.join(output_path, 'b1.tiff'), 60)
    b2 = resize(b2_path, os.path.join(output_path, 'b1.tiff'), 10)
    b3 = resize(b3_path, os.path.join(output_path, 'b1.tiff'), 10)
    b4 = resize(b4_path, os.path.join(output_path, 'b1.tiff'), 10)
    b5 = resize(b5_path, os.path.join(output_path, 'b5.tiff'), 20)
    b6 = resize(b6_path, os.path.join(output_path, 'b6.tiff'), 20)
    b7 = resize(b7_path, os.path.join(output_path, 'b7.tiff'), 20)
    b8 = resize(b8_path, os.path.join(output_path, 'b1.tiff'), 10)
    b8a = resize(b8a_path, os.path.join(output_path, 'b8a.tiff'), 20)
    b9 = resize(b9_path, os.path.join(output_path, 'b9.tiff'), 60)
    b11 = resize(b11_path, os.path.join(output_path, 'b11.tiff'), 20)
    b12 = resize(b12_path, os.path.join(output_path, 'b12.tiff'), 20)


    # Save metadata from one band
    source = rasterio.open(b2_path)
    metadata = source.meta.copy()
    metadata.update(({'count': 12}))

    # Build the multiband array
    merged_im = np.squeeze(np.stack((b1, b2, b3, b4, b5, b6, b7, b8, b8a, b9, b11, b12), axis=0))

    save_name = 'S2_' + image[-54:-46] + '_' + image[-27:-21] + '.tiff'

    with rasterio.open(os.path.join(output_path, save_name), 'w', **metadata) as dst:
        dst.write(merged_im)

    print(str(image) + ' done.')
















    '''
    output_path = os.path.join(output_path, 'temp')

    resize(b1_path, os.path.join(output_path, 'b1.tiff'), 60)
    resize(b2_path, os.path.join(output_path, 'b2.tiff'), 10)
    resize(b3_path, os.path.join(output_path, 'b3.tiff'), 10)
    resize(b4_path, os.path.join(output_path, 'b4.tiff'), 10)
    resize(b5_path, os.path.join(output_path, 'b5.tiff'), 20)
    resize(b6_path, os.path.join(output_path, 'b6.tiff'), 20)
    resize(b7_path, os.path.join(output_path, 'b7.tiff'), 20)
    resize(b8_path, os.path.join(output_path, 'b8.tiff'), 10)
    resize(b8a_path, os.path.join(output_path, 'b8a.tiff'), 20)
    resize(b9_path, os.path.join(output_path, 'b9.tiff'), 60)
    resize(b11_path, os.path.join(output_path, 'b11.tiff'), 20)
    resize(b12_path, os.path.join(output_path, 'b12.tiff'), 20)

    # Paths to the input TIFF files
    b1_path = os.path.join(output_path, 'b1.tiff')
    b2_path = os.path.join(output_path, 'b2.tiff')
    b3_path = os.path.join(output_path, 'b3.tiff')
    b4_path = os.path.join(output_path, 'b4.tiff')
    b5_path = os.path.join(output_path, 'b5.tiff')
    b6_path = os.path.join(output_path, 'b6.tiff')
    b7_path = os.path.join(output_path, 'b7.tiff')
    b8_path = os.path.join(output_path, 'b8.tiff')
    b8a_path = os.path.join(output_path, 'b8a.tiff')
    b9_path = os.path.join(output_path, 'b9.tiff')
    b11_path = os.path.join(output_path, 'b11.tiff')
    b12_path = os.path.join(output_path, 'b12.tiff')

    # Paths to the output multiband TIFF file
    save_name = 'S2_' + image[-54:-46] + '.tiff'
    output_path = os.path.join(main_path, save_name)

    # Load the TIFF files
    b1 = tifffile.TiffFile(b1_path)
    b2 = tifffile.TiffFile(b2_path)
    b3 = tifffile.TiffFile(b3_path)
    b4 = tifffile.TiffFile(b4_path)
    b5 = tifffile.TiffFile(b5_path)
    b6 = tifffile.TiffFile(b6_path)
    b7 = tifffile.TiffFile(b7_path)
    b8 = tifffile.TiffFile(b8_path)
    b8a = tifffile.TiffFile(b8a_path)
    b9 = tifffile.TiffFile(b9_path)
    b11 = tifffile.TiffFile(b11_path)
    b12 = tifffile.TiffFile(b12_path)

    # Extract image data from the two TIFF files
    b1 = b1.asarray()
    b2 = b2.asarray()
    b3 = b3.asarray()
    b4 = b4.asarray()
    b5 = b5.asarray()
    b6 = b6.asarray()
    b7 = b7.asarray()
    b8 = b8.asarray()
    b8a = b8a.asarray()
    b9 = b9.asarray()
    b11 = b11.asarray()
    b12 = b12.asarray()

    # Combine the images into a multiband image
    multiband_image = np.stack((b1, b2, b3, b4, b5, b6, b7, b8, b8a, b9, b11, b12), axis=0)

    # Combine the metadata
    metadata = {
        'metadata_b1': b1.pages[0].tags,
        'metadata_b2': b2.pages[0].tags,
        'metadata_b3': b3.pages[0].tags,
        'metadata_b4': b4.pages[0].tags,
        'metadata_b5': b5.pages[0].tags,
        'metadata_b6': b6.pages[0].tags,
        'metadata_b7': b7.pages[0].tags,
        'metadata_b8': b8.pages[0].tags,
        'metadata_b8a': b8a.pages[0].tags,
        'metadata_b9': b9.pages[0].tags,
        'metadata_b11': b11.pages[0].tags,
        'metadata_b12': b12.pages[0].tags
    }

    # Save the multiband image with metadata to the output file
    with tifffile.TiffWriter(output_path) as tif:
        tif.save(multiband_image, description=metadata)

    # Close the input files
    b1.close()
    b2.close()
    b3.close()
    b4.close()
    b5.close()
    b6.close()
    b7.close()
    b8.close()
    b8a.close()
    b9.close()
    b11.close()
    b12.close()
    '''

