import ctypes
import cv2
# import gst_helper
import gst_cv_helper
import numpy as np
import time
import platform
import threading
import gst_admeta as admeta
from gi.repository import Gst, GObject, GLib, GstVideo


def GPIO_alert(status):
    DOstatus=status.split(',')
    #print("GPIO_alert(status)=", DOstatus)
    SetDO(0, int(DOstatus[0]))
    SetDO(1, int(DOstatus[1]))
    SetDO(2, int(DOstatus[2]))
    SetDO(3, int(DOstatus[3]))




def SetDO(i, val):
#list information
    loadclib = ctypes.cdll.LoadLibrary   
    lib = loadclib("/usr/lib/Neon/libNeon.so")  #Change lib here
    libc = loadclib("libc.so.6")   
    lib.Neon_SetDOState(ctypes.c_int(i), ctypes.c_int(val))

#def Set DO


def gst_video_caps_make(fmt):
    return "video/x-raw, " \
           "format = (string) " + fmt + " , " \
                                        "width = " + GstVideo.VIDEO_SIZE_RANGE + ", " \
                                                                                 "height = " + GstVideo.VIDEO_SIZE_RANGE + ", " \
                                                                                                                           "framerate = " + GstVideo.VIDEO_FPS_RANGE


class GPIOAlert(Gst.Element):
    GST_PLUGIN_NAME = 'GPIOAlert'

    __gstmetadata__ = ("GPIO Alert",
                       "GstElement",
                       "control NEON's GPIO when the alert type matched in ADLINK detection result metadata. set NEON DO0-DO4 ON/OFF. e.g. parameter DO-Status=1,1,0,0, DO0-DO1 ON, DO2-DO3 OFF",
                       "Dr. Paul Lin <paul.lin@adlinktech.com>")

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.from_string(gst_video_caps_make("{ BGR }"))),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.from_string(gst_video_caps_make("{ BGR }"))))

    _sinkpadtemplate = __gsttemplates__[1]
    _srcpadtemplate = __gsttemplates__[0]

    __gproperties__ = {
        "alert-type": (str, "Alert-type", "Alert type string name.", "", GObject.ParamFlags.READWRITE),
        "DO-status": (str, "DO-status", "set NEON DO0-DO4 ON/OFF. e.g. parameter DO-Status=1,1,0,0, DO0-DO1 ON, DO2-DO3 OFF","1,0,0,0", GObject.ParamFlags.READWRITE),
        "vote-count": (int,"vote-count","the number of vote_counts you want to skip",0, 100, 0,GObject.ParamFlags.READWRITE),}

    def __init__(self):
        # Initialize properties before Base Class initialization
        self.alertType = ""
        self.DOstatus = ""
        self.send_time = time.time()
        self.alert_duration = 1.2 # delay time
        self.count = 0
        self.DetecCount = 0
        super(GPIOAlert, self).__init__()

        self.sinkpad = Gst.Pad.new_from_template(self._sinkpadtemplate, 'sink')
        self.sinkpad.set_chain_function_full(self.chainfunc, None)
        self.sinkpad.set_chain_list_function_full(self.chainlistfunc, None)
        self.sinkpad.set_event_function_full(self.eventfunc, None)
        self.add_pad(self.sinkpad)

        self.srcpad = Gst.Pad.new_from_template(self._srcpadtemplate, 'src')
        self.srcpad.set_event_function_full(self.srceventfunc, None)
        self.srcpad.set_query_function_full(self.srcqueryfunc, None)
        self.add_pad(self.srcpad)



    def do_get_property(self, prop: GObject.GParamSpec):
        if prop.name == 'alert-type':
            return self.alertType
        elif prop.name == 'DO-status':
            return self.DOstatus
        elif prop.name == 'vote-count':
            return self.VoteCount
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_set_property(self, prop: GObject.GParamSpec, value):
        if prop.name == 'alert-type':
            self.alertType = str(value)
        elif prop.name == 'DO-status':
            self.DOstatus = str(value)
        elif prop.name == 'vote-count':
            self.VoteCount = int(value)
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def chainfunc(self, pad: Gst.Pad, parent, buff: Gst.Buffer) -> Gst.FlowReturn:
        boxes = admeta.get_detection_box(buff, 0)
        
        with boxes as det_box:
            for box in det_box:
                metaString = box.meta.decode('utf-8')
                #print("1-metastring: ",metaString,"alert type",self.alertType)
                self.count=self.count+1
                #print("---get meta data--- = ")                    
                    #if time.time() - self.send_time > self.alert_duration:# Check if out of duration
                #print("    2-metastring:  ",metaString,"time:",time.time() - self.send_time)
                if self.alertType in metaString: # Check if this is alert type
                    self.DetecCount=self.DetecCount+1
                if self.count>=self.VoteCount and self.DetecCount>=(self.VoteCount/2):
                    #print(" metastring:  ",metaString,)
                    self.count=0
                    self.DetecCount=0
                    #print (self.count)
                    #if self.count>self.vote-count:
                                 
                        
                    GPIO_thread = threading.Thread(target=GPIO_alert,args=(self.DOstatus,))
                    GPIO_thread.start()
                        
                    #else:
                     #   print("XXXLED off", " metastring:  ",metaString,)
                        #self.conut=self.count-1

        return self.srcpad.push(buff)

    def chainlistfunc(self, pad: Gst.Pad, parent, buff_list: Gst.BufferList) -> Gst.FlowReturn:
        return self.srcpad.push(buff_list.get(0))

    def eventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
        return self.srcpad.push_event(event)

    def srcqueryfunc(self, pad: Gst.Pad, parent, query: Gst.Query) -> bool:
        return self.sinkpad.query(query)

    def srceventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
        return self.sinkpad.push_event(event)


GObject.type_register(GPIOAlert)
__gstelementfactory__ = (GPIOAlert.GST_PLUGIN_NAME,
                         Gst.Rank.NONE, GPIOAlert)
