# Quick Start Guide

## Running the Script

```bash
python3 DFT_FrothSpeedNG_laser_v9_Video.py
```

## Requirements

```bash
pip install opencv-python numpy
```

## What It Does

The script:
1. Loads video from `/home/pi/Videos/Platinum Mile -1.mp4`
2. Processes each frame to detect froth speed using laser line analysis
3. Displays real-time visualization with overlays
4. Loops the video continuously when it ends
5. Shows performance metrics

## Controls

- **q** - Quit the application
- **Ctrl+C** - Force interrupt

## Expected Output

```
============================================================
DFT Froth Speed NG - Laser v9 - Video Mode
============================================================
Video source: /home/pi/Videos/Platinum Mile -1.mp4
Loop enabled: True
============================================================
Video file opened: /home/pi/Videos/Platinum Mile -1.mp4
Video properties: 1920x1080 @ 30fps, 1500 frames
Processing started. Press 'q' to quit.
```

## Visualization

The display window shows:
- **Green line** - Laser line position (Y=240)
- **Blue rectangle** - Region of interest
- **Red lines** - Detected froth features
- **White text** - Speed, frame count, timestamp

## Looping Behavior

When the video reaches the end:
```
End of video reached. Looping...
```
The video automatically restarts from frame 0 and continues processing indefinitely.

## Configuration (in script)

Edit these variables to customize:

```python
VIDEO_PATH = '/home/pi/Videos/Platinum Mile -1.mp4'  # Video file path
LOOP_VIDEO = True                                     # Enable looping
DISPLAY_WINDOW = True                                 # Show window
FRAME_DELAY = 30                                      # ms between frames
LASER_LINE_Y = 240                                    # Laser Y position
ROI_HEIGHT = 50                                       # ROI height in pixels
```

## Troubleshooting

**Video file not found:**
```
IOError: Cannot open video file: /home/pi/Videos/Platinum Mile -1.mp4
```
→ Ensure the video file exists at the specified path

**No display window:**
→ Set `DISPLAY_WINDOW = True` in the script
→ Ensure X11 forwarding is enabled if running remotely

**Import errors:**
```
ImportError: No module named 'cv2'
```
→ Install OpenCV: `pip install opencv-python`

## Performance Tips

- Adjust `FRAME_DELAY` for faster/slower processing
- Set `DISPLAY_WINDOW = False` for headless mode (faster)
- Reduce `ROI_HEIGHT` for faster edge detection

## Validation

To verify the script is configured correctly:

```bash
python3 validate_script.py
```

Expected output:
```
============================================================
✓ All validations PASSED
============================================================
```
