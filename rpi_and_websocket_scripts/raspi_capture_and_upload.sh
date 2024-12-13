
# Define the bucket name and the directory where you want to save images
BUCKET_NAME="bucketlambdafunc"
# Create a unique folder  per client with the serial number of the device
DEVICE_ID=$(cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2)
HOME_DIR="/home/pi"
IMAGE_DIR="$HOME_DIR/$DEVICE_ID"
IMAGE_NAME="image_$(date +'%Y%m%d_%H%M%S').jpg"
IMAGE_PATH="$IMAGE_DIR/$IMAGE_NAME"
export PYTHONPATH="/home/pi/.local/lib/python3.6/site-packages"
export PATH=$PATH:/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games

# Ensure the image directory exists
# NEED TO CREATE THE APPROPRIATE OF BUCKET S3 BEFORE SHIPPING THE DEVICE
mkdir -p "$IMAGE_DIR"

# Capture the image
#libcamera-still -o "$IMAGE_PATH" --nopreview 

#libcamera-still -o "$IMAGE_PATH" --nopreview --autofocus --metering centre --shutter 100000 --gain 1.0
#libcamera-still -o "$IMAGE_PATH" --nopreview --autofocus-mode continuous --autofocus-on-capture yes --autofocus-range macro --autofocus-window 50%,50%,25%,25% --shutter 20000 --gain 1.0 --metering centre --awb auto
#libcamera-still -o "$IMAGE_PATH" --nopreview --autofocus-mode continuous --autofocus-on-capture yes --autofocus-range normal --autofocus-window 50%,50%,50%,50% --shutter 10000 --gain 1.0 --metering spot --awb cloudy

libcamera-still -o "$IMAGE_PATH" --nopreview --autofocus-mode manual --lens-position 0.5 --shutter 20000 --gain 1.5 --metering matrix --awb auto --brightness 0.1 --contrast 1.2 --saturation 1.1 --sharpness 1.5 --denoise off --quality 95

# Check if the image was successfully captured
if [ -f "$IMAGE_PATH" ]; then
    # Upload the image to S3, using the device ID as a folder
    # aws s3 cp "$IMAGE_PATH" "s3://$BUCKET_NAME/$DEVICE_ID/$IMAGE_NAME"
    aws s3 cp "$IMAGE_PATH" "s3://$BUCKET_NAME/$DEVICE_ID/$IMAGE_NAME"

    
    if [ $? -eq 0 ]; then
        echo "Image successfully uploaded to S3: $BUCKET_NAME/$DEVICE_ID/$IMAGE_NAME"
    else
        echo "Failed to upload the image to S3."
    fi
    
    # Optionally, remove the image file after upload to save space
    # rm "$IMAGE_PATH"
else
    echo "Failed to capture the image."
fi
