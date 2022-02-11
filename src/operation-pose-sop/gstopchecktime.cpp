#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gst/gst.h>
#include <gst/video/video.h>
#include <gst/video/gstvideofilter.h>
#include "gstopchecktime.h"
#include <chrono>
#include <iostream>
#include <fstream>
#include <regex>
#include <string>
#include <vector>
#include "gstadmeta.h"
#include "utils.h"
#define NANO_SECOND 1000000000.0
////#define DEFAULT_ALERT_TYPE "EXCEED"


GST_DEBUG_CATEGORY_STATIC (gst_opchecktime_debug_category);
#define GST_CAT_DEFAULT gst_opchecktime_debug_category

static void gst_opchecktime_set_property (GObject * object, guint property_id, const GValue * value, GParamSpec * pspec);
static void gst_opchecktime_get_property (GObject * object, guint property_id, GValue * value, GParamSpec * pspec);
static void gst_opchecktime_dispose (GObject * object);
static void gst_opchecktime_finalize (GObject * object);

static void gst_opchecktime_before_transform (GstBaseTransform * trans, GstBuffer * buffer);
static gboolean gst_opchecktime_start (GstBaseTransform * trans);
static gboolean gst_opchecktime_stop (GstBaseTransform * trans);
static gboolean gst_opchecktime_set_info (GstVideoFilter * filter, GstCaps * incaps, GstVideoInfo * in_info, GstCaps * outcaps, GstVideoInfo * out_info);
//static GstFlowReturn gst_opchecktime_transform_frame (GstVideoFilter * filter, GstVideoFrame * inframe, GstVideoFrame * outframe);
static GstFlowReturn gst_opchecktime_transform_frame_ip (GstVideoFilter * filter, GstVideoFrame * frame);

static void mapGstVideoFrame2OpenCVMat(GstOpchecktime *opchecktime, GstVideoFrame *frame, GstMapInfo &info);
static void getDetectedData(GstOpchecktime *opchecktime, GstBuffer* buffer);
static void doAlgorithm(GstOpchecktime *opchecktime, GstBuffer* buffer);
static void drawAlertArea(GstOpchecktime *opchecktime);

enum class PROC_STATUS {Empty, Object_Only, Wrist_Only, Both};

struct _GstOPCheckTimePrivate
{
    std::string object_place_definition_path;
    std::vector<std::vector<double>> ratio_vec;
    std::vector<cv::Point> area_point_vec;
    std::vector<std::vector<cv::Point>> obj_vec;
    std::vector<cv::Point> wrist_vec;
    PROC_STATUS status;
    PROC_STATUS last_status;
    float statusSec;
    bool area_display;
    bool object_display;
    bool alert;
	gchar* alertType;
};

enum
{
    PROP_0,
    PROP_STATUS_SEC,
    PROP_ALERT_AREA_DEFINITION,
    PROP_ALERT_AREA_DISPLAY,
    PROP_ALERT_OBJ_DISPLAY,
    PROP_ALERT_TYPE,
};

#define DEBUG_INIT GST_DEBUG_CATEGORY_INIT(GST_CAT_DEFAULT, "gstopchecktime", 0, "debug category for gstopchecktime element");
G_DEFINE_TYPE_WITH_CODE(GstOpchecktime, gst_opchecktime, GST_TYPE_VIDEO_FILTER, G_ADD_PRIVATE(GstOpchecktime) DEBUG_INIT)

/* pad templates */

/* FIXME: add/remove formats you can handle */
#define VIDEO_SRC_CAPS \
    GST_VIDEO_CAPS_MAKE("{ BGR }")

/* FIXME: add/remove formats you can handle */
#define VIDEO_SINK_CAPS \
    GST_VIDEO_CAPS_MAKE("{ BGR }")

/* class initialization */
static void gst_opchecktime_class_init (GstOpchecktimeClass * klass)
{
  GObjectClass *gobject_class = G_OBJECT_CLASS (klass);
  GstBaseTransformClass *base_transform_class = GST_BASE_TRANSFORM_CLASS (klass);
  GstVideoFilterClass *video_filter_class = GST_VIDEO_FILTER_CLASS (klass);

  /* Setting up pads and setting metadata should be moved to
     base_class_init if you intend to subclass this class. */
  gst_element_class_add_pad_template (GST_ELEMENT_CLASS(klass),
      gst_pad_template_new ("src", GST_PAD_SRC, GST_PAD_ALWAYS,
        gst_caps_from_string (VIDEO_SRC_CAPS)));
  gst_element_class_add_pad_template (GST_ELEMENT_CLASS(klass),
      gst_pad_template_new ("sink", GST_PAD_SINK, GST_PAD_ALWAYS,
        gst_caps_from_string (VIDEO_SINK_CAPS)));

  gst_element_class_set_static_metadata (GST_ELEMENT_CLASS(klass),
      "Adlink OP-Check-Time video filter", "Filter/Video", "An ADLINK OP-Check-Time demo video filter", "Dr. Paul Lin <paul.lin@adlinktech.com>");

  gobject_class->set_property = gst_opchecktime_set_property;
  gobject_class->get_property = gst_opchecktime_get_property;
  
  // Install the properties to GObjectClass
  g_object_class_install_property (G_OBJECT_CLASS (klass), PROP_STATUS_SEC,
                                   g_param_spec_float("status-ok-time", "rstatus-ok-time", "Each status must not keep exceed this setting time.", 0, 100, 7, G_PARAM_READWRITE));
  g_object_class_install_property (G_OBJECT_CLASS (klass), PROP_ALERT_AREA_DEFINITION,
                                   g_param_spec_string ("obj-place-def", "Obj-place-def", "The definition place location of the object respect the frame based on the specific resolution.", "", (GParamFlags)(G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS)));
  
  g_object_class_install_property (G_OBJECT_CLASS (klass), PROP_ALERT_TYPE,
                                   g_param_spec_string ("alert-type", "Alert-Type", "The alert type name when event occurred.", "excced\0"/*DEFAULT_ALERT_TYPE*/, (GParamFlags)(G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS)));
  
  g_object_class_install_property (G_OBJECT_CLASS (klass), PROP_ALERT_AREA_DISPLAY,
                                   g_param_spec_boolean("area-display", "Area-display", "Show alert area in frame.", FALSE, G_PARAM_READWRITE));
  
  g_object_class_install_property (G_OBJECT_CLASS (klass), PROP_ALERT_OBJ_DISPLAY,
                                   g_param_spec_boolean("object-display", "Object-display", "Show inferenced object in frame.", FALSE, G_PARAM_READWRITE));
  
  
  gobject_class->dispose = gst_opchecktime_dispose;
  gobject_class->finalize = gst_opchecktime_finalize;
  base_transform_class->before_transform = GST_DEBUG_FUNCPTR(gst_opchecktime_before_transform);
  base_transform_class->start = GST_DEBUG_FUNCPTR (gst_opchecktime_start);
  base_transform_class->stop = GST_DEBUG_FUNCPTR (gst_opchecktime_stop);
  video_filter_class->set_info = GST_DEBUG_FUNCPTR (gst_opchecktime_set_info);
  //video_filter_class->transform_frame = GST_DEBUG_FUNCPTR (gst_opchecktime_transform_frame);
  video_filter_class->transform_frame_ip = GST_DEBUG_FUNCPTR (gst_opchecktime_transform_frame_ip);

}

static void gst_opchecktime_init (GstOpchecktime *opchecktime)
{
    /*< private >*/
    opchecktime->priv = (GstOpchecktimePrivate *)gst_opchecktime_get_instance_private (opchecktime);
    
    opchecktime->priv->area_display = false;
    opchecktime->priv->object_display = false;
    opchecktime->priv->alert = false;
    opchecktime->priv->statusSec = 7;
    
    opchecktime->baseTick = 0;
    opchecktime->runningTime = 0;
    opchecktime->idlingTime = 0;
    opchecktime->idleStartTime = 0;
    opchecktime->statusIdleCounter = 0;
    
    opchecktime->priv->alertType = "exceed\0";//DEFAULT_ALERT_TYPE;
}

void gst_opchecktime_set_property (GObject * object, guint property_id, const GValue * value, GParamSpec * pspec)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (object);

  GST_DEBUG_OBJECT (opchecktime, "set_property");

  switch (property_id)
  {
    case PROP_STATUS_SEC:
    {
        opchecktime->priv->statusSec = g_value_get_float(value);
        break;
    }
    case PROP_ALERT_AREA_DEFINITION:
    {
        opchecktime->priv->object_place_definition_path = g_value_dup_string(value);
        GST_MESSAGE(std::string("opchecktime->priv->object_place_definition_path = " + opchecktime->priv->object_place_definition_path).c_str());
        
        GST_MESSAGE("Start parsing definition file...");
        std::ifstream infile(opchecktime->priv->object_place_definition_path);
        if(!infile) 
        {
            std::cout << "Cannot open input file.\n";
            break;
        }
        std::string lineString;
        while (std::getline(infile, lineString))
        {
            std::vector<std::string> ratioVec = split(lineString);
            double x = std::atof(ratioVec[0].c_str());
            double y = std::atof(ratioVec[1].c_str());
            
            std::vector<double> vec;
            vec.push_back(x);
            vec.push_back(y);
            opchecktime->priv->ratio_vec.push_back(vec);
        }
        GST_MESSAGE("Parsing definition file done!");
        
        break;  
    }
    case PROP_ALERT_TYPE:
    {
        opchecktime->priv->alertType = g_value_dup_string(value);
        break;  
    }
    case PROP_ALERT_AREA_DISPLAY:
    {
        opchecktime->priv->area_display = g_value_get_boolean(value);
        if(opchecktime->priv->area_display)
            GST_MESSAGE("Display area is enabled!");
        break;
    }
    case PROP_ALERT_OBJ_DISPLAY:
    {
        opchecktime->priv->object_display = g_value_get_boolean(value);
        if(opchecktime->priv->object_display)
            GST_MESSAGE("Display inferenced person is enabled!");
        break;
    }
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
        break;
  }
}

void gst_opchecktime_get_property (GObject * object, guint property_id, GValue * value, GParamSpec * pspec)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (object);

  GST_DEBUG_OBJECT (opchecktime, "get_property");

  switch (property_id)
  {
    case PROP_STATUS_SEC:
        g_value_set_float(value, opchecktime->priv->statusSec);
        break;
    case PROP_ALERT_AREA_DEFINITION:
       g_value_set_string (value, opchecktime->priv->object_place_definition_path.c_str());
       break;
    case PROP_ALERT_TYPE:
       //g_value_set_string (value, opchecktime->priv->alertType.c_str());
	   g_value_set_string (value, opchecktime->priv->alertType);
       break;
    case PROP_ALERT_AREA_DISPLAY:
       g_value_set_boolean(value, opchecktime->priv->area_display);
       break;
    case PROP_ALERT_OBJ_DISPLAY:
       g_value_set_boolean(value, opchecktime->priv->object_display);
       break;
    default:
       G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
      break;
  }
}

void gst_opchecktime_dispose (GObject * object)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (object);

  GST_DEBUG_OBJECT (opchecktime, "dispose");

  /* clean up as possible.  may be called multiple times */

  G_OBJECT_CLASS (gst_opchecktime_parent_class)->dispose (object);
}

void gst_opchecktime_finalize (GObject * object)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME(object);

  GST_DEBUG_OBJECT (opchecktime, "finalize");

  /* clean up object here */

  G_OBJECT_CLASS (gst_opchecktime_parent_class)->finalize (object);
}

static gboolean gst_opchecktime_start (GstBaseTransform * trans)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (trans);

  GST_DEBUG_OBJECT (opchecktime, "start");
  
  return TRUE;
}

static gboolean gst_opchecktime_stop (GstBaseTransform * trans)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (trans);

  opchecktime->baseTick = 0;
  opchecktime->runningTime = 0;
    
  GST_DEBUG_OBJECT (opchecktime, "stop");

  return TRUE;
}

static gboolean gst_opchecktime_set_info (GstVideoFilter * filter, GstCaps * incaps, GstVideoInfo * in_info, GstCaps * outcaps, GstVideoInfo * out_info)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (filter);

  GST_DEBUG_OBJECT (opchecktime, "set_info");
  
                
  // Start to parse the real area point
  int width = in_info->width;
  int height = in_info->height;
  for(uint id = 0; id < opchecktime->priv->ratio_vec.size(); ++id)
  {
      cv::Point2d p;
      p.x = (int)(width * opchecktime->priv->ratio_vec[id][0]);
      p.y = (int)(height * opchecktime->priv->ratio_vec[id][1]);
      
      opchecktime->priv->area_point_vec.push_back(p);
  }
  return TRUE;
}

/* transform */
// static GstFlowReturn gst_opchecktime_transform_frame (GstVideoFilter * filter, GstVideoFrame * inframe, GstVideoFrame * outframe)
// {
//   GstOpchecktime *opchecktime = GST_OPCHECKTIME (filter);
// 
//   GST_DEBUG_OBJECT (opchecktime, "transform_frame");
// 
//   return GST_FLOW_OK;
// }

double getElementLifeTime(GstOpchecktime *opchecktime)
{
    long base_time = (GST_ELEMENT (opchecktime))->base_time;
    long current_time = gst_clock_get_time((GST_ELEMENT (opchecktime))->clock);
    return (current_time - base_time)/NANO_SECOND;
}

static void gst_opchecktime_before_transform (GstBaseTransform * trans, GstBuffer * buffer)
{
    GstOpchecktime *opchecktime = GST_OPCHECKTIME (trans);
    opchecktime->runningTime = getElementLifeTime(opchecktime);
}

static GstFlowReturn gst_opchecktime_transform_frame_ip (GstVideoFilter * filter, GstVideoFrame * frame)
{
  GstOpchecktime *opchecktime = GST_OPCHECKTIME (filter);
  GstMapInfo info;

  GST_DEBUG_OBJECT (opchecktime, "transform_frame_ip");
  gst_buffer_map(frame->buffer, &info, GST_MAP_READ);
  // map frame data from stream to opchecktime srcMat
  mapGstVideoFrame2OpenCVMat(opchecktime, frame, info);
  
  // get inference detected object and pose wrist
  getDetectedData(opchecktime, frame->buffer);
  
  // do algorithm
  doAlgorithm(opchecktime, frame->buffer);
  
  // draw alert area
  drawAlertArea(opchecktime);
  
  gst_buffer_unmap(frame->buffer, &info);
  return GST_FLOW_OK;
}

static void mapGstVideoFrame2OpenCVMat(GstOpchecktime *opchecktime, GstVideoFrame *frame, GstMapInfo &info)
{
    if(opchecktime->srcMat.cols == 0 || opchecktime->srcMat.rows == 0)
        opchecktime->srcMat = cv::Mat(frame->info.height, frame->info.width, CV_8UC3, info.data);
    else if((opchecktime->srcMat.cols != frame->info.width) || (opchecktime->srcMat.rows != frame->info.height))
    {
        opchecktime->srcMat.release();
        opchecktime->srcMat = cv::Mat(frame->info.height, frame->info.width, CV_8UC3, info.data);
    }
    else
        opchecktime->srcMat.data = info.data;
}

static void getDetectedData(GstOpchecktime *opchecktime, GstBuffer* buffer)
{
    // reset for each frame
    opchecktime->priv->obj_vec.clear();
    opchecktime->priv->wrist_vec.clear();
    
    
    GstAdBatchMeta *meta = gst_buffer_get_ad_batch_meta(buffer);
    if (meta == NULL)
        GST_MESSAGE("Adlink metadata is not exist!");
    else
    {
        AdBatch &batch = meta->batch;
        
        bool frame_exist = batch.frames.size() > 0 ? true : false;
        if(frame_exist)
        {
            VideoFrameData frame_info = batch.frames[0];
                
            int detectionBoxResultNumber = frame_info.detection_results.size();
            int width = opchecktime->srcMat.cols;
            int height = opchecktime->srcMat.rows;
            for(int i = 0 ; i < detectionBoxResultNumber ; ++i)
            {
                adlink::ai::DetectionBoxResult detection_result = frame_info.detection_results[i];
                if(detection_result.meta.compare("pose") == 0)
                {
                    // Each line annotation is recorded in "class_label", console out it for clearly understand the meta.
                    //std::cout << "pose box class label = " << detection_result.class_label << std::endl;
                    
                    // point1 and point2 denotes one single line(max 18 openpose point)
                    if(detection_result.class_label.compare("r_elb,r_wri") == 0)
                    {
                        // Elbow
                        int x1 = (int)(width * detection_result.x1);
                        int y1 = (int)(height * detection_result.y1);
                        
                        // Wrist
                        int x2 = (int)(width * detection_result.x2);
                        int y2 = (int)(height * detection_result.y2);
                        
                        opchecktime->priv->wrist_vec.push_back(cv::Point2d(x2, y2));
                        
                        if(opchecktime->priv->object_display)
                        {
                            // paint elbow
                            cv::circle(opchecktime->srcMat, cv::Point(x1, y1), 6, cv::Scalar(165,42,42), 3);
                            cv::circle(opchecktime->srcMat, cv::Point(x1, y1), 3, cv::Scalar(191,239,255), 3);
                            
                            // paint wrist
                            cv::circle(opchecktime->srcMat, cv::Point(x2, y2), 6, cv::Scalar(0,0,255), 3);
                            cv::circle(opchecktime->srcMat, cv::Point(x2, y2), 3, cv::Scalar(144,238,144), 3);
                            cv::line(opchecktime->srcMat, cv::Point(x1, y1), cv::Point(x2, y2), cv::Scalar(0,128,68), 3);
                        }
                    }
                }
                
                if(detection_result.obj_label.compare("obj") == 0)
                {
                    int x1 = (int)(width * detection_result.x1);
                    int y1 = (int)(height * detection_result.y1);
                    int x2 = (int)(width * detection_result.x2);
                    int y2 = (int)(height * detection_result.y2);
                    
                    std::vector<cv::Point> objPoint_vec;
                    objPoint_vec.push_back(cv::Point2d(x1, y1));
                    objPoint_vec.push_back(cv::Point2d(x2, y1));
                    objPoint_vec.push_back(cv::Point2d(x2, y2));
                    objPoint_vec.push_back(cv::Point2d(x1, y2));
                    
                    opchecktime->priv->obj_vec.push_back(objPoint_vec);
                    
                    int current_id = opchecktime->priv->obj_vec.size() - 1;
                    
                    if(opchecktime->priv->object_display)
                        cv::rectangle(opchecktime->srcMat, cv::Point(opchecktime->priv->obj_vec[current_id][0].x, opchecktime->priv->obj_vec[current_id][0].y), cv::Point(opchecktime->priv->obj_vec[current_id][2].x, opchecktime->priv->obj_vec[current_id][2].y), cv::Scalar(0,128,128), 3, cv::LINE_8);
                        
                }
            }
        }
    }
}

static void doAlgorithm(GstOpchecktime *opchecktime, GstBuffer* buffer)
{
    // If no region, return directly. Points must larger than 2.
    if(opchecktime->priv->area_point_vec.size() <= 2)
        return;
    
    // If metadata does not exist, return directly.
    GstAdBatchMeta *meta = gst_buffer_get_ad_batch_meta(buffer);
    if (meta == NULL)
    {
        GST_MESSAGE("Adlink metadata is not exist!");
        return;
    }
    AdBatch &batch = meta->batch;
    bool frame_exist = batch.frames.size() > 0 ? true : false;
    
    std::vector<cv::Point> intersectionPolygon;
    int num_obj_detected = opchecktime->priv->obj_vec.size();
    bool isObjInArea = false;
    for(int id = 0; id < num_obj_detected; ++id)
    {
        float intersectArea = cv::intersectConvexConvex(opchecktime->priv->area_point_vec, opchecktime->priv->obj_vec[id], intersectionPolygon, true);
        
        double obj_area = contourArea(opchecktime->priv->obj_vec[id], false);
        
        isObjInArea = intersectArea / obj_area > 0.75 ? true : false;
    }
    
    // Check whether the wrist inside area or not
    int num_wrist_detected = opchecktime->priv->wrist_vec.size();
    bool isWristInArea = false;
    for(int id = 0 ; id < num_wrist_detected ; ++id)
    {
        if(cv::pointPolygonTest(opchecktime->priv->area_point_vec, opchecktime->priv->wrist_vec[id], false) >= 0)
        {
            isWristInArea = true;
            break;
        }
    }
    
    // Current Status
    if(isObjInArea == false && isWristInArea == false)
    {
        opchecktime->priv->status = PROC_STATUS::Empty;
    }
    else if(isObjInArea == true && isWristInArea == false)
    {
        opchecktime->priv->status = PROC_STATUS::Object_Only;
    }
    else if(isObjInArea == false && isWristInArea == true)
    {
        opchecktime->priv->status = PROC_STATUS::Wrist_Only;
    }
    else
    {
        opchecktime->priv->status = PROC_STATUS::Both;
    }
    
    // Status Checking
    if(opchecktime->priv->last_status == opchecktime->priv->status)
    {
        opchecktime->idlingTime = opchecktime->runningTime - opchecktime->idleStartTime;
    }
    else
    {
        // status changed, check the time excced
        if(opchecktime->idlingTime > opchecktime->priv->statusSec)
        {
            opchecktime->statusIdleCounter++;
            
            // set alert
            opchecktime->priv->alert = true;
            if(frame_exist)
            {
                // alert message format:",type<time>", must used append.
                std::string alertMessage = "," + std::string(opchecktime->priv->alertType) + "<" + return_current_time_and_date() + ">";
                
                // write alert message to meta by creating new object<use alert area>
                adlink::ai::DetectionBoxResult target_area;
                target_area.meta += alertMessage; 
                meta->batch.frames[0].detection_results.push_back(target_area);
            }
        }
        
        // status changed, reset the idle start time
        opchecktime->idlingTime = 0;
        opchecktime->idleStartTime = opchecktime->runningTime;
    }
    
    // Update Status
    opchecktime->priv->last_status = opchecktime->priv->status;
    
}

static void drawAlertArea(GstOpchecktime *opchecktime)
{
    if(opchecktime->priv->area_display)
    {
        int lineType = cv::LINE_8;
        int pt_num = opchecktime->priv->area_point_vec.size();
        cv::Scalar color = opchecktime->priv->alert == true ? cv::Scalar(0, 0, 255) : cv::Scalar(255, 0, 0);
        int thickness = opchecktime->priv->alert == true ? 6 : 2;
        for(int i = 0; i < pt_num; ++i)
            cv::line(opchecktime->srcMat, opchecktime->priv->area_point_vec[i%pt_num], opchecktime->priv->area_point_vec[(i+1)%pt_num], color, thickness, lineType);
    }
                        
    if(opchecktime->priv->object_display)
    {
        int width = opchecktime->srcMat.cols;
        int height = opchecktime->srcMat.rows;
        float scale = 0.03;
        int font = cv::FONT_HERSHEY_COMPLEX;
        double font_scale = std::min(width, height)/(25/scale);
        int thickness = 2; 
        
        int startX = width / 3;
        int startY = height / 8;
        int heightShift = cv::getTextSize("Text", font, font_scale, thickness, 0).height * 1.5;
        
        // paint idling timer
        cv::putText(opchecktime->srcMat, "accumulating time = " + round2String(opchecktime->idlingTime, 3) +" s", cv::Point(startX, startY), font, font_scale, cv::Scalar(0, 139, 69), thickness, 8, 0);
        
        startY += heightShift;
        
        // paint idle time 
        cv::putText(opchecktime->srcMat, "NG Status count = " + round2String(opchecktime->statusIdleCounter, 0), cv::Point(startX, startY), font, font_scale, cv::Scalar(0, 0, 255), thickness, 8, 0);
    }
}
