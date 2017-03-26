import numpy as np
from matplotlib import pyplot as plt
from tkinter import *

from open import load_dicom_folder, dicom_datasets_to_numpy
from mainwindow import MainWindow


root = Tk()
root.minsize(600, 400)
root.geometry("600x400+300+300")
app = MainWindow(root)

root.mainloop()

# folder_path = r"C:\Users\Daniel\Dropbox\DICOM series\ct_head_ex"
#
# datasets = load_dicom_folder(folder_path)
# series_arr, axes = dicom_datasets_to_numpy(datasets)


# Plot slice 80
# fig = plt.figure()
# plt.axes().set_aspect('equal', 'datalim')
# plt.set_cmap(plt.gray())
# plt.pcolormesh(axes[0], axes[1], np.flipud(series_arr[:, :, 80]))
#
# plt.show()
