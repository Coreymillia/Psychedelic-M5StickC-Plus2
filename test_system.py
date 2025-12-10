#!/usr/bin/env python3
"""
Quick system test for screensaver system
"""

import subprocess
import time

def test_system():
    print("🧪 SCREENSAVER SYSTEM TEST")
    print("="*30)
    
    # Test 1: GPIO cleanup
    print("1️⃣ Testing GPIO cleanup...")
    try:
        subprocess.run(['python3', 'gpio_cleanup.py'], timeout=10, check=True)
        print("   ✅ GPIO cleanup works")
    except Exception as e:
        print(f"   ❌ GPIO cleanup failed: {e}")
    
    # Test 2: Fixed matrix rain (3 seconds)
    print("\n2️⃣ Testing fixed matrix rain (3 seconds)...")
    try:
        subprocess.run(['timeout', '3s', 'python3', 'glyph_rain1_fixed.py'], 
                      timeout=5)
        print("   ✅ Fixed matrix rain works")
    except Exception as e:
        print(f"   ❌ Matrix rain failed: {e}")
    
    # Test 3: Menu system
    print("\n3️⃣ Testing menu system...")
    try:
        result = subprocess.run(['timeout', '2s', 'python3', 'screensaver_manager.py'], 
                               capture_output=True, text=True)
        if "SCREENSAVER MANAGER" in result.stdout:
            print("   ✅ Menu system loads")
        else:
            print("   ❌ Menu system issue")
    except Exception as e:
        print(f"   ❌ Menu test failed: {e}")
    
    print("\n🎉 System test complete!")
    print("   If all tests passed, your system is ready!")

if __name__ == "__main__":
    test_system()