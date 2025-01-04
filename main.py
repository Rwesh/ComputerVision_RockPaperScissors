import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cam = cv2.VideoCapture(0)
cam.set(3,500)
cam.set(4, 400)

detector = HandDetector(maxHands= 1)

timer = 0
stateResult = False
startGame = False
scores = [0,0] #[player, ai]

while True:
    bg = cv2.imread("resources/rps.png")
    succes, img = cam.read()
    scaledImg = img[50: 450,190:505]
   
    
    #locate hand
    hands, img = detector.findHands(scaledImg)
    
    if startGame:
        
        if stateResult == False:
            timer = time.time() - gameTime
            cv2.putText(bg ,str(int(timer)), (470,348), cv2.FONT_HERSHEY_PLAIN, 4, (250,0,0), 4)
           
            
            if timer > 3:
                stateResult = True
                timer = 0
                
        
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [1,1,1,1,1]:
                        playerAction = 1
                    if fingers == [0,0,0,0,0]:
                        playerAction = 2
                    if fingers == [0,1,1,0,0]:
                        playerAction = 3
                        
                    randInt= random.randint(1,3)\
                        
                    #player win cases
                    if(playerAction == 1 and randInt == 2) or \
                        (playerAction ==2 and randInt == 3) or \
                        (playerAction == 3 and randInt ==1):
                            scores[0] +=1
                            
                    #AI win cases
                    if(playerAction == 2 and randInt == 1) or \
                        (playerAction ==3 and randInt == 2) or \
                        (playerAction == 1 and randInt ==3):
                            scores[1] +=1
                            
                    aiImg = cv2.imread(f'resources/{randInt}.png', cv2.IMREAD_UNCHANGED)
                    bg = cvzone.overlayPNG(bg,aiImg,(516,180))
                    #print (playerAction)
            
    #embed webcam
    bg[154:554,77:392] = scaledImg
    
    if stateResult:
        bg = cvzone.overlayPNG(bg,aiImg,(516,180))
        
    cv2.putText(bg ,str(scores[0]), (320,150), cv2.FONT_HERSHEY_PLAIN, 4, (250,0,0), 4)
    cv2.putText(bg ,str(scores[1]), (835,150), cv2.FONT_HERSHEY_PLAIN, 4, (250,0,0), 4)
            
    
    cv2.imshow("BG", bg)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        gameTime = time.time()
        stateResult = False
       
    
   
    
