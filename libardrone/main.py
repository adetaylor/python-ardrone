#!/usr/bin/env python

import libardrone
import cv2
import numpy as np
import time

def main():
    last_bat = -1

    drone = libardrone.ARDrone(True)
    drone.reset()

    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.startWindowThread()

    while True:
        bat = drone.navdata.get(0, dict()).get('battery', 0)
        if bat != last_bat:
            print('Battery: %i%%' % bat)
            last_bat = bat

        # look down
        drone.set_camera_view(False)
        img = drone.get_image()

        if not img.any():
            time.sleep(0.1)
            continue

        # the camera output is RGB, switch to bgr for 
        r,g,b = cv2.split(img)
        img = cv2.merge((b,g,r))

        #    screen.blit(rotsurface, (0, 0))
        # battery status
        cv2.imshow('image',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
