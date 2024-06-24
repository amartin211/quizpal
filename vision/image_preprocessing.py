import tempfile
import logging
import numpy as np
from PIL import Image
from skimage import measure
from skimage.measure import label, regionprops
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.morphology import closing, square
from skimage.segmentation import clear_border
from skimage.transform import rotate
import cv2
from ultralytics import YOLO
import os
import logging

# Basic configuration of logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def preprocessing_raw_image(path_raw_img, processed_path):

    try:
        yolo_path = "yolo_cropped.jpeg"
        detect_screen(path_raw_img, yolo_path)
        # Load the image
        img = Image.open(yolo_path)
    except Exception as e:
        # raise ValueError("No screen has been detected on this image") from e
        return

    img_width, img_height = img.size

    # Convert image to np.array for processing
    img_np = np.array(img)

    # Convert the image to grayscale
    gray_img = rgb2gray(img_np)

    # Threshold the image to binary using Otsu's method
    thresh = threshold_otsu(gray_img)
    binary = gray_img > thresh

    # Perform a morphological closing operation to close the gaps between white areas
    closed = closing(binary, square(3))

    # Label the regions in the closed image
    label_image = label(closed)

    # Get the properties of the labeled regions
    props = regionprops(label_image)

    # Filter the regions based on their area, keeping only the largest region
    largest_region = max(props, key=lambda prop: prop.area)

    # Get the bounding box of the largest region
    minr, minc, maxr, maxc = largest_region.bbox

    side_margin = (
        70  # Margin to add to each side BECAUSE MATHPIX COULD NOT OCR LONG STRING !!!
    )
    new_minc = max(minc - side_margin, 0)
    new_maxc = min(maxc + side_margin, img_width)

    # Crop the image to the bounding box of the largest region
    cropped_img = img.crop((new_minc, minr, new_maxc, maxr))

    # if cropped_img.width < cropped_img.height:
    # Rotate the image 90 degrees to make bands horizontal
    #    cropped_img = cropped_img.rotate(-90, expand=True)

    cropped_img.save(processed_path)
    cropped_img = improved_rotate_image_using_lines(processed_path)
    cv2.imwrite(processed_path, cropped_img)

    # Display the image in a window named 'image_window'
    # cv2.imshow('image_window', cropped_img)

    # Wait indefinitely until a key is pressed
    # cv2.waitKey(0)

    # Close all OpenCV windows
    # cv2.destroyAllWindows()

    # remove intermediary yolo crop
    # os.remove(yolo_path)

    return cropped_img


def preprocessing_raw_image_without_crop_screen(path_raw_img, processed_path):

    try:
        yolo_path = "yolo_cropped.jpeg"
        detect_screen(path_raw_img, yolo_path)
        # Load the image
    except Exception as e:
        # raise ValueError("No screen has been detected on this image") from e
        return

    cropped_img = improved_rotate_image_using_lines(yolo_path)
    cv2.imwrite(processed_path, cropped_img)

    return cropped_img


def preprocessing_raw_image_new(path_raw_img, processed_path):

    try:
        yolo_path = "yolo_cropped.jpeg"
        detect_screen(path_raw_img, yolo_path)
        # Load the image
        img = Image.open(yolo_path)
    except Exception as e:
        raise ValueError("No screen has been detected on this image") from e

    img_width, img_height = img.size

    # Convert image to np.array for processing
    img_np = np.array(img)

    # Convert the image to grayscale
    gray_img = rgb2gray(img_np)

    # Threshold the image to binary using Otsu's method
    thresh = threshold_otsu(gray_img)
    binary = gray_img > thresh

    # Perform a morphological closing operation to close the gaps between white areas
    closed = closing(binary, square(3))

    # Label the regions in the closed image
    label_image = label(closed)

    # Get the properties of the labeled regions
    props = regionprops(label_image)

    minr, minc, maxr, maxc = img_height, img_width, 0, 0

    for prop in props:
        # Update collective bounding box
        bbox = prop.bbox
        if (
            bbox[2] - bbox[0] > img_height * 0.01
        ):  # Example condition: consider regions with a minimum height
            minr = min(minr, bbox[0])
            minc = min(minc, bbox[1])
            maxr = max(maxr, bbox[2])
            maxc = max(maxc, bbox[3])

    # Add margin to sides (left and right)
    side_margin = 70  # Adjust as necessary
    new_minc = max(minc - side_margin, 0)
    new_maxc = min(maxc + side_margin, img_width)

    cropped_img = img.crop((new_minc, minr, new_maxc, maxr))

    # if cropped_img.width < cropped_img.height:
    # Rotate the image 90 degrees to make bands horizontal
    #    cropped_img = cropped_img.rotate(-90, expand=True)

    cropped_img.save(processed_path)
    cropped_img = improved_rotate_image_using_lines(processed_path)
    cv2.imwrite(processed_path, cropped_img)

    # Display the image in a window named 'image_window'
    # cv2.imshow('image_window', cropped_img)

    # Wait indefinitely until a key is pressed
    # cv2.waitKey(0)

    # Close all OpenCV windows
    # cv2.destroyAllWindows()

    # remove intermediary yolo crop
    # os.remove(yolo_path)

    return cropped_img


def crop_middle(img_orig):

    img_orig = Image.fromarray(cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB))
    # Calculate the dimensions of the image
    width, height = img_orig.size

    # Calculate the center point of the image
    center_x, center_y = width // 2, height // 2

    # Define the "small square" as a region of the image centered at the middle point
    # and with side length equal to half of the shorter dimension of the image
    side_length = min(width, height) // 2
    left = center_x - side_length // 2
    right = center_x + side_length // 2
    upper = center_y - side_length // 2
    lower = center_y + side_length // 2

    # Crop the image to the small square
    img_cropped = img_orig.crop((left, upper, right, lower))

    return img_cropped


def detect_vertical_band_refined(img):
    img_cropped = crop_middle(img)
    img_gray = img_cropped.convert("L")

    # Convert the image data to a NumPy array
    img_array = np.array(img_gray)

    # Sum the pixel intensities along the horizontal axis
    sum_intensities = np.sum(img_array, axis=0)

    # Calculate the mean and standard deviation of the pixel intensity sums
    mean_intensity = np.mean(sum_intensities)
    std_intensity = np.std(sum_intensities)
    print(std_intensity)

    # Set the threshold as the mean plus 2 standard deviations
    threshold = mean_intensity + 2 * std_intensity

    # Check if there is a peak that surpasses the threshold
    vertical_band_present = np.any(sum_intensities > threshold)

    # Set the threshold as the mean minus 2 standard deviations
    threshold_low = mean_intensity - 3 * std_intensity

    # Check if there is a dip that goes below the threshold
    vertical_band_present_low = np.any(sum_intensities < threshold_low)

    return vertical_band_present


def detect_vertical_band_simplified(img):
    img_cropped = crop_middle(img)
    img_gray = img_cropped.convert("L")

    # Convert the image data to a NumPy array
    img_array = np.array(img_gray)

    # Sum the pixel intensities along the horizontal axis
    sum_intensities = np.sum(img_array, axis=0)

    # Calculate the mean and standard deviation of the pixel intensity sums
    mean_intensity = np.mean(sum_intensities)
    std_intensity = np.std(sum_intensities)
    print(std_intensity)

    return std_intensity > 6000


def split_if_band(img_orig, path_to_output):
    img_orig = Image.fromarray(cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB))
    width, height = img_orig.size
    # Define the areas for the left and right crops
    left_crop_area = (0, 0, width // 2, height)
    right_crop_area = (width // 2, 0, width, height)

    # Crop the image to the left and right areas
    left_crop = img_orig.crop(left_crop_area)
    right_crop = img_orig.crop(right_crop_area)

    left_crop.save(path_to_output[0])
    right_crop.save(path_to_output[1])

    return left_crop, right_crop


def crop_white_area(img):
    # Convert the image to grayscale
    gray_img = np.array(img.convert("L"))

    # Threshold the grayscale image to create a binary image
    binary_img = gray_img > 200

    # Identify the bounding box of each white region in the binary image
    properties = measure.regionprops(measure.label(binary_img))

    # Filter out small regions
    properties = [prop for prop in properties if prop.area > 100]

    # If there is no white area, return the original image
    if not properties:
        return img

    # Get the bounding box of the largest white region
    largest_white_region = max(properties, key=lambda prop: prop.area)
    minr, minc, maxr, maxc = largest_white_region.bbox

    # Crop the original image using the bounding box
    return img.crop((minc, minr, maxc, maxr))


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


def detect_screen(source, output_path):
    model = YOLO("yolov8m.pt")  # load a pretrained model

    # Detect objects from classes 0 and 1 only
    classes = [62, 63]

    # Set the confidence threshold
    conf_thresh = 0.6

    # Call the predict function with the specified parameters
    results = model.predict(
        source=source, classes=classes, conf=conf_thresh, device="cpu"
    )

    for result in results:
        boxes = result.boxes.cpu().numpy()

    index = np.argmax(boxes.data[:, -2])
    bbox = boxes.data[index][:4].astype(int)

    crop_and_save_image_with_bbox(source, output_path, bbox)


# preprocessing_raw_image_new(
#    "/home/aime/python-environments/exam_script_deploy/image_folder/image_20240406_111227.jpeg",
#    "/home/aime/python-environments/exam_script_deploy/image_folder/CROPPED_3_image_20240406_111227.jpeg",
# )
