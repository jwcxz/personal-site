Homebridge is a tool that creates virtual HomeKit accessories from various
kinds of devices.  Integrating an off-the-shelf IP camera as a HomeKit camera
is one valuable use case.  Following are some notes concerning integration of a
[Panoraxy B100V.3](https://www.amazon.com/gp/product/B072C2D7RW/ref=ask_ql_qh_dp_hza)
IP camera into a Homebridge instance running on a Raspberry Pi.


<!--break-->

## Configuring the Camera

Following the prescribed setup instructions, it is probably wise to treat the
device as a black box and isolate it from the internet.  For example, one could
configure their router to prevent the device from connecting to the internet or
set up an entirely separate wireless network that consists solely of the camera
and the Homebridge host.

This product appears to have a web-based configuration and control utility
based on a platform called "CloudLive."  Entertainingly, the username `admin`
and password `admin` appears to be the default login credentials (though there
is page in the system configuration allowing one to adjust these credentials).

The platform also supports [ONVIF](https://www.onvif.org/) for control and
streaming.

The platform appears to support up to two streams.  The first stream is
configured to be 1280x720 at 15 FPS.  The second stream is configured to be
640x352 at 15 FPS, though it is not used.

The first stream can be accessed from the URL:

```
rtsp://admin:admin@IP_ADDRESS/11
```

And the second from:

```
rtsp://admin:admin@IP_ADDRESS/12
```

Furthermore, one can obtain still snapshots from the device via the URL:

```
http://admin:admin@IP_ADDRESS/cgi-bin/hi3510/snap.cgi?&-getstream&-chn=1
```


## Configuring Homebridge


To interface this device with Homebridge, I performed the following steps:

1.  As I was using a Raspberry Pi 2 Model B running Arch Linux ARM, I installed
    [ffmpeg-mmal](https://aur.archlinux.org/packages/ffmpeg-mmal) to take
    advantage of hardware encoding/decoding.

2.  In addition to installing and setting up
    [Homebridge](https://homebridge.io/), I installed the
    [homebridge-camera-ffmpeg](https://github.com/KhaosT/homebridge-camera-ffmpeg)
    plugin and added the following node to the top-level dictionary within
    `~/.homebridge/config`:

```json
"platforms": [
{
    "platform": "Camera-ffmpeg",
    "cameras": [
        {
            "name": "Camera 0",
            "videoConfig": {
                "source": "-vcodec h264_mmal -re -rtsp_transport tcp -i rtsp://admin:admin@IP_ADDRESS/11",
                "stillImageSource": "-i http://admin:admin@IP_ADDRESS/cgi-bin/hi3510/snap.cgi?&-getstream&-chn=1",
                "maxStreams": 2,
                "maxWidth": 1280,
                "maxHeight": 720,
                "vcodec": "h264_omx",
                "maxFPS": 15
            }
        }
    ]
}
]
```

3.  At this point, I was able to add the camera accessory created by the above configuration.


## Observations

* On a RPi, the ffmpeg-mmal package (along with the above configuration to use
  the accelerated H.264 decoder and encoder) allows for the transcoding process
  to occur at around 1x speed.  Use of the fallback CPU codecs results in
  extremely slow transcoding speed (around 0.07x).

  The inclusion of "-vcodec h264_mmal" in the `source` key instructs FFmpeg to
  use the accelerated decoder on the incoming stream.  The enclusion of the
  `"vcodec": "h264_omx"` entry instructs FFmpeg to use the accelerated encoder
  on the outgoing stream.

  The Arch Linux package simply compiles FFmpeg with the `--enable-omx-rpi`
  flag included.

* One can add a `"debug": true` entry to the configuration, which will show the
  FFmpeg transcoding process output whenever a client connects to the stream.

* Initially, I pointed at the second, lower-resolution stream in the hopes of
  using fewer resources.  I observed that the Home app on my phone would appear
  to connect to the camera, but would seemingly never request Homebridge to
  start the stream (culminating in an eventual timeout).

* Removing and re-adding the camera from HomeKit requires one to either change
  the name of the camera in the Homebridge configuration or to remove the
  relevant files (or all files) in `~/.homebridge/persist`.

* This particular camera has a feature that sends an email when motion is
  detected.  One could write a simple email server that looks for such emails
  and flags a Homebridge motion detector accessory.

* This camera also has the facility to upload motion-triggered captures to an
  FTP server.  I observed that it does not try to create the directory tree
  prior to uploading files, so the directory tree must either be pre-populated
  or the FTP server must support automatic directory creation.

* This camera does not persist time if it is shut off.  It can be configured to
  connect to an NTP server, but if its access to the internet is cut off, one
  would need to create a dummy NTP server and redirect the camera's NTP traffic
  to that local server.
