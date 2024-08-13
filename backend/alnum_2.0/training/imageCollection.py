import cv2
import os
import time
import uuid

images_path = os.path.join('collectedimages')
labels = ['3', '4', '5']
number_imgs = 15

# Define the ROI coordinates (x, y, width, height)
roi_x, roi_y, roi_w, roi_h = 100, 100, 300, 300

for label in labels:
    # Create directory for the label if it does not exist
    label_path = os.path.join(images_path, label)
    os.makedirs(label_path, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    print('Collecting images for {}'.format(label))
    time.sleep(5)  # Give time for the camera to warm up

    recording = False  # Initial state of recording
    imgnum = 0  # Initialize image number
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Draw the ROI on the frame
        roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)

        if recording:
            if imgnum < number_imgs:
                imgname = os.path.join(label_path, f'{label}_{uuid.uuid1()}.jpg')
                cv2.imwrite(imgname, roi_frame)
                imgnum += 1
                print(f'Saving image {imgnum}/{number_imgs}')
                time.sleep(2)  # Adjust delay as needed
            else:
                print(f'Finished collecting images for {label}')
                break

        # Display the frame with ROI
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF

        # Toggle recording state with 'q'
        if key == ord('q'):
            recording = not recording
            print(f'Recording {"started" if recording else "paused"}')

        # Exit the loop if 'esc' is pressed
        if key == 27:  # ESC key
            break
    
    cap.release()
    cv2.destroyAllWindows()  # Close all OpenCV windows after capturing
