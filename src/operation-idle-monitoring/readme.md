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

<!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=5,IE=9" ><![endif]-->

<!DOCTYPE html>
<html>
<head>
<title>OIM</title>
<meta charset="utf-8"/>
</head>
<body><div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;tpdc-km.adlinktech.com\&quot; modified=\&quot;2022-02-11T06:11:18.415Z\&quot; agent=\&quot;5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36\&quot; etag=\&quot;Ib_WXfSNPdSURTmV4N6l\&quot; version=\&quot;15.2.8\&quot; type=\&quot;atlas\&quot;&gt;&lt;mxAtlasLibraries/&gt;&lt;diagram id=\&quot;0xkf9zAJJiEXn8yoqzZ-\&quot; name=\&quot;Page-1\&quot;&gt;5VxRc6M2EP41frQHhI3tx5zj3GUmvXSaae/SlxsZZEMCiBMitvvrK2FhA5KJL3GM1M5kErRISNrdb7W7ktJzZvHmM4Fp8Bv2UdQDlr/pOdc9AOwJAD3+Y/lbQbHH4x1lRUJf0A6Eh/AfJIiWoOahj7JaRYpxRMO0TvRwkiCP1miQELyuV1viqN5rCleiR+tAePBghKRq30KfBjvqBIwP9C8oXAVlz7Y73b2JYVlZfDgLoI/XFZIz7zkzgjHdPcWbGYo490q+7NrdHHm7HxhBCT2lwezHbfpXPE7x33f9LfyWzNIfs37J5hcY5WLGYrR0W7IA+YwjoogJDfAKJzCaH6ifCM4TH/F+LFY61LnDOGVEmxGfEKVbIV6YU8xIAY0j8Vaei5hehnPiobYJCJ2AZIVoSz0hFT6XSgeCU58RjhElW1aBoAjS8KUufSiUaLWvd+AzexCs/hW2S1x/YDOgMuujiCk6Z/E6CCl6SGHBjDUDW52BMEt32r8MN1wQxzn6gghFm1YelG9LzRXY7ZfldQUIghRUMFDSzs81x3BlHZ6orDbQSluHEtvvFxSGCZ9KgIph/MxDwnjKPpQsEWOMVxR8SGEPuBGb66cFYU8r/mQPelyTdmTIlYegZfFd92fOrSFjNmWiuOKjBjerkEZwMYB+FCbPFHnBwMMxo6cwjwYRH8UNDPtsAN5zP+Mo6mc5wwojLyK8YH989MJ+Z8Rjv3GKCOMYTvqhH6F+jJOQYhImK95RRnHqBch7pmGMBl6a9oBz50yHh4GVU2CfSVKc8bkzFsPqPPlwymry3IFRcx8CV567j9hAaCFfvHjiVqcu6DoDGvB8xYydwWo5o5rRsiey0QIjhdVyP8xqycbeLKs1PdFqDbUyWlMF1w2BXeFDNmF3hyGHnGheeLdIF8zZVt1TmMqY2zsTl8HcSJL+V9wF6tAmpN9Fc/78yJ8HI1G63lReXW9F4R3OMDjVwTgVq0LA1sByXRHynAxf8bXfcZjQShW8XGaISiLed/oOqY8lqT+y2LFDsduaid39VbHbY3ekvdjBUVOfpTBpOmPam//h2JbN/21W9bcK3/uKLwDOTZvjyUdRY0EDCiTA8SLPXo8vz7BITOtrBBgrFonhJcPJPb66WRH25uCx8kZtGhjTybbSiBcfq+8OzYrSGUzKyaGqZokVOVY1CPdjGfcP3GZa9yXwlxFccbFg/gwjHoFq4QH2G7kix1Wg272kCwiMz2y6hkLQ/f9AkJJcFwTuEx36IFBWBIPc8Q7W3FMTLWCkFeCBHHaZE2zrLGa9Emq2wRm14cQ5ElKtSZjtIyrYFlHpEzoNVab9oqGTY0n80DR0ejtOwakhEJhohVNgcgg0GR3zv0qgmhIBjbr3v1QG26QIqPRzjEOgvPvwX0WgxgHQRQEIyJen2/TRvcnv0Xr+x6dgbEV9VV7aKPxNZPwpJ2rrBb+JwfCbgmPw83JSiJDrD6TM89QEdo29X1cFu4/a/FVqoyr/pCns2tD0Kuo6ywK0jdpE0I34Kdgm6GY45sIrFJnpMRMlQS8h5rjTG4DjYdcAVG7ImoRA59R1r7OFr23YRkJwqFj3/kx9yLsQp0xL1FnL4vxTgjaFN0pgrI0L2jwHNeoairqkZt+ORUUM2Kb8mkBRDr072vr4eMZ3Fnu3jdpIG2hPZBv4FRUnrYujUxaMEKF7A+jjdZJRgmCsY866EY1PFJdHlNH4OXLW6sXamJz1fk/Kru1IHTao3rMn1YZhw4yswXH+CCiOeD/UQB6jLOOXE/neVJFra79pcnFnx7EbCHe6dnYUh79M83bsU4N/Wy8oKg7cd3zW422HAC5lcFVyvsylmqLpFSFwW6mQ8sPaWeXL5entcnOrGdnY1qRx2/i1FuWN7oOW7Qbx1qPgrWytqOF8s9u1qIWL3F/q0jdq3FGzVCkb1SW1j3OO5NzBPPFl/Op0H9m2FUfIz3QhmRUPN/N32nn4BwfO/F8=&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
</body>
</html>

