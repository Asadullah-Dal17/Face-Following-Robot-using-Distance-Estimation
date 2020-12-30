
import dlib
import cv2

x, y , h , w = 0,0 ,0 ,0
DISTANCE=0

Know_distance =31.5 # Inches
#mine is 14.3 something, measure your face width, are google it 
Know_width_face =5.7 #Inches

# =============================================================================================
def FocalLengthFinder(Measured_distance, real_width_of_face, width_of_face_in_image):
    # finding focal length
    focal_length = (width_of_face_in_image* Measured_distance)/real_width_of_face
    return focal_length

def Distance_Measurement(face_real_width, Focal_Length, face_with_in_image):
   distance= (face_real_width * Focal_Length)/face_with_in_image 
   return distance 

# =============================================================================================
# print(dlib.__version__)

# print(cv2.__version__)

camera = cv2.VideoCapture(2)
# Dlib Face Detector Object
face_detector = dlib.get_frontal_face_detector()
GREEN = (0, 255, 0)
RED = (0, 0 , 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (0,255,255)
BLACK=(0,0,0)

PERPEL = (255,0,255)

fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 =cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 =cv2.FONT_HERSHEY_TRIPLEX
Radius =20



def Face_Data(image, CallOut, Distance):
    # Variables 
    face_width = 0
    face_x, face_y =0,0
    face_center_x =0
    face_center_y =0

    Distance_level = int(Distance*1.9)
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray_frame,1)
    w = 0

    for face in faces:
        x = face.left()
        y = face.top()
        w = face.right() - x
        h = face.bottom() - y
        w = w
        face_width= w 
        # cv2.circle(frame, (x,y+h),Radius, WHITE, 2, cv2.FILLED )
        # Finding The Center of Face 
        face_center_x =int(w/2)+x
        face_center_y =int(h/2)+y
        # print(face_center_x, face_center_y)
        # drwaing the Circle
        # cv2.circle(frame, (face_center_x, face_center_y), Radius, YELLOW, cv2.FILLED)
        # cv2.rectangle(image, (x, y), (x+w, y+h), (WHITE), 2)
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

            # cv2.line(image, (x,y), (face_center_x,face_center_y ), (155,155,155),1)
            # Box for Text over the face 
            Above_face = 30
            cv2.line(image, (x,y-Above_face), (x+225, y-Above_face), (YELLOW), 25)
            cv2.line(image, (x,y-Above_face), (x+Distance_level, y-Above_face), (GREEN), 25)

            # Puting in the Text on Screen
            cv2.putText(image, f"Distance {round(Distance,2)} Inch", (x-5,y-24), fonts,0.7, (BLACK),2)
            
            # cv2.circle(image, (face_center_x, face_center_y),2, (255,0,255), 1 )
            # cv2.circle(image, (x, y),2, (255,0,255), 1 )
    return w

reference_image = cv2.imread("Reference_Image/Ref_image.png")
reference_face_width = Face_Data(reference_image, True, 10)
print(reference_face_width)
FOCAL_LENGHT = FocalLengthFinder(Know_distance, Know_width_face,reference_face_width)
print(FOCAL_LENGHT)
cv2.imshow("ref", reference_image)
# cv2.waitKey(0)
Distance =0
while True:
    
    ret, frame = camera.read()
    width_of_face =Face_Data(frame, True, Distance)
    # print(width_of_face)
    if width_of_face !=0:
        print(Distance)
        DISTANCE = Distance_Measurement(Know_width_face, FOCAL_LENGHT, width_of_face)
        print(DISTANCE)
        Distance = DISTANCE
    cv2.imshow("frame", frame)
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
camera.release()