#! /usr/bin/python

# import the necessary packages
from picamera2 import Picamera2, MappedArray, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2.outputs import FileOutput #when detect face for 1+ seconds, grab snapshot and video to email 
from flask import Flask, Response, render_template
import socket
import time
import numpy as np
import cv2

app = Flask(__name__)

# Configuration
UDP_IP = "REMOTE_IP"  # Replace with the sender's IP
UDP_PORT = 10001  # The port the sender is using
BUFFER_SIZE = 65536  # Buffer size for UDP packets

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/security_footage')
def stream_footage():
    return Response(udp_grab_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def udp_grab_frames():
    # Set up the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))  # Bind to the specified IP and port
    
    # Set a timeout for receiving data
    #sock.settimeout(1)  # 1 second timeout

    # Create a buffer to store incoming data
    buffer = b""
    
    while True:
        try:
            # Receive data from the UDP socket
            data, addr = sock.recvfrom(BUFFER_SIZE)
            buffer += data

            # Check if we have enough data to process
            while len(buffer) > 0:
                # Assume that we know how to extract the frames from the H.264 stream
                # The following example assumes you can extract complete NAL units
                # Modify as per your stream structure
                
                # For simplicity, we are using a hypothetical function `get_h264_frame`
                frame, buffer = get_h264_frame(buffer)
                
                if frame is None:
                    # No complete frame available
                    break

                # Encode the frame to JPEG
                _, jpeg_frame = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame.tobytes() + b'\r\n')
        except socket.timeout:
            # Handle timeout - no data received within the timeout period
            yield b'--frame\r\nContent-Type: text/plain\r\n\r\nNo data received. Trying again...\r\n'
    
        except Exception as e:
            # Handle other exceptions (e.g., socket errors)
            print(f"Error: {e}")
            yield b'--frame\r\nContent-Type: text/plain\r\n\r\nError receiving data. Trying to reconnect...\r\n'

        # Optional: Add a small sleep to avoid busy-waiting
        time.sleep(0.1)  # Adjust the sleep time as needed
    

def get_h264_frame(buffer):
    # Example function to extract a complete H.264 frame from the buffer
    # This will depend on your specific H.264 stream structure
    # Here, we just simulate a frame extraction process
    
    # Check for start codes (e.g., 0x00000001) to identify frame boundaries
    start_code = b'\x00\x00\x00\x01'
    
    start = buffer.find(start_code)
    if start == -1:
        return None, buffer  # No complete frame found

    # Extract the frame (for simplicity, assume it's the whole buffer after the start code)
    frame_end = buffer.find(start_code, start + len(start_code))
    
    if frame_end == -1:
        # No more complete frames available
        return None, buffer

    frame_data = buffer[start:frame_end]
    remaining_buffer = buffer[frame_end:]  # Remaining data after the frame

    # Decode the H.264 frame into an OpenCV-compatible format
    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

    return frame, remaining_buffer


if __name__=="__main__":
    app.run(debug=True)
