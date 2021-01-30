'''
-------------------------------------------
-    Author: Asadullah Dal                -
-    =============================        -
-    Company Name: AiPhile                -
-    =============================        -
-    Purpose : Youtube Channel            -
-    ============================         -
-    Link: https://youtube.com/c/aiphile  -
-------------------------------------------

'''


# Loading Necessary Modules
import cv2
import serial # Allow us to Communicate with Arduino 
import time 
# variables
# distance from camera to object(face) measured
x, y , h , w = 0,0 ,0 ,0
DISTANCE=0

Known_distance =31.5 # Inches
#mine is 14.3 something, measure your face width, are google it 
Known_width=5.7 #Inches
# Colors  >>> BGR Format(BLUE, GREEN, RED)
GREEN = (0,255,0) 
RED = (0,0,255)
BLACK = (0,0,0)
YELLOW =(0,255,255)
PERPEL = (255,0,255)
WHITE = (255,255,255)

fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 =cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 =cv2.FONT_HERSHEY_TRIPLEX

cap = cv2.VideoCapture(2)
Distance_level =0
# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# focal length finder function
def FocalLength(measured_distance, real_width, width_in_rf_image):
    # Function Discrption (Doc String)
    '''
    This Function Calculate the Focal Length(distance between lens to CMOS sensor), it is simple constant we can find by using 
    MEASURED_DISTACE, REAL_WIDTH(Actual width of object) and WIDTH_OF_OBJECT_IN_IMAGE 

    :param1 Measure_Distance(int): It is distance measured from object to the Camera while Capturing Reference image
    
    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 5.7 Inches)

    :param3 Width_In_Image(int): It is object width in the frame /image in our case in the reference image(found by Face detector) 
    :retrun Focal_Length(Float):
    '''
    focal_length = (width_in_rf_image* measured_distance)/ real_width
    return focal_length
# distance estimation function
def Distance_finder (Focal_Length, real_face_width, face_width_in_frame):
    # Function Discrption (Doc String)
    '''
    This Function simply Estimates the distance between object and camera using arguments(Focal_Length, Actual_object_width, Object_width_in_the_image)

    :param1 Focal_length(float): return by the Focal_Length_Finder function
    
    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 5.7 Inches)

    :param3 object_Width_Frame(int): width of object in the image(frame in our case, using Video feed)

    :return Distance(float) : distance Estimated  
    
    '''
    distance = (real_face_width * Focal_Length)/face_width_in_frame

    return distance
    
#face detection Fauction 
def face_data(image, CallOut, Distance_level):
    # Function Discrption (Doc String)
    '''
    
    This function Detect face and Draw Rectangle and display the distance over Screen
    
    :param1 Image(Mat): simply the frame 
    :param2 Call_Out(bool): If want show Distance and Rectangle on the Screen or not
    :param3 Distance_Level(int): which change the line according the Distance changes(Intractivate)

    :return1  face_width(int): it is width of face in the frame which allow us to calculate the distance and find focal length
    :return2 face(list): length of face and (face paramters)
    :return3 face_center_x: face centroid_x coordinate(x)
    :return4 face_center_y: face centroid_y coordinate(y)
 
    '''
    face_width = 0
    face_x, face_y =0,0
    face_center_x =0
    face_center_y =0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    scaleFactor=1.3
    minNeighbors=5,
    minSize=(30, 30),
    # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    faces = face_detector.detectMultiScale(gray_image,  scaleFactor=1.301, minNeighbors=5,minSize=(10, 10)) # better detection at scaling factor 1.21/ conumse more cpu.
    for (x, y, h, w) in faces:
        # cv2.rectangle(image, (x, y), (x+w, y+h), BLACK, 1)
        face_width = w
        face_center=[]
        # Drwaing circle at the center of the face 
        face_center_x =int(w/2)+x
        face_center_y =int(h/2)+y
        if Distance_level <10:
            Distance_level=10
        
        # cv2.circle(image, (face_center_x, face_center_y),5, (255,0,255), 3 )
        if CallOut==True:
            LLV = int(h*0.12) 
             # print(LLV)
            line_thickness =2

            # cv2.rectangle(image, (x, y), (x+w, y+h), BLACK, 1)
            cv2.line(image, (x,y+LLV), (x+w, y+LLV), (GREEN),line_thickness)
            cv2.line(image, (x,y+h), (x+w, y+h), (GREEN),line_thickness)
            cv2.line(image, (x,y+LLV), (x, y+LLV+LLV), (GREEN),line_thickness)
            cv2.line(image, (x+w,y+LLV), (x+w, y+LLV+LLV), (GREEN),line_thickness)
            cv2.line(image, (x,y+h), (x, y+h-LLV), (GREEN),line_thickness)
            cv2.line(image, (x+w,y+h), (x+w, y+h-LLV), (GREEN),line_thickness)

            cv2.line(image, (x,y), (face_center_x,face_center_y ), (155,155,155),1)
            cv2.line(image, (x,y-11), (x+210, y-11), (YELLOW), 25)
            cv2.line(image, (x,y-11), (x+Distance_level, y-11), (GREEN), 25)
            
            cv2.circle(image, (face_center_x, face_center_y),2, (255,0,255), 1 )
            cv2.circle(image, (x, y),2, (255,0,255), 1 )
           
        # face_x = x
        # face_y = y

    return face_width, faces, face_center_x, face_center_y

# reading reference image from directory
ref_image = cv2.imread(r"Reference_Image/Ref_image.png")

ref_image_face_width,_, _,_= face_data(ref_image, False, Distance_level)
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)

# cv2.imshow("ref_image", ref_image)
# Setting up Arduino For Communication
Arduino = serial.Serial(baudrate=9600, port = 'COM3')
# variable for Arduino Communication 
Direction =0
# Max 0 and Min 255 Speed of Motors 
Motor1_Speed =0 # Speed of motor Accurding to PMW values in Arduino 
Motor2_Speed =0
Truing_Speed =110
net_Speed =180

while True:
    _, frame = cap.read()
    frame_height, frame_width, _ = frame.shape
    # print(frame_height, frame_width)
    # calling face_data function
    # Distance_leve =0
    RightBound = frame_width-140
    Left_Bound =140

    face_width_in_frame,Faces ,FC_X, FC_Y= face_data(frame, True, Distance_level)
    # finding the distance by calling function Distance finder
    for (face_x, face_y, face_w, face_h) in Faces:
        if face_width_in_frame !=0:
            Distance = Distance_finder(Focal_length_found, Known_width,face_width_in_frame)
            Distance = round(Distance,2)
            # Drwaing Text on the screen
            Distance_level= int(Distance)
            cv2.line(frame, (50,33), (130, 33), (BLACK), 15)
            cv2.putText(frame, f"Robot State", (50,35), fonts,0.4, (YELLOW),1)
            # cv2.line(frame, (50,65), (170, 65), (BLACK), 15)
            
            # Direction Decider Condition
            if FC_X<Left_Bound:
                # Writing The motor Speed 
                Motor1_Speed=Truing_Speed
                Motor2_Speed=Truing_Speed
                print("Left Movement")
                # Direction of movement
                Direction=3
                cv2.line(frame, (50,65), (170, 65), (BLACK), 15)
                cv2.putText(frame, f"Move Left {FC_X}", (50,70), fonts,0.4, (YELLOW),1)

            elif FC_X>RightBound:
                # Writing The motor Speed 
                Motor1_Speed=Truing_Speed
                Motor2_Speed=Truing_Speed
                print("Right Movement")
                # Direction of movement
                Direction=4
                cv2.line(frame, (50,65), (170, 65), (BLACK), 15)
                cv2.putText(frame, f"Move Right {FC_X}", (50,70), fonts,0.4, (GREEN),1)
            
                # cv2.line(frame, (50,65), (170, 65), (BLACK), 15)
                # cv2.putText(frame, f"Truing = False", (50,70), fonts,0.4, (WHITE),1)

            elif Distance >70 and Distance<=200:
                # Writing The motor Speed 
                Motor1_Speed=net_Speed
                Motor2_Speed=net_Speed
                # Direction of movement
                Direction=2
                cv2.line(frame, (50,55), (200, 55), (BLACK), 15)
                cv2.putText(frame, f"Forward Movement", (50,58), fonts,0.4, (PERPEL),1)
                print("Move Forward")
            
            elif Distance >20 and Distance<=70:
                # Writing The motor Speed 
                Motor1_Speed=net_Speed
                Motor2_Speed=net_Speed
                # Direction of movement
                Direction=1
                print("Move Backward")
                cv2.line(frame, (50,55), (200, 55), (BLACK), 15)
                cv2.putText(frame, f"Backward Movement", (50,58), fonts,0.4, (PERPEL),1)
            
            else:
                # Writing The motor Speed 
                Motor1_Speed=0
                Motor2_Speed=0
                # Direction of movement
                Direction=0
                cv2.line(frame, (50,55), (200, 55), (BLACK), 15)
                cv2.putText(frame, f"No Movement", (50,58), fonts,0.4, (PERPEL),1)

            cv2.putText(frame, f"Distance {Distance} Inch", (face_x-6,face_y-6), fonts,0.6, (BLACK),2)
            data = f"A{Motor1_Speed}B{Motor2_Speed}D{Direction}" #A233B233D2
            print(data)
            # Sending data to Arduino 
            Arduino.write(data.encode()) #Encoding the data into Byte fromat and then sending it to the arduino 
            time.sleep(0.002) # Providing time to Arduino to Receive data.
            Arduino.flushInput() #Flushing out the Input.

    cv2.line(frame, (Left_Bound, 80), (Left_Bound, 480-80), (YELLOW), 2)
    cv2.line(frame, (RightBound, 80),(RightBound, 480-80), (YELLOW), 2)
    cv2.imshow("frame", frame )

    if cv2.waitKey(1)==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
