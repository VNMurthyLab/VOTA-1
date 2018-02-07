import uc480
import pylab as pl
import matplotlib.pyplot as plt
import cv2
import time

cam = uc480.uc480()

cam.connect()
cam.set_exposure(10)

time.sleep(1)
print(cam.get_exposure())

# cam.disconnect()
# pl.imshow(img)
# pl.show()XVID

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280,1024))

cam.start_live()
cam.set_pixelclock(43)
fps = cam.set_framerate(25.01)
print(fps)
print(cam.get_pixelclock())
while(True):
    # Capture frame-by-frame
    time.sleep(0.04)
    frame = cam.read()
    #frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    # Our operations on the frame scome here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #out.write(frame)
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.stop_live()
cam.disconnect()
cv2.destroyAllWindows()