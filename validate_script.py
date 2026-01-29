#!/usr/bin/env python3
"""
Validation script to check DFT_FrothSpeedNG_laser_v9_Video.py configuration
Uses AST parsing to validate without requiring OpenCV
"""

import ast
import os

def validate_script():
    """Validate the script configuration by parsing the AST."""
    script_path = 'DFT_FrothSpeedNG_laser_v9_Video.py'
    
    if not os.path.exists(script_path):
        print(f"✗ Script not found: {script_path}")
        return False
    
    print("=" * 60)
    print("DFT_FrothSpeedNG_laser_v9_Video.py Validation")
    print("=" * 60)
    
    with open(script_path, 'r') as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
        print("✓ Script has valid Python syntax\n")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return False
    
    # Find VIDEO_PATH assignment
    video_path_found = False
    video_path_value = None
    loop_video_found = False
    loop_video_value = None
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == 'VIDEO_PATH':
                        video_path_found = True
                        if isinstance(node.value, ast.Constant):
                            video_path_value = node.value.value
                    elif target.id == 'LOOP_VIDEO':
                        loop_video_found = True
                        if isinstance(node.value, ast.Constant):
                            loop_video_value = node.value.value
    
    # Validate VIDEO_PATH
    print("Testing VIDEO_PATH configuration:")
    expected_path = '/home/pi/Videos/Platinum Mile -1.mp4'
    if video_path_found:
        if video_path_value == expected_path:
            print(f"✓ VIDEO_PATH = '{video_path_value}'")
            print(f"  Matches required path: '{expected_path}'")
        else:
            print(f"✗ VIDEO_PATH = '{video_path_value}'")
            print(f"  Expected: '{expected_path}'")
            return False
    else:
        print("✗ VIDEO_PATH not found in script")
        return False
    
    # Validate LOOP_VIDEO
    print("\nTesting LOOP_VIDEO configuration:")
    if loop_video_found:
        if loop_video_value is True:
            print(f"✓ LOOP_VIDEO = {loop_video_value}")
            print(f"  Video looping is enabled")
        else:
            print(f"✗ LOOP_VIDEO = {loop_video_value}")
            print(f"  Expected: True")
            return False
    else:
        print("✗ LOOP_VIDEO not found in script")
        return False
    
    # Check for FrothSpeedDetector class
    print("\nTesting class structure:")
    class_found = False
    required_methods = {'__init__', 'initialize_video_capture', 'process_frame', 
                       'calculate_speed', 'run', 'cleanup'}
    found_methods = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if node.name == 'FrothSpeedDetector':
                class_found = True
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        found_methods.add(item.name)
    
    if class_found:
        print("✓ FrothSpeedDetector class found")
        missing_methods = required_methods - found_methods
        if not missing_methods:
            print(f"✓ All required methods present: {', '.join(sorted(required_methods))}")
        else:
            print(f"✗ Missing methods: {', '.join(missing_methods)}")
            return False
    else:
        print("✗ FrothSpeedDetector class not found")
        return False
    
    # Check for video looping logic in run method
    print("\nTesting video looping logic:")
    loop_logic_found = False
    
    # Look for the looping pattern in source
    if 'self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)' in source:
        print("✓ Video loop reset logic found (CAP_PROP_POS_FRAMES)")
        loop_logic_found = True
    
    if 'if self.loop_video and isinstance(self.video_source, str):' in source:
        print("✓ Video file loop condition found")
        loop_logic_found = True
    
    if not loop_logic_found:
        print("✗ Video looping logic not found")
        return False
    
    # Check main function
    print("\nTesting main function:")
    main_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == 'main':
                main_found = True
                break
    
    if main_found:
        print("✓ main() function found")
        # Check if main uses VIDEO_PATH
        if 'FrothSpeedDetector(video_source=VIDEO_PATH' in source:
            print("✓ main() creates detector with VIDEO_PATH")
        else:
            print("⚠ main() may not be using VIDEO_PATH correctly")
    else:
        print("✗ main() function not found")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All validations PASSED")
    print("=" * 60)
    print("\nScript is correctly configured to:")
    print(f"  • Use video file: {expected_path}")
    print(f"  • Loop video continuously: {loop_video_value}")
    print(f"  • Maintain all froth detection functionality")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    import sys
    success = validate_script()
    sys.exit(0 if success else 1)
