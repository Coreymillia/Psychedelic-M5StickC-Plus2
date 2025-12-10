#!/usr/bin/env python3
"""
Julia Set - Dynamic Fractal
Animated Julia sets with varying parameters
"""

import LCD_1in44
import time
import random
import math
from PIL import Image

class JuliaSet:
    def __init__(self):
        print("🎭 Initializing Julia Set...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Julia set parameters
        self.c_real = -0.7
        self.c_imag = 0.27015
        self.max_iter = 25
        self.time = 0
        
        # Animated parameters
        self.param_speed = 0.01
        
        # Color palette - psychedelic
        self.colors = []
        for i in range(256):
            t = i / 255.0
            r = int(255 * (0.5 + 0.5 * math.cos(t * 6.28 + 0)))
            g = int(255 * (0.5 + 0.5 * math.cos(t * 6.28 + 2.09)))
            b = int(255 * (0.5 + 0.5 * math.cos(t * 6.28 + 4.18)))
            self.colors.append((r, g, b))
        
        print(f"🎭 Julia set ready")
    
    def julia(self, z, c):
        """Calculate Julia set iterations"""
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return self.max_iter
    
    def draw_frame(self):
        """Draw Julia set"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Julia set bounds
        x_min, x_max = -2.0, 2.0
        y_min, y_max = -2.0, 2.0
        
        c = complex(self.c_real, self.c_imag)
        
        for y in range(self.height):
            for x in range(self.width):
                # Map pixel to complex plane
                real = x_min + (x / self.width) * (x_max - x_min)
                imag = y_min + (y / self.height) * (y_max - y_min)
                
                z = complex(real, imag)
                iterations = self.julia(z, c)
                
                if iterations == self.max_iter:
                    color = (0, 0, 50)  # Inside set = dark blue
                else:
                    # Color based on iterations with time offset
                    color_index = (iterations * 8 + int(self.time * 50)) % len(self.colors)
                    color = self.colors[color_index]
                
                image.putpixel((x, y), color)
        
        return image
    
    def update(self):
        """Update Julia set parameters"""
        self.time += self.param_speed
        
        # Animate the Julia set parameter
        self.c_real = -0.7 + 0.3 * math.sin(self.time * 0.5)
        self.c_imag = 0.27015 + 0.2 * math.cos(self.time * 0.7)
        
        # Occasionally jump to interesting Julia parameters
        if random.random() < 0.002:  # 0.2% chance
            interesting_c = [
                (-0.7269, 0.1889),
                (-0.8, 0.156),
                (-0.4, 0.6),
                (0.285, 0.01),
                (-0.75, 0.11),
                (-0.1, 0.651),
            ]
            self.c_real, self.c_imag = random.choice(interesting_c)
    
    def run(self):
        """Main animation loop"""
        print("🎭 Starting Julia Set...")
        print("   Dynamic fractal with morphing parameters")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                self.update()
                
                frame += 1
                
                if frame % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"🎭 {elapsed:.1f}s: c=({self.c_real:.3f}, {self.c_imag:.3f})")
                
                time.sleep(0.08)  # ~12 FPS
                
        except KeyboardInterrupt:
            print(f"\n🎭 Julia set stopped")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Clearing screen...")
            self.LCD.LCD_Clear()
            print("✅ Cleanup complete")
        except Exception as e:
            print(f"Cleanup error: {e}")

if __name__ == "__main__":
    try:
        screensaver = JuliaSet()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()