import os
import mock
from libardrone import paveparser
from libardrone import h264decoder


def test_h264_decoder():
    outfileobj = mock.Mock()
    decoder = h264decoder.H264Decoder(outfileobj)
    example_video_stream = open(os.path.join(os.path.dirname(__file__), 'paveparser.output'))
    while True:
        data = example_video_stream.read(1000)
        if len(data) == 0:
            break
        decoder.write(data)

    assert outfileobj.image_ready.called
