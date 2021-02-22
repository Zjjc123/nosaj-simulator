import cv2
import os
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-o","--output",required=True)
ap.add_argument("-i","--input",required=True)

args=vars(ap.parse_args())

image_folder = args["input"]
video_name = args["output"]
fourcc=cv2.VideoWriter_fourcc('M','J','P','G')

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = [os.path.join(image_folder, image) for image in images]
images.sort(key=os.path.getctime)
frame = cv2.imread(os.path.join(images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, fourcc, 60.0, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image)))

cv2.destroyAllWindows()
video.release()
