#!/usr/bin/env python3
"""
DFT Froth Speed Next Generation - Laser Version 9 - Video
This script processes video input to measure froth speed using laser detection.
"""

import cv2
import numpy as np
import time
from datetime import datetime

# Configuration
VIDEO_PATH = '/home/pi/Videos/Platinum Mile -1.mp4'
CAMERA_INDEX = 0  # Default camera index (not used when VIDEO_PATH is set)
DISPLAY_WINDOW = True
FRAME_DELAY = 30  # milliseconds between frames
LOOP_VIDEO = True  # Loop video continuously

# Processing parameters
LASER_LINE_Y = 240  # Y-coordinate of laser line
ROI_HEIGHT = 50  # Region of interest height around laser line
SPEED_CALCULATION_FRAMES = 30  # Number of frames to calculate speed over


class FrothSpeedDetector:
    """Detects and measures froth speed from video input."""
    
    def __init__(self, video_source=VIDEO_PATH, loop=LOOP_VIDEO):
        """
        Initialize the froth speed detector.
        
        Args:
            video_source: Path to video file or camera index
            loop: Whether to loop the video continuously
        """
        self.video_source = video_source
        self.loop_video = loop
        self.cap = None
        self.frame_count = 0
        self.start_time = time.time()
        self.speeds = []
        
    def initialize_video_capture(self):
        """Initialize video capture from file or camera."""
        if isinstance(self.video_source, str):
            # Video file
            self.cap = cv2.VideoCapture(self.video_source)
            if not self.cap.isOpened():
                raise IOError(f"Cannot open video file: {self.video_source}")
            print(f"Video file opened: {self.video_source}")
            
            # Get video properties
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"Video properties: {width}x{height} @ {fps}fps, {frame_count} frames")
        else:
            # Camera
            self.cap = cv2.VideoCapture(self.video_source)
            if not self.cap.isOpened():
                raise IOError(f"Cannot open camera: {self.video_source}")
            print(f"Camera opened: {self.video_source}")
    
    def process_frame(self, frame):
        """
        Process a single frame to detect froth speed.
        
        Args:
            frame: Input frame from video
            
        Returns:
            Processed frame with visualizations
        """
        if frame is None:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Define ROI around laser line
        height, width = gray.shape
        roi_y_start = max(0, LASER_LINE_Y - ROI_HEIGHT // 2)
        roi_y_end = min(height, LASER_LINE_Y + ROI_HEIGHT // 2)
        roi = gray[roi_y_start:roi_y_end, :]
        
        # Apply edge detection in ROI
        edges = cv2.Canny(roi, 50, 150)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
        
        # Draw laser line position
        cv2.line(frame, (0, LASER_LINE_Y), (width, LASER_LINE_Y), (0, 255, 0), 2)
        
        # Draw ROI rectangle
        cv2.rectangle(frame, (0, roi_y_start), (width, roi_y_end), (255, 0, 0), 2)
        
        # Draw detected lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Adjust coordinates to full frame
                cv2.line(frame, (x1, y1 + roi_y_start), (x2, y2 + roi_y_start), (0, 0, 255), 2)
        
        # Calculate and display speed (placeholder calculation)
        speed = self.calculate_speed(lines)
        if speed is not None:
            self.speeds.append(speed)
            if len(self.speeds) > SPEED_CALCULATION_FRAMES:
                self.speeds.pop(0)
            avg_speed = np.mean(self.speeds)
            cv2.putText(frame, f"Speed: {avg_speed:.2f} px/s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Display frame count and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"Frame: {self.frame_count} | {timestamp}", (10, height - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def calculate_speed(self, lines):
        """
        Calculate froth speed based on detected lines.
        
        Args:
            lines: Detected lines from Hough transform
            
        Returns:
            Calculated speed or None
        """
        if lines is None or len(lines) == 0:
            return None
        
        # Simple speed calculation based on line positions
        # This is a placeholder - actual implementation would track features across frames
        total_length = 0
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_length += length
        
        # Return average line length as a proxy for speed
        return total_length / len(lines)
    
    def run(self):
        """Main processing loop."""
        self.initialize_video_capture()
        
        print("Processing started. Press 'q' to quit.")
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                # Handle end of video file
                if not ret:
                    if self.loop_video and isinstance(self.video_source, str):
                        # Loop the video by resetting to beginning
                        print("End of video reached. Looping...")
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    else:
                        # End of video/camera stream
                        print("End of video stream.")
                        break
                
                self.frame_count += 1
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                if processed_frame is not None and DISPLAY_WINDOW:
                    # Display the result
                    cv2.imshow('Froth Speed Detection', processed_frame)
                    
                    # Wait for key press
                    key = cv2.waitKey(FRAME_DELAY) & 0xFF
                    if key == ord('q'):
                        print("Quit requested by user.")
                        break
                
                # Print progress every 100 frames
                if self.frame_count % 100 == 0:
                    elapsed = time.time() - self.start_time
                    fps = self.frame_count / elapsed
                    print(f"Processed {self.frame_count} frames at {fps:.2f} fps")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Release resources."""
        if self.cap is not None:
            self.cap.release()
        if DISPLAY_WINDOW:
            cv2.destroyAllWindows()
        
        # Print final statistics
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            fps = self.frame_count / elapsed
            print(f"\nProcessing complete:")
            print(f"  Total frames: {self.frame_count}")
            print(f"  Total time: {elapsed:.2f}s")
            print(f"  Average FPS: {fps:.2f}")
            if self.speeds:
                print(f"  Average speed: {np.mean(self.speeds):.2f} px/s")


def main():
    """Main entry point."""
    print("=" * 60)
    print("DFT Froth Speed NG - Laser v9 - Video Mode")
    print("=" * 60)
    print(f"Video source: {VIDEO_PATH}")
    print(f"Loop enabled: {LOOP_VIDEO}")
    print("=" * 60)
    
    try:
        detector = FrothSpeedDetector(video_source=VIDEO_PATH, loop=LOOP_VIDEO)
        detector.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
