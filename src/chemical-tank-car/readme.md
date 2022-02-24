# Chemical Tank Car

Security check is one of the most concerned issue in manufacture, especially for the area checking. For instance, most of the area expressly stipulated the standard protection guardrail. This kind of the protection must placed before operating. Checking irregular placement can remind the operator amend the status.

## Clone the repository

Follow the command below to clone the repository:

```
$ git clone http://GitLab.Adlinktech.com/paul.lin/ai-quick-start-suite.git
```

This might required you to input your adlink account and password. If you do not have the permission, please contact to paul.lin@adlinktech.com.

## Algorithm Description

In this element, the algorithm is designed for monitoring the object that can not appear in the pre-defined area. Illustration below is the main logic implemented:

[You can follow the code line indicate through this link](https://viewer.diagrams.net/?tags={}&highlight=0000ff&edit=_blank&layers=1&nav=1#R7Vtdc5s4FP0t%2B%2BCXnSEDwgb7MU2cbLvJth1vN5unjgyyUQzIESK28%2BsrGWE%2BhLGb2AbPZCaTwEUC6erec44upGNeBctbCufePXGR3wG6u%2ByY1x0AjD4AHfGju6vEYtt2YphS7MpGmWGEX5E06tIaYxdFhYaMEJ%2FhedHokDBEDivYIKVkUWw2IX7xqXM4lU%2FUM8PIgT5Smj1gl3mJtQ%2FszP4XwlMvfbJhDZIrAUwbyxtHHnTJImcyhx3zihLCkqNgeYV84bzUL0m%2Fmy1XNwOjKGT7dFiZAfCffkzAg6V9t%2FznLz%2FspWbJsbFVOmHk8vnLU0KZR6YkhP4ws36iJA5dJO6q87OszR0hc240uPEJMbaSiwljRrjJY4Evr6IlZv%2BL7hc9efaYu3K9lHden6zSk5DRVa6TOH3MX8u6rc%2FSfqqXpOMiElNHzvmzPh2D3mswA99enfnfyCXxSEujDdIpkl3t59HPb5ez2%2FvHx9unq8Un57%2Fr72k74bfcA%2BQa3CISID4e3oAiHzL8UowrKMNzumm36fqNYD5koMtUsmQYyTwyTb14h2ScslMWBvwgN4rMtA6O6kCp88YL9GM5gxF%2FIlPDx%2Fd5aoowWXiYodEcrp284OhQDAIYzZN8neClCKbtK%2FWCKEPLWt%2FKq6DoI5D6aJHLXGnycknb17cvRsGPv%2B001WuPHMw%2BUm5LKllqylWiVkoOJ8452ygFSjIhJeeU%2BxiD0o3soyUvHo7t1T0KJlG%2F%2B%2FXLg%2F%2F1KvhXA20Jw3egMdgTjs1Dh8a%2BCFDp%2Bb7i%2BX9Ik%2Flv5LI%2Fw4Jd%2BV%2FI%2FgwMDk%2B5%2By6ycXDSfR%2FOqwnWAZbPBM0JrqFosrZaz7FQe3xhGF%2B2S%2FFQcDPFzIfjC%2Bj6OJwx5HgXDgm4fQ5j%2F4Lb%2BCHE2nOMnZkWCc7VopgzKzePfTIW44URQ5QfRNThvx0PBZgLWI3BcKY5UFzhM%2BVmZ3Yx55M179bDk2PhR1Pxd7jEkYAsMn4SvMxnHAoVixh0IYMd8yadkRhP2kkJZeqRYBxHu%2Bn%2FAGyv9Yqo2q2g%2B40kOA3fd5U4GIZuuzSSaZe4aHA6kVRJ5oOK3PkQSLXkthMfrUb0UW%2FwRn1Uuo8FTiuPzEYC7pjsWqua89FTS2cHDp9LSuEq12Au1jPaHl2aUYqLvqnXhpHSoWvrpXhJxvDW6Kl169mQ%2F0Al%2F0vHiYOYLyYS8eGhLEqAHsbBWDxhD%2FY%2FIuenIaCrbGVUcbx1ALqqBAt1S98EerydQirKWicCgX3dXjfsc0kyo1uRZXcEukJTkxAzQoWXKIItSSyze8LEqtM257LCoKsu8O0aMEv4udlQTagYU7alasfC96ymEbWnLHyzNZJU5zdeI9m3RtpuEaeX9pt6b4eI048r4uq8ejbgY6vg8zmqRB3uXESj5HiBeYYrBHQGpR2rAqQqSzvlHejh9IcaIW2uoddWTXeXV3ut0n5ALas1wxAncD1o7P1F7bjPBRhNawsw%2BjjA%2Bd0sxwkLBgK5ErQTk%2BDE00IsNMt8eMoyd3VQqG%2B1mnqtffIKbAqNuzF0cBT9peglsI0qD188rQYslRjPUb43GT%2B175Ia1u%2Flb2rSGv82%2BV5ub1v17btGbfvjqH1D3XK2m9V2yv0Nrf2RMFmJ7lpIa6BbCqxeRR3CPiWtgSqtc1Yic9AYtrxPT1S9Am5xOgK9Ih9H6zyEPhIfReoBiiLxZfF6%2F83pUL9vSdUvFZVl1dBvuvwLVEz%2B%2BFZyj41iA0L0fetst0wvvu2TuCaXuc160TJ%2BTy%2BW27dSL4IzezclpNWeelGMe60YNePPtWj8yS%2B1Tix2y7uQI4pFfpr9U04SQdm%2FNpnDXw%3D%3D)

![Operation Idle Monitoring Flow Chart](../../resources/tank-car.jpg)

## Compilation

This scenario required to install EVASDK in the device. After installing the EVASDK, follow the next steps to compile this plugin and install into your device:

1. Path to the folder of this scenario. Assume that you clone this source code in Home folder.

   ```
   $ cd ~/ai-quick-start-suite/src/chemical-tank-car
   ```

   If you clone in another path, please path to folder "chemical-tank-car".

2. Make the build script executable if needed.

   ```
   $ sudo chmod +x tankcar-build.sh
   ```

   This step is just make sure you have the execute permission for this script.

3. Run the build script and then install to your device.

   ```
   $ ./tankcar-build.sh
   ```

   After run this build script, the plugin will be copied to EVASDK relative folder then clean the GStreamer cache as well.

4. Test the plugin's information.

   for plugin metadata:

   ```
   $ gst-inspect-1.0 python
   ```

   for element metadata:

   ```
   $ gst-inspect-1.0 geocheck
   ```

This plugin, geocheck, contains one feature called geocheck. you can use the command to see the detail in terminal after built.

## Run the plugin

There exists one test optimized models for JNX(NVIDIA NX) in /ai-quick-start-suite/src/chemical-tank-car/NX:

1. yolov4-tiny-608.engine for pose detection

   (if you are using other architecture, you can optimize it through EVASDK user manual by using /ai-quick-start-suite/src/chemical-tank-car/misc/yolov4-tiny-608.onnx)


and other required materials needed in /ai-quick-start-suite/src/chemical-tank-car/NX:

1. area.txt 

   this file could be generated through widget. This widget located in [area-generator.py](../../widgets/area-generator.py). Follow the [instructions here](../../widgets/readme.md) to generate your own area.txt.

2. labels.txt

   lable file used by yolov4-tiny-608.engine.

Test videos are located in [Data](/Data) folder. The videos are used for testing this plugin.

For running this plugin, run the command below for testing:

```
$ gst-launch-1.0 filesrc location=Data/4-4.MP4 ! decodebin ! nvvideoconvert ! videoconvert ! adrt model=NX/yolov4-tiny-608.engine scale=0.004 mean="0 0 0" rgbconv=true ! adtrans_yolo label=NX/label.txt input-width=608 input-height=608 blob-size="19,38" mask="(3,4,5),(1,2,3)" anchor="(10,14),(23,27),(37,58),(81,82),(135,169),(344,319)" class-num=8 use-sigmoid=True ! geocheck alert-area-def=NX/area.txt object-name=traffic-cones-irregular ! videoconvert ! ximagesink sync=false
```

You will see the following result displayed:

![displayed screen](../../resources/tankcar-event.jpg)

Illustrated red area denotes the pre-defied ara provide by user. The object "traffic-cones-irregular" is the target that can not occur in the area. This object name can be set int the property, object-name, of the plugin. This scenario can widly extended to any situation that illegal object is trained in the model and check whether it is appear in the area or not.

