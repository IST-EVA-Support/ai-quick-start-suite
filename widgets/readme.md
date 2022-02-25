# Widgets

In this folder, we provide some wedgets for all the scenarios to simply generate required materials. Each method described as below. All the execution path must under this path. Assume that you clone this source code in Home folder.

```
$ cd ~/ai-quick-start-suite/widgets
```

If you clone in another path, please path to folder "widgets".

## area-generator.py

This tool is provided for you to generate the "area.txt" file used for some scenarios. Before using this python code, please extract one frame by some 3rd party free tools or software and place the frame image in this folder. Then run the following steps:

1. Modify the image file name [here](http://gitlab.adlinktech.com/paul.lin/ai-quick-start-suite/blob/dev/widgets/area-generator.py#L44), or just modify the file name to "test.jpg".

2. Run this python code

   ```
   $ python3 area-generator.py
   ```

   Then you will see the window displaed the frame you prepared.

3. Select the polygon points

   Left mouse down : Select the points.

   Right moouse down : End the selection and enclose the polygon. And save to "area.txt"(if this file already exists, it will be repaced.)

   ctrl key: reset the selected points.

   Esc key or close the window: exit this program.

After finish this selection, the area.txt will be saved under the same path of this widget. Copy this file to the path you want to use.



## record-video.py

This tool is provided for you to simply record some mp4 videos as training materials for labeling. Two default GStreamer plugins are provided:

1. for webcam: v4l2src

   use the command as below to run the recorder:

   ```
   $ python3 record-video.py v4l2
   ```

   The default resolution is 640x480, you can define the resolution, for example 800X600, below:

   ```
   $ python3 record-video.py v4l2 800 600
   ```

   

2. for pylon camera: pylonsrc

   use the command as below to run the recorder:

   ```
   $ python3 record-video.py pylon
   ```

   The default resolution is 640x480, you can define the resolution, for example 800X600, below:

   ```
   $ python3 record-video.py pylon 800 600
   ```

The recorded mp4 file will save under the same path of this tool.