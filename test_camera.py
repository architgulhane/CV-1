import cv2
import sys

print("Testing camera access...")
print(f"OpenCV version: {cv2.__version__}")

# Test camera access
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Cannot access camera (index 0)")
    print("Trying different camera indices...")
    
    # Try different camera indices
    for i in range(1, 5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            break
        cap.release()
    else:
        print("No camera found. Please check if:")
        print("1. Camera is connected and not being used by other applications")
        print("2. Camera permissions are granted")
        print("3. Camera drivers are installed")
        sys.exit(1)

print("Camera access successful!")
print("Press 'q' to quit the camera test")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    frame_count += 1
    cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Camera Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera test completed successfully!")
