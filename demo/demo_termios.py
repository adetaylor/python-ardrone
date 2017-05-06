'''
For testing purpose only
'''
import termios
import fcntl
import os

def main():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    drone = ARDrone(is_ar_drone_2=True)

    import cv2
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
