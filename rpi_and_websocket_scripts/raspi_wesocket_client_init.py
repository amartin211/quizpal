import asyncio
import socket
import time
import websockets
import uuid
import json
import signal
import sys
import logging
from gpiozero import PWMOutputDevice, LED, Button
from signal import pause
import subprocess

motor = PWMOutputDevice(21)
orange_led = LED(17)  # Orange LED for Internet Connectivity
green_led = LED(27)  # Green LED for WebSocket Connection
red_led = LED(22)  # Red LED for Power Status
button = Button(14)  # Button connected to GPIO pin 14

loop = None
button_timeout_task = None
button_cnt = 0

# Define the script path
capture_script_path = "/home/pi/capture_and_upload.sh"
switch_aphost_script_path = "/home/pi/scripts/switch_aphost.sh"

logging.basicConfig(filename="/home/pi/websocket_client.log", level=logging.DEBUG)


def signal_handler(signum, frame):
    print("Shutting down gracefully...")
    # ws.close()  # Close WebSocket connection gracefully
    orange_led.off()
    green_led.off()
    red_led.off()
    sys.exit(0)


# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


async def switch_aphost():
    logging.info("Calling script")
    cmd = " ".join(["sudo /bin/bash", switch_aphost_script_path, " > /home/pi/test.log 2>&1"])
    logging.info(cmd)
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )  # Execute the script

    stdout, stderr = await proc.communicate()
    logging.info(stdout)
    logging.info(stderr)


# Define the function to capture and upload
async def capture_and_upload():
    red_led.blink(on_time=0.5, off_time=0.5, n=1, background=False)  # Signal capture
    proc = await asyncio.create_subprocess_shell(
        " ".join(["/bin/bash", capture_script_path, " > /home/pi/test.log 2>&1 &"]),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )  # Execute the script

    stdout, stderr = await proc.communicate()
    # print(stdout.decode())
    # print(stderr.decode())
    # Update the green LED based on internet connection
    if await check_internet():
        orange_led.on()
    else:
        orange_led.off()


async def check_internet(host="8.8.8.8", port=53, timeout=3, retries=3, delay=5):
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


def on_error(ws, error):
    logging.info(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    green_led.off()
    logging.info("Closed")


def get_device_id():
    # Path to the CPU information
    cpuinfo_path = "/proc/cpuinfo"
    serial_number = None

    try:
        with open(cpuinfo_path, "r") as cpuinfo_file:
            # Iterate over each line in the cpuinfo file
            for line in cpuinfo_file:
                # Look for the line that starts with 'Serial'
                if line.startswith("Serial"):
                    # Extract the serial number (it's the last element of the line when split by ':')
                    serial_number = line.strip().split(": ")[1]
                    break
    except FileNotFoundError:
        print("The system does not support /proc/cpuinfo, or the file does not exist.")

    return serial_number


async def vibrate_on_message(message):
    """Vibrate based on the message."""
    vibration_mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "None": 0}
    count = vibration_mapping.get(message, 0)
    if count > 0:
        for _ in range(count):
            motor.value = 0.5  # Motor on (full speed)
            await asyncio.sleep(0.5)  # Duration of vibration
            motor.value = 0.0  # Motor off
            await asyncio.sleep(0.5)  # Pause between vibrations
    else:
        # Specific pattern for 'None' message (customize as needed)
        for _ in range(3):  # For instance, a quick triple pulse
            motor.value = 0.5
            await asyncio.sleep(0.1)
            motor.value = 0.0
            await asyncio.sleep(0.1)


async def wsrun(uri, client_id):
    async for ws in websockets.connect(uri):
        try:
            green_led.on()
            # mac = get_device_id() # here
            # client_id = mac  # Or us

            # Send registration message to server
            register_msg = json.dumps({"action": "register", "client_id": client_id})
            await ws.send(register_msg)
            logging.info(f"Registration message sent: {register_msg}, and client_id: {client_id}")

            while True:
                message = await ws.recv()
                logging.info(f"Received: {message}")
                data = json.loads(message)
                received_message = data.get("message")  # assuming 'message' key contains the A, B, C, D, E, or None
                logging.info(received_message)
                await vibrate_on_message(received_message)
            logging.info(f"Connection closed")
        except websockets.ConnectionClosed:
            continue


async def wait_for_button_timeout():
    global button_cnt

    await asyncio.sleep(0.5)

    logging.info(button_cnt)

    if button_cnt == 1:
        logging.info("call script here")
        await capture_and_upload()
    elif button_cnt >= 5:
        logging.info("Switch to AP Mode here")
        await switch_aphost()

    button_cnt = 0
    button_timeout_task = None


async def handle_button_press():
    global button_timeout_task
    global button_cnt
    try:
        button_cnt = button_cnt + 1

        if button_timeout_task is not None:
            button_timeout_task.cancel()
        loop = asyncio.get_event_loop()
        button_timeout_task = loop.create_task(wait_for_button_timeout())
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logging.info(e)


def done_cb(task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logging.exception(e)


def create_task():
    global loop
    try:
        task = loop.create_task(handle_button_press())
        task.add_done_callback(done_cb)
        loop.call_soon_threadsafe(task)
    except Exception as e:
        logging.debug(e)


async def register_cb():
    button.when_pressed = create_task


def main(client_id):
    global ws
    global loop

    loop = asyncio.get_event_loop()

    # Assign the function to button press event
    # button.when_pressed = l
    logging.info("Delaying initial internet connectivity check for 30 seconds...")
    # time.sleep(5)

    # while not check_internet():
    #     print("No internet connectivity. Retrying in 5 seconds...")
    #     time.sleep(5)
    # if not check_internet():
    #     orange_led.off()
    #     print("No internet connectivity, switching to AP mode.")
    #     switch_to_ap_mode()
    #     subprocess.call(["python", "/home/pi/app.py"])
    # else:
    #     orange_led.on()

    # websocket.enableTrace(True)
    # mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
    # mac = get_device_id()
    # client_id = mac  # Or use another method to ensure uniqueness
    ws_url = f"wss://ypvy1ycxbh.execute-api.eu-north-1.amazonaws.com/production?client_id={client_id}"
    loop.create_task(wsrun(ws_url, client_id))
    loop.create_task(register_cb())
    # loop.run_until_complete(wsrun(ws_url))
    loop.run_forever()


if __name__ == "__main__":
    client_id = get_device_id()
    main(client_id)
