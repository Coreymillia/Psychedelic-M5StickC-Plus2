#!/usr/bin/env python3
"""
GPIO Cleanup Utility for Waveshare LCD HAT
Kills all conflicting processes and clears GPIO locks
"""

import subprocess
import time
import os

def cleanup_gpio():
    """Clean up all GPIO-using processes and services"""
    print("🧹 Starting GPIO cleanup...")
    
    # Kill all Python screensaver processes
    processes_to_kill = [
        'glyph_rain',
        'matrix_',
        'screensaver',
        'button_',
        'micro_dots',
        'flames',
        'plasma',
        'bouncing',
        'kaleidoscope',
        'raindrops',
        'neon_rain',
        'mandelbrot',
        'julia_set',
        'sierpinski',
        'dragon_curve',
        'campfire',
        'retro_geometry'
    ]
    
    killed_processes = 0
    for process in processes_to_kill:
        try:
            result = subprocess.run(['pkill', '-f', process], capture_output=True)
            if result.returncode == 0:
                killed_processes += 1
                print(f"  ❌ Killed process matching: {process}")
        except:
            pass
    
    # Stop all LCD-related services
    services_to_stop = [
        'lcd-stable.service',
        'lcd-random.service', 
        'lcd-screensaver.service',
        'lcd-glyph-locked.service',
        'lcd-button-switcher.service'
    ]
    
    stopped_services = 0
    for service in services_to_stop:
        try:
            result = subprocess.run(['sudo', 'systemctl', 'stop', service], 
                                  capture_output=True)
            if result.returncode == 0:
                stopped_services += 1
                print(f"  🛑 Stopped service: {service}")
        except:
            pass
    
    # Wait a moment for cleanup
    if killed_processes > 0 or stopped_services > 0:
        print("  ⏳ Waiting for GPIO release...")
        time.sleep(2)
    
    # Check if any Python processes are still running
    try:
        result = subprocess.run(['pgrep', '-f', 'python3.*\.py'], 
                              capture_output=True, text=True)
        remaining = result.stdout.strip().split('\n') if result.stdout.strip() else []
        remaining = [p for p in remaining if p and 'screensaver_manager' not in p]
        
        if remaining:
            print(f"  ⚠️ Warning: {len(remaining)} Python processes still running")
            # Force kill them
            for pid in remaining:
                try:
                    subprocess.run(['kill', '-9', pid], capture_output=True)
                    print(f"  💀 Force killed PID: {pid}")
                except:
                    pass
    except:
        pass
    
    print("✅ GPIO cleanup complete!")
    print(f"   Processes killed: {killed_processes}")
    print(f"   Services stopped: {stopped_services}")
    print()

if __name__ == "__main__":
    cleanup_gpio()