"""
		This is a sample python plugin with ADLINK
		In this sample, we will guide you by comment on the section with !!!ADLINK!!!
		The main task of this sample is :
		- Read inference result ( Boxes ) from adlink metadata
		- Draw the box inference result in image.
"""

import ctypes
import numpy as np

import cv2
import gst_helper
import gst_cv_helper
import gst_admeta as admeta

from gi.repository import Gst, GObject, GLib, GstVideo
#!!!ADLINK!!!

def hand_up(pose):
	if pose[2][0]==0 and pose[0][0]==0 and pose[0][1]==0: #no target keypoints
		return 0
	elif (pose[2][0]>0 and pose[0][0]>0) or (pose[2][0]>0 and pose[1][0]>0): # left hand or right hand keypoint exist.
		if (pose[2][0]>0 and pose[0][0]>0) and (pose[0][1]< pose[2][1]) :# left hand exist and left hand over neck.
			return 1
		elif (pose[2][0]>0 and pose[1][0]>0) and (pose[1][1]<pose[2][1]): # right hand exist and right hand over neck.
			return 1
	return 0
	
	
def draw_boxs(img, boxs,text):

	h, w, c = img.shape
	face = cv2.FONT_HERSHEY_TRIPLEX
	scale = 1
	thickness = 1
	baseline = 0

	x1, y1 = int(boxs[2][0]*w), int(boxs[2][1]*h)
	cv2.rectangle(img, ((x1-130), (y1-180)),((x1+150), (y1-240)),(0, 255, 255), -1)
	cv2.putText(img, text, ((x1-100), (y1-200) ), face, scale, (0, 0, 255), thickness+1,cv2.LINE_AA)

def gst_video_caps_make(fmt):
	return  "video/x-raw, "\
		"format = (string) " + fmt + " , "\
		"width = " + GstVideo.VIDEO_SIZE_RANGE + ", "\
		"height = " + GstVideo.VIDEO_SIZE_RANGE + ", "\
		"framerate = " + GstVideo.VIDEO_FPS_RANGE


class handup(Gst.Element):

		# !!!ADLINK !!!!
		# Change name of your plugin here, this name will be used when you run gst-inspect
		GST_PLUGIN_NAME = 'handup'
		# !!!ADLINK !!!!
		# Change info of your plugin her, it will show when you run gst-inspect		
		__gstmetadata__ = ("handup","ADLINK hand up detection.",'Support posenet AI model.',"Jie Gao <jie.gao@adlinktech.com>")

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
		
		# MODIFIED - Gstreamer plugin properties
		# !!!ADLINK!!!
		# Here you can define your parameter which can be pass from pipeline to your plugin function.
		# I put here 1 integer parameter and 1 string parameter
		__gproperties__ = {
            "model": (int, 
                           "model",
                           "Select a pose model. 0: posenet",
                           0, 1, 0,
                           GObject.ParamFlags.READWRITE),

		}

		def __init__(self):
			# !!!ADLINK!!!
			# Init the internal value to store the num and file-name parameter
			self.num = 1
			self.pose_model=0
			self.neck = 17
			self.left_hand = 7
			self.right_hand = 8
			self.file_name = ""
			super(handup, self).__init__()

			self.sinkpad = Gst.Pad.new_from_template(self._sinkpadtemplate, 'sink')

			self.sinkpad.set_chain_function_full(self.chainfunc, None)

			self.sinkpad.set_chain_list_function_full(self.chainlistfunc, None)

			self.sinkpad.set_event_function_full(self.eventfunc, None)
			self.add_pad(self.sinkpad)

			self.srcpad = Gst.Pad.new_from_template(self._srcpadtemplate, 'src')

			self.srcpad.set_event_function_full(self.srceventfunc, None)

			self.srcpad.set_query_function_full(self.srcqueryfunc, None)
			self.add_pad(self.srcpad)

		# !!!ADLINK!!!
		# Get the prarameter ( property is the name of parameter in gstreamer api )
		def do_get_property(self, prop: GObject.GParamSpec):
			if prop.name == 'model':
				return self.pose_model
			else:
				raise AttributeError('unknown property %s' % prop.name)

		# !!!ADLINK!!!
		# Set the prarameter to the value from pipeline
		def do_set_property(self, prop: GObject.GParamSpec, value):
			if prop.name == 'model':
				self.pose_model = int(value)		
			else :
				raise AttributeError('unknown property %s' % prop.name)

		# !!!ADLINK!!!
		# Main function to get image buffer and adlink metadata 
		def chainfunc(self, pad: Gst.Pad, parent, buff: Gst.Buffer) -> Gst.FlowReturn:
			# !!!ADLINK !!!!		
			# frame id used to identify frame in a batched input, we have 1 stream so always set to 0
			frame_idx =0
			# !!!ADLINK !!!!		
			# This function will get inference result data from buffer
			boxes = admeta.get_detection_box(buff, 0)
			# !!!ADLINK !!!!
			# This function will get image buffer to a numpy array img to allow drawing to it
			img = gst_cv_helper.pad_and_buffer_to_numpy(pad, buff, ro=False)
			pose_box=[[0,0],[0,0],[0,0]] #left-hand,right-hand,neck
			self.pose_model=0

			with boxes as det_box :
				if det_box is not None :
					for box in det_box:
						# Check if this is pose result or not
						if box.meta == b'pose' :

							if int(box.obj_id) == self.left_hand : #set left hand's x y coordinate.
								pose_box[0][0]=box.x1
								pose_box[0][1]=box.y1
								continue
							elif int(box.obj_id) == self.right_hand : #set right hand's x y coordinate.
								pose_box[1][0]=box.x1
								pose_box[1][1]=box.y1
								continue
							elif int(box.obj_id)==self.neck : #set neck's x y coordinate.
								pose_box[2][0]=box.x1
								pose_box[2][1]=box.y1
								continue

							if (self.pose_model==0 and int(box.obj_id)>= 17 ):
								hand_up_index=hand_up(pose_box) # hand up
								if int(hand_up_index)>0 :
									draw_boxs(img, pose_box,'hand_up')
								else:
									draw_boxs(img, pose_box,'hand_down')
								pose_box=[[0,0],[0,0],[0,0]]	


							
			# !!!ADLINK !!!!
			# This function will draw detection box result to image buffer 

			return self.srcpad.push(buff)

		def chainlistfunc(self, pad: Gst.Pad, parent, list: Gst.BufferList) -> Gst.FlowReturn:
			return self.srcpad.push(list.get(0))

		def eventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
			return self.srcpad.push_event(event)

		def srcqueryfunc(self, pad: Gst.Pad, parent, query: Gst.Query) -> bool:
			return self.sinkpad.query(query)

		def srceventfunc(self, pad: Gst.Pad, parent, event: Gst.Event) -> bool:
			return self.sinkpad.push_event(event)	

# Register plugin to use it from command line
GObject.type_register(handup)
__gstelementfactory__ = (handup.GST_PLUGIN_NAME,
												 Gst.Rank.NONE, handup)

