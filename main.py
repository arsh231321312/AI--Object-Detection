from ultralytics import YOLO
import cv2 as cv
import numpy as np
import os
from time import time, sleep
import multiprocessing
import threading
from windowcapture import WindowCapture
import mss
from imageai.Detection import VideoObjectDetection
import signal
import pyautogui
import random
from PIL import Image
from ctypes import windll
import numpy as np
from pyHM import mouse
# FIXES SLOW TIME.SLEEP IN WINDOWS OS
timeBeginPeriod = windll.winmm.timeBeginPeriod #new
timeBeginPeriod(1) #new

sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            move_mouse(current_x:=move_x,current_y:=move_y)
    return current_x,current_y


# import matplotlib.pyplot as plt
#
# fig = plt.figure(figsize=[13,13])
# plt.axis('off')
# for y in np.linspace(-200,200,1):
#     points = []
#     wind_mouse(0,y,500,y,move_mouse=lambda x,y: points.append([x,y]))
#     print("first:", points)
#     points = np.asarray(points)
#     print(points)
#     plt.plot(*points.T)
#     print(points.T)
#     points.T
# plt.xlim(-50,550)
# plt.ylim(-250,250)
# plt.show()

def mouse_movement(x=100,y=100, duration=0.3):
    points = []
    cur_x,cur_y = pyautogui.position()
    g = random.randrange(5,9)
    w = random.randrange(2,5)
    m = random.randrange(8,17)
    d = random.randrange(7,14)
    wind_mouse(cur_x,cur_y,x,y,g,w,m,d,move_mouse=lambda x,y: points.append([x,y]))
    #print(points)
    for i in points:
        size = len(points)
        d = duration / size
        x = i[0]
        y = i[1]
        #print(i)
        #print("x:", i[0])
        #print("y:", i[1])
        mouse_movement(x, y)
        time.sleep(d)
flag,flagzomb,flagwhite,flagattack,flagbig,flageat,flagprayer=False,False,False,False,False,False,False
lock,lock2,lock3,lock4,lock5,lock6,lock7,lock8,lock9,lock10,lock11 = threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock()
vorkposx,vorkposy,width,height=0,0,0,0
trueposx,trueposy,truewidth,trueheight=0,0,0,0
sharkx,sharky,sharkwidth,sharkheight=0,0,0,0
prayerx,prayery,prayerwidth,prayerheight=0,0,0,0
goodx,goody,goodwidth,goodheight,count=0,0,0,0,0
bestx,besty,bestwidth,bestheight=0,0,0,0
prayerexist=True
sharkexist=True
flagblobs=False
stop_flag = False
stop_woox=False
wooxstart=False
testing=False

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#pyautogui.moveTo replaced by mouse.move
#pyautogui.click() replaced by mouse.click()
#replace pyautogui.moveTo with mouse_movement
# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - ChickNCurry') #RuneLite - ChickNCurry #(270) Range Vorkath Made Easy OSRS - YouTube - Google Chrome
model = YOLO("C:/ALL_YOLOv8_Folders/runs/detect/train68/weights/best.pt")



#yolo task=detect mode=train model=yolov8s.pt data=attacksnew2/data.yaml epochs=400 imgsz=992,653 device=0 batch=10
#yolo task=detect mode=train model=runs/detect/train68/weights/best.pt data=attacksnew2/data.yaml epochs=500 imgsz=992,653 device=0 batch=10

def showing():
    loop_time = time()
    global flag,flagzomb,flagwhite,vorkposx,vorkposy,width,height,trueposx,trueposy,truewidth,testing,trueheight,flagbig,flageat,flagprayer,sharkx,sharky,sharkwidth,sharkheight,sharkexist,prayerx,prayery,prayerwidth,prayerheight,prayerexist,flagblobs,stop_flag,goodx,goody,goodwidth,goodheight,bestx,besty,bestwidth,bestheight
    while(True):
        
        screenshot = wincap.get_screenshot()
        results=model.predict(source=screenshot, show=True,conf=.4,device=0,save_txt=False,stream=True,show_labels=False)
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()
        
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes: 
                if ((result.names[int(box.cls[0])] == 'vork')):
                    vorkath = box.xywh[0].astype(int)
                    vorkposx,vorkposy,width,height= vorkath
                elif((result.names[int(box.cls[0])] == 'blob') and (flagblobs==False)):
                    flagblobs=True
                    
                    t7=threading.Thread(target=woox)
                    t7.start()
                elif((result.names[int(box.cls[0])] == 'shark')):
                    shark= box.xywh[0].astype(int)
                    sharkx,sharky,sharkwidth,sharkheight= shark
                elif((result.names[int(box.cls[0])] == 'prayer_pot')):
                    prayer= box.xywh[0].astype(int)
                    prayerx,prayery,prayerwidth,prayerheight= prayer
                    prayerexist=False
                    
                elif ((result.names[int(box.cls[0])] == 'true')):
                    true=box.xywh[0].astype(int)
                    trueposx,trueposy,truewidth,trueheight=true
                elif ((result.names[int(box.cls[0])] == 'off') and (flag==False)): #checks if box is class 's'
                    
                    flag=True
                    t = threading.Thread(target=methods)
                    t.start()
                elif ((result.names[int(box.cls[0])] == 'zombie_ground') and (flagzomb==False)):
                    r = box.xywh[0].astype(int)
                    flagzomb=True
                    t2 = threading.Thread(target=zombattack, args=(r,))
                    t2.start()
                elif ((result.names[int(box.cls[0])] == 'w') and (flagwhite==False)):
                    flagwhite=True
                    stop_flag=True
                    t3 = threading.Thread(target=white)
                    t3.start()
                elif ((result.names[int(box.cls[0])] == 'big') and (flagbig==False)):
                    flagbig=True
                    t4 = threading.Thread(target=big)
                    t4.start()
                elif ((result.names[int(box.cls[0])] == 'lowh') and (flagprayer==False) and (flageat==False) and (flagbig==False) and (flagzomb==False) and (flagblobs==False)): #woox
                    flageat=True
                    t5 = threading.Thread(target=eat)
                    t5.start()
                elif ((result.names[int(box.cls[0])] == 'lowp') and (flagprayer==False) and (flageat==False) and (flagbig==False) and (flagzomb==False) and (flagblobs==False)): #woox
                    flagprayer=True
                    t6 = threading.Thread(target=prayer1)
                    t6.start()
                elif (result.names[int(box.cls[0])] == 'good'):
                    goodtile=box.xywh[0].astype(int)
                    goodx,goody,goodwidth,goodheight=goodtile
                    if(bestx>=goodx and testing==False):
                        bestx,besty,bestwidth,bestheight=goodtile
                    
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

def good():
    global goodx,goody,goodwidth,goodheight,trueposx,trueposy,truewidth,trueheight,bestx,besty,bestwidth,bestheight,wooxstart
    if (stop_woox==True and wooxstart==False):
        if (bestx-trueposx<15):
            wooxwalk()
    else:
        t=threading.Thread(target=good2)
        t.start()
        good()

def good2():
    global testing,bestx,besty,bestheight
    with lock10:
        mouse_movement(bestx+5,besty+bestheight*2/3,.05)
        testing=True
        pyautogui.click()
        sleep(20)
def wooxwalk():
    randomtime=random.randint(10,15)/100
    global count,wooxstart
    wooxstart=True
    global flagblobs,stop_flag,vorkposx,trueposx,trueposy,truewidth,trueheight,stop_woox,testing #might remove
    if stop_woox==True:
        
        attackvork2()
        sleep(.12+.15-randomtime)
        mouse_movement(trueposx,trueposy+3.5*trueheight-10,randomtime)
        pyautogui.click()
        count=count+1
        sleep(.06)
        wooxwalk()
    else:
        pass
def woox():
    global flagblobs,stop_flag,vorkposx,trueposx,trueposy,truewidth,trueheight,stop_woox,testing
    randomtime=random.randint(7,10)/100
    with lock8:
        stop_flag=True
        stop_woox=True
        mouse_movement(trueposx+2*truewidth,trueposy+2*trueheight-10,randomtime)
        pyautogui.click()
        sleep(.5)
        t1=threading.Thread(target=good)
        t1.start()
        sleep(16)
        flagblobs=False
        stop_flag=False
        stop_woox=False
        testing=False
        sleep(10)
def eat():

    global sharkx,sharky,sharkwidth,sharkheight,flageat,stop_flag
    randomheight=random.randint(20,28)
    randomwidth=random.randint(-5,5)
    randomtime=random.randint(10,15)/100
    with lock6:
        if stop_flag==False:
            mouse_movement(sharkx+randomwidth,sharky+randomheight,randomtime)
            pyautogui.click()
            attackvork()
            flageat=False
            sleep(2)
        else:
            pass
        
def prayer1():
    
    global prayerx,prayery,prayerwidth,prayerheight,flagprayer,stop_flag
    
    randomwidth=random.randint(-5,5)
    randomheight=random.randint(20,28)
    randomtime=random.randint(10,15)/100
    with lock7:
        if stop_flag==False:
            mouse_movement(prayerx+randomwidth,prayery+randomheight,randomtime)
            pyautogui.click()
            attackvork()
            flagprayer=False
            sleep(2)
        else:
            pass
    

def big():
    global vorkposx,trueposx,trueposy,truewidth,trueheight,flagbig,stop_flag
    randomheight=random.randint(70,80)/10
    randomtime=random.randint(10,15)/100
    stop_flag=True
    with lock5:
        if((vorkposx-trueposx)<=0):
            #mouse_movement(trueposx-2*truewidth,trueposy+trueheight/randomheight,randomtime)
            mouse_movement(trueposx-2*truewidth,trueposy+20,randomtime)
            pyautogui.click()
            sleep(1.2)
            attackvorkl()
        else:
            #mouse_movement(trueposx+2*truewidth,trueposy+trueheight/randomheight,randomtime)
            mouse_movement(trueposx+2*truewidth,trueposy+20,randomtime)
            pyautogui.click()
            sleep(1.2)
            attackvorkr()
        sleep(.3)
        stop_flag=False
        flagbig=False
def attackvork2():
    
    global vorkposy
    global vorkposx,stop_flag
    with lock4:
            speed = random.randint(30, 35)/100
            mouse_movement(vorkposx+15,vorkposy+15,speed)
            pyautogui.click()
            sleep(.35-speed)
   
def attackvork():
    
    global vorkposy
    global vorkposx,stop_flag
    with lock4:
        if not stop_flag:
            speed = random.randint(20, 40)/100
            mouse_movement(vorkposx+15,vorkposy+15,speed)
            pyautogui.click()
        else:
            pass
def attackvorkl():
    
    global vorkposy
    global vorkposx,stop_flag
    with lock4:
        speed = random.randint(20, 40)/100
        mouse_movement(vorkposx+55,vorkposy+15,speed)
        pyautogui.click()
        
def attackvorkr():
    
    global vorkposy
    global vorkposx,stop_flag
    with lock4:
        speed = random.randint(20, 40)/100
        mouse_movement(vorkposx-35,vorkposy+15,speed)
        pyautogui.click()
        

def methods():
    random.seed(threading.get_ident())
    time = random.uniform(0.18, 0.23)
    delay=random.uniform(0.10, 0.20)
    x= random.randint(1461, 1477)
    y= random.randint(112, 126)
    global flag
    with lock:
        sleep(delay)
        mouse_movement(x, y,time)
        sleep(delay)
        pyautogui.click()
        sleep(1)
        flag=False
        sleep(1)
        
    
def zombattack(r):
    x,y,w,h=r 
    global flagzomb,stop_flag
    time=random.uniform(0.05, 0.08)
    with lock2:
        mouse_movement(x+w/2, y+h/2+5,time)
        pyautogui.click()
        sleep(.1)
        attackvork()
        sleep(2)
        stop_flag=False
        flagzomb=False
        sleep(5)
        
def white():
    global flagwhite,stop_flag
    random_posx = random.randint(590, 1050)
    random_posy = random.randint(390, 540)
    delay=random.uniform(0.1, 0.25)
    x=random.randint(1535, 1542)
    y=random.randint(804, 816)
    delay2= random.uniform(0.2, 0.27)
    delay3= random.uniform(0.3, 0.5)
    with lock3:
        pyautogui.press('f3')
        sleep(delay)
        mouse_movement(random_posx, random_posy,delay3)
        pyautogui.click()
        sleep(delay)
        mouse_movement(x, y,delay2)
        pyautogui.click()
        sleep(delay)
        pyautogui.press('f1')
        stop_flag=False
        sleep(5)
        flagwhite=False
        sleep(5)
        
        
"""""
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:                                          # iterate boxes
                r = box.xywh[0].astype(int)      
                x,y,w,h=r               #inputs values of the box into those variables
                print('xva',x,'yva',y,'width',w,'height',h)
                print(result.names[int(box.cls[0])] )  #https://docs.ultralytics.com/modes/predict/#streaming-source-for-loop
                #if result.names[int(box.cls[0])] == 's': #checks if box is class 's'
"""""

if __name__ == '__main__':
    # Create a new process
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    p = multiprocessing.Process(target=showing)
    
    # Start the process
    p.start()
    
    # Wait for the process to finish

    p.join()