Getting Started:
----------------

```python
>>> from libardrone import ardrone
>>> drone = ardrone.ARDrone()
>>> # You might need to call drone.reset() before taking off if the drone is in
>>> # emergency mode
>>> drone.takeoff()
>>> drone.land()
>>> drone.halt()
```

Using the drone's function `get_image()` you can get the latest image from the camera.
At present this is in the format of a numpy array with dimensions (width, height, 3) that can be used e.g. in opencv:


```python
>>> import cv2
>>> cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
>>> while True:
>>>      # get image data as numpy array
>>>      img = drone.get_image()
>>>      # show image using opencv
>>>      cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
>>>      if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to quit
>>>          break
```

The drone's property `navdata` contains always the latest navdata.
You can for example get the current battery charge from that:

```python
>>> bat = drone.navdata.get(0, dict()).get('battery', 0)
>>> print('Battery: %i%%' % bat)
```

Demo (pygame):
--------------

There is also a demo application included which shows the video from the drone
and lets you remote-control the drone with the keyboard (you need pygame for it to work):

    RETURN      - takeoff
    SPACE       - land
    BACKSPACE   - reset (from emergency - DO NOT USE IN FLIGHT)
    w           - forward
    a           - left
    s           - back
    d           - right
    LEFT/q      - turn left
    RIGHT/e     - turn right
    1,2,...,0   - speed
    UP/DOWN     - altitude
    r           - switch to front facing camera
    f           - switch to downward facing camera

Here is a [video] of the library in action:

  [video]: http://youtu.be/2HEV37GbUow

Repository:
-----------

The public repository is located here for the AR.Drone 1.0:

  git://github.com/venthur/python-ardrone.git

At present the AR.Drone 2.0 has a separate fork here:

  git://github.com/adetaylor/python-ardrone.git

Requirements:
-------------

This software was tested with the following setup:

  * Python 2.7.13
  * Unmodified AR.Drone firmware 2.0


License:
--------

This software is published under the terms of the MIT License:

  http://www.opensource.org/licenses/mit-license.php
