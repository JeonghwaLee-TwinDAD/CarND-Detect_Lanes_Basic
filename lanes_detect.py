import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from moviepy.editor import VideoFileClip
from IPython.display import HTML

#check if the git works
def make_corrdinates(image, line_parameters):
    slope, Intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - Intercept)/slope)
    x2 = int((y2 - Intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    lett_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            lett_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    lett_fit_average = np.average(lett_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
#    print(lett_fit_average)
#    print(right_fit_average)
    left_line = make_corrdinates(image, lett_fit_average)
    right_line = make_corrdinates(image, right_fit_average)
    return np.array([left_line, right_line])

        
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return gray, blur, canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for  x1, y1, x2, y2 in lines:
             cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(100, height),(900, height), (483, 307)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
'''
image_names = os.listdir("test_images/")
for image_name in image_names:
    file = pathlib.Path('./test_images/' + image_name)
    if file.exists(): #check if exit original image file 
        image = cv2.imread('./test_images/' + image_name)
        lane_image = np.copy(image)
        gray_image, blur_image, canny_image = canny(lane_image)
        cropped_image = region_of_interest(canny_image)
        lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 40, np.array([]), minLineLength=20, maxLineGap=40)
        averaged_lines = average_slope_intercept(cropped_image, lines)
        line_image = display_lines(lane_image, averaged_lines)
        combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
        plt.imshow(combo_image)
        plt.show()

        #Save pipeline image files in the image output directory 
        image_list = [image, gray_image, blur_image, canny_image, cropped_image, line_image, combo_image]
        count = 0
        for img in image_list:
            cv2.imwrite('./test_images_output/'+ image_name + str(count) +'.jpg',img)
            count += 1    
else:
    print ("File not exist")
'''
#Test video operation 
video_name = "./test_videos/solidWhiteRight.mp4"
white_output = './test_videos_output/solidWhiteRight.mp4'

'''cap = cv2.VideoCapture(video_name) 
while(cap.isOpened()):
    _, frame = cap.read()
    gray_image, blur_image, canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 40, np.array([]), minLineLength=20, maxLineGap=40)
    averaged_lines = average_slope_intercept(cropped_image, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    
    cv2.imshow('result', combo_image)
    cv2.waitKey(1)
'''

clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
for frame in clip1.iter_frames():
    gray_image, blur_image, canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 40, np.array([]), minLineLength=20, maxLineGap=40)
    averaged_lines = average_slope_intercept(cropped_image, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
white_clip = clip1.fl_image(combo_image) #NOTE: this function expects color images!!
white_clip.write_videofile(white_output, audio=False)
   
    #cv2.imshow('result', combo_image)
    #cv2.waitKey(1)