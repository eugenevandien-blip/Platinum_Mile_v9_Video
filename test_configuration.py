#!/usr/bin/env python3
"""
Test script to validate DFT_FrothSpeedNG_laser_v9_Video.py configuration
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    try:
        import DFT_FrothSpeedNG_laser_v9_Video as froth_module
        print("✓ Module imports successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_configuration():
    """Test that configuration is correct."""
    print("\nTesting configuration...")
    try:
        import DFT_FrothSpeedNG_laser_v9_Video as froth_module
        
        # Check VIDEO_PATH
        expected_path = '/home/pi/Videos/Platinum Mile -1.mp4'
        if froth_module.VIDEO_PATH == expected_path:
            print(f"✓ VIDEO_PATH correctly set to: {expected_path}")
        else:
            print(f"✗ VIDEO_PATH is {froth_module.VIDEO_PATH}, expected {expected_path}")
            return False
        
        # Check LOOP_VIDEO
        if froth_module.LOOP_VIDEO == True:
            print(f"✓ LOOP_VIDEO correctly set to: True")
        else:
            print(f"✗ LOOP_VIDEO is {froth_module.LOOP_VIDEO}, expected True")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Configuration test error: {e}")
        return False

def test_class_exists():
    """Test that FrothSpeedDetector class exists."""
    print("\nTesting class structure...")
    try:
        import DFT_FrothSpeedNG_laser_v9_Video as froth_module
        
        # Check class exists
        if hasattr(froth_module, 'FrothSpeedDetector'):
            print("✓ FrothSpeedDetector class exists")
        else:
            print("✗ FrothSpeedDetector class not found")
            return False
        
        # Check required methods
        required_methods = ['__init__', 'initialize_video_capture', 'process_frame', 
                          'calculate_speed', 'run', 'cleanup']
        
        cls = froth_module.FrothSpeedDetector
        for method in required_methods:
            if hasattr(cls, method):
                print(f"✓ Method '{method}' exists")
            else:
                print(f"✗ Method '{method}' not found")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Class test error: {e}")
        return False

def test_initialization():
    """Test that detector can be initialized with video path."""
    print("\nTesting initialization...")
    try:
        import DFT_FrothSpeedNG_laser_v9_Video as froth_module
        
        # Create detector instance
        detector = froth_module.FrothSpeedDetector(
            video_source='/home/pi/Videos/Platinum Mile -1.mp4',
            loop=True
        )
        
        # Check attributes
        if detector.video_source == '/home/pi/Videos/Platinum Mile -1.mp4':
            print(f"✓ Detector video_source set correctly")
        else:
            print(f"✗ Detector video_source is {detector.video_source}")
            return False
        
        if detector.loop_video == True:
            print(f"✓ Detector loop_video set correctly")
        else:
            print(f"✗ Detector loop_video is {detector.loop_video}")
            return False
        
        print("✓ Detector initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Initialization test error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("DFT_FrothSpeedNG_laser_v9_Video Configuration Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("Class Structure", test_class_exists()))
    results.append(("Initialization", test_initialization()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("All tests PASSED ✓")
        return 0
    else:
        print("Some tests FAILED ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
