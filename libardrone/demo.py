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


"""Demo app for the AR.Drone.

This simple application allows to control the drone and see the drone's video
stream.
"""


import pygame
import pygame.surfarray

import pygame.transform
import time
import libardrone
import libfakeardrone
from threading import Thread

FAKE = 1

def main():
    pygame.init()
    W, H = 640, 480
    screen = pygame.display.set_mode((W, H))
    if FAKE:
        drone = libfakeardrone.ARDrone(True)
    else:
        drone = libardrone.ARDrone(True)
    drone.reset()
    clock = pygame.time.Clock()
    time.sleep(2.0)
    drone.trim()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                drone.hover()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.reset()
                    running = False
                # takeoff / land
                elif event.key == pygame.K_RETURN:
                    print "return"
                    drone.takeoff()
                elif event.key == pygame.K_SPACE:
                    print "space"
                    drone.land()
                # emergency
                elif event.key == pygame.K_BACKSPACE:
                    drone.reset()
                # forward / backward
                elif event.key == pygame.K_w:
                    drone.move_forward()
                elif event.key == pygame.K_s:
                    drone.move_backward()
                # left / right
                elif event.key == pygame.K_a:
                    drone.move_left()
                elif event.key == pygame.K_d:
                    drone.move_right()
                # up / down
                elif event.key == pygame.K_UP:
                    drone.move_up()
                elif event.key == pygame.K_DOWN:
                    drone.move_down()
                # turn left / turn right
                elif event.key == pygame.K_LEFT:
                    drone.turn_left()
                elif event.key == pygame.K_RIGHT:
                    drone.turn_right()
                # speed
                elif event.key == pygame.K_1:
                    drone.speed = 0.1
                elif event.key == pygame.K_2:
                    drone.speed = 0.2
                elif event.key == pygame.K_3:
                    drone.speed = 0.3
                elif event.key == pygame.K_4:
                    drone.speed = 0.4
                elif event.key == pygame.K_5:
                    drone.speed = 0.5
                elif event.key == pygame.K_6:
                    drone.speed = 0.6
                elif event.key == pygame.K_7:
                    drone.speed = 0.7
                elif event.key == pygame.K_8:
                    drone.speed = 0.8
                elif event.key == pygame.K_9:
                    drone.speed = 0.9
                elif event.key == pygame.K_0:
                    drone.speed = 1.0
                elif event.key == pygame.K_x:
                    t = Thread(target=fly_around_school, args=(drone, ))
                    t.daemon = True
                    t.start()

        try:
            # print pygame.image
            pixelarray = drone.get_image()
            if pixelarray != None:
                surface = pygame.surfarray.make_surface(pixelarray)
                rotsurface = pygame.transform.rotate(surface, 270)
                screen.blit(rotsurface, (0, 0))
            # battery status
            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."

def fly_around_school(drone):
    print "Taking off"
    drone.trim()
    drone.takeoff()
    time.sleep(2.0)

    print "Setting speed to 0.1"
    drone.speed = 0.1
    time.sleep(5.0)

    for x in range(0,10):
        print "Moving forwards..."
        drone.move_forward()
        time.sleep(0.3)

    current_rotation = get_rotation(drone)
    desired_rotation = (current_rotation + 180) % 360
    print "Current rotation is " + str(current_rotation)
    print "We want to turn to " + str(desired_rotation)

    for x in range(0,30):
        print "Flying a bit higher"
        drone.move_up()
        time.sleep(0.1)

    time.sleep(1.0)
    print "Continuing to turn until rotation is as desired"
    current_rotation = get_rotation(drone)
    while (current_rotation > (desired_rotation+5) or current_rotation < (desired_rotation - 5)):
        print "Current rotation is "+str(current_rotation)+", turning further..."
        drone.turn_left()
        current_rotation = get_rotation(drone)
        time.sleep(0.1)

    print "Stopping turn..."
    time.sleep(1.0)

    for x in range(0,10):
        print "Moving forwards..."
        drone.move_forward()
        time.sleep(0.3)

    print "Landing"
    drone.land()
    print "Landed."

def get_rotation(drone):
    return (drone.navdata.get(0, dict()).get('psi', 0)) % 360

if __name__ == '__main__':
    main()
