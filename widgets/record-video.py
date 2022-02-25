import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject


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
    
    # Define the record pipeline here
    commands = {
        "v4l2":"v4l2src ! videoconvert ! videoscale ! video/x-raw,width=" + str(width) + ",height=" + str(height) + " ! tee name=t ! queue ! x264enc tune=zerolatency ! mp4mux ! filesink location=video.mp4 t. ! queue ! textoverlay text=Recording valignment=top halignment=left font-desc=\"Sans, 20\" ! videoconvert ! ximagesink",
        "pylon":"pylonsrc pixel-format=BayerRG8 width=" + str(width) + " height=" + str(height) + " fps=7 ! tee name=t ! queue ! autovideosink t. ! x264enc ! mp4mux ! filesink location=video.mp4",
        "test":"videotestsrc pattern=18 ! autovideosink"
        }
    
    # Initialize GStreamer
    Gst.init(sys.argv)
    
    pipeline_command = ""
    if sys.argv[1] in commands:
        pipeline_command = commands[sys.argv[1]]
    else:
        pipeline_command = commands["error"]
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
    
