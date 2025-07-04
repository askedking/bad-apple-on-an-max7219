import cv2
import serial
import time
from ffpyplayer.player import MediaPlayer

# --- Configuration ---
VIDEO_PATH = "c:/Users/colli/Downloads/Touhou-BadApple.mp4"
SERIAL_PORT = 'COM7'
BAUD_RATE = 9600
MATRIX_SIZE = 8
FRAME_DELAY = 0.01

# --- Initialize Serial Connection ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Failed to connect to serial port: {e}")
    exit()

# --- Load Video and Audio ---
cap = cv2.VideoCapture(VIDEO_PATH)
player = MediaPlayer(VIDEO_PATH)

if not cap.isOpened():
    print("Error: Couldn't open video.")
    ser.close()
    exit()

print("Streaming video + audio to Arduino... Press 'q' to quit.")


start_time = time.time()  # Place this before the loop starts

# --- Main Loop ---
try:
    while cap.isOpened():
        
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()  # ffpyplayer handles audio internally
        import time

        # Inside your while loop, after reading the frame:
        play_time = cap.get(cv2.CAP_PROP_POS_MSEC)  # Video timestamp in milliseconds
        elapsed = (time.time() - start_time) * 1000  # Elapsed real time in milliseconds
        delay = max(1, int(play_time - elapsed))  # How much to wait to sync

        cv2.waitKey(delay)

        if not ret:
            break

        # Display original video
        original_display = cv2.resize(frame, (480, 360))
        cv2.imshow("Original Video", original_display)

        # Process for matrix
        small_frame = cv2.resize(frame, (MATRIX_SIZE, MATRIX_SIZE))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 127, 1, cv2.THRESH_BINARY)
        preview = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("8x8 Matrix Preview", preview)

        for row in binary:
            byte = 0
            for bit in row:
                byte = (byte << 1) | bit
            ser.write(bytes([byte]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Optional: Respect audio/video sync delay if provided
        if val == 'eof':
            break

except KeyboardInterrupt:
    print("\nStopped manually.")

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()
ser.close()
print("Video complete. Serial connection closed.")
