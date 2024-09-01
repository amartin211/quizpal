import logging
import numpy as np
import cv2
from ultralytics import YOLO
import logging
import uuid
import os


# Basic configuration of logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def crop_and_save_image_with_bbox(input_file_path, output_file_path, box):
    """
    Crops an image using the given box coordinates.

    Parameters:
    - input_file_path (str): The path to the input image.
    - output_file_path (str): The path where the cropped image should be saved.
    - box (tuple): A tuple containing (x, y, w, h).
    """
    # with Image.open(input_file_path) as img:
    img = cv2.imread(input_file_path)

    top_margin = 50  # The size of the margin to add at the top

    # Calculate the new y_min, ensuring it doesn't go below 0
    new_y_min = max(box[1] - top_margin, 0)

    # Crop the image with the adjusted box to include the margin at the top
    enlarged_crop = img[new_y_min : box[3], box[0] : box[2]]

    crop = img[box[1] : box[3], box[0] : box[2]]
    cv2.imwrite(output_file_path, enlarged_crop)


def detect_screen_using_custom_yolo(source, output_path):

    model = YOLO("yolo_screen_detector.pt")  # load a pretrained model

    # Set the confidence threshold
    conf_thresh = 0.6

    # Call the predict function with the specified parameters
    results = model.predict(source=source, conf=conf_thresh, device="cpu")

    for result in results:
        boxes = result.boxes.cpu().numpy()

    index = np.argmax(boxes.data[:, -2])
    bbox = boxes.data[index][:4].astype(int)

    crop_and_save_image_with_bbox(source, output_path, bbox)


def improved_rotate_image_using_lines(img_path):
    # Read the image
    image = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use the Canny edge detector to find edges in the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Use Hough Line Transform to detect lines in the image
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = (theta * 180 / np.pi) - 90
            if -45 <= angle <= 45:
                angles.append(angle)

        # If we have no valid angles, return the original image
        if not angles:
            return image

        # Use the median of the angles for a more robust estimate
        rotation_angle = np.median(angles)

        # Get the image's center
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        # Create a rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1)

        # Rotate the image
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

        return rotated_image
    else:
        # If no lines are detected, return the original image
        return image


def improved_rotate_image_using_lines_two(img_path):
    # Read the image
    image = cv2.imread(img_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filtering to reduce noise
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)

    # Use the Canny edge detector to find edges in the image
    edges = cv2.Canny(filtered, 50, 150, apertureSize=3)

    # Use Hough Line Transform to detect lines in the image
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = (theta * 180 / np.pi) - 90
            if -45 <= angle <= 45:
                angles.append(angle)

        # If we have no valid angles, return the original image
        if not angles:
            return image

        # Use the median of the angles for a more robust estimate
        rotation_angle = np.median(angles)

        # Get the image's center
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        # Create a rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1)

        # Rotate the image
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

        return rotated_image
    else:
        # If no lines are detected, return the original image
        return image

def preprocessing_raw_image_double_detect(path_raw_img, processed_path):

    try:

        unique_filename = str(uuid.uuid4()) + ".jpeg"
        yolo_path = "/tmp/" + unique_filename

        detect_tv_laptop(path_raw_img, yolo_path)
        detect_screen_using_custom_yolo(yolo_path, yolo_path)
        cropped_img = improved_rotate_image_using_lines(yolo_path)

        os.remove(yolo_path)

    except Exception as e:
        raise ValueError("No screen has been detected on this image") from e

    cv2.imwrite(processed_path, cropped_img)

    return cropped_img


def detect_tv_laptop(source, output_path):
    model = YOLO("yolov8m.pt")  # load a pretrained model

    # Detect objects from classes 0 and 1 only
    classes = [62, 63]

    # Set the confidence threshold
    conf_thresh = 0.6

    # Call the predict function with the specified parameters
    results = model.predict(source=source, classes=classes, conf=conf_thresh, device="cpu")

    for result in results:
        boxes = result.boxes.cpu().numpy()

    index = np.argmax(boxes.data[:, -2])
    bbox = boxes.data[index][:4].astype(int)

    crop_and_save_image_with_bbox(source, output_path, bbox)
