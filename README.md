# VesselEnhancement

This project was a developed as a homework for a university course. It is a visualizer for 3D images of brains where vessels were previously enhanced and segmented by applying some algorithm. Vessel enhancement is a previous step for vessel segmentation. As a consequence, the program will also allow to overlay manual and automatic segmentations on the original and enhanced images of brains and control their transparency value. 

The program will include a quantitative analysis, by calculating the Dice coefficient between manual and automatic segmentations.

Additional features that seek to improve the interface are:

Color coded visualization of strictly manually segmented voxels, strictly automatically segmented voxels and voxels segmented by both methods.

3D visualization of segmentations.

Synchronization in the Z direction between visualizations of original and enhanced brains.

Window and level adjustments.

Others.

## Required software

Nibabel 2.0.2 to read Niftii images

PyQt version 4.11.2 to link python and Qt

Python 2.7.9 

Pyuic4 to convert Qt windows to python code.

Qt version 4.8.6 for GUI

Vtk version 5.8.0 for Visualization algorithms
