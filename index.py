from framegrabber import FrameGrabber
import cv2
import numpy as np
import time as t
import keys as k

keys = k.Keys()

team_red = np.array([100,0,0]), np.array([150,255,255])

#rocket_red = np.array([0,0,0]), np.array([255,255,255])
rocket_blue = np.array([130,30,150]), np.array([180,200,255])

is_red = False

base_difference_weight = 5.5
difference_weight = base_difference_weight

previous_ms = 0
previous_ms_diff = 0
previous_mean = 0
threshold = 0.255

def team_color(color):
    hsv = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, *team_red)

    # matches = np.argwhere(mask == 255)
    mean = np.mean(mask)

    return mean > 49

def get_rocket_pos(screen):
    global difference_weight
    global previous_mean
    global previous_ms
    global previous_ms_diff
    global threshold

    mask = None

    if is_red:
        hsv = cv2.cvtColor(screen, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, *rocket_blue)
    else:
        hsv = cv2.cvtColor(screen, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, *rocket_red)

    # matches = np.argwhere(mask == 255)

    # mean_x = np.mean(matches[:1,])
    # mean_y = np.mean(matches[:,1])
    # target = screen.shape[1] / 2


    def right_click():
        keys.keys_worker.sendMouse(0,0, keys.mouse_rb_press)
        keys.keys_worker.sendMouse(0,0, keys.mouse_rb_release)


    #cv2.imshow("Team Fortress 2", mask)

    mean = np.mean(mask)

    if mean > 0.12:
        right_click()


    # if mean > previous_mean:
    #     difference = mean - previous_mean
    
    #     # if mean > 2.5:
    #     #     difference_weight = base_difference_weight

    #     # if (mean / threshold + ((difference / threshold) * difference_weight)) >= 1:
    #     #     right_click()

    #     #     if t.time() - previous_ms > .5 and difference_weight <= 100:
    #     #         difference_weight *= 1.354

    #     #         previous_ms = t.time()
    # else:
    #     difference = previous_mean - mean

    previous_mean = mean

for i in range(2):
    print(i)

    t.sleep(1)

fg = FrameGrabber(0,30,1600,900, "Team Fortress 2")

for i in range(10000):
    screen = fg.grab()

    if i == 0 or i%100:
        color = screen[865:870, 0:5]
        is_red = team_color(color)
    
    get_rocket_pos(screen)

    #screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2RGB)
    # cv2.imshow("Team Fortress 2", screen)
    cv2.waitKey(1)

keys.keys_worker.sendMouse(0,0, keys.mouse_rb_release)
cv2.destroyAllWindows()