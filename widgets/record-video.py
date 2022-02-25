import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
from datetime import datetime


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def on_message(bus: Gst.Bus, message: Gst.Message, loop: GObject.MainLoop, pipeline):
    mtype = message.type
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()
    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        pipeline.send_event(Gst.Event.new_eos())
        bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
        loop.quit()
    elif mtype == Gst.MessageType.ANY:
        err, debug = message.parse_warning()
        print(err, debug)

    return True


if __name__ == '__main__':
    
    width=640
    height=480
    
    if len(sys.argv) > 2:
        n, ret = intTryParse(sys.argv[2])
        if ret == False:
            print("Width is not an integer.")
            sys.exit()
        else:
            width = n
    if len(sys.argv) > 3:
        n, ret = intTryParse(sys.argv[3])
        if ret == False:
            print("Height is not an integer.")
            sys.exit()
        else:
            height = n
    
    file_name = datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + ".mp4"
    print("save to file: ", file_name)
    
    # Define the record pipeline here
    commands = {
        "v4l2":"v4l2src ! videoconvert ! videoscale ! video/x-raw,width=" + str(width) + ",height=" + str(height) + " ! tee name=t ! queue ! x264enc tune=zerolatency ! mp4mux ! filesink location=" + file_name + " t. ! queue ! textoverlay text=Recording valignment=top halignment=left font-desc=\"Sans, 20\" ! videoconvert ! ximagesink",
        "pylon":"pylonsrc width=" + str(width) + " height=" + str(height) + " ! videoconvert ! tee name=t ! queue ! x264enc tune=zerolatency ! mp4mux ! filesink location=" + file_name + " t. ! queue ! textoverlay text=Recording valignment=top halignment=left font-desc=\"Sans, 20\" ! videoconvert ! ximagesink",
        "demo":"videotestsrc pattern=18 ! autovideosink"
        }
    
    # Initialize GStreamer
    Gst.init(sys.argv)
    
    pipeline_command = ""
    if sys.argv[1] in commands:
        pipeline_command = commands[sys.argv[1]]
    else:
        print("record command does not exist.")
        sys.exit()
    print('your command:\n', pipeline_command)
    

    
    # Define gstreamer command pipeline
    #pipeline_command = "videotestsrc pattern=18 ! autovideosink"
    
    # Create pipeline via parse_launch
    pipeline = Gst.parse_launch(pipeline_command)
    
    # Allow bus to emit messages to main thread
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    
    # Start pipeline
    pipeline.set_state(Gst.State.PLAYING)
    loop = GObject.MainLoop()
    
    # Add handler to specific signal
    bus.connect("message", on_message, loop, pipeline)
    

    try:
        print("Start to run the pipeline.")
        try:
            print("recording...")
            loop.run()
        except:
            pipeline.send_event(Gst.Event.new_eos())
            bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    except Exception:
        print("in exception")
        traceback.print_exc()
        loop.quit()

    # Stop Pipeline
    pipeline.set_state(Gst.State.NULL)
    del pipeline
    print('pipeline stopped.\n')
    
