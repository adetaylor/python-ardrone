#!/usr/bin/env python

# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""
For testing purpose only
"""
import termios
import fcntl
import os
import cv2

def main():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    drone = ARDrone(is_ar_drone_2=True)

    try:
        startvideo = True
        video_waiting = False
        while 1:
            time.sleep(.0001)
            if startvideo:
                try:
                    cv2.imshow("Drone camera", cv2.cvtColor(drone.get_image(), cv2.COLOR_BGR2RGB))
                    cv2.waitKey(1)
                except:
                    if not video_waiting:
                        print("Video will display when ready")
                    video_waiting = True
                    pass

            try:
                c = sys.stdin.read(1)
                c = c.lower()
                print("Got character", c)
                if c == 'a':
                    drone.move_left()
                if c == 'd':
                    drone.move_right()
                if c == 'w':
                    drone.move_forward()
                if c == 's':
                    drone.move_backward()
                if c == ' ':
                    drone.land()
                if c == '\n':
                    drone.takeoff()
                if c == 'q':
                    drone.turn_left()
                if c == 'e':
                    drone.turn_right()
                if c == '1':
                    drone.move_up()
                if c == '2':
                    drone.hover()
                if c == '3':
                    drone.move_down()
                if c == 't':
                    drone.reset()
                if c == 'x':
                    drone.hover()
                if c == 'y':
                    drone.trim()
                if c == 'i':
                    startvideo = True
                    try:
                        navdata = drone.get_navdata()

                        print('Emergency landing =', navdata['drone_state']['emergency_mask'])
                        print('User emergency landing = ', navdata['drone_state']['user_el'])
                        print('Navdata type= ', navdata['drone_state']['navdata_demo_mask'])
                        print('Altitude= ', navdata[0]['altitude'])
                        print('video enable= ', navdata['drone_state']['video_mask'])
                        print('vision enable= ', navdata['drone_state']['vision_mask'])
                        print('command_mask= ', navdata['drone_state']['command_mask'])
                    except:
                        pass

                if c == 'j':
                    print("Asking for configuration...")
                    drone.at(at_ctrl, 5)
                    time.sleep(0.5)
                    drone.at(at_ctrl, 4)
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        drone.halt()

if __name__ == "__main__":
    main()
