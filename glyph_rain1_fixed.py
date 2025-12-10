#!/usr/bin/env python3
"""
Glyph Rain Screensaver - Fixed Version for Long-Term Stability
Matrix-style falling characters with memory leak fixes and resource management
"""

import LCD_1in44
import time
import random
import gc
from PIL import Image, ImageDraw, ImageFont

class GlyphRainFixed:
    def __init__(self):
        print("🌧️ Initializing Fixed Glyph Rain with official Waveshare driver...")
        
        # Initialize LCD using official driver
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R  # Setting #5
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Glyph characters for the matrix rain
        self.glyphs = '0123456789ABCDEFabcdef!@#$%^&*()[]{}+-=<>?/\\|_~πΩαβγδλμσφ'
        
        # Create falling columns with memory limits
        self.columns = []
        col_width = 8  # Character width spacing
        self.max_chars_per_column = 15  # Limit characters per column to prevent memory leak
        
        for x in range(0, self.width, col_width):
            self.columns.append({
                'x': x,
                'chars': [],
                'spawn_timer': random.randint(0, 50)
            })
        
        # Performance tracking
        self.frame_count = 0
        self.last_cleanup = time.time()
        self.last_gc = time.time()
        
        print(f"🌧️ Created {len(self.columns)} falling columns")
        print(f"🔒 Memory protection: Max {self.max_chars_per_column} chars per column")
    
    def update(self):
        """Update all falling characters with memory management"""
        current_time = time.time()
        
        for col in self.columns:
            # Spawn new character at top (but limit total characters)
            if col['spawn_timer'] <= 0 and len(col['chars']) < self.max_chars_per_column:
                col['chars'].append({
                    'char': random.choice(self.glyphs),
                    'y': -10,
                    'brightness': 255,
                    'speed': random.uniform(0.8, 2.5)
                })
                col['spawn_timer'] = random.randint(25, 100)
            else:
                col['spawn_timer'] -= 1
            
            # Update existing characters with aggressive cleanup
            chars_to_remove = []
            for i, char in enumerate(col['chars']):
                char['y'] += char['speed']
                char['brightness'] = max(0, char['brightness'] - 4)
                
                # More aggressive removal conditions to prevent memory buildup
                if (char['y'] > self.height + 5 or 
                    char['brightness'] <= 10 or 
                    char['y'] > self.height * 1.5):  # Extra safety margin
                    chars_to_remove.append(i)
            
            # Remove characters in reverse order to maintain indices
            for i in reversed(chars_to_remove):
                del col['chars'][i]
        
        # Periodic memory cleanup
        if current_time - self.last_cleanup > 30:  # Every 30 seconds
            self.memory_cleanup()
            self.last_cleanup = current_time
        
        # Periodic garbage collection
        if current_time - self.last_gc > 60:  # Every 60 seconds
            collected = gc.collect()
            if collected > 0:
                print(f"🧹 Garbage collected: {collected} objects")
            self.last_gc = current_time
    
    def memory_cleanup(self):
        """Aggressive memory cleanup to prevent leaks"""
        total_chars_before = sum(len(col['chars']) for col in self.columns)
        
        # Remove excess characters from overloaded columns
        for col in self.columns:
            if len(col['chars']) > self.max_chars_per_column:
                # Keep only the most recent characters
                col['chars'] = col['chars'][-self.max_chars_per_column:]
        
        total_chars_after = sum(len(col['chars']) for col in self.columns)
        if total_chars_before != total_chars_after:
            print(f"🧹 Memory cleanup: {total_chars_before} -> {total_chars_after} characters")
    
    def draw_frame(self):
        """Draw the current frame"""
        # Create black background
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Use default font
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw all falling characters
        for col in self.columns:
            for char in col['chars']:
                if 0 <= char['y'] <= self.height:
                    b = char['brightness']
                    
                    # Color scheme: bright white for lead, green trail
                    if b > 200:
                        color = (255, 255, 255)  # Bright white lead
                    elif b > 150:
                        color = (200, 255, 200)  # Light green
                    elif b > 100:
                        green = int(b * 0.9)
                        color = (0, green, 0)    # Medium green
                    else:
                        green = int(b * 0.6)
                        color = (0, green, 0)    # Dark green trail
                    
                    try:
                        draw.text((col['x'], int(char['y'])), 
                                 char['char'], fill=color, font=font)
                    except:
                        # Fallback for unsupported characters
                        draw.text((col['x'], int(char['y'])), 
                                 '?', fill=color, font=font)
        
        return image
    
    def run(self):
        """Main animation loop with enhanced stability"""
        print("🌧️ Starting Stable Matrix-style Glyph Rain...")
        print("   Press Ctrl+C to stop")
        print("   🔒 Fixed version with memory leak protection")
        
        self.frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                # Update character positions
                self.update()
                
                # Draw frame
                image = self.draw_frame()
                
                # Display on LCD
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                self.frame_count += 1
                
                # Enhanced status update every 10 seconds
                if self.frame_count % 300 == 0:
                    elapsed = time.time() - start_time
                    fps = self.frame_count / elapsed if elapsed > 0 else 0
                    total_chars = sum(len(col['chars']) for col in self.columns)
                    max_chars = max(len(col['chars']) for col in self.columns) if self.columns else 0
                    
                    print(f"🌧️ {elapsed:.1f}s: {total_chars} glyphs (max {max_chars}/col), {fps:.1f} FPS")
                
                # Control frame rate (~30 FPS)
                time.sleep(0.033)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Glyph Rain stopped after {self.frame_count} frames ({(self.frame_count * 0.033 / 60):.1f} minutes)")
            self.cleanup()
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            self.cleanup()
            raise
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Clearing screen and cleaning up...")
            
            # Clear all character lists to free memory
            for col in self.columns:
                col['chars'].clear()
            
            # Clear LCD
            self.LCD.LCD_Clear()
            
            # Final garbage collection
            collected = gc.collect()
            print(f"🗑️ Final cleanup: {collected} objects collected")
            print("✅ Cleanup complete")
            
        except Exception as e:
            print(f"Cleanup error: {e}")

def main():
    try:
        screensaver = GlyphRainFixed()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()