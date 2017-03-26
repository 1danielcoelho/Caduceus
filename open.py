import dicom
from dicom.errors import InvalidDicomError
import os
import numpy as np
from matplotlib import pyplot, cm


def load_dicom_folder(folder_path):
    dcm_files = []

    print("Loading files in \"" + folder_path + "\"")

    # Get all filenames in the target folder
    for dir_name, subdir_list, file_list in os.walk(folder_path):
        for file_name in file_list:
            dcm_files.append(os.path.join(dir_name, file_name))

    print("Found " + str(len(dcm_files)) + " files")

    # Clear non-dicom files
    datasets = []
    for file in dcm_files:
        try:
            datasets.append(dicom.read_file(file))
        except InvalidDicomError:
            print("File \"" + file + "\" is not a valid dicom file!")
            dcm_files.remove(file)

    print("Found " + str(len(dcm_files)) + " DICOM files")

    # Try to sort based on instance number then SOPInstanceUID
    try:
        datasets.sort(key=lambda x: x.InstanceNumber)
        print("Sorted based on InstanceNumber")
    except AttributeError:
        try:
            datasets.sort(key=lambda x: x.SOPInstanceUID)
            print("Sorted based on SOPInstanceUID")
        except AttributeError:
            print("Sorted based on filenames")

    return datasets


def dicom_datasets_to_numpy(datasets):
    img_dims = (int(datasets[0].Rows), int(datasets[0].Columns), len(datasets))
    img_spacings = (float(datasets[0].PixelSpacing[0]), float(datasets[0].PixelSpacing[1]), float(datasets[0].SliceThickness))

    print("Series dims: " + str(img_dims))
    print("Series spacings: " + str(img_spacings))

    # Create axes
    x = np.arange(0.0, (img_dims[0]+1)*img_spacings[0], img_spacings[0])
    y = np.arange(0.0, (img_dims[1]+1)*img_spacings[1], img_spacings[1])
    z = np.arange(0.0, (img_dims[2]+1)*img_spacings[2], img_spacings[2])

    # Load pixel data
    series_arr = np.zeros(img_dims, dtype='int32')
    for i, d in enumerate(datasets):
        # Also performs rescaling. 'unsafe' since it converts from float64 to int32
        np.copyto(series_arr[:, :, i], d.RescaleSlope * d.pixel_array + d.RescaleIntercept, 'unsafe')

    return series_arr, (x, y, z)

