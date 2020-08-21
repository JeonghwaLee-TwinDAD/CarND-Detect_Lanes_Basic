import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from moviepy.editor import VideoFileClip
from IPython.display import HTML

#os.mkdir('test_images_output')
#os.rename("solidWhiteRight_out.jpg", './test_images_output/solidWhiteRight_out.jpg')
#os.remove('./test_images_output/'+'solidWhiteRight_out2.jpg')
#image_names = os.listdir("test_images/")
#print(image_names)


param1 = 34
param2 = 43

def process_image(img):
    global param1
    global param2
    if param1 > param2:
        #do whatever
        param1 = param2 * 2
    return image
    
white_output = './test_videos_output/solidWhiteRight.mp4'
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)

final_clip = clip1.fl_image(process_image)
final_clip.write_videofile(white_output, audio=False)

#plt.imshow(clip1.get_frame())
#plt.show()
#white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
#white_clip.write_videofile(white_output, audio=False)

