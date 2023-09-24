import socket
import cv2
import numpy as np

# to connect with integrsted camera
cap = cv2.VideoCapture(1)

# creating socket with the help of socket module
# Here "AF_INET" address family and "TCP" protocol is used
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Removing the "Address already in use" ERROR
# allows server to reuse the port

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# port binding
# to bind ip address with port number

s.bind(("10.0.0.103",1000))

# In TCP programming ,we always need to mention state/mode
# to set "listen" state/mode

s.listen()
session, addr = s.accept()

try:
    # infinite while loop to receive and send stream of images i.e. video continuously
    while True:
             
        ret, photo = cap.read()
        
        # converting clicked image into byte string with the help of tobytes() function
        photo_bytes = cv2.imencode(".jpeg", photo)[1].tobytes()
 
        # sending image to the clients
        session.sendall(photo_bytes)
    
        # receving image
        client_photo = session.recv(100000000)

        # converting received byte string into numpy array
        # frombuffer() function will convert received byte string into 1D array
        client_photo_final = np.frombuffer(client_photo, dtype='uint8')

        # converting 1D array into 3D array by using imencode() function
        client_photo_show = cv2.imdecode(client_photo_final, 1) # here inside imencode() function, argument "1" is for converting 1D array into color image and "0" is for converting 1D array into black n white/gray image. This "1","0" are flag.

        # now to show image received from server, use imshow() function
        cv2.imshow("mypic", client_photo_show)

        # waitKey() function is use to hold video window
        if cv2.waitKey(10) == 27:
            # to close the session
            s.close()
            break
            
    cv2.destroyAllWindows()
    cap.release()
except:
    print("Session closed by client")
