# AI Quick Start Suite

This repository is focusing on demonstrating "simple", "generic" and "quick" GStreamer elements without considering too much about the accuracy. Just only for linking trained model from the ADLINK training docker. Once you are interesting in the case, you can:

1. Design the element based on the source codes in this repository;
2. For more advanced algorithm design in similar way, please refer to [ADLINK EVA Showcases](https://github.com/IST-EVA-Support/EVA_Show-Case);
3. Or start from scratch to design your own GStreamer plugins.

In this AI quick start suite, contains:

1. [Operation Idle Monitoring, OIM](src/operation-idle-monitoring);
2. [Chemical Tank Car](src/chemical-tank-car);
3. [Geofencing](src/geofencing)

## Note

If your EVASDK version is less than 3.8.1, please update the libadtrans.so for successfully run the yolov4 tiny 608 we offered in default. Replace the original libadtrans.so in /opt/adlink/eva/plugins with the file we offered in resources/3.8.1-libadtrans/your OS architecture.

