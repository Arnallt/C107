import cv2
import time
import math

p1 = 530
p2 = 300
xs = []
ys = []

video = cv2.VideoCapture("bb3.mp4")

tracker = cv2.TrackerCSRT_create()
returned, image = video.read()
bBox = cv2.selectROI("tracking", image, False)
tracker.init(image,bBox)

def drawBox(image,bBox):
    x,y,w,h = int(bBox[0]), int(bBox[1]), int(bBox[2]), int(bBox[3])
    cv2.rectangle(image,(x,y),(x+w,y+h), (0,255,0), 3,1 )
    cv2.putText(image,"Tracking", (75,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0), 2)

def goal_track(image,bBox):
    x,y,w,h = int(bBox[0]), int(bBox[1]), int(bBox[2]), int(bBox[3])
    c1 = x+int(w/2)
    c2 = y+int(h/2)
    cv2.circle(image,(c1,c2), 2,(0,0,255),5)
    
    cv2.circle(image, (int(p1), int(p2)), 3,(25,25,0),3)
    dist = math.sqrt(((c1-p1)**2) + (c2-p2)**2)

    if dist <= 20:
        cv2.putText(image,"Goal", (300,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs)-1):
        cv2.circle(image,(xs[i], ys[i]), 2, (0,0,255), 5)


while True:
    check,image = video.read()   
    success, bBox = tracker.update(image)

    if(success):
        drawBox(image,bBox)
    else:
        cv2.putText(image,"Lost", (75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
    
    goal_track(image,bBox)

    cv2.imshow("result",image)

    key = cv2.waitKey(25)

    if key == 32:
        print("Stopped!")
        break


video.release()
cv2.destroyALLwindows()



