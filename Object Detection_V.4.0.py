import cv2
import ctypes
import numpy as np
from line_notify import LineNotify
import winsound


ACCESS_TOKEN = "IUmNdJYFQuetWIZDUlbvOBS5vSjXZvJOAwlT8Zcmd03"
notify = LineNotify(ACCESS_TOKEN)


img_counter = 0


frequency = 3500  # Set Frequency To 2500 Hertz
duration = 250  # Set Duration To 1000 ms == 1 second


WINDOW_NAME = 'Full Integration'


CLASSES = [
    "BACKGROUND",
    "AEROPLANE",
    "BICYCLE",
    "BIRD",
    "BOAT",
    "BOTTLE",
    "BUS",
    "CAR",
    "CAT",
    "CHAIR",
    "COW",
    "DININGTABLE",
    "DOG",
    "HORSE",
    "MOTORBIKE",
    "PERSON",
    "POTTEDPLANT",
    "SHEEP",
    "SOFA",
    "TRAIN",
    "TVMONITOR"
    ]
CLASSES_NAME = [
    "วัตถุบางสิ่ง",
    "เครื่องบิน", #AIRPLANE
    "จักรยานยนต์",
    "นก",
    "เรือ",
    "ขวด",
    "รถบรรทุก",  #BUS
    "รถยนต์",
    "แมว",
    "เก้าอี้",
    "โค-กระบือ",
    "โต๊ะ",
    "สุนัข",
    "ม้า",
    "จักรยานยนต์",
    "คน",
    "กระถางต้นไม้",
    "แกะ",
    "โซฟา",
    "รถไฟ",
    "จอมอนิเตอร์"
    ]
COLORS = np.random.uniform(0,100, size=(len(CLASSES), 3))
#โหลดmodelจากแฟ้ม
net = cv2.dnn.readNetFromCaffe("./MobileNetSSD/MobileNetSSD.prototxt","./MobileNetSSD/MobileNetSSD.caffemodel")



video_capture = cv2.VideoCapture(0)
#video_capture = cv2.VideoCapture("Video_1.mp4")
# if there is no external camera then take the built-in camera
if not video_capture.read()[0]:
    video_capture = cv2.VideoCapture(1)


# Full screen mode
cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)




while (video_capture.isOpened()):
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    ret, frame = video_capture.read()
    #frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    scaleWidth = float(screen_width)/float(frame_width)
    scaleHeight = float(screen_height)/float(frame_height)


    if scaleHeight>scaleWidth:
        imgScale = scaleWidth


    else:
        imgScale = scaleHeight


    newX,newY = frame.shape[1]*imgScale, frame.shape[0]*imgScale
    frame = cv2.resize(frame,(int(newX),int(newY)))


    if ret:
       
        (h,w) = frame.shape[:2]
        # ท ำ preprocessing
       
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300,300), 127.5)
       
        net.setInput(blob)
        #feedเข้าmodelพร้อมได้ผลลัพธ์ทั้งหมดเก็บมาในตัวแปร detections
       
        detections = net.forward()


       
        for i in np.arange(0, detections.shape[2]):
           
            percent = detections[0,0,i,2]
            #กรองเอาเฉพาะค่าpercentที่สูงกว่า 0.5 เพิ่มลดได้ตามต้องการ
           
            if percent > 0.9900:
            #if percent > 0.50:
               
                class_index = int(detections[0,0,i,1])
               
                box = detections[0,0,i,3:7]*np.array([w,h,w,h])
               
                (startX, startY, endX, endY) = box.astype("int")


                #ส่วนตกแต่งสามารถลองแก้กันได้ วาดกรอบและชื่อ
               
                label = "{} [{:.2f}%]".format(CLASSES[class_index], percent*100)


                TEXT_Notify = "{} ที่หน้าบ้าน".format(CLASSES_NAME[class_index], percent*100)
               
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[class_index], 2)
               
                cv2.rectangle(frame, (startX-1, startY-30), (endX+1, startY), COLORS[class_index], cv2.FILLED)
               
                y = startY - 15 if startY-15>15 else startY+15
               
                cv2.putText(frame, label, (startX+20, y+5), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1)
 
                img_name = "PICTURE/image_1.jpg".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                #img_counter += 1
 
                notifying = img_name        # format(img_name)
                Notify = (" " +  TEXT_Notify)
                ACCESS_TOKEN = "IUmNdJYFQuetWIZDUlbvOBS5vSjXZvJOAwlT8Zcmd03"
                notify = LineNotify(ACCESS_TOKEN)
                 # ส่งข้อความ + ภาพที่อยู่ในโฟลเดอร์เดียวกันนี้
                notify.send(Notify, notifying)
 
                winsound.Beep(frequency, duration)


    cv2.imshow(WINDOW_NAME, frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
     break


# release video capture object
video_capture.release()
cv2.destroyAllWindows()



