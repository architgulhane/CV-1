import mediapipe as mp
import cv2

print("Testing MediaPipe...")
print(f"MediaPipe version: {mp.__version__}")

# Test MediaPipe Hands initialization
try:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils
    print("MediaPipe Hands initialized successfully!")
    
    cap = cv2.VideoCapture(0)
    print("Starting MediaPipe hand detection test...")
    print("Show your hand to the camera. Press 'q' to quit.")
    
    frame_count = 0
    detection_count = 0
    
    while True:
        success, image = cap.read()
        if not success:
            print("Failed to read from camera")
            break
            
        frame_count += 1
        
        # Process the image
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        # Draw results
        if results.multi_hand_landmarks:
            detection_count += 1
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(image, f'Hand Detected! Count: {detection_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(image, 'No hand detected', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.putText(image, f'Frame: {frame_count}', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.imshow('MediaPipe Test', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"Test completed. Detected hands in {detection_count}/{frame_count} frames")
    
except Exception as e:
    print(f"Error initializing MediaPipe: {e}")
    import traceback
    traceback.print_exc()
