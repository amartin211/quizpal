#!/usr/bin/env python3

import asyncio
import time
import websockets
import json
import signal
import sys
import logging
from gpiozero import PWMOutputDevice, LED, Button
import os
from datetime import datetime
import uuid
import socket  # Added import for socket module

# Hardware setup
motor = PWMOutputDevice(21)
orange_led = LED(17)  # Orange LED for Internet Connectivity
green_led = LED(27)  # Green LED for WebSocket Connection
red_led = LED(22)  # Red LED for Power Status
button = Button(14)  # Button connected to GPIO pin 14

# Global variables and state
BUCKET_NAME = "bucketlambdafunc"
LONG_PRESS_THRESHOLD = 3.0  # Threshold for long press in seconds
SHORT_PRESS_THRESHOLD = 0.5  # Threshold for very short press in seconds
AP_MODE_PRESS_COUNT = 5  # Number of presses required to switch to AP mode
AP_MODE_PRESS_INTERVAL = 0.5  # Max interval between presses in seconds
capture_interval = 0.5  # Time between captures in seconds
capture_script_path = "/home/pi/capture_and_upload.sh"
switch_aphost_script_path = "/home/pi/scripts/switch_aphost.sh"


class State:
    def __init__(self):
        self.capturing_images = False
        self.button_press_time = 0
        self.processing = False
        self.session_id = None
        self.press_duration = 0
        self.button_count = 0
        self.button_timeout_task = None
        self.capturing_task = None  # Keep track of the capturing task
        self.long_press_task = None  # Task to check for long press


state = State()

DEVICE_ID = None
IMAGE_DIR = None
captured_images = []


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create handlers
    file_handler = logging.FileHandler("/home/pi/websocket_client.log")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


setup_logging()
logger = logging.getLogger()


def get_device_id():
    """Get the Raspberry Pi's serial number from /proc/cpuinfo"""
    cpuinfo_path = "/proc/cpuinfo"
    serial_number = None

    try:
        with open(cpuinfo_path, "r") as cpuinfo_file:
            for line in cpuinfo_file:
                if line.startswith("Serial"):
                    serial_number = line.strip().split(": ")[1]
                    break
    except FileNotFoundError:
        logger.error("Could not find /proc/cpuinfo")
        return "unknown"

    return serial_number


def initialize_directories():
    """Initialize global variables and create necessary directories"""
    global DEVICE_ID, IMAGE_DIR
    DEVICE_ID = get_device_id()
    IMAGE_DIR = os.path.join("/home/pi/images", DEVICE_ID)
    os.makedirs(IMAGE_DIR, exist_ok=True)
    logger.info(f"Initialized directories. Image directory: {IMAGE_DIR}")


async def wsrun(uri, client_id):
    """Handle WebSocket connection with reconnection logic and heartbeats."""
    backoff = 1  # Initial backoff interval in seconds
    max_backoff = 32  # Maximum backoff interval
    while True:
        try:
            async with websockets.connect(
                uri,
                ping_interval=20,  # Send a ping every 20 seconds
                ping_timeout=20,  # Wait 20 seconds for a pong before closing
                close_timeout=5,  # Wait 5 seconds for the connection to close
            ) as ws:
                green_led.on()
                # Generate a unique connection ID for this session
                connection_id = str(uuid.uuid4())
                register_msg = json.dumps(
                    {"action": "register", "client_id": client_id, "connection_id": connection_id}
                )
                await ws.send(register_msg)
                logger.info(f"Registration message sent: {register_msg}")

                # Reset backoff on successful connection
                backoff = 1

                # Store the WebSocket for graceful shutdown
                state.websocket = ws

                while True:
                    message = await ws.recv()
                    logger.info(f"Received message: {message}")
                    data = json.loads(message)
                    received_message = data.get("message")
                    logger.info(f"Received command: {received_message}")
                    await vibrate_on_message(received_message)
        except websockets.ConnectionClosedError as e:
            logger.warning(f"WebSocket connection closed with error: {e}, reconnecting...")
            green_led.off()
        except websockets.InvalidStatusCode as e:
            logger.error(f"WebSocket connection failed with status code: {e.status_code}")
            green_led.off()
        except Exception as e:
            logger.error(f"Unexpected WebSocket error: {e}")
            green_led.off()
        finally:
            # Exponential backoff before reconnecting
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)
            logger.info(f"Reconnecting in {backoff} seconds...")


async def vibrate_on_message(message):
    """Vibrate based on the message."""
    if message == "None":
        # Error vibration pattern: Quick triple pulse
        logger.info("Starting error vibration pattern for 'None'")
        for _ in range(3):
            motor.value = 0.2
            await asyncio.sleep(0.1)  # Short vibration
            motor.value = 0.0
            await asyncio.sleep(0.1)
        logger.info("Error vibration pattern completed")
    elif message == "X":
        # Validation vibration pattern: Three long vibrations
        logger.info("Starting validation vibration pattern for 'X'")
        for _ in range(3):
            motor.value = 0.2  # Motor on
            await asyncio.sleep(1.0)  # Long vibration duration
            motor.value = 0.0  # Motor off
            await asyncio.sleep(0.2)  # Short pause between vibrations
        logger.info("Validation vibration pattern completed")
    elif message in ["A", "B", "C", "D", "E", "F"]:
        # Vibration mapping for letters A-F
        vibration_mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
        count = vibration_mapping.get(message, 0)
        if count > 0:
            logger.info(f"Starting vibration pattern for message '{message}'")
            for _ in range(count):
                motor.value = 0.2  # Motor on
                await asyncio.sleep(0.5)  # Short vibration duration
                motor.value = 0.0  # Motor off
                await asyncio.sleep(0.5)  # Pause between vibrations
            logger.info(f"Vibration pattern for message '{message}' completed")
    else:
        # Unknown message: Single short vibration
        logger.warning(f"Unknown message '{message}', performing default vibration pattern")
        motor.value = 0.2
        await asyncio.sleep(0.2)
        motor.value = 0.0


def handle_button_press():
    """Handle initial button press"""
    if state.processing:
        logger.info("Ignoring button press - still processing previous capture")
        return

    state.button_press_time = time.monotonic()
    red_led.on()
    logger.info("Button pressed")

    # Start a task to check for long press
    state.long_press_task = loop.create_task(check_for_long_press())


async def check_for_long_press():
    await asyncio.sleep(LONG_PRESS_THRESHOLD)
    if button.is_pressed:
        # Start capturing images
        state.capturing_images = True
        state.processing = True
        state.session_id = str(uuid.uuid4())
        captured_images.clear()
        state.capturing_task = loop.create_task(capture_images())
        logger.info("Long press detected - started capturing images")


def handle_button_release():
    """Handle button release and determine press type"""
    red_led.off()
    state.press_duration = time.monotonic() - state.button_press_time
    logger.info(f"Button released after {state.press_duration} seconds")

    # Cancel the long press task if it's still pending
    if state.long_press_task:
        state.long_press_task.cancel()
        state.long_press_task = None

    if state.capturing_task:
        # Long press was in progress, stop capturing
        state.capturing_images = False
        logger.info("Stopped capturing images due to button release")
    else:
        # Short press
        if state.press_duration < SHORT_PRESS_THRESHOLD:
            # Very short press, count towards AP mode switch
            state.button_count += 1
            logger.info(f"Very short press detected. Button count: {state.button_count}")

            # Cancel existing timeout task if any
            if state.button_timeout_task:
                state.button_timeout_task.cancel()

            # Start or reset the timeout task
            state.button_timeout_task = loop.create_task(wait_for_button_timeout())
        elif state.press_duration < LONG_PRESS_THRESHOLD:
            # Normal short press, capture single image
            logger.info("Short press detected")
            if not state.processing:
                state.processing = True
                state.session_id = str(uuid.uuid4())
                loop.create_task(capture_single_image())
            else:
                logger.info("Ignoring button press - still processing previous capture")


async def wait_for_button_timeout():
    await asyncio.sleep(AP_MODE_PRESS_INTERVAL)  # Wait for 0.5 seconds of inactivity

    if state.button_count >= AP_MODE_PRESS_COUNT:
        logger.info("Five very short presses detected - switching to AP mode")
        await switch_aphost()
    else:
        logger.info(f"{state.button_count} very short presses detected - no action")

    # Reset the button count and timeout task
    state.button_count = 0
    state.button_timeout_task = None


async def capture_images():
    """Capture images continuously while button is pressed"""
    try:
        while state.capturing_images:
            await capture_image()
            await asyncio.sleep(capture_interval)
    finally:
        # After capturing is done, process the images
        await process_after_capture(long_press=True)
        state.processing = False
        state.capturing_task = None


async def capture_single_image():
    """Capture a single image for short press"""
    try:
        captured_images.clear()
        await capture_image()
        await process_after_capture(long_press=False)
    finally:
        state.processing = False


async def capture_image():
    """Capture a single image"""
    try:
        image_name = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        logger.info(f"Capturing image: {image_name}")

        cmd = f"/bin/bash {capture_script_path} {image_name}"
        env = os.environ.copy()
        # Set the PATH to include directories where commands may be located
        env["PATH"] = env.get("PATH", "") + ":/home/pi/.local/bin:/usr/local/bin:/usr/bin"

        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        )

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30.0)
            if proc.returncode == 0:
                captured_images.append(image_name)
                logger.info(f"Successfully captured image: {image_name}")
            else:
                logger.error(f"Failed to capture image: {stderr.decode().strip()}")
        except asyncio.TimeoutError:
            logger.error("Image capture timed out after 30 seconds")
            proc.kill()
            await proc.wait()  # Ensure the process has terminated
    except Exception as e:
        logger.error(f"Error capturing image: {e}")


async def process_after_capture(long_press):
    """Process captured images after capture is complete"""
    try:
        if not captured_images:
            logger.info("No images captured after waiting")
            return

        logger.info(f"Processing {len(captured_images)} captured images")

        if not long_press:
            logger.info("Short press detected - single image mode")
            # Only process first image for short press
            image_name = captured_images[0]
            s3_key = f"{DEVICE_ID}/{image_name}"
            await upload_single_image(image_name, s3_key)
        else:
            logger.info("Long press detected - session mode")
            await create_session_folder()
    except Exception as e:
        logger.error(f"Error in process_after_capture: {e}")


async def create_session_folder():
    """Create a session folder and manifest file for a long press session"""
    try:
        # Create manifest content with session details
        manifest_content = {
            "session_id": state.session_id,
            "device_id": DEVICE_ID,
            "timestamp": datetime.now().isoformat(),
            "image_count": len(captured_images),
            "images": captured_images,
        }

        # Create and upload manifest file
        manifest_name = "manifest.json"
        manifest_path = os.path.join(IMAGE_DIR, manifest_name)
        with open(manifest_path, "w") as f:
            json.dump(manifest_content, f, indent=2)

        logger.info(f"Created manifest file with {len(captured_images)} images")

        # Upload manifest file
        s3_key = f"{DEVICE_ID}/{state.session_id}/{manifest_name}"
        await upload_file(manifest_path, s3_key)

        # Upload all images in the session
        for image_name in captured_images:
            s3_key = f"{DEVICE_ID}/{state.session_id}/{image_name}"
            await upload_single_image(image_name, s3_key)

        # Clean up manifest file
        os.remove(manifest_path)
        logger.info("Removed local manifest file")

    except Exception as e:
        logger.error(f"Error creating session folder: {e}")


async def upload_single_image(image_name, s3_key):
    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.isfile(image_path):
        logger.error(f"Image file does not exist: {image_path}")
        return False

    return await upload_file(image_path, s3_key, image_name)


async def upload_file(file_path, s3_key, file_name=None):
    """Helper function to upload a file to S3 using AWS CLI"""
    if file_name is None:
        file_name = os.path.basename(file_path)

    try:
        # Try possible aws cli locations
        aws_paths = ["/home/pi/.local/bin/aws", "/usr/local/bin/aws", "/usr/bin/aws"]
        aws_cmd = next((path for path in aws_paths if os.path.exists(path)), None)

        if aws_cmd is None:
            logger.error("AWS CLI not found in expected paths")
            return False

        cmd = f"{aws_cmd} s3 cp {file_path} s3://{BUCKET_NAME}/{s3_key}"
        logger.info(f"Uploading file with command: {cmd}")

        env = os.environ.copy()
        # Set the PATH to include directories where commands may be located
        env["PATH"] = env.get("PATH", "") + ":/home/pi/.local/bin:/usr/local/bin:/usr/bin"

        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode == 0:
            logger.info(f"Uploaded {file_name} to s3://{BUCKET_NAME}/{s3_key}")
            try:
                os.remove(file_path)
                logger.info(f"Removed local file: {file_name}")
                return True
            except FileNotFoundError:
                logger.error(f"Failed to remove file: {file_path}")
        else:
            logger.error(f"Failed to upload file: {file_name}")
            logger.error(f"AWS CLI stderr: {stderr.decode().strip()}")
        return False
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return False


async def switch_aphost():
    logger.info("Switching to AP mode")
    cmd = f"sudo /bin/bash {switch_aphost_script_path} > /home/pi/test.log 2>&1"
    logger.info(f"Executing command: {cmd}")
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    logger.info(f"Switch AP stdout: {stdout.decode()}")
    logger.info(f"Switch AP stderr: {stderr.decode()}")


async def check_internet(host="8.8.8.8", port=53, timeout=3, retries=3, delay=5):
    """Check for internet connectivity by trying to connect to a known host"""
    for i in range(retries):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True  # Internet connectivity confirmed
        except Exception as ex:
            if i < retries - 1:  # Wait and retry if not the last attempt
                await asyncio.sleep(delay)
            else:
                return False  # Return False only after all retries failed


async def internet_monitor():
    """Periodically check internet connectivity and update orange LED"""
    while True:
        connected = await check_internet()
        if connected:
            orange_led.on()
            logger.info("Internet connected - orange LED ON")
        else:
            orange_led.off()
            logger.info("Internet disconnected - orange LED OFF")
        await asyncio.sleep(10)  # Check every 10 seconds


def signal_handler(signum, frame):
    """Handle graceful shutdown."""
    logger.info("Shutting down gracefully...")
    orange_led.off()
    green_led.off()
    red_led.off()
    # Attempt to close the WebSocket connection gracefully
    if state.websocket and not state.websocket.closed:
        asyncio.create_task(state.websocket.close())
        logger.info("WebSocket connection closed.")
    sys.exit(0)


# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    global loop
    loop = asyncio.get_event_loop()

    # Initialize directories
    initialize_directories()
    logger.info("Starting main loop")

    # Set up button handlers
    button.when_pressed = handle_button_press
    button.when_released = handle_button_release

    # WebSocket connection
    client_id = DEVICE_ID
    ws_url = f"wss://ypvy1ycxbh.execute-api.eu-north-1.amazonaws.com/production?client_id={client_id}"
    loop.create_task(wsrun(ws_url, client_id))

    # Start internet connectivity monitor
    loop.create_task(internet_monitor())

    # Run the event loop
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Exiting...")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
