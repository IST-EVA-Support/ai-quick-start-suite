# Medical Tank Car

Security check is one of the most concerned issue in manufacture, especially for the area checking. For instance, most of the area expressly stipulated the standard protection guardrail. This kind of the protection must placed before operating. Checking irregular placement can remind the operator amend the status.

## Clone the repository

Follow the command below to clone the repository:

```
$ git clone http://GitLab.Adlinktech.com/paul.lin/ai-quick-start-suite.git
```

This might required you to input your adlink account and password. If you do not have the permission, please contact to paul.lin@adlinktech.com.

## Algorithm Description

In this element, the algorithm is designed for monitoring the object that can not appear in the pre-defined area. Illustration below is the main logic implemented:

[You can follow the code line indicate through this link](https://viewer.diagrams.net/?tags={}&highlight=0000ff&edit=_blank&layers=1&nav=1#R1Vldc6IwFP01PurwJepjt7XdznZ3O%2BPDbh8DXCE1EBpCxf76TSAIiLV2qivMdEpyuPk6uedyEwfmdZjdMRQHP6kHZGBoXjYwbwaGoVuGMZB%2FmrcpkIk9KwCfYU8ZVcACv4ECNYWm2IOkYcgpJRzHTdClUQQub2CIMbpumi0paY4aI1%2BNqFXAwkUEWmZ%2FsMeDAp0akwr%2FDtgPypH1cn0hKo1Vx0mAPLquQeZ8YF4zSnlRCrNrIJK8kpei3e07b7cTYxDxYxrca75jjN%2FClfH45sY%2FwKPpYmgWvbwikqoFq8nyTckAeIIQVaWMB9SnESLzCv3GaBp5IIfRRK2yeaA0FqAuwGfgfKN2F6WcCijgIVFv20tRq0toylw4MP%2FSJRDzgR%2BwU8uSa6kNoIi6AxoCZxthwIAgjl%2Bbm4%2BUD%2Flbu4pmUVBMf4J1vcX6QqyAt6knRPi5pHgdYA6LGOVkrIXUmgSiJC6cf4kzuRHvM%2FoKjEN2kIPyra0cVynXmKj6uqYDBQU1CZTYyVkb99xXjSN91eqUrxp7WLcJl04nN57BMkftl1QGMsEUFzxeyTGNWx9zgpwR8giOVhzcYOTSUOAxSslIYKKI8PAlxe5qmEgFDJNU%2BLmAHUId8fDgVfxPmCunDh4WcXnIUbQauojJ%2FoG6AbirUSzWaT7opllNRJR8%2BXygyJPhmEaYU5Z%2FFQCVS5ATKA1bzvSB5k4hMaspMXOPxHRjj8bsc2ls1nONWUdqbNopjVn90ZjkYFdivx2O5EAaD6Ai37BRKCUTOUmcG2vUeZZfqW5qz7IvrT29nRY8idS3V%2FqbHqm%2FMr3viAD1SYv6X%2FQSzEOG%2Bd9a%2BUl2NRqr2k2mes4rm7ISCQq2jWSl1kpWq2Z5rWz3H3a5W2n3tEdh1m6H2fukFly3wVTDEQeWFOU1FqGrleyYt0fFXBbQ0EmTj08bp4i%2BRjP6jq090dfeE3117Wzht%2FdnYa2fsizn3Qdd6tNZW5hJLkhEQB7htRCSRF4q5cqkOcCRhzhqZ0SdTITs2cUTofZJ%2FzJf4y9o8djDvt6t075udyUHLTOhMt35VCa0rZw7Ezp6n0%2B%2BzXnTK8bQpmYQUxFzklrPjxKotD5pSn26e2V82NyaaTsOVoxfudt2IV%2FwwPaF0zzDiZxVBJl8LBkKIU9qLpnA7NyOTqYXvh3V25cI88hrK7dLV8oz%2FWykiWr100rhm9UPVOb8Hw%3D%3D)

![Operation Idle Monitoring Flow Chart](../../resources/tank-car.jpg)

## Compilation

This scenario required to install EVASDK in the device. After installing the EVASDK, follow the next steps to compile this plugin and install into your device:

1. Path to the folder of this scenario. Assume that you clone this source code in Home folder.

   ```
   $ cd ~/ai-quick-start-suite/src/medical-tank-car
   ```

   If you clone in another path, please path to folder "medical-tank-car".

2. Make the build script executable if needed.

   ```
   $ sudo chmod +x opcheck-build.sh 
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

There exists one test optimized models for JNX(NVIDIA NX) in /ai-quick-start-suite/src/medical-tank-car/NX:

1. yolov4-tiny-608.engine for pose detection

   (if you are using other architecture, you can optimize it through EVASDK user manual by using /ai-quick-start-suite/src/medical-tank-car/misc/yolov4-tiny-608.onnx)


and other required materials needed in /ai-quick-start-suite/src/medical-tank-car/NX:

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

