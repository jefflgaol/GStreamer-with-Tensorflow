import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import logging
import numpy as np

Gst.init(None)

from plugin.tensorflow import GstTfDetectionPluginPy
from plugin.cairo import GstDetectionOverlay

class VideoPlayer(object):
    source_file = None

    def __init__(self, **kwargs):
        if kwargs.get('src'):
            self.source_file = kwargs.get('src')
        self.__setup()

    def run(self):
        self.loop.run()

    def stop(self):
        self.loop.quit()

    def __setup(self):
        self.__setup_pipeline()

    def __setup_pipeline(self):
        self.player = Gst.ElementFactory.make('playbin', 'player')
        self.player.set_property('uri', 'file://' + self.source_file)
        self.fakesinkaudio = Gst.ElementFactory.make('fakesink', 'fakesinkaudio')
        self.player.set_property("audio-sink", self.fakesinkaudio)
        self.bin = Gst.Bin.new("my-bin")
        self.queue = Gst.ElementFactory.make('queue')
        self.bin.add(self.queue)
        pad = self.queue.get_static_pad("sink")
        ghostpad = Gst.GhostPad.new("sink", pad)
        self.bin.add_pad(ghostpad)
        self.plugin = GstTfDetectionPluginPy()
        self.plugin.do_set_property("config", os.path.join(os.getcwd(), "data/tf_object_api_cfg.yml"))
        self.bin.add(self.plugin)
        self.videoconvert1 = Gst.ElementFactory.make('videoconvert')
        self.bin.add(self.videoconvert1)
        self.plugin2 = GstDetectionOverlay()
        self.bin.add(self.plugin2)
        self.videoconvert2 = Gst.ElementFactory.make('videoconvert')
        self.bin.add(self.videoconvert2)
        self.gtksink = Gst.ElementFactory.make('gtksink')
        self.gtksink.set_property("sync", False)
        self.bin.add(self.gtksink)
        link1 = self.queue.link(self.plugin)
        if not link1:
            _log.error('Could not link1!\n{0}'.format(
                    link1))
        link2 = self.plugin.link(self.videoconvert1)
        if not link2:
            _log.error('Could not link2!\n{0}'.format(
                    link2))
        link3 = self.videoconvert1.link(self.plugin2)
        if not link3:
            _log.error('Could not link3!\n{0}'.format(
                    link3))
        link4 = self.plugin2.link(self.videoconvert2)
        if not link4:
            _log.error('Could not link4!\n{0}'.format(
                    link4))
        link5 = self.videoconvert2.link(self.gtksink)
        if not link5:
            _log.error('Could not link5!\n{0}'.format(
                    link5))
        self.player.set_property("video-sink", self.bin)
        GObject.threads_init()
        self.loop = GObject.MainLoop()
        self.player.set_state(Gst.State.PLAYING)
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_message)
   
    def __on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            exit()
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print('Error: %s' %err, debug)
            exit()

def main():
    player = VideoPlayer(src=os.path.join(os.getcwd(), "video.mp4"))
    player.run()

if __name__ == '__main__':
    main()
