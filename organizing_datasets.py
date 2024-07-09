import os
import shutil
from sklearn.model_selection import train_test_split


root_folder = "/home/aime/python-environments/exam_script_deploy/datafolder"
# Paths setup
image_dir = f"{root_folder}/images"  # Update with the correct path
label_dir = f"{root_folder}/labels"  # Update with the correct path
classes_file = f"{root_folder}/classes.txt"  # Not needed for this script but ensure it's correctly placed


# Ensure dataset directories exist
os.makedirs("dataset/train/images", exist_ok=True)
os.makedirs("dataset/train/labels", exist_ok=True)
os.makedirs("dataset/val/images", exist_ok=True)
os.makedirs("dataset/val/labels", exist_ok=True)
os.makedirs("dataset/test/images", exist_ok=True)
os.makedirs("dataset/test/labels", exist_ok=True)

# Get list of image files
images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
labels = [f.replace(".jpg", ".txt") for f in images]

# Split data
train_imgs, val_imgs, train_labels, val_labels = train_test_split(
    images, labels, test_size=0.3, random_state=42
)
val_imgs, test_imgs, val_labels, test_labels = train_test_split(
    val_imgs, val_labels, test_size=0.5, random_state=42
)


# Function to copy files
def copy_files(files, src, dest):
    for file in files:
        shutil.copy(os.path.join(src, file), os.path.join(dest, file))


# Copy files to corresponding folders
copy_files(train_imgs, image_dir, "dataset/train/images")
copy_files(train_labels, label_dir, "dataset/train/labels")
copy_files(val_imgs, image_dir, "dataset/val/images")
copy_files(val_labels, label_dir, "dataset/val/labels")
copy_files(test_imgs, image_dir, "dataset/test/images")
copy_files(test_labels, label_dir, "dataset/test/labels")
