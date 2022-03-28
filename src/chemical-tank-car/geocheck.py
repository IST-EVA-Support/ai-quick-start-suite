import ctypes
import numpy as np
import time
from datetime import datetime

import cv2
import gst_helper
import gst_cv_helper
import gst_admeta as admeta

from gi.repository import Gst, GObject, GLib, GstVideo

def check_inside_area(img, object_boxes, obj_name, limit_num, area_points, display):
	alert = False
	
	h, w, c = img.shape
	face = cv2.FONT_HERSHEY_COMPLEX
	scale = 0.75
	thickness = 2
	exist_num = 0
	obj_list=obj_name.split(',')
	
	stencil = np.zeros(img.shape).astype(img.dtype)
	contours = [np.array(area_points)]
	color = [255, 255, 255]
	cv2.fillPoly(stencil, contours, color)
	area_img = cv2.bitwise_and(img, stencil)
	
	for box in object_boxes:
		l =  box.obj_label.decode("utf-8").strip() if box.obj_label.decode("utf-8").strip() != '' else str(box.class_id)
		for objName in obj_list:
			if l == objName:
				x1, x2, y1, y2 = int(box.x1*w), int(box.x2*w), int(box.y1*h), int(box.y2*h)
				object_points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
				
				stencil = np.zeros(img.shape).astype(img.dtype)
				contours = [np.array(object_points)]
				color = [255, 255, 255]
				cv2.fillPoly(stencil, contours, color)
				obj_img = cv2.bitwise_and(img, stencil)
				
				intersectNum = np.sum(np.logical_and(area_img, obj_img))

				if intersectNum > 0:
					exist_num = exist_num + 1
				if display == True:
					size = cv2.getTextSize(l, face, scale, thickness+1)
					cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), thickness)
					cv2.rectangle(img, (x1, y1), (x1+size[0][0], y1+size[0][1]+size[1]), (255, 255, 255), -1)
					cv2.putText(img, l, (x1, y1 + size[0][1]), face, scale, (0, 0, 255), thickness+1)
	if limit_num >= 0:
		if exist_num != limit_num:
			alert = True
	#else:
		#if exist_num == (limit_num * -1):
			#alert = True
	return alert

def gst_video_caps_make(fmt):
	return  "video/x-raw, "\
		"format = (string) " + fmt + " , "\
		"width = " + GstVideo.VIDEO_SIZE_RANGE + ", "\
		"height = " + GstVideo.VIDEO_SIZE_RANGE + ", "\
		"framerate = " + GstVideo.VIDEO_FPS_RANGE


class GeoCheck(Gst.Element):

		GST_PLUGIN_NAME = 'geocheck'	
		__gstmetadata__ = ("geocheck",
                           "Adlink geocheck video filter",
                           "Simple detected object check in area.",
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
            
			"alert-area-def": (str, 
                               "alert-area-def",
                               "The definition file location of the alert area respect the frame based on the specific resolution.",
                               "", 
                               GObject.ParamFlags.READWRITE),
            "alert-type": (str, 
                           "alert-type",
                           "The alert type name when event occurred.",
                           "alert",
                           GObject.ParamFlags.READWRITE),
            "object-name": (str, 
                           "object-name",
                           "The object name that can not appear in the area.",
                           "",
                           GObject.ParamFlags.READWRITE),
            "limit-num": (int, 
                           "limit-num",
                           "The object number that can or cannot appear in the area. The limit-num = 0 means cannot exist the object; limit-num > 0 means can exist specific number of the object.",
                           0, 1000, 0,
                           GObject.ParamFlags.READWRITE),
            "display": (bool,
                        "display",
                        "Display the defined area in frame",
                        True,
                        GObject.ParamFlags.READWRITE),
		}

		def __init__(self):

			self.alert_area_def_path = ""
			self.alert_type = "alert"
			self.object_name = ""
			self.limit_num = 0
			self.display = True
			self.area_points = []
			self.parsed = False

			super(GeoCheck, self).__init__()

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
			if prop.name == 'alert-area-def':
				return self.alert_area_def_path
			elif prop.name == 'alert-type':
				return self.alert_type
			elif prop.name == 'object-name':
				return self.object_name
			elif prop.name == 'limit-num':
				return self.limit_num
			elif prop.name == 'display':
				return self.display
			else:
				raise AttributeError('unknown property %s' % prop.name)


		def do_set_property(self, prop: GObject.GParamSpec, value):
			if prop.name == 'alert-area-def':
				self.alert_area_def_path = str(value)	
				#print('start loading area definition file:', self.alert_area_def_path, '...')
				# Reset list and parse flag
				self.area_points.clear()
				self.parsed = False
				f = open(self.alert_area_def_path)
				for line in f:
					mystr = line.strip()
					x, y = mystr.split(',')
					self.area_points.append([float(x), float(y)])
				#print(self.area_points)
				f.close()
					
			elif prop.name == 'alert-type':
				self.alert_type = str(value)
			elif prop.name == 'object-name':
				self.object_name = str(value)
			elif prop.name == 'limit-num':
				self.limit_num = int(value)
			elif prop.name == 'display':
				self.display = bool(value)
			else :
				raise AttributeError('unknown property %s' % prop.name)


		def chainfunc(self, pad: Gst.Pad, parent, buff: Gst.Buffer) -> Gst.FlowReturn:

			frame_idx =0
			boxes = admeta.get_detection_box(buff, 0)

			img = gst_cv_helper.pad_and_buffer_to_numpy(pad, buff, ro=False)
			height, width, ch = img.shape
			object_boxes = []
			with boxes as det_box :
				if det_box is not None :
					for box in det_box:
						# Check if this is pose result or not
						if box.meta == b'pose' :
							continue
						else :
							object_boxes.append(box)

			# inspect area parsing
			point_n = len(self.area_points)
			if self.parsed == False:
				for i in range(point_n):
					self.area_points[i][0] = int(self.area_points[i][0]*width)
					self.area_points[i][1] = int(self.area_points[i][1]*height)
				#print(self.area_points)
				self.parsed = True
            
            # Check if object is in the area  
			alert = check_inside_area(img, object_boxes, self.object_name, self.limit_num, self.area_points, self.display)
			
			if self.display == True:
				for i in range(point_n):
					x1, y1 = self.area_points[i%point_n]
					x2, y2 = self.area_points[(i+1)%point_n]
					if alert == True:
						cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 5)
					else:
						cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 3)
			
			if alert == True:
				# write alert metadata into admetadata by making a fake box
				currentTimeString = "<" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">"
				messsageStr = "," + self.alert_type + currentTimeString
				arr = []
				arr.append(admeta._DetectionBox(0, 0, 0, 0,0.1,0.2,0.3,0.4,0.5, messsageStr))
				admeta.set_detection_box(buff, pad, arr)

			else:
				messsageStr ="none"
				arr = []
				arr.append(admeta._DetectionBox(0, 0, 0, 0,0.1,0.2,0.3,0.4,0.5, messsageStr))
				admeta.set_detection_box(buff, pad, arr)
			
			return self.srcpad.push(buff)

		def chainlistfunc(self, pad: Gst.Pad, parent, list: Gst.BufferList) -> Gst.FlowReturn:
			return self.srcpad.push(list.get(0))

		def eventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
			return self.srcpad.push_event(event)

		def srcqueryfunc(self, pad: Gst.Pad, parent, query: Gst.Query) -> bool:
			return self.sinkpad.query(query)

		def srceventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
			return self.sinkpad.push_event(event)	
        
		def do_state_changed(self, oldstate: Gst.State, newstate: Gst.State, pending: Gst.State):
			if newstate == Gst.State.PLAYING:
				# Reset list and parse flag
				self.area_points.clear()
				self.parsed = False
				f = open(self.alert_area_def_path)
				for line in f:
					mystr = line.strip()
					x, y = mystr.split(',')
					self.area_points.append([float(x), float(y)])
				#print(self.area_points)
				f.close()

# Register plugin to use it from command line
GObject.type_register(GeoCheck)
__gstelementfactory__ = (GeoCheck.GST_PLUGIN_NAME, Gst.Rank.NONE, GeoCheck)

