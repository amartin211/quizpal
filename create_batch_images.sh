#!/bin/bash

# Directory containing the images
dir="/home/aime/python-environments/exam_script_deploy/cropped_exam_photos"

# Name of the master folder
master_folder="master_folder"

# Change to the directory with images
cd "$dir"

# Create the master folder if it doesn't exist
if [ ! -d "$master_folder" ]; then
    mkdir "$master_folder"
fi

# Batch size: number of images per folder
batch_size=80

# Counter for creating unique subfolder names
folder_count=1

# Create an array of all jpg files
files=($(ls *.jpg))

# Total number of files
total_files=${#files[@]}

# Loop through all files and move them into subfolders
for (( i=0; i<${total_files}; i++ )); do
    # Folder to move current batch of images
    target_folder="$master_folder/task_$folder_count"

    # Create folder if it doesn't exist
    if [ ! -d "$target_folder" ]; then
        mkdir "$target_folder"
    fi

    # Move image to the appropriate subfolder
    mv "${files[$i]}" "$target_folder"

    # Increment folder count every batch_size files
    if (( (i + 1) % batch_size == 0 )); then
        folder_count=$((folder_count + 1))
    fi
done
