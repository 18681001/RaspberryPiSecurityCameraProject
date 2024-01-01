# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import argparse
import sys
import numpy as np
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import datetime
import os

# Define Variables

# Define Time Data to access Default Directory

# return Years-Months-Days
dateday = datetime.datetime.now().strftime('%y-%m-%d') 
# return Years-Months-Days_Hours:Minutes:Seconds to define file name
datenow = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') 

#Set Video File Property
# User Defined Saving video location
# Please change your-directory-name to your real External Device
# You can check name using LXTerminal opening at External Device
dirloc = '/media/your-directory-name/' + dateday 

# if you want to make directory automatically please use below codes.
# if not os.path.exist(dirloc):
#   os.makedir(dirloc)
# else
#   print("Directory Already Exist or Invalid Directory")

if not os.path.exists(dirloc):
    print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Defined Directory doesn't exist at " + dirloc)
    dirloc = '/home/pi/RaspberryPiSecurityCameraProject/ICT/' + dateday #Video save location
    if not os.path.exists(dirloc):
      print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Create Default Directory at " + dirloc)
      os.makedirs(dirloc)
    else:
      print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Default Directory " + dirloc + " exists.")

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (255, 0, 255)  # change color red to ???


def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:

    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    probability100 = int(probability*100) # return probabilty to percent
    result_text = category_name + ' (' + str(probability100) + '%)'
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)
    ##cv2.rectangle(image, ((_MARGIN + bbox.origin_x),(_MARGIN + bbox.origin_x)), ((_MARGIN + _ROW_SIZE + bbox.origin_y),(_MARGIN + _ROW_SIZE + bbox.origin_y)) , (255,255,255), cv2.FILLED)

  return image

def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """
  # video Record Defined
  # Define Codec (default Setting is XVID)
  fourcc = cv2.VideoWriter_fourcc(*'XVID')

  # Define file extension (default Setting is avi)
  ext = "avi"

  #Define Video Files Saving Location 
  videofileloc = os.path.join(dirloc, f"object_{datenow}.{ext}")

  # Define File save type
  out = cv2.VideoWriter(videofileloc, fourcc, 15.0, (width, height))
  video_record = False

  # Variables to calculate FPS
  counter = 0
  

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(0) #define video device
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (255, 255, 255)  # chanage color red to white
  font_size = 0.5
  font_thickness = 1
  #fps_avg_frame_count = 10

  # Initialize the object detection model
  base_options = core.BaseOptions(
      file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
  detection_options = processor.DetectionOptions(
      max_results=3, score_threshold=0.3)
  options = vision.ObjectDetectorOptions(
      base_options=base_options, detection_options=detection_options)
  detector = vision.ObjectDetector.create_from_options(options)
  
  

  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from camera device. Please verify your camera settings.'
      )

    counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    # Draw keypoints and edges on input image
    image = visualize(image, detection_result)
    
    # add timestamp with magenta color text
    cv2.putText(image, datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S'), (10, 70), cv2.FONT_HERSHEY_DUPLEX, font_size, (255, 0, 255))
    cv2.putText(image, 'pi camera', (10, 30), cv2.FONT_HERSHEY_DUPLEX, font_size, (0, 255, 255))
      
    # Start Recording Code
    if detection_result.detections:
      video_record = True
    
    # Save Videos
    if video_record:
      cv2.putText(image, "Start Recording...", (10, 50), cv2.FONT_HERSHEY_DUPLEX, font_size, (0, 255, 0))
      out.write(image)
    # If Record is not Detected 
    if not detection_result.detections:
      cv2.putText(image, "Record Stopped", (10, 50), cv2.FONT_HERSHEY_DUPLEX, font_size, (0, 0, 255))
      video_record = False      
    
    # Stop the program if the q key is pressed
    if cv2.waitKey(1) == ord('q'):
      print("[" + datetime.datetime.now().strftime('%y-%m-%d_%H:%M:%S') + "] Motion Detect Recording Terminating...")
      break
    cv2.imshow('object_detector', image)

  # Release Resource
  cap.release()
  out.release()
  cv2.destroyAllWindows()


# Original Code's main Argument

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  args = parser.parse_args()

  run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
  main()
