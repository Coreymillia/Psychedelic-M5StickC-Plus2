#!/usr/bin/env python3
"""
Matrix Binary Rain - Classic Matrix Style
Mostly 1s and 0s falling in green with occasional strange symbols
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class MatrixBinaryRain:
    def __init__(self):
        print("🔋 Initializing Matrix Binary Rain...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Character sets
        self.binary = ['0', '1']  # 90% of characters
        self.matrix_symbols = ['日', '文', '字', 'ﾊ', 'ﾐ', 'ﾋ', 'ｰ', 'ｳ', 'ｼ', 'ﾅ', 'ﾓ', 'ﾆ', 'ｻ', 'ﾜ', 'ﾂ', 'ｵ', 'ﾘ', 'ｱ', 'ﾎ', 'ﾃ', 'ﾏ', 'ｹ', 'ﾒ', 'ｴ', 'ｶ', 'ｷ', 'ﾑ', 'ﾕ', 'ﾗ', 'ｾ', 'ﾈ', 'ｽ', 'ﾀ', 'ﾇ', 'ﾍ']  # Japanese katakana-like
        self.rare_symbols = ['☯', '☮', '☢', '☣', '⚡', '⚠', '♦', '♠', '♣', '♥', '※', '◊', '◈', '⬢', '⬡']  # Very rare
        
        # Create falling columns - more dense like real Matrix
        self.columns = []
        col_width = 6  # Tighter spacing for more Matrix feel
        for x in range(0, self.width, col_width):
            self.columns.append({
                'x': x,
                'chars': [],
                'spawn_timer': random.randint(0, 30),
                'speed_multiplier': random.uniform(0.8, 1.5)  # Varied column speeds
            })
        
        print(f"🔋 Created {len(self.columns)} Matrix columns")
    
    def get_character(self):
        """Get character based on Matrix probability"""
        rand = random.random()
        
        if rand < 0.85:  # 85% binary
            return random.choice(self.binary)
        elif rand < 0.98:  # 13% matrix symbols
            return random.choice(self.matrix_symbols)
        else:  # 2% rare symbols
            return random.choice(self.rare_symbols)
    
    def update(self):
        """Update falling characters"""
        for col in self.columns:
            # Spawn new character - Matrix has dense streams
            if col['spawn_timer'] <= 0:
                col['chars'].append({
                    'char': self.get_character(),
                    'y': -8,
                    'brightness': 255,
                    'speed': random.uniform(1.0, 3.0) * col['speed_multiplier'],
                    'is_lead': True  # Mark as leading character
                })
                col['spawn_timer'] = random.randint(5, 25)  # Frequent spawning
            else:
                col['spawn_timer'] -= 1
            
            # Update existing characters
            for i, char in enumerate(col['chars'][:]):
                char['y'] += char['speed']
                
                # Leading character stays bright longer
                if char['is_lead']:
                    if i > 0:  # No longer the lead
                        char['is_lead'] = False
                        char['brightness'] = 200
                else:
                    char['brightness'] = max(0, char['brightness'] - 6)  # Fade trail
                
                # Remove characters that are off screen or too dim
                if char['y'] > self.height + 10 or char['brightness'] <= 0:
                    col['chars'].remove(char)
                    
                # Update lead status
                if i == 0:
                    char['is_lead'] = True
    
    def draw_frame(self):
        """Draw the current frame"""
        # Black background
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw all falling characters
        for col in self.columns:
            for i, char in enumerate(col['chars']):
                if 0 <= char['y'] <= self.height:
                    b = char['brightness']
                    
                    # Matrix green color scheme
                    if char['is_lead'] and i == 0:
                        # Bright white lead character (like in the movies)
                        color = (255, 255, 255)
                    elif b > 180:
                        # Bright green for recent characters
                        color = (0, 255, 0)
                    elif b > 120:
                        # Medium green
                        green = int(b * 0.9)
                        color = (0, green, 0)
                    elif b > 60:
                        # Dim green
                        green = int(b * 0.7)
                        color = (0, green, 0)
                    else:
                        # Very dim green trail
                        green = int(b * 0.5)
                        color = (0, green, 0)
                    
                    try:
                        draw.text((col['x'], int(char['y'])), 
                                 char['char'], fill=color, font=font)
                    except:
                        # Fallback for unsupported characters
                        draw.text((col['x'], int(char['y'])), 
                                 random.choice(self.binary), fill=color, font=font)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🔋 Starting Matrix Binary Rain...")
        print("   Welcome to the Matrix...")
        print("   Press Ctrl+C to exit the Matrix")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Occasional status (Matrix doesn't talk much)
                if frame % 600 == 0:  # Every 20 seconds
                    elapsed = time.time() - start_time
                    total_chars = sum(len(col['chars']) for col in self.columns)
                    print(f"🔋 The Matrix has you... {total_chars} streams active")
                
                time.sleep(0.04)  # 25 FPS for smooth Matrix feel
                
        except KeyboardInterrupt:
            print(f"\n🔋 You chose the red pill... Exiting the Matrix")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Clearing the Matrix...")
            self.LCD.LCD_Clear()
            print("✅ Back to reality")
        except Exception as e:
            print(f"Cleanup error: {e}")

if __name__ == "__main__":
    try:
        matrix = MatrixBinaryRain()
        matrix.run()
    except Exception as e:
        print(f"❌ Matrix error: {e}")
        import traceback
        traceback.print_exc()