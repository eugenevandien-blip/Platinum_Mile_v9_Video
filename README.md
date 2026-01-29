# Platinum_Mile_v9_Video

DFT Froth Speed Detection System - Video Mode

## Overview

This repository contains the `DFT_FrothSpeedNG_laser_v9_Video.py` script, which is configured to process video input instead of live camera feed for froth speed detection using laser line analysis.

## Features

- **Video File Input**: Uses `/home/pi/Videos/Platinum Mile -1.mp4` instead of camera
- **Continuous Looping**: Video loops automatically for continuous testing
- **Froth Speed Detection**: Analyzes froth movement using laser line detection
- **Real-time Visualization**: Displays processed frames with detection overlay
- **Performance Metrics**: Tracks and displays processing statistics

## Configuration

The script is pre-configured with the following settings:

- **Video Path**: `/home/pi/Videos/Platinum Mile -1.mp4`
- **Loop Mode**: Enabled (video loops continuously)
- **Display Window**: Enabled
- **Laser Line Position**: Y-coordinate 240 (configurable)
- **ROI Height**: 50 pixels around laser line

## Usage

### Running the Script

```bash
python3 DFT_FrothSpeedNG_laser_v9_Video.py
```

### Controls

- Press `q` to quit the application
- Press `Ctrl+C` to interrupt processing

### Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```

## How It Works

1. **Video Loading**: Opens the specified video file
2. **Frame Processing**: Each frame is analyzed for froth movement
3. **Laser Line Detection**: Uses edge detection and Hough transform
4. **Speed Calculation**: Calculates froth speed based on detected features
5. **Visualization**: Displays processed frames with overlays
6. **Looping**: Automatically restarts video when it ends

## Modifications from Camera Version

The script has been modified to:
- Use video file input instead of camera (line 13: `VIDEO_PATH`)
- Enable automatic video looping (line 17: `LOOP_VIDEO = True`)
- Handle end-of-video by resetting to frame 0 (lines 158-167)
- Maintain all original froth detection functionality

## Output

The script displays:
- Current frame number and timestamp
- Detected laser line (green)
- Region of interest (blue rectangle)
- Detected lines/features (red)
- Calculated speed (pixels per second)
- Processing statistics (FPS, frame count)
