import cv2
import numpy as np

def simple_hand_detection():
    """
    Simple hand detection using OpenCV without MediaPipe
    This is a basic implementation for demonstration
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Create background subtractor
    backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
    
    print("Hand Detection Running (OpenCV only)")
    print("Move your hand in front of the camera")
    print("Press ESC to exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
    
        fgMask = backSub.apply(frame)
        
        # Find contours
        contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and draw the largest one
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            if area > 5000:  # Minimum area threshold
                # Draw contour
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                
                # Simple finger counting based on contour area
                hull = cv2.convexHull(largest_contour)
                hull_area = cv2.contourArea(hull)
                contour_area = cv2.contourArea(largest_contour)
                
                # Rough finger estimation based on area ratio
                if hull_area > 0:
                    ratio = contour_area / hull_area
                    finger_count = int((1 - ratio) * 10)  # Simple estimation
                    finger_count = max(0, min(finger_count, 5))  # Clamp to 0-5
                else:
                    finger_count = 0
              
                cv2.putText(frame, f'Fingers (approx): {finger_count}', (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                cv2.putText(frame, 'Hand detected', (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show frames
        cv2.imshow('Hand Detection (OpenCV)', frame)
        cv2.imshow('Mask', fgMask)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    simple_hand_detection()
