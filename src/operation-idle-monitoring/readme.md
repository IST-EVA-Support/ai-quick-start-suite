# Operation Idle Monitoring (OIM)

Operation idle monitor, OIM, is a quite useful weapon in measuring the production capacity.

This plugin, opcheck, contains one feature called opchecktime. you can use the following command to see the detail in terminal as bellow:

for plugin metadata:

```
$ gst-inspect-1.0 opcheck
```

for element metadata:

```
$ gst-inspect-1.0 opchecktime
```

In this element, the algorithm is designed for monitoring the idle status and accumulating. Illustration below is the main logic implemented:

