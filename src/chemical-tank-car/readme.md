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

[You can follow the code line indicate through this link](https://viewer.diagrams.net/?tags={}&highlight=0000ff&edit=_blank&layers=1&nav=1#R7Vltb5swEP41%2BZgIDCXJx61Lt2ndixRNWz86cAEvBjPbNKS%2FfjaYACFLiZqlibQqKvZxfrnH5%2BfOZuDcxvl7jtPoMwuADpAV5APn3QAh20VooH9WsCkl4%2FG4FIScBEapFszJExihZaQZCUC0FCVjVJK0LfRZkoAvWzLMOVu31ZaMtkdNcWhGtGrB3McUOmo%2FSCCjUjpB41r%2BAUgYVSPb3rR8E%2BNK2XQsIhywdUPkzAbOLWdMlqU4vwWqwatwKdvd%2FeXtdmIcEtmnwUcrXKCbp3iFvj356ScIWDYfOmUvj5hmxmAzWbmpEIBAAWKqjMuIhSzBdFZL33KWJQHoYSxVq3XuGUuV0FbCXyDlxqwuziRTokjG1LztmmKsEyzjPhyYf%2BUSmIcgD%2BgZs7QtjQEMUO%2BBxSD5RilwoFiSx%2FbiY%2BND4VavhlkVDNJHoG53UJ8rC2QXekqVn2uI1xGRME9xAcZabbU2gFikpfMvSa4X4u%2BIPgKXkB%2FEoHrrGcc1OxeNTX3d2AdGFDW2QCU7OWo3V%2B6rqKevumfy1e8C%2BNfFL%2B04yKJ4AbRC1aNSO5VeWA7LQur9zjRRKSSkwumN7hPdhUSqdiMcUJKsJPjRyGexkqc4oyMlU0VMhr8z4q%2BGQnv4UGTKj5V4QdlCPQJ4VP8F9%2FXUICCKd4cSJ6uhj7nuH5gfgb8apcoO5952nHoiqhTq5z3DgaZblhDJeMH6gCsT9AQqxRIfPdPSzNNaEmMhgR9rDHrO51Fj6c0eabj7M6ywZIm8ZVShorUdS%2F3NZkZe7RL3RGThtsnC2UMWNtrDFt7xbKGqDdc9gkCmV04gbk8CmfwnkP17Ttu4yx9fFxLrgSwZQQ0u8nCsd1OyEGmhbDFj6MUTC%2BrDK%2B6V8orrXSCv2N187kGdWa6KWyY9uaU6l11KJj3uQP%2BFvQbykBP5s1F%2B0F2NbkztXW56LiqbqpIoCLaNdKXRSlfrZkWtaneGVT7Xeen6QojXDSEfRSNwbAOFRRJF3KIsr4liq06W6txdQzzxesSTycF4wiMWLzLx%2FDn2nJEFtSPLjbsnsnh7IottnTO0XP0FjfWfcl567J1Mu5wjCq7BFPS1kRWDEPoisyAdVggkDrDE3UT24vmmMPdZwrGtwSHGuSCe2clgveklZrDdu7XXSaNeQDR9r9fsc92v9YTeu5TDQ5XCVnnqUSnstvKvU9je63zyZS6avuEcbxoKKVOMKxo9f9OCevuP27t%2FsvuR5rC6O7V2HKwcv3a3rSEv8EDU8cBZToSeVQK5fiw5jqHIVne8sndidwoi3fkeMZ688veIikiauCVBd%2Bde0kecqf3PQFPV%2BmNm6Zv1J2Fn9gc%3D)

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

