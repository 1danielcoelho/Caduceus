# Caduceus
Super simple DICOM viewer with Python and Pydicom

## Dependencies
* Python 3.6.0 (very easy to port back to 2 if necessary)
* Numpy 1.12.1
* Pydicom 0.9.9 (for parsing DICOM files)
* Tkinter 
* Pillow 4.0.0 (for converting numpy arrays into Tkinter PhotoImages)

## Instructions
* Run __main__.py to run the application
* File -> Open and select which images to display. It will automatically ignore non-DICOM files and sort the images as best as it can
* Use the scrollwheel to switch between images
* Hold the scrollwheel and move the mouse to modify the center and width of the brightness windowing

## License
See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
