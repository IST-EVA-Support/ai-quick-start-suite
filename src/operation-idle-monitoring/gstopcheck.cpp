#ifdef HAVE_CONFIG_H
#include "config.h"
#else

#ifndef VERSION
#define VERSION "1.1.0"
#endif
#ifndef PACKAGE
#define PACKAGE "An ADLINK OP Check plugin"
#endif
#ifndef PACKAGE_NAME
#define PACKAGE_NAME "libopcheck.so"
#endif
#ifndef GST_PACKAGE_ORIGIN
#define GST_PACKAGE_ORIGIN "https://www.adlinktech.com/"
#endif

#endif

#include "gstopchecktime.h"

GST_DEBUG_CATEGORY_STATIC (opcheck_debug);
#define GST_CAT_DEFAULT opcheck_debug
/*** GStreamer Plugin Registration ***/
// register the element to the plugin
static gboolean plugin_init (GstPlugin * plugin)
{
    GST_DEBUG_CATEGORY_INIT (opcheck_debug, "[opcheck debug]", 0, "opcheck plugins");
    if (!gst_element_register (plugin, "opchecktime", GST_RANK_NONE, GST_TYPE_OPCHECKTIME))
        return FALSE;
    return TRUE;
}
//define the plugin information
GST_PLUGIN_DEFINE (GST_VERSION_MAJOR,
    GST_VERSION_MINOR,
    opcheck,
    PACKAGE,
    plugin_init, VERSION, "LGPL", PACKAGE_NAME, GST_PACKAGE_ORIGIN)
