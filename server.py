import socket
import cv2
import base64
import threading
import imutils
import numpy as np
from datetime import datetime

RHOST = '127.0.0.1'
RPORT = 4444
ADDRESS = (RHOST, RPORT)

WIDTH = 400
BUF_SIZE = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUF_SIZE)
sock.bind(ADDRESS)
print(f"Listening at {RHOST}:{RPORT}")

capture = cv2.VideoCapture(0)    # Change any video to transmit

def transmit(addr):
    print(f"Transmitting to {addr[0]}:{addr[1]}")
    while True:
        _, captured = capture.read()
        frame = cv2.resize(captured, (WIDTH, WIDTH))
        frame = cv2.flip(frame, 1)
        frame = cv2.putText(frame, str(datetime.now()), (15, 15), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        encoded_frame = base64.b64encode(buffer)
        sock.sendto(encoded_frame, addr)

while True:
    _, addr = sock.recvfrom(BUF_SIZE)
    print(f"Connected from {addr[0]}:{addr[1]}")
    t = threading.Thread(target=transmit, args=(addr,))
    t.start()