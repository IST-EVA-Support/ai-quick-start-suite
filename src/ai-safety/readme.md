# AI Enhances Safety for Cargo Tank Hazmat Offload at Semiconduction Factory

Security check is one of the most concerned issue in manufacture, especially for the area checking. For instance, most of the area expressly stipulated the standard protection guardrail. This kind of the protection must placed before operating. Checking irregular placement can remind the operator amend the status.

## Clone the repository
### The samples path are designed at ~/Downloads

Follow the command below to clone the repository:

```
$ git clone https://github.com/IST-EVA-Support/ai-quick-start-suite.git
$ mv ai-quick-start-suite ~/Downloads
```

## Algorithm Description

In this element, the algorithm is designed for monitoring the object that can not appear in the pre-defined area. Illustration below is the main logic implemented:

[You can follow the code line indicate through this link](https://viewer.diagrams.net/?tags={}&highlight=0000ff&edit=_blank&layers=1&nav=1#R7VrbcuI4EP2WfeCRlC1jGx4zCcnObLKTKXY2m6ctYQvsYFtElgPk60fCMr5IGJKAMVVTlSJW69463afVdse4Cpe3BM69e%2ByioAM0d9kxrjsA6H0AOvxPc1epxLbtVDAlvisa5YKR%2F4aEUBPSxHdRXGpIMQ6oPy8LHRxFyKElGSQEL8rNJjgozzqHUzGjlgtGDgyQ1OzRd6mXSvvAzuV%2FIn%2FqZTPr1iCtCWHWWAwce9DFi4LIGHaMK4IxTZ%2FC5RUKuPIyvaT9brbUbhZGUET36bAyQhA8%2F5yAR6v7wwpevv20l11LrI2usg0jl%2B1fFDGhHp7iCAbDXPqF4CRyER9VY6W8zR3GcybUmfAZUboShwkTipnIo2EgatHSp%2F%2Fx7hemKD0Vaq6XYuR1YZUVIkpWhU68%2BFSsy7utS1k%2FWUtCcTFOiCP2%2FFWbjoH5Fs7Aw5sz%2Fwu5OBl1M7RBMkWiq%2F0y%2Bv%2FhcnZ7%2F%2FR0%2B3y1%2BOL8e%2F0ja8f1VphAnMEtwiFi62ENCAog9V%2FLuIICntNNu03XB%2ByzJQNNmJIlYCTsyDC08gjpOkWnHAbsobCKXLQGhxooddp4hUEidjBiM1IZPkHATJPDZOH5FI3mcK3kBfMOZRDAeJ7a68RfcjBtP6lXRCha1upW1IKyjkCmo0XBcoXIKxhtX9t%2BGCU9vltpstaemDP7bXJbTMmSTU7ptTJyaNjmbL0ClHRDks1J4%2BiDykD20YzXH47t1T0KJ3G%2F9%2F3bY%2FD9KvynC9oCw094Y7CnOzYODY19PYBS831J83%2FjU9q%2FXrD%2B3Bfssv%2BS9efO4PCUu%2B8h6wcn3c%2F5ednAOsAKKKc5zjUETdZS6yXh0R47GMqO7ZJPCm6mPg3g%2BAK6gR%2FNKHK8CweHTD6HSXDBZOwR%2Bt2XxHdm3ZhzbjdOGLMy8TjAY75eGFNE2ENMHPbreCj0WQDbpTCadR3Ia9hOmdiZXczZZo279fLEWtjTlP8fLv2Yuyw8fua8zHYc8SgWUehCCjvGTbYjvp6skwRl4uFwnMS76f8AbN81y161p6D7TUjQDN%2F3JBwMI7ddMZJhl7XW15oLkpRkPlDYzu8AqZbcdvpH6yTxkTn4YHxUGccCzYZHxkkAd0x2rY2ai%2BippbMDw%2BeSELgqNJjz84y3o6urV3DRN7RaGEkderZWwUu6ho%2Bip1atZ0P%2BA5n8Lx0nCRN2mIjjw0M5SoAWJeGYz7AH%2Bx%2BR82vYSldxvHUAulI6C%2FlKfwrv8XEKUaS1GnIC%2B6q9btnnYmR6T2Fldxi6PKbGkU8x4VoiCLbEsIxeg4ZVF9ucywmDnnzAt2uHWfGfmwvVhPA15Veqdhy8aZ3ao5rSwZ82R5LF%2BSfPkeybI213EKdVcp%2BauSOI044bxNVp9Wycjy07n6%2Bx0usw5SISp88Ln1m4REBnkNqxFE5Kmdqp3kAPF3%2FICGlzDr02a7o7vWq2KvYDclrtHLPoTSWJVMdcm648dprIFC5%2FE3KY%2B%2BV33ss1Zq%2BWOXa2t3e07%2Bm17Y%2FDTIp3yK2mJsPaQk2BH%2FrFfALTnQVDzh0p3%2FBNMOpvIRsZ1YikyRcNalDI7xVP9WFB8%2B7N3JfFBs24N7AtWDl8%2BlpNj3Joco4XqFPip0l6fC%2BrbbxIBi%2BtnqWq7dvJavKlv92stvPCtaG1P1Imq9BdG2kNVMIyVSbIbpLWgCrWOasb1uBkvuVz8YTqJXyLzRFoCnscre0QBoh%2FlqqFKI75t93rDAijQ%2B2%2BJXnXzPqqUcNAYX0HysOyYv6deerC86%2F1jeEv)

![Operation Idle Monitoring Flow Chart](../../resources/tank-car.jpg)

## Compilation

This scenario required to install EVASDK in the device. After installing the EVASDK, follow the next steps to compile this plugin and install into your device:

1. Path to the folder of this scenario. Assume that you clone this source code in Home folder.

   ```
   $ cd ~/Downloads/ai-quick-start-suite/src/ai-safety
   ```

   If you clone in another path, please path to folder "ai-safety".

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

There exists one test optimized models for JNX(NVIDIA NX) in /ai-quick-start-suite/src/ai-safety/NX:

1. yolov4-tiny-608.engine for pose detection

   (if you are using other architecture, you can optimize it through EVASDK user manual by using /ai-quick-start-suite/src/ai-safety/misc/yolov4-tiny-608.onnx)

   Convert onnx model as by tensorrt. Refer to portal[https://eva-support.adlinktech.com/docs/yolov4nbsp] for more detail.

For Neon-JT2 / Neon-JNO
```
$ /usr/src/tensorrt/bin/trtexec --onnx=/home/adlink/Downloads/ai-quick-start-suite/src/ai-safety/misc/yolov4-tiny-608.onnx \
--buildOnly --saveEngine=/home/adlink/Downloads/ai-quick-start-suite/src/ai-safety/misc/yolov4-tiny-608.engine \
 --maxBatch=4 --fp16 --workspace=3000 --verboase
```

and other required materials needed in /ai-quick-start-suite/src/ai-safety/NX:

1. area.txt 

   this file could be generated through widget. This widget located in [area-generator.py](../../widgets/area-generator.py). Follow the [instructions here](../../widgets/readme.md) to generate your own area.txt.

2. labels.txt

   lable file used by yolov4-tiny-608.engine.

Test videos are located in [Data](./Data) folder. The videos are used for testing this plugin.

For running this plugin, run the command below for testing:
For Neon-NX
```
$ gst-launch-1.0 filesrc location=Data/4-4.MP4 ! decodebin ! nvvideoconvert ! videoconvert ! adrt model=NX/yolov4-tiny-608.engine scale=0.004 mean="0 0 0" rgbconv=true ! adtrans_yolo label=NX/label.txt input-width=608 input-height=608 blob-size="19,38" mask="(3,4,5),(1,2,3)" anchor="(10,14),(23,27),(37,58),(81,82),(135,169),(344,319)" class-num=8 use-sigmoid=True ! geocheck alert-area-def=NX/area.txt object-name=traffic-cones-irregular ! videoconvert ! ximagesink sync=false
```
For Neon-JT2 / Neon-JNO
```
$ gst-launch-1.0 filesrc location=Data/4-4.MP4 ! decodebin ! nvvideoconvert ! videoconvert ! adrt model=misc/yolov4-tiny-608.engine scale=0.004 mean="0 0 0" rgbconv=true ! adtrans_yolo label=NX/label.txt input-width=608 input-height=608 blob-size="19,38" mask="(3,4,5),(1,2,3)" anchor="(10,14),(23,27),(37,58),(81,82),(135,169),(344,319)" class-num=8 use-sigmoid=True ! geocheck alert-area-def=NX/area.txt object-name=traffic-cones-irregular ! videoconvert ! ximagesink sync=false
```

You will see the following result displayed:

![displayed screen](../../resources/tankcar-event.jpg)

Illustrated red area denotes the pre-defied ara provide by user. The object "traffic-cones-irregular" is the target that can not occur in the area. This object name can set in the property, object-name, of the plugin. The other property, limit-num, can set the object number that can or cannot appear in the area.  The limit-num = 0 means cannot exist the object; limit-num > 0 means can exist specific number of the object. This scenario can widly extended to any situation that illegal object is trained in the model and check whether it is appear in the area or not.

