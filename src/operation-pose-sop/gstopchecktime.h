#ifndef _GST_OPCHECKTIME_H_
#define _GST_OPCHECKTIME_H_

#include <gst/video/video.h>
#include <gst/video/gstvideofilter.h>
#include <opencv2/opencv.hpp>

G_BEGIN_DECLS

#define GST_TYPE_OPCHECKTIME   (gst_opchecktime_get_type())
#define GST_OPCHECKTIME(obj)   (G_TYPE_CHECK_INSTANCE_CAST((obj),GST_TYPE_OPCHECKTIME,GstOpchecktime))
#define GST_OPCHECKTIME_CLASS(klass)   (G_TYPE_CHECK_CLASS_CAST((klass),GST_TYPE_OPCHECKTIME,GstOpchecktimeClass))
#define GST_IS_OPCHECKTIME(obj)   (G_TYPE_CHECK_INSTANCE_TYPE((obj),GST_TYPE_OPCHECKTIME))
#define GST_IS_OPCHECKTIME_CLASS(obj)   (G_TYPE_CHECK_CLASS_TYPE((klass),GST_TYPE_OPCHECKTIME))

typedef struct _GstOpchecktime GstOpchecktime;
typedef struct _GstOpchecktimeClass GstOpchecktimeClass;
typedef struct _GstOPCheckTimePrivate GstOpchecktimePrivate;

struct _GstOpchecktime
{
  GstVideoFilter base_opchecktime;
  
  /*< private >*/
  GstOpchecktimePrivate *priv;
  
  cv::Mat srcMat;
  long baseTick;
  double runningTime;
  double idlingTime;
  double idleStartTime;
  int statusIdleCounter; 
};

struct _GstOpchecktimeClass
{
  GstVideoFilterClass base_opchecktime_class;
};

GType gst_opchecktime_get_type (void);

G_END_DECLS

#endif
