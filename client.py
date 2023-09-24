import socket
import numpy as np
import cv2
# to connect with internal camera

cap = cv2.VideoCapture(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# to connect client with server

s.connect(("10.0.0.103",1000))

# here is the final code to send and receive stream of images i.e. video from server
# here we are creating try-except block for error/exeption handling
try:
    # infinite while loop to receive and send stream of images i.e. video continuously
    while True:
        # receving image(in the form byte string) from the server with thw help of recv() function
        server_photo = s.recv(100000000)
        
        # converting received byte string into numpy array
        # frombuffer() function will convert received byte string into 1D array
        server_photo_final = np.frombuffer(server_photo, dtype='uint8')
        
        # converting 1D array into 3D array by using imencode() function
        server_photo_show = cv2.imdecode(server_photo_final, 1)
        cv2.imshow("Video from Server", server_photo_show)
        
        # waitKey() function is use to hold video window
        if cv2.waitKey(10) == 27:
            s.close()
            break
            
        # read() function for clicking image
        ret, photo = cap.read()
        
        # converting clicked image into byte string with the help of tobytes() function
        photo_bytes = cv2.imencode(".jpeg", photo)[1].tobytes()
        
        # sending image to the server in the form of byte string 
        s.sendall(photo_bytes)
        
    cv2.destroyAllWindows()
    cap.release()
    
except:
    print("Session closed by server")
