#include <M5StickCPlus2.h>

// M5StickC Plus2 Display Framework for Psychedelic Screensavers
// Based on the successful biorhythm calculator display system

#define Disp M5.Lcd
#define SCREEN_WIDTH 135
#define SCREEN_HEIGHT 240

// Color definitions for psychedelic effects
#define BLACK      0x0000
#define WHITE      0xFFFF
#define RED        0xF800
#define GREEN      0x07E0
#define BLUE       0x001F
#define CYAN       0x07FF
#define MAGENTA    0xF81F
#define YELLOW     0xFFE0
#define ORANGE     0xFC00
#define PURPLE     0x8010
#define PINK       0xFE19
#define LIME       0x87F0

// Screensaver modes
enum ScreenSaverMode {
  DIGITAL_DREAMS,
  PLASMA_WAVES,
  SPIRAL_COLORS,
  BOUNCING_BALLS,
  NEON_RAIN,
  KALEIDOSCOPE,
  LIQUID_METAL,
  CAMPFIRE,
  DRAGON_CURVE,
  GLYPH_RAIN,
  HEAVY_RAIN,
  JULIA_SET,
  MANDELBROT,
  MATRIX_BINARY,
  MICRO_DOTS,
  RAINDROPS,
  RETRO_GEOMETRY,
  SIERPINSKI,
  SIMPLE_FLAMES,
  WALKING_TRIANGLE,
  WALKING_SQUARE,
  WALKING_STAR,
  SPIROGRAPH,
  RECURSIVE_POLYGONS,
  FLOW_FIELD,
  COLOR_SHIMMER,
  STARFIELD_WARP,
  FIREFLY_SWARM,
  MODE_COUNT
};

ScreenSaverMode currentMode = DIGITAL_DREAMS;
unsigned long lastModeChange = 0;
unsigned long modeChangeInterval = 10000; // Change every 10 seconds
unsigned long frameTime = 0;

// v1.1 Speed control variables
int speedLevel = 5; // Default speed (1=slowest, 10=fastest)
float speedMultipliers[10] = {0.1f, 0.2f, 0.4f, 0.6f, 0.8f, 1.0f, 1.3f, 1.6f, 2.0f, 2.5f};
unsigned long lastButtonPress = 0;
const unsigned long buttonDebounceTime = 200;

// Animation variables
float time_counter = 0;
int frame_counter = 0;

// Function declarations
void drawPlasmaWaves();
void drawSpiralColors();
void drawBouncingBalls();
void drawNeonRain();
void drawKaleidoscope();
void drawLiquidMetal();
void drawCampfire();
void drawDragonCurve();
void drawGlyphRain();
void drawHeavyRain();
void drawJuliaSet();
void drawMandelbrot();
void drawMatrixBinary();
void drawMicroDots();
void drawRaindrops();
void drawRetroGeometry();
void drawSierpinski();
void drawSimpleFlames();
void drawWalkingTriangle();
void drawWalkingSquare();
void drawWalkingStar();
void drawSpirograph();
void drawRecursivePolygons();
void drawFlowField();
void drawColorShimmer();
void drawStarfieldWarp();
void drawFireflySwarm();
void drawDigitalDreams();
void switchMode();
void switchModePrevious();
void cycleSpeed();
void drawModeIndicator();
void drawSpeedIndicator();
uint16_t getColorFromHSV(float h, float s, float v);
uint16_t interpolateColor(uint16_t color1, uint16_t color2, float ratio);
String generateDragonString(int iterations);

void setup() {
  Serial.begin(115200);
  M5.begin();
  
  // Initialize display
  Disp.setRotation(0);  // Portrait mode like biorhythm calc
  Disp.fillScreen(BLACK);
  
  // Welcome message
  Disp.setTextColor(CYAN);
  Disp.setTextSize(2);
  Disp.drawString("PSYCHEDELIC", 10, 50, 1);
  Disp.drawString("M5 SAVERS", 15, 80, 1);
  
  Disp.setTextColor(WHITE);
  Disp.setTextSize(1);
  Disp.drawString("Press M5 to change modes", 5, 120, 1);
  Disp.drawString("Manual control only", 15, 140, 1);
  
  delay(2000);
  Disp.fillScreen(BLACK);
  
  Serial.println("🌈 Psychedelic M5 Screensavers Started!");
}

void loop() {
  M5.update();
  
  // v1.1 Button handling with debouncing
  unsigned long currentTime = millis();
  if (currentTime - lastButtonPress > buttonDebounceTime) {
    
    // BtnA: Speed control (currently working button)
    if (M5.BtnA.wasClicked()) {
      cycleSpeed();
      lastButtonPress = currentTime;
    }
    
    // BtnB: Next screensaver
    if (M5.BtnB.wasClicked()) {
      switchMode();
      lastButtonPress = currentTime;
    }
    
    // BtnC (Power button): Previous screensaver
    if (M5.BtnPWR.wasClicked()) {
      switchModePrevious();
      lastButtonPress = currentTime;
    }
  }
  
  // AUTO-CYCLING DISABLED - Manual control only via M5 button
  // if (millis() - lastModeChange > modeChangeInterval) {
  //   switchMode();
  // }
  
  // Draw current screensaver
  frameTime = millis();
  time_counter += 0.05f * speedMultipliers[speedLevel - 1]; // Apply speed multiplier
  frame_counter++;
  
  switch (currentMode) {
    case DIGITAL_DREAMS:
      drawDigitalDreams();
      break;
    case PLASMA_WAVES:
      drawPlasmaWaves();
      break;
    case SPIRAL_COLORS:
      drawSpiralColors();
      break;
    case BOUNCING_BALLS:
      drawBouncingBalls();
      break;
    case NEON_RAIN:
      drawNeonRain();
      break;
    case KALEIDOSCOPE:
      drawKaleidoscope();
      break;
    case LIQUID_METAL:
      drawLiquidMetal();
      break;
    case CAMPFIRE:
      drawCampfire();
      break;
    case DRAGON_CURVE:
      drawDragonCurve();
      break;
    case GLYPH_RAIN:
      drawGlyphRain();
      break;
    case HEAVY_RAIN:
      drawHeavyRain();
      break;
    case JULIA_SET:
      drawJuliaSet();
      break;
    case MANDELBROT:
      drawMandelbrot();
      break;
    case MATRIX_BINARY:
      drawMatrixBinary();
      break;
    case MICRO_DOTS:
      drawMicroDots();
      break;
    case RAINDROPS:
      drawRaindrops();
      break;
    case RETRO_GEOMETRY:
      drawRetroGeometry();
      break;
    case SIERPINSKI:
      drawSierpinski();
      break;
    case SIMPLE_FLAMES:
      drawSimpleFlames();
      break;
    case WALKING_TRIANGLE:
      drawWalkingTriangle();
      break;
    case WALKING_SQUARE:
      drawWalkingSquare();
      break;
    case WALKING_STAR:
      drawWalkingStar();
      break;
    case SPIROGRAPH:
      drawSpirograph();
      break;
    case RECURSIVE_POLYGONS:
      drawRecursivePolygons();
      break;
    case FLOW_FIELD:
      drawFlowField();
      break;
    case COLOR_SHIMMER:
      drawColorShimmer();
      break;
    case STARFIELD_WARP:
      drawStarfieldWarp();
      break;
    case FIREFLY_SWARM:
      drawFireflySwarm();
      break;
  }
  
  // Clean immersive experience - no indicators!
  // Frame rate control
  delay(50); // ~20 FPS
}

void switchMode() {
  currentMode = static_cast<ScreenSaverMode>((currentMode + 1) % MODE_COUNT);
  lastModeChange = millis();
  frame_counter = 0;
  
  // Brief mode name display
  Disp.fillRect(0, 0, SCREEN_WIDTH, 30, BLACK);
  Disp.setTextColor(WHITE);
  Disp.setTextSize(1);
  
  String modeName;
  switch (currentMode) {
    case DIGITAL_DREAMS: modeName = "DIGITAL DREAMS"; break;
    case PLASMA_WAVES: modeName = "PLASMA WAVES"; break;
    case SPIRAL_COLORS: modeName = "SPIRAL COLORS"; break;
    case BOUNCING_BALLS: modeName = "BOUNCING BALLS"; break;
    case NEON_RAIN: modeName = "NEON RAIN"; break;
    case KALEIDOSCOPE: modeName = "KALEIDOSCOPE"; break;
    case LIQUID_METAL: modeName = "LIQUID METAL"; break;
    case CAMPFIRE: modeName = "CAMPFIRE"; break;
    case DRAGON_CURVE: modeName = "DRAGON CURVE"; break;
    case GLYPH_RAIN: modeName = "GLYPH RAIN"; break;
    case HEAVY_RAIN: modeName = "HEAVY RAIN"; break;
    case JULIA_SET: modeName = "JULIA SET"; break;
    case MANDELBROT: modeName = "MANDELBROT"; break;
    case MATRIX_BINARY: modeName = "MATRIX BINARY"; break;
    case MICRO_DOTS: modeName = "MICRO DOTS"; break;
    case RAINDROPS: modeName = "RAINDROPS"; break;
    case RETRO_GEOMETRY: modeName = "RETRO GEOMETRY"; break;
    case SIERPINSKI: modeName = "SIERPINSKI"; break;
    case SIMPLE_FLAMES: modeName = "SIMPLE FLAMES"; break;
    case WALKING_TRIANGLE: modeName = "WALKING TRIANGLE"; break;
    case WALKING_SQUARE: modeName = "WALKING SQUARE"; break;
    case WALKING_STAR: modeName = "WALKING STAR"; break;
    case SPIROGRAPH: modeName = "SPIROGRAPH"; break;
    case RECURSIVE_POLYGONS: modeName = "RECURSIVE POLYGONS"; break;
    case FLOW_FIELD: modeName = "FLOW FIELD"; break;
    case COLOR_SHIMMER: modeName = "COLOR SHIMMER"; break;
    case STARFIELD_WARP: modeName = "STARFIELD WARP"; break;
    case FIREFLY_SWARM: modeName = "FIREFLY SWARM"; break;
  }
  
  Disp.drawString(modeName, 5, 10, 1);
  Serial.println("🎨 Mode: " + modeName);
}

void drawPlasmaWaves() {
  // Plasma wave effect - mathematical beauty
  for (int y = 0; y < SCREEN_HEIGHT; y += 2) {
    for (int x = 0; x < SCREEN_WIDTH; x += 2) {
      float plasma = sin(x * 0.1f + time_counter) + 
                    sin(y * 0.1f + time_counter * 1.3f) +
                    sin((x + y) * 0.08f + time_counter * 0.7f);
      
      float hue = plasma * 60.0f + time_counter * 50.0f;
      uint16_t color = getColorFromHSV(hue, 1.0f, 0.8f);
      
      Disp.fillRect(x, y, 2, 2, color);
    }
  }
}

void drawSpiralColors() {
  // Colorful spiral pattern
  int centerX = SCREEN_WIDTH / 2;
  int centerY = SCREEN_HEIGHT / 2;
  
  for (int r = 5; r < 100; r += 3) {
    float angle = time_counter * 2.0f + r * 0.2f;
    int x = centerX + cos(angle) * r;
    int y = centerY + sin(angle) * r;
    
    if (x >= 0 && x < SCREEN_WIDTH && y >= 0 && y < SCREEN_HEIGHT) {
      float hue = r * 5.0f + time_counter * 100.0f;
      uint16_t color = getColorFromHSV(hue, 1.0f, 1.0f);
      Disp.fillCircle(x, y, 3, color);
    }
  }
  
  // Clear old trails
  if (frame_counter % 30 == 0) {
    Disp.fillScreen(BLACK);
  }
}

void drawBouncingBalls() {
  // Classic bouncing balls screensaver inspired by your Python version
  static float balls[6][4]; // x, y, vx, vy for 6 balls
  static uint16_t ballColors[6];
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize balls
    for (int i = 0; i < 6; i++) {
      balls[i][0] = random(20, SCREEN_WIDTH - 20);   // x
      balls[i][1] = random(20, SCREEN_HEIGHT - 20);  // y  
      balls[i][2] = (random(100) - 50) / 20.0f;      // vx
      balls[i][3] = (random(100) - 50) / 20.0f;      // vy
      
      // Psychedelic neon colors
      float hue = i * 60.0f;
      ballColors[i] = getColorFromHSV(hue, 1.0f, 1.0f);
    }
    initialized = true;
  }
  
  // Fade background for trail effect
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0841);
  
  for (int i = 0; i < 6; i++) {
    // Update position
    balls[i][0] += balls[i][2];
    balls[i][1] += balls[i][3];
    
    // Bounce off walls
    if (balls[i][0] <= 8 || balls[i][0] >= SCREEN_WIDTH - 8) {
      balls[i][2] = -balls[i][2];
      balls[i][0] = constrain(balls[i][0], 8, SCREEN_WIDTH - 8);
    }
    if (balls[i][1] <= 8 || balls[i][1] >= SCREEN_HEIGHT - 8) {
      balls[i][3] = -balls[i][3];
      balls[i][1] = constrain(balls[i][1], 8, SCREEN_HEIGHT - 8);
    }
    
    // Color cycling
    float hue = i * 60.0f + time_counter * 30.0f;
    ballColors[i] = getColorFromHSV(hue, 1.0f, 1.0f);
    
    // Draw ball with glow effect
    int x = (int)balls[i][0];
    int y = (int)balls[i][1];
    
    Disp.fillCircle(x, y, 6, ballColors[i]);
    Disp.fillCircle(x, y, 3, WHITE);
  }
}

void drawNeonRain() {
  // Neon digital rain inspired by your Python version
  static int drops[15];
  static int dropSpeeds[15];
  static uint16_t dropColors[15];
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize drops
    for (int i = 0; i < 15; i++) {
      drops[i] = random(-50, 0);
      dropSpeeds[i] = random(2, 6);
      
      float hue = i * 24.0f;
      dropColors[i] = getColorFromHSV(hue, 1.0f, 1.0f);
    }
    initialized = true;
  }
  
  // Dark background with slight fade
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0020);
  
  for (int i = 0; i < 15; i++) {
    int x = i * (SCREEN_WIDTH / 15);
    
    // Update drop position
    drops[i] += dropSpeeds[i];
    if (drops[i] > SCREEN_HEIGHT + 20) {
      drops[i] = random(-50, 0);
      dropSpeeds[i] = random(2, 6);
    }
    
    // Color cycling for neon effect
    float hue = i * 24.0f + time_counter * 50.0f;
    dropColors[i] = getColorFromHSV(hue, 1.0f, 1.0f);
    
    // Draw neon rain drop with trail
    for (int j = 0; j < 8; j++) {
      int y = drops[i] - j * 3;
      if (y >= 0 && y < SCREEN_HEIGHT) {
        float brightness = 1.0f - (j / 8.0f);
        uint16_t color = getColorFromHSV(hue, 1.0f, brightness);
        
        Disp.fillRect(x, y, 8, 2, color);
      }
    }
  }
}

void drawKaleidoscope() {
  // Kaleidoscope pattern - placeholder for now
  Disp.fillScreen(BLACK);
  
  int centerX = SCREEN_WIDTH / 2;
  int centerY = SCREEN_HEIGHT / 2;
  
  for (int i = 0; i < 6; i++) {
    float angle = (time_counter + i * 60.0f) * M_PI / 180.0f;
    int x = centerX + cos(angle) * 40;
    int y = centerY + sin(angle) * 40;
    
    float hue = time_counter * 50.0f + i * 60.0f;
    uint16_t color = getColorFromHSV(hue, 1.0f, 1.0f);
    
    Disp.fillCircle(x, y, 10, color);
  }
}

void drawLiquidMetal() {
  // Liquid metal effect - placeholder for now
  for (int y = 0; y < SCREEN_HEIGHT; y += 3) {
    for (int x = 0; x < SCREEN_WIDTH; x += 3) {
      float wave = sin(x * 0.2f + time_counter * 2.0f) * 
                  cos(y * 0.15f + time_counter * 1.5f);
      
      uint8_t intensity = (wave + 1.0f) * 127.0f;
      uint16_t color = Disp.color565(intensity, intensity/2, intensity/4);
      
      Disp.fillRect(x, y, 3, 3, color);
    }
  }
}

void drawModeIndicator() {
  // Small indicator showing current mode
  Disp.fillCircle(SCREEN_WIDTH - 10, 10, 3, WHITE);
  Disp.drawString(String(currentMode + 1), SCREEN_WIDTH - 15, 20, 1);
}

uint16_t getColorFromHSV(float h, float s, float v) {
  // Convert HSV to RGB565 color
  h = fmod(h, 360.0f);
  if (h < 0) h += 360.0f;
  
  float c = v * s;
  float x = c * (1.0f - abs(fmod(h / 60.0f, 2.0f) - 1.0f));
  float m = v - c;
  
  float r, g, b;
  
  if (h < 60) { r = c; g = x; b = 0; }
  else if (h < 120) { r = x; g = c; b = 0; }
  else if (h < 180) { r = 0; g = c; b = x; }
  else if (h < 240) { r = 0; g = x; b = c; }
  else if (h < 300) { r = x; g = 0; b = c; }
  else { r = c; g = 0; b = x; }
  
  r = (r + m) * 255;
  g = (g + m) * 255;
  b = (b + m) * 255;
  
  return Disp.color565((uint8_t)r, (uint8_t)g, (uint8_t)b);
}

uint16_t interpolateColor(uint16_t color1, uint16_t color2, float ratio) {
  uint8_t r1 = (color1 >> 11) & 0x1F;
  uint8_t g1 = (color1 >> 5) & 0x3F;
  uint8_t b1 = color1 & 0x1F;
  
  uint8_t r2 = (color2 >> 11) & 0x1F;
  uint8_t g2 = (color2 >> 5) & 0x3F;
  uint8_t b2 = color2 & 0x1F;
  
  uint8_t r = r1 + (r2 - r1) * ratio;
  uint8_t g = g1 + (g2 - g1) * ratio;
  uint8_t b = b1 + (b2 - b1) * ratio;
  
  return (r << 11) | (g << 5) | b;
}

void drawCampfire() {
  // Campfire effect inspired by your Python version
  static float flames[8][3]; // x, height, flicker_phase
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize flame positions
    for (int i = 0; i < 8; i++) {
      flames[i][0] = 20 + i * 12;  // x position
      flames[i][1] = random(15, 35); // base height
      flames[i][2] = random(0, 628) / 100.0f; // flicker phase
    }
    initialized = true;
  }
  
  // Dark background
  Disp.fillScreen(BLACK);
  
  // Draw campfire base (logs)
  Disp.fillRect(0, SCREEN_HEIGHT - 15, SCREEN_WIDTH, 15, 0x4208); // Dark brown
  
  // Draw flames
  for (int i = 0; i < 8; i++) {
    int x = flames[i][0];
    float base_height = flames[i][1];
    flames[i][2] += 0.15f; // Update flicker phase
    
    // Calculate flame height with flicker
    float flicker = sin(flames[i][2]) * 8 + cos(flames[i][2] * 1.7f) * 5;
    int height = base_height + flicker + sin(time_counter * 3 + i) * 6;
    
    // Draw flame with gradient colors
    for (int h = 0; h < height && h < 80; h++) {
      int y = SCREEN_HEIGHT - 15 - h;
      if (y < 0) break;
      
      // Color transitions: red -> orange -> yellow -> white
      float flame_ratio = h / (float)height;
      uint16_t color;
      
      if (flame_ratio < 0.3f) {
        // Red to orange
        color = getColorFromHSV(0 + flame_ratio * 60, 1.0f, 0.8f + flame_ratio * 0.2f);
      } else if (flame_ratio < 0.7f) {
        // Orange to yellow
        color = getColorFromHSV(20 + (flame_ratio - 0.3f) * 60, 1.0f, 1.0f);
      } else {
        // Yellow to white
        float white_mix = (flame_ratio - 0.7f) / 0.3f;
        color = getColorFromHSV(60, 1.0f - white_mix * 0.5f, 1.0f);
      }
      
      // Flame width varies with height
      int width = 6 - (h / 15);
      width = max(width, 2);
      
      Disp.fillRect(x - width/2, y, width, 1, color);
    }
  }
  
  // Add sparks
  for (int i = 0; i < 5; i++) {
    int spark_x = random(10, SCREEN_WIDTH - 10);
    int spark_y = random(SCREEN_HEIGHT - 60, SCREEN_HEIGHT - 20);
    
    if (random(100) < 30) { // 30% chance for spark
      uint16_t spark_color = getColorFromHSV(random(0, 60), 1.0f, 1.0f);
      Disp.drawPixel(spark_x, spark_y, spark_color);
    }
  }
}

void drawDragonCurve() {
  // Dragon curve fractal inspired by your Python version - BIGGER SIZE!
  static int iteration = 1;
  static int step_count = 0;
  static float x = SCREEN_WIDTH / 2;
  static float y = SCREEN_HEIGHT / 2;
  static int direction = 0; // 0=right, 1=down, 2=left, 3=up
  static String dragon_string = "F";
  static int string_pos = 0;
  static bool initialized = false;
  
  if (!initialized) {
    Disp.fillScreen(BLACK);
    initialized = true;
  }
  
  // Generate dragon curve string for current iteration
  if (step_count == 0) {
    dragon_string = generateDragonString(iteration);
    string_pos = 0;
    x = SCREEN_WIDTH / 2;
    y = SCREEN_HEIGHT / 2;
    direction = 0;
    
    // Clear screen every few iterations
    if (iteration % 3 == 1) {
      Disp.fillScreen(BLACK);
    }
  }
  
  // Draw more steps per frame for bigger curves
  for (int steps = 0; steps < 8 && string_pos < dragon_string.length(); steps++) {
    char cmd = dragon_string.charAt(string_pos);
    
    if (cmd == 'F') {
      // Draw forward with BIGGER step size
      float new_x = x;
      float new_y = y;
      
      int step_size = 4; // Increased from 2 to 4 for bigger curves
      switch (direction) {
        case 0: new_x += step_size; break; // right
        case 1: new_y += step_size; break; // down  
        case 2: new_x -= step_size; break; // left
        case 3: new_y -= step_size; break; // up
      }
      
      // Wrap around screen
      if (new_x < 0) new_x = SCREEN_WIDTH - 1;
      if (new_x >= SCREEN_WIDTH) new_x = 0;
      if (new_y < 0) new_y = SCREEN_HEIGHT - 1;
      if (new_y >= SCREEN_HEIGHT) new_y = 0;
      
      // Color based on position and iteration
      float hue = fmod(string_pos * 3 + iteration * 30 + time_counter * 20, 360);
      uint16_t color = getColorFromHSV(hue, 1.0f, 0.9f);
      
      // Draw thicker lines for more visible curves
      Disp.drawLine(x, y, new_x, new_y, color);
      Disp.drawLine(x+1, y, new_x+1, new_y, color); // Make it thicker
      
      x = new_x;
      y = new_y;
    } else if (cmd == 'L') {
      // Turn left
      direction = (direction + 3) % 4;
    } else if (cmd == 'R') {
      // Turn right
      direction = (direction + 1) % 4;
    }
    
    string_pos++;
  }
  
  step_count++;
  
  // Move to next iteration when done
  if (string_pos >= dragon_string.length()) {
    step_count = 0;
    iteration++;
    if (iteration > 15) iteration = 1; // Increased max iterations for bigger patterns
  }
}

void drawGlyphRain() {
  // Matrix-style glyph rain inspired by your Python version
  static char glyphs[] = "0123456789ABCDEF!@#$%^&*()[]{}+-=<>?/\\|_~";
  static int drops[20][4]; // x, y, speed, char_index
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize drops
    for (int i = 0; i < 20; i++) {
      drops[i][0] = i * (SCREEN_WIDTH / 20); // x position
      drops[i][1] = random(-100, 0);         // y position
      drops[i][2] = random(1, 4);            // speed
      drops[i][3] = random(0, strlen(glyphs)); // character index
    }
    initialized = true;
  }
  
  // Fade background
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0020);
  
  for (int i = 0; i < 20; i++) {
    // Update drop position
    drops[i][1] += drops[i][2];
    
    // Reset drop when it goes off screen
    if (drops[i][1] > SCREEN_HEIGHT + 10) {
      drops[i][1] = random(-50, 0);
      drops[i][2] = random(1, 4);
      drops[i][3] = random(0, strlen(glyphs));
    }
    
    // Change character occasionally for matrix effect
    if (random(100) < 10) {
      drops[i][3] = random(0, strlen(glyphs));
    }
    
    // Draw glyph trail
    for (int trail = 0; trail < 8; trail++) {
      int y = drops[i][1] - trail * 8;
      if (y >= 0 && y < SCREEN_HEIGHT) {
        float brightness = 1.0f - (trail / 8.0f);
        
        // Matrix green with some color variation
        float hue = 120 + sin(time_counter * 0.5f + i) * 30;
        uint16_t color = getColorFromHSV(hue, 1.0f, brightness);
        
        // Simple character rendering using rectangles
        char current_char = glyphs[drops[i][3]];
        int x = drops[i][0];
        
        // Draw character as a simple pattern
        if (current_char >= '0' && current_char <= '9') {
          // Numbers - draw as filled rect
          Disp.fillRect(x, y, 4, 6, color);
        } else if (current_char >= 'A' && current_char <= 'F') {
          // Letters - draw as outline
          Disp.drawRect(x, y, 4, 6, color);
          Disp.drawPixel(x + 2, y + 3, color);
        } else {
          // Symbols - draw as dots/lines
          Disp.drawPixel(x + 1, y + 1, color);
          Disp.drawPixel(x + 3, y + 3, color);
          Disp.drawPixel(x + 2, y + 5, color);
        }
      }
    }
  }
}

// Helper function for dragon curve generation
String generateDragonString(int iterations) {
  String result = "F";
  
  for (int i = 0; i < iterations; i++) {
    String newResult = "";
    for (int j = 0; j < result.length(); j++) {
      char c = result.charAt(j);
      if (c == 'F') {
        newResult += "F+F";
      } else if (c == '+') {
        newResult += i % 2 == 0 ? "L" : "R";
      } else {
        newResult += c;
      }
    }
    result = newResult;
    if (result.length() > 500) break; // Limit complexity
  }
  
  return result;
}

void drawHeavyRain() {
  // Heavy rain effect - intense downpour inspired by your Python version
  static int heavy_drops[30][3]; // x, y, speed - more drops for heavy rain
  static int splash_particles[20][4]; // x, y, vx, vy for splash effects
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize heavy rain drops
    for (int i = 0; i < 30; i++) {
      heavy_drops[i][0] = random(0, SCREEN_WIDTH);  // x
      heavy_drops[i][1] = random(-100, 0);          // y
      heavy_drops[i][2] = random(4, 8);             // faster speed for heavy rain
    }
    
    // Initialize splash particles
    for (int i = 0; i < 20; i++) {
      splash_particles[i][0] = -10; // inactive
      splash_particles[i][1] = -10;
      splash_particles[i][2] = 0;
      splash_particles[i][3] = 0;
    }
    initialized = true;
  }
  
  // Dark stormy background
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x18C3); // Dark blue-gray
  
  // Update and draw heavy rain drops
  for (int i = 0; i < 30; i++) {
    // Update position
    heavy_drops[i][1] += heavy_drops[i][2];
    
    // Create splash when drop hits bottom
    if (heavy_drops[i][1] >= SCREEN_HEIGHT - 5) {
      // Create splash particles
      for (int j = 0; j < 3; j++) { // Multiple splash particles per drop
        int splash_idx = (i * 3 + j) % 20;
        splash_particles[splash_idx][0] = heavy_drops[i][0];
        splash_particles[splash_idx][1] = SCREEN_HEIGHT - 5;
        splash_particles[splash_idx][2] = random(-3, 3); // horizontal velocity
        splash_particles[splash_idx][3] = random(-4, -1); // upward velocity
      }
      
      // Reset drop
      heavy_drops[i][0] = random(0, SCREEN_WIDTH);
      heavy_drops[i][1] = random(-50, -10);
      heavy_drops[i][2] = random(4, 8);
    }
    
    // Draw rain drop with storm colors
    int x = heavy_drops[i][0];
    int y = heavy_drops[i][1];
    
    if (y >= 0 && y < SCREEN_HEIGHT) {
      // Heavy rain is thicker and more intense
      uint16_t rain_color = getColorFromHSV(200 + sin(time_counter + i) * 30, 0.8f, 0.9f);
      
      // Draw thicker rain streaks
      for (int streak = 0; streak < 6; streak++) {
        int streak_y = y - streak * 2;
        if (streak_y >= 0) {
          float brightness = 1.0f - (streak / 6.0f);
          uint16_t streak_color = getColorFromHSV(200, 0.8f, brightness);
          Disp.drawPixel(x, streak_y, streak_color);
        }
      }
    }
  }
  
  // Update and draw splash particles
  for (int i = 0; i < 20; i++) {
    if (splash_particles[i][0] >= 0) { // Active particle
      // Update position
      splash_particles[i][0] += splash_particles[i][2];
      splash_particles[i][1] += splash_particles[i][3];
      splash_particles[i][3]++; // gravity
      
      // Remove if off screen or too old
      if (splash_particles[i][1] >= SCREEN_HEIGHT || splash_particles[i][3] > 3) {
        splash_particles[i][0] = -10; // deactivate
      } else {
        // Draw splash particle
        uint16_t splash_color = getColorFromHSV(180, 0.6f, 0.7f);
        Disp.drawPixel(splash_particles[i][0], splash_particles[i][1], splash_color);
      }
    }
  }
  
  // Add lightning effect occasionally
  if (random(1000) < 5) { // 0.5% chance per frame
    Disp.fillScreen(WHITE);
    delay(20); // Brief flash
  }
}

void drawJuliaSet() {
  // Julia set fractal inspired by your Python version
  static float c_real = -0.7f;
  static float c_imag = 0.27015f;
  static float param_time = 0;
  static int render_line = 0;
  
  param_time += 0.02f;
  
  // Animate Julia set parameters for dynamic effect
  c_real = -0.7f + 0.3f * sin(param_time * 0.7f);
  c_imag = 0.27015f + 0.2f * cos(param_time * 0.5f);
  
  // Render a few lines per frame for smooth animation
  for (int lines = 0; lines < 8 && render_line < SCREEN_HEIGHT; lines++) {
    int y = render_line;
    
    for (int x = 0; x < SCREEN_WIDTH; x++) {
      // Map pixel to complex plane
      float real = (x - SCREEN_WIDTH/2) * 4.0f / SCREEN_WIDTH;
      float imag = (y - SCREEN_HEIGHT/2) * 4.0f / SCREEN_HEIGHT;
      
      // Julia set iteration
      int iterations = 0;
      int max_iter = 25;
      
      for (iterations = 0; iterations < max_iter; iterations++) {
        float real2 = real * real;
        float imag2 = imag * imag;
        
        if (real2 + imag2 > 4.0f) break;
        
        float new_real = real2 - imag2 + c_real;
        float new_imag = 2 * real * imag + c_imag;
        
        real = new_real;
        imag = new_imag;
      }
      
      // Color based on iterations with psychedelic palette
      if (iterations == max_iter) {
        Disp.drawPixel(x, y, BLACK); // Inside set
      } else {
        float t = iterations / (float)max_iter;
        float hue = fmod(t * 360 + param_time * 100, 360);
        uint16_t color = getColorFromHSV(hue, 1.0f, 0.8f + 0.2f * sin(param_time + t * 6.28f));
        Disp.drawPixel(x, y, color);
      }
    }
    
    render_line++;
  }
  
  // Reset when finished rendering frame
  if (render_line >= SCREEN_HEIGHT) {
    render_line = 0;
  }
}

void drawMandelbrot() {
  // Mandelbrot set fractal inspired by your Python version
  static float zoom = 1.0f;
  static float center_x = -0.5f;
  static float center_y = 0.0f;
  static float zoom_speed = 1.02f;
  static int render_line = 0;
  static float color_offset = 0;
  
  zoom *= zoom_speed;
  color_offset += 2.0f;
  
  // Reset zoom when too close
  if (zoom > 100.0f) {
    zoom = 1.0f;
    // Change center point for variety
    center_x = -0.5f + random(-50, 50) / 100.0f;
    center_y = 0.0f + random(-50, 50) / 100.0f;
  }
  
  // Render a few lines per frame for smooth animation
  for (int lines = 0; lines < 6 && render_line < SCREEN_HEIGHT; lines++) {
    int y = render_line;
    
    for (int x = 0; x < SCREEN_WIDTH; x++) {
      // Map pixel to complex plane with zoom
      float real = center_x + (x - SCREEN_WIDTH/2) * 4.0f / (SCREEN_WIDTH * zoom);
      float imag = center_y + (y - SCREEN_HEIGHT/2) * 4.0f / (SCREEN_HEIGHT * zoom);
      
      // Mandelbrot iteration
      float z_real = 0;
      float z_imag = 0;
      int iterations = 0;
      int max_iter = 30;
      
      for (iterations = 0; iterations < max_iter; iterations++) {
        float z_real2 = z_real * z_real;
        float z_imag2 = z_imag * z_imag;
        
        if (z_real2 + z_imag2 > 4.0f) break;
        
        float new_z_real = z_real2 - z_imag2 + real;
        float new_z_imag = 2 * z_real * z_imag + imag;
        
        z_real = new_z_real;
        z_imag = new_z_imag;
      }
      
      // Color based on iterations with animated palette
      if (iterations == max_iter) {
        Disp.drawPixel(x, y, BLACK); // Inside set
      } else {
        float t = iterations / (float)max_iter;
        float hue = fmod(t * 270 + color_offset, 360);
        float saturation = 0.8f + 0.2f * sin(time_counter + t * 3.14f);
        float brightness = 0.4f + 0.6f * t;
        
        uint16_t color = getColorFromHSV(hue, saturation, brightness);
        Disp.drawPixel(x, y, color);
      }
    }
    
    render_line++;
  }
  
  // Reset when finished rendering frame
  if (render_line >= SCREEN_HEIGHT) {
    render_line = 0;
  }
}

void drawMatrixBinary() {
  // Matrix binary rain - mostly 1s and 0s inspired by your Python version
  static char binary_chars[] = "01";
  static char matrix_symbols[] = "!@#$%^&*()[]{}+-=<>?/\\|_~";
  static int drops[25][4]; // x, y, speed, char_type (0=binary, 1=symbol)
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize binary rain drops
    for (int i = 0; i < 25; i++) {
      drops[i][0] = i * (SCREEN_WIDTH / 25); // x position
      drops[i][1] = random(-100, 0);         // y position
      drops[i][2] = random(1, 3);            // speed
      drops[i][3] = random(100) < 90 ? 0 : 1; // 90% binary, 10% symbols
    }
    initialized = true;
  }
  
  // Dark background with green tint
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0020);
  
  for (int i = 0; i < 25; i++) {
    // Update drop position
    drops[i][1] += drops[i][2];
    
    // Reset drop when it goes off screen
    if (drops[i][1] > SCREEN_HEIGHT + 10) {
      drops[i][1] = random(-50, 0);
      drops[i][2] = random(1, 3);
      drops[i][3] = random(100) < 90 ? 0 : 1; // Refresh char type
    }
    
    // Change character occasionally for matrix effect
    if (random(100) < 15) {
      drops[i][3] = random(100) < 90 ? 0 : 1;
    }
    
    // Draw binary/symbol trail
    for (int trail = 0; trail < 12; trail++) {
      int y = drops[i][1] - trail * 6;
      if (y >= 0 && y < SCREEN_HEIGHT) {
        float brightness = 1.0f - (trail / 12.0f);
        
        // Matrix green with intensity variation
        uint16_t color = getColorFromHSV(120, 1.0f, brightness);
        
        // Choose character based on type
        int x = drops[i][0];
        
        if (drops[i][3] == 0) {
          // Binary characters - draw as rectangles
          char bin_char = binary_chars[random(2)];
          if (bin_char == '1') {
            Disp.fillRect(x, y, 3, 5, color);
          } else {
            Disp.drawRect(x, y, 3, 5, color);
          }
        } else {
          // Matrix symbols - draw as complex patterns
          Disp.fillRect(x, y, 2, 2, color);
          Disp.fillRect(x+2, y+2, 2, 2, color);
          Disp.drawPixel(x+1, y+4, color);
        }
      }
    }
  }
}

void drawMicroDots() {
  // Ultra-dense micro dots inspired by your Python version
  static int dots[100][3]; // x, y, speed - maximum density!
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize micro dots everywhere
    for (int i = 0; i < 100; i++) {
      dots[i][0] = random(0, SCREEN_WIDTH);   // x
      dots[i][1] = random(-200, 0);           // y (spread over larger area)
      dots[i][2] = random(1, 4);              // speed
    }
    initialized = true;
  }
  
  // Very dark background for contrast
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0841);
  
  // Update and draw micro dots
  for (int i = 0; i < 100; i++) {
    // Update position
    dots[i][1] += dots[i][2];
    
    // Reset dot when off screen
    if (dots[i][1] > SCREEN_HEIGHT + 5) {
      dots[i][0] = random(0, SCREEN_WIDTH);
      dots[i][1] = random(-50, 0);
      dots[i][2] = random(1, 4);
    }
    
    // Draw micro dot with neon colors
    int x = dots[i][0];
    int y = dots[i][1];
    
    if (y >= 0 && y < SCREEN_HEIGHT && x >= 0 && x < SCREEN_WIDTH) {
      // Alternate between neon green and blue
      float hue = (i % 2 == 0) ? 120 : 240; // Green or blue
      hue += sin(time_counter * 0.1f + i * 0.5f) * 30; // Slight color variation
      
      uint16_t dot_color = getColorFromHSV(hue, 1.0f, 1.0f);
      
      // Draw single pixel dot
      Disp.drawPixel(x, y, dot_color);
      
      // Occasionally add a slight glow for variety
      if (random(100) < 5) {
        Disp.drawPixel(x+1, y, dot_color);
        Disp.drawPixel(x, y+1, dot_color);
      }
    }
  }
}

void drawRaindrops() {
  // Realistic raindrops inspired by your Python version
  static int raindrops[20][4]; // x, y, speed, size
  static int splash_particles[15][4]; // x, y, vx, vy
  static int puddles[SCREEN_WIDTH]; // puddle height at each x position
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize raindrops
    for (int i = 0; i < 20; i++) {
      raindrops[i][0] = random(0, SCREEN_WIDTH);  // x
      raindrops[i][1] = random(-100, 0);          // y
      raindrops[i][2] = random(2, 5);             // speed
      raindrops[i][3] = random(2, 4);             // size
    }
    
    // Initialize splash particles (inactive)
    for (int i = 0; i < 15; i++) {
      splash_particles[i][0] = -10;
      splash_particles[i][1] = -10;
    }
    
    // Initialize puddles
    for (int i = 0; i < SCREEN_WIDTH; i++) {
      puddles[i] = 0;
    }
    
    initialized = true;
  }
  
  // Cloudy sky background
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x39C7); // Light gray-blue
  
  // Update and draw raindrops
  for (int i = 0; i < 20; i++) {
    // Update position
    raindrops[i][1] += raindrops[i][2];
    
    // Create splash when drop hits bottom
    if (raindrops[i][1] >= SCREEN_HEIGHT - 3) {
      // Add to puddle
      int x = raindrops[i][0];
      if (x >= 0 && x < SCREEN_WIDTH) {
        puddles[x] = min(puddles[x] + 1, 5); // Max puddle height
        
        // Create splash particle
        int splash_idx = i % 15;
        splash_particles[splash_idx][0] = x;
        splash_particles[splash_idx][1] = SCREEN_HEIGHT - puddles[x];
        splash_particles[splash_idx][2] = random(-2, 2); // horizontal velocity
        splash_particles[splash_idx][3] = random(-3, -1); // upward velocity
      }
      
      // Reset raindrop
      raindrops[i][0] = random(0, SCREEN_WIDTH);
      raindrops[i][1] = random(-50, -10);
      raindrops[i][2] = random(2, 5);
      raindrops[i][3] = random(2, 4);
    }
    
    // Draw raindrop
    int x = raindrops[i][0];
    int y = raindrops[i][1];
    int size = raindrops[i][3];
    
    if (y >= 0 && y < SCREEN_HEIGHT - 5) {
      // Water blue colors
      uint16_t water_color = getColorFromHSV(200 + sin(time_counter + i) * 20, 0.7f, 0.9f);
      
      // Draw teardrop shape
      for (int dy = 0; dy < size + 2; dy++) {
        if (y + dy < SCREEN_HEIGHT) {
          float width = (size / 2.0f) * (1.0f - dy / (float)(size + 2));
          for (int dx = -width; dx <= width; dx++) {
            if (x + dx >= 0 && x + dx < SCREEN_WIDTH) {
              Disp.drawPixel(x + dx, y + dy, water_color);
            }
          }
        }
      }
    }
  }
  
  // Draw puddles
  for (int x = 0; x < SCREEN_WIDTH; x++) {
    if (puddles[x] > 0) {
      uint16_t puddle_color = getColorFromHSV(210, 0.6f, 0.7f);
      Disp.fillRect(x, SCREEN_HEIGHT - puddles[x], 1, puddles[x], puddle_color);
      
      // Slowly evaporate puddles
      if (random(1000) < 3) {
        puddles[x] = max(0, puddles[x] - 1);
      }
    }
  }
  
  // Update splash particles
  for (int i = 0; i < 15; i++) {
    if (splash_particles[i][0] >= 0) { // Active particle
      // Update position
      splash_particles[i][0] += splash_particles[i][2];
      splash_particles[i][1] += splash_particles[i][3];
      splash_particles[i][3]++; // gravity
      
      // Remove if off screen
      if (splash_particles[i][1] >= SCREEN_HEIGHT || splash_particles[i][3] > 2) {
        splash_particles[i][0] = -10; // deactivate
      } else {
        // Draw splash particle
        uint16_t splash_color = getColorFromHSV(190, 0.5f, 0.8f);
        Disp.drawPixel(splash_particles[i][0], splash_particles[i][1], splash_color);
      }
    }
  }
}

void drawRetroGeometry() {
  // 1990s style geometric screensaver inspired by your Python version
  static float shapes[10][6]; // x, y, size, rotation, type, color_index
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize geometric shapes
    for (int i = 0; i < 10; i++) {
      shapes[i][0] = random(0, SCREEN_WIDTH);   // x
      shapes[i][1] = random(0, SCREEN_HEIGHT);  // y
      shapes[i][2] = random(10, 30);            // size
      shapes[i][3] = random(0, 360);            // rotation
      shapes[i][4] = random(0, 4);              // type (0=square, 1=circle, 2=triangle, 3=diamond)
      shapes[i][5] = random(0, 12);             // color index
    }
    initialized = true;
  }
  
  // Dark retro background
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0841);
  
  for (int i = 0; i < 10; i++) {
    // Update rotation
    shapes[i][3] += 2.0f;
    if (shapes[i][3] >= 360) shapes[i][3] -= 360;
    
    // Get shape properties
    int x = shapes[i][0];
    int y = shapes[i][1]; 
    int size = shapes[i][2];
    float rotation = shapes[i][3];
    int type = shapes[i][4];
    
    // Add color cycling
    float hue = fmod((shapes[i][5] * 30) + time_counter * 50, 360);
    uint16_t color = getColorFromHSV(hue, 1.0f, 1.0f);
    
    // Draw shape based on type
    switch (type) {
      case 0: // Rotating square
        {
          int half = size / 2;
          Disp.drawRect(x - half, y - half, size, size, color);
          if ((int)rotation % 45 < 23) {
            Disp.fillRect(x - half + 2, y - half + 2, size - 4, size - 4, color);
          }
        }
        break;
        
      case 1: // Pulsing circle
        {
          int pulse_size = size + sin(time_counter * 2 + i) * 5;
          Disp.drawCircle(x, y, pulse_size / 2, color);
          if ((int)rotation % 60 < 30) {
            Disp.fillCircle(x, y, pulse_size / 4, color);
          }
        }
        break;
        
      case 2: // Triangle
        {
          int half = size / 2;
          Disp.drawLine(x, y - half, x - half, y + half, color);
          Disp.drawLine(x, y - half, x + half, y + half, color);
          Disp.drawLine(x - half, y + half, x + half, y + half, color);
        }
        break;
        
      case 3: // Diamond
        {
          int half = size / 2;
          Disp.drawLine(x, y - half, x + half, y, color);
          Disp.drawLine(x + half, y, x, y + half, color);
          Disp.drawLine(x, y + half, x - half, y, color);
          Disp.drawLine(x - half, y, x, y - half, color);
        }
        break;
    }
    
    // Slowly move shapes
    shapes[i][0] += sin(time_counter * 0.1f + i) * 0.5f;
    shapes[i][1] += cos(time_counter * 0.1f + i) * 0.5f;
    
    // Wrap around screen
    if (shapes[i][0] < -size) shapes[i][0] = SCREEN_WIDTH + size;
    if (shapes[i][0] > SCREEN_WIDTH + size) shapes[i][0] = -size;
    if (shapes[i][1] < -size) shapes[i][1] = SCREEN_HEIGHT + size;
    if (shapes[i][1] > SCREEN_HEIGHT + size) shapes[i][1] = -size;
  }
}

void drawSierpinski() {
  // Sierpinski triangle using chaos game algorithm inspired by your Python version
  static float current_x = SCREEN_WIDTH / 2;
  static float current_y = SCREEN_HEIGHT / 2;
  static int points_drawn = 0;
  static float vertices[3][2] = {
    {SCREEN_WIDTH / 2, 10},           // Top
    {10, SCREEN_HEIGHT - 10},         // Bottom left
    {SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10}  // Bottom right
  };
  
  // Clear screen occasionally to start fresh
  if (points_drawn == 0) {
    Disp.fillScreen(BLACK);
  }
  
  // Draw many points per frame for faster generation
  for (int i = 0; i < 50; i++) {
    // Choose random vertex
    int vertex = random(0, 3);
    
    // Move halfway to chosen vertex
    current_x = (current_x + vertices[vertex][0]) / 2.0f;
    current_y = (current_y + vertices[vertex][1]) / 2.0f;
    
    // Color based on which vertex was chosen and time
    float hue = vertex * 120 + time_counter * 30; // Different color per vertex
    hue = fmod(hue, 360);
    uint16_t color = getColorFromHSV(hue, 1.0f, 0.9f);
    
    // Draw the point
    if (current_x >= 0 && current_x < SCREEN_WIDTH && 
        current_y >= 0 && current_y < SCREEN_HEIGHT) {
      Disp.drawPixel((int)current_x, (int)current_y, color);
    }
    
    points_drawn++;
  }
  
  // Reset after drawing many points
  if (points_drawn > 5000) {
    points_drawn = 0;
    current_x = SCREEN_WIDTH / 2;
    current_y = SCREEN_HEIGHT / 2;
  }
  
  // Draw the three vertices as reference points
  for (int i = 0; i < 3; i++) {
    float hue = i * 120 + time_counter * 30;
    uint16_t vertex_color = getColorFromHSV(hue, 1.0f, 1.0f);
    Disp.fillCircle(vertices[i][0], vertices[i][1], 3, vertex_color);
  }
}

void drawSimpleFlames() {
  // Simple flame effect inspired by your Python version
  static int flame_particles[40][4]; // x, y, life, heat
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize flame particles
    for (int i = 0; i < 40; i++) {
      flame_particles[i][0] = random(0, SCREEN_WIDTH);  // x
      flame_particles[i][1] = SCREEN_HEIGHT;            // y (start at bottom)
      flame_particles[i][2] = random(20, 60);           // life
      flame_particles[i][3] = random(100, 255);         // heat
    }
    initialized = true;
  }
  
  // Dark background
  Disp.fillScreen(BLACK);
  
  // Update and draw flame particles
  for (int i = 0; i < 40; i++) {
    // Update particle
    flame_particles[i][1] -= 2; // Rise up
    flame_particles[i][2]--;    // Decrease life
    flame_particles[i][3] = max(0, flame_particles[i][3] - 3); // Cool down
    
    // Add some horizontal drift
    flame_particles[i][0] += random(-1, 2);
    
    // Reset particle when it dies or goes off screen
    if (flame_particles[i][2] <= 0 || flame_particles[i][1] < -10) {
      flame_particles[i][0] = random(20, SCREEN_WIDTH - 20);
      flame_particles[i][1] = SCREEN_HEIGHT - random(0, 10);
      flame_particles[i][2] = random(30, 80);
      flame_particles[i][3] = random(150, 255);
    }
    
    // Draw flame particle
    int x = flame_particles[i][0];
    int y = flame_particles[i][1];
    int heat = flame_particles[i][3];
    int life = flame_particles[i][2];
    
    if (x >= 0 && x < SCREEN_WIDTH && y >= 0 && y < SCREEN_HEIGHT) {
      // Color based on heat (red -> orange -> yellow -> white)
      uint16_t flame_color;
      
      if (heat > 200) {
        // Hot: yellow to white
        flame_color = getColorFromHSV(60, 1.0f - (heat - 200) / 55.0f, 1.0f);
      } else if (heat > 120) {
        // Medium: orange to yellow  
        float t = (heat - 120) / 80.0f;
        flame_color = getColorFromHSV(20 + t * 40, 1.0f, 1.0f);
      } else {
        // Cool: red to orange
        float t = heat / 120.0f;
        flame_color = getColorFromHSV(t * 20, 1.0f, 0.8f + t * 0.2f);
      }
      
      // Draw particle with some flickering
      Disp.drawPixel(x, y, flame_color);
      
      // Add glow for hotter particles
      if (heat > 180 && random(100) < 50) {
        if (x > 0) Disp.drawPixel(x - 1, y, flame_color);
        if (x < SCREEN_WIDTH - 1) Disp.drawPixel(x + 1, y, flame_color);
        if (y > 0) Disp.drawPixel(x, y - 1, flame_color);
      }
    }
  }
  
  // Draw fire base
  for (int x = 0; x < SCREEN_WIDTH; x++) {
    for (int y = SCREEN_HEIGHT - 5; y < SCREEN_HEIGHT; y++) {
      if (random(100) < 70) {
        uint16_t base_color = getColorFromHSV(random(0, 40), 1.0f, 0.6f);
        Disp.drawPixel(x, y, base_color);
      }
    }
  }
}

void drawWalkingTriangle() {
  // Classic 90s "Walking Shape" screensaver - triangle leaves a trail
  static float triangle_x = SCREEN_WIDTH / 2;
  static float triangle_y = SCREEN_HEIGHT / 2;
  static float triangle_size = 15;
  static float triangle_rotation = 0;
  static int step_counter = 0;
  static float color_hue = 0;
  
  // Don't clear the screen! That's the key - we want to see the trail
  // Only clear occasionally to prevent complete fill
  if (step_counter == 0) {
    Disp.fillScreen(BLACK);
  }
  
  // Classic 90s random walk - small steps in random directions
  float step_size = 3.0f;
  float angle = random(0, 360) * PI / 180.0f;
  
  // Move the triangle
  triangle_x += cos(angle) * step_size;
  triangle_y += sin(angle) * step_size;
  
  // Wrap around screen edges
  if (triangle_x < 0) triangle_x = SCREEN_WIDTH;
  if (triangle_x > SCREEN_WIDTH) triangle_x = 0;
  if (triangle_y < 0) triangle_y = SCREEN_HEIGHT;
  if (triangle_y > SCREEN_HEIGHT) triangle_y = 0;
  
  // Slowly rotate the triangle
  triangle_rotation += 2.0f;
  if (triangle_rotation >= 360) triangle_rotation -= 360;
  
  // Cycle through rainbow colors
  color_hue += 3.0f;
  if (color_hue >= 360) color_hue -= 360;
  
  uint16_t triangle_color = getColorFromHSV(color_hue, 1.0f, 0.9f);
  
  // Calculate triangle vertices with rotation
  float rad = triangle_rotation * PI / 180.0f;
  float cos_r = cos(rad);
  float sin_r = sin(rad);
  
  // Triangle points (equilateral triangle)
  float px1 = 0;
  float py1 = -triangle_size;
  float px2 = -triangle_size * 0.866f;  // cos(60°) ≈ 0.866
  float py2 = triangle_size * 0.5f;
  float px3 = triangle_size * 0.866f;
  float py3 = triangle_size * 0.5f;
  
  // Rotate and translate triangle points
  int x1 = triangle_x + (px1 * cos_r - py1 * sin_r);
  int y1 = triangle_y + (px1 * sin_r + py1 * cos_r);
  int x2 = triangle_x + (px2 * cos_r - py2 * sin_r);
  int y2 = triangle_y + (px2 * sin_r + py2 * cos_r);
  int x3 = triangle_x + (px3 * cos_r - py3 * sin_r);
  int y3 = triangle_y + (px3 * sin_r + py3 * cos_r);
  
  // Draw the triangle at current position
  Disp.drawLine(x1, y1, x2, y2, triangle_color);
  Disp.drawLine(x2, y2, x3, y3, triangle_color);
  Disp.drawLine(x3, y3, x1, y1, triangle_color);
  
  // Sometimes fill the triangle for variety
  if (step_counter % 20 < 10) {
    // Simple triangle fill - draw a few lines inside
    int center_x = (x1 + x2 + x3) / 3;
    int center_y = (y1 + y2 + y3) / 3;
    
    // Draw lines from center to edges for fill effect
    Disp.drawLine(center_x, center_y, x1, y1, triangle_color);
    Disp.drawLine(center_x, center_y, x2, y2, triangle_color);
    Disp.drawLine(center_x, center_y, x3, y3, triangle_color);
  }
  
  step_counter++;
  
  // Clear screen every so often to prevent complete fill
  if (step_counter > 400) {
    step_counter = 0;
  }
}

void drawWalkingSquare() {
  // Walking square that leaves a geometric trail - even better than 90s!
  static float square_x = SCREEN_WIDTH / 2;
  static float square_y = SCREEN_HEIGHT / 2;
  static float square_size = 12;
  static float square_rotation = 0;
  static int step_counter = 0;
  static float color_hue = 120; // Start with green
  
  // Only clear occasionally
  if (step_counter == 0) {
    Disp.fillScreen(BLACK);
  }
  
  // More interesting movement pattern - spiral tendency
  float step_size = 2.5f;
  float angle = random(0, 360) * PI / 180.0f;
  
  // Add slight bias toward center for more interesting patterns
  if (square_x > SCREEN_WIDTH * 0.75f) angle += PI * 0.25f;  // Turn left
  if (square_x < SCREEN_WIDTH * 0.25f) angle -= PI * 0.25f;  // Turn right
  if (square_y > SCREEN_HEIGHT * 0.75f) angle += PI * 0.5f;  // Turn up
  if (square_y < SCREEN_HEIGHT * 0.25f) angle -= PI * 0.5f;  // Turn down
  
  square_x += cos(angle) * step_size;
  square_y += sin(angle) * step_size;
  
  // Wrap edges
  if (square_x < 0) square_x = SCREEN_WIDTH;
  if (square_x > SCREEN_WIDTH) square_x = 0;
  if (square_y < 0) square_y = SCREEN_HEIGHT;
  if (square_y > SCREEN_HEIGHT) square_y = 0;
  
  // Dynamic rotation and scaling
  square_rotation += 3.0f;
  square_size = 12 + sin(step_counter * 0.05f) * 4; // Breathing effect
  
  // Color shifting
  color_hue += 2.0f;
  if (color_hue >= 360) color_hue -= 360;
  
  uint16_t square_color = getColorFromHSV(color_hue, 1.0f, 0.9f);
  
  // Calculate rotated square vertices
  float rad = square_rotation * PI / 180.0f;
  float cos_r = cos(rad);
  float sin_r = sin(rad);
  float half_size = square_size / 2.0f;
  
  // Square corners
  int x1 = square_x + (-half_size * cos_r - (-half_size) * sin_r);
  int y1 = square_y + (-half_size * sin_r + (-half_size) * cos_r);
  int x2 = square_x + (half_size * cos_r - (-half_size) * sin_r);
  int y2 = square_y + (half_size * sin_r + (-half_size) * cos_r);
  int x3 = square_x + (half_size * cos_r - half_size * sin_r);
  int y3 = square_y + (half_size * sin_r + half_size * cos_r);
  int x4 = square_x + (-half_size * cos_r - half_size * sin_r);
  int y4 = square_y + (-half_size * sin_r + half_size * cos_r);
  
  // Draw the square
  Disp.drawLine(x1, y1, x2, y2, square_color);
  Disp.drawLine(x2, y2, x3, y3, square_color);
  Disp.drawLine(x3, y3, x4, y4, square_color);
  Disp.drawLine(x4, y4, x1, y1, square_color);
  
  // Add diagonal lines for extra geometric beauty
  if (step_counter % 15 < 8) {
    Disp.drawLine(x1, y1, x3, y3, square_color);
    Disp.drawLine(x2, y2, x4, y4, square_color);
  }
  
  step_counter++;
  if (step_counter > 350) {
    step_counter = 0;
  }
}

void drawWalkingStar() {
  // Walking 5-pointed star - my creative addition!
  static float star_x = SCREEN_WIDTH / 2;
  static float star_y = SCREEN_HEIGHT / 2;
  static float star_size = 10;
  static float star_rotation = 0;
  static int step_counter = 0;
  static float color_hue = 270; // Start with purple
  
  if (step_counter == 0) {
    Disp.fillScreen(BLACK);
  }
  
  // Chaotic movement with occasional sudden direction changes
  float step_size = 2.0f;
  static float momentum_angle = 0;
  
  if (random(100) < 85) {
    // Mostly continue in same direction with slight variation
    momentum_angle += (random(-30, 30) * PI / 180.0f);
  } else {
    // Sudden direction change!
    momentum_angle = random(0, 360) * PI / 180.0f;
  }
  
  star_x += cos(momentum_angle) * step_size;
  star_y += sin(momentum_angle) * step_size;
  
  // Wrap edges
  if (star_x < 0) star_x = SCREEN_WIDTH;
  if (star_x > SCREEN_WIDTH) star_x = 0;
  if (star_y < 0) star_y = SCREEN_HEIGHT;
  if (star_y > SCREEN_HEIGHT) star_y = 0;
  
  // Fast rotation and pulsing
  star_rotation += 5.0f;
  star_size = 10 + sin(step_counter * 0.1f) * 3;
  
  // Rapid color cycling
  color_hue += 4.0f;
  if (color_hue >= 360) color_hue -= 360;
  
  uint16_t star_color = getColorFromHSV(color_hue, 1.0f, 1.0f);
  
  // Draw 5-pointed star
  float rad = star_rotation * PI / 180.0f;
  
  // Calculate star points (5 outer points, 5 inner points)
  int star_points[10][2];
  for (int i = 0; i < 10; i++) {
    float angle = (i * 36.0f - 90.0f + star_rotation) * PI / 180.0f;
    float radius = (i % 2 == 0) ? star_size : star_size * 0.4f; // Outer/inner radius
    
    star_points[i][0] = star_x + cos(angle) * radius;
    star_points[i][1] = star_y + sin(angle) * radius;
  }
  
  // Draw star outline
  for (int i = 0; i < 10; i++) {
    int next = (i + 1) % 10;
    Disp.drawLine(star_points[i][0], star_points[i][1], 
                  star_points[next][0], star_points[next][1], star_color);
  }
  
  // Add center burst lines occasionally
  if (step_counter % 25 < 12) {
    for (int i = 0; i < 5; i++) {
      Disp.drawLine(star_x, star_y, 
                    star_points[i * 2][0], star_points[i * 2][1], star_color);
    }
  }
  
  step_counter++;
  if (step_counter > 300) {
    step_counter = 0;
  }
}

void drawSpirograph() {
  // Classic Spirograph curves - mathematical beauty!
  static float R = 40;  // Outer radius
  static float r = 15;  // Inner radius  
  static float d = 20;  // Distance from center of inner circle
  static float t = 0;   // Parameter
  static float color_offset = 0;
  
  // Don't clear screen - let the curves build up!
  static int frame_count = 0;
  if (frame_count == 0) {
    Disp.fillScreen(BLACK);
  }
  
  // Calculate spirograph point
  float k = r / R;
  float x = (R - r) * cos(t) + d * cos((1 - k) * t / k);
  float y = (R - r) * sin(t) - d * sin((1 - k) * t / k);
  
  // Center on screen
  int screen_x = SCREEN_WIDTH / 2 + x;
  int screen_y = SCREEN_HEIGHT / 2 + y;
  
  // Rainbow color based on position
  float hue = fmod(color_offset + t * 20, 360);
  uint16_t curve_color = getColorFromHSV(hue, 1.0f, 0.9f);
  
  // Draw the point and a small trail
  if (screen_x >= 0 && screen_x < SCREEN_WIDTH && screen_y >= 0 && screen_y < SCREEN_HEIGHT) {
    Disp.fillCircle(screen_x, screen_y, 2, curve_color);
    
    // Add glow effect
    Disp.drawPixel(screen_x + 1, screen_y, curve_color);
    Disp.drawPixel(screen_x - 1, screen_y, curve_color);
    Disp.drawPixel(screen_x, screen_y + 1, curve_color);
    Disp.drawPixel(screen_x, screen_y - 1, curve_color);
  }
  
  // Increment parameters
  t += 0.15f;
  color_offset += 0.5f;
  
  frame_count++;
  
  // Slowly change spirograph parameters for variety
  if (frame_count > 800) {
    R = 30 + sin(millis() * 0.001f) * 15;
    r = 10 + cos(millis() * 0.0015f) * 8;
    d = 15 + sin(millis() * 0.002f) * 10;
    frame_count = 0;
    t = 0;
  }
}

void drawRecursivePolygons() {
  // Nested rotating polygons with pulse effects
  static float rotation = 0;
  static float pulse_phase = 0;
  
  Disp.fillScreen(BLACK);
  
  rotation += 2.0f;
  pulse_phase += 0.1f;
  
  // Draw multiple nested polygons
  for (int level = 0; level < 6; level++) {
    float size = 50 - level * 6 + sin(pulse_phase + level) * 4; // Pulsing size
    float angle_offset = rotation + level * 15; // Different rotation speeds
    int sides = 6; // Hexagons
    
    // Color based on level and time
    float hue = fmod(level * 60 + rotation * 2, 360);
    uint16_t poly_color = getColorFromHSV(hue, 1.0f, 0.8f - level * 0.1f);
    
    // Calculate polygon vertices
    float center_x = SCREEN_WIDTH / 2;
    float center_y = SCREEN_HEIGHT / 2;
    
    for (int i = 0; i < sides; i++) {
      float angle1 = (i * 360.0f / sides + angle_offset) * PI / 180.0f;
      float angle2 = ((i + 1) * 360.0f / sides + angle_offset) * PI / 180.0f;
      
      int x1 = center_x + cos(angle1) * size;
      int y1 = center_y + sin(angle1) * size;
      int x2 = center_x + cos(angle2) * size;
      int y2 = center_y + sin(angle2) * size;
      
      // Draw polygon edge
      if (x1 >= 0 && x1 < SCREEN_WIDTH && y1 >= 0 && y1 < SCREEN_HEIGHT &&
          x2 >= 0 && x2 < SCREEN_WIDTH && y2 >= 0 && y2 < SCREEN_HEIGHT) {
        Disp.drawLine(x1, y1, x2, y2, poly_color);
        
        // Add vertices as dots
        Disp.fillCircle(x1, y1, 1, poly_color);
      }
    }
    
    // Connect to center occasionally for web effect
    if (level % 2 == 0) {
      for (int i = 0; i < sides; i++) {
        float angle = (i * 360.0f / sides + angle_offset) * PI / 180.0f;
        int x = center_x + cos(angle) * size;
        int y = center_y + sin(angle) * size;
        
        if (x >= 0 && x < SCREEN_WIDTH && y >= 0 && y < SCREEN_HEIGHT) {
          Disp.drawLine(center_x, center_y, x, y, poly_color);
        }
      }
    }
  }
}

void drawFlowField() {
  // Flow field particles - organic energy motion
  static float particles[80][4]; // x, y, vx, vy
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize particles
    for (int i = 0; i < 80; i++) {
      particles[i][0] = random(0, SCREEN_WIDTH);  // x
      particles[i][1] = random(0, SCREEN_HEIGHT); // y
      particles[i][2] = 0; // vx
      particles[i][3] = 0; // vy
    }
    initialized = true;
  }
  
  // Fade background for trail effect
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x1082);
  
  float flow_time = millis() * 0.002f;
  
  // Update and draw particles
  for (int i = 0; i < 80; i++) {
    float x = particles[i][0];
    float y = particles[i][1];
    
    // Calculate flow field force based on position and time
    float force_x = sin(x * 0.02f + flow_time) * cos(y * 0.015f + flow_time * 1.3f);
    float force_y = cos(x * 0.015f + flow_time * 0.7f) * sin(y * 0.02f + flow_time);
    
    // Apply force to velocity
    particles[i][2] += force_x * 0.3f;
    particles[i][3] += force_y * 0.3f;
    
    // Damping
    particles[i][2] *= 0.95f;
    particles[i][3] *= 0.95f;
    
    // Update position
    particles[i][0] += particles[i][2];
    particles[i][1] += particles[i][3];
    
    // Wrap around edges
    if (particles[i][0] < 0) particles[i][0] = SCREEN_WIDTH;
    if (particles[i][0] >= SCREEN_WIDTH) particles[i][0] = 0;
    if (particles[i][1] < 0) particles[i][1] = SCREEN_HEIGHT;
    if (particles[i][1] >= SCREEN_HEIGHT) particles[i][1] = 0;
    
    // Color based on velocity and position
    float speed = sqrt(particles[i][2] * particles[i][2] + particles[i][3] * particles[i][3]);
    float hue = fmod(i * 15 + flow_time * 50 + speed * 100, 360);
    uint16_t particle_color = getColorFromHSV(hue, 1.0f, 0.7f + speed * 0.3f);
    
    // Draw particle
    int px = (int)particles[i][0];
    int py = (int)particles[i][1];
    
    if (px >= 0 && px < SCREEN_WIDTH && py >= 0 && py < SCREEN_HEIGHT) {
      Disp.fillCircle(px, py, 1 + speed * 2, particle_color);
      
      // Draw velocity vector as a short line
      int tail_x = px - particles[i][2] * 3;
      int tail_y = py - particles[i][3] * 3;
      if (tail_x >= 0 && tail_x < SCREEN_WIDTH && tail_y >= 0 && tail_y < SCREEN_HEIGHT) {
        Disp.drawLine(px, py, tail_x, tail_y, particle_color);
      }
    }
  }
}

void drawColorShimmer() {
  // Digital acid shimmer - living noise cloud with hue cycling
  static float shimmer_time = 0;
  static float hue_offset = 0;
  
  shimmer_time += 0.05f;
  hue_offset += 2.0f;
  if (hue_offset >= 360) hue_offset -= 360;
  
  // Create shimmering pixel field
  for (int y = 0; y < SCREEN_HEIGHT; y += 2) { // Skip pixels for performance
    for (int x = 0; x < SCREEN_WIDTH; x += 2) {
      // Multi-layer noise for complex shimmer
      float noise1 = sin(x * 0.1f + shimmer_time * 3.0f) * cos(y * 0.08f + shimmer_time * 2.5f);
      float noise2 = sin(x * 0.15f - shimmer_time * 2.0f) * sin(y * 0.12f + shimmer_time * 1.8f);
      float noise3 = cos(x * 0.05f + shimmer_time * 4.0f) * cos(y * 0.06f - shimmer_time * 3.2f);
      
      float combined_noise = (noise1 + noise2 + noise3) / 3.0f;
      
      // Map noise to color
      float hue = fmod(hue_offset + combined_noise * 180 + (x + y) * 2, 360);
      float saturation = 0.8f + combined_noise * 0.2f;
      float brightness = 0.4f + (combined_noise + 1) * 0.3f; // 0.4 to 1.0
      
      uint16_t shimmer_color = getColorFromHSV(hue, saturation, brightness);
      
      // Draw 2x2 blocks for better visibility
      Disp.fillRect(x, y, 2, 2, shimmer_color);
    }
  }
  
  // Add some brighter sparkles
  for (int i = 0; i < 15; i++) {
    int sparkle_x = random(0, SCREEN_WIDTH);
    int sparkle_y = random(0, SCREEN_HEIGHT);
    
    float sparkle_noise = sin(shimmer_time * 5 + i) + cos(shimmer_time * 3.7f + i * 1.3f);
    if (sparkle_noise > 1.2f) {
      uint16_t sparkle_color = getColorFromHSV(fmod(hue_offset + i * 25, 360), 1.0f, 1.0f);
      Disp.fillCircle(sparkle_x, sparkle_y, 2, sparkle_color);
    }
  }
}

void drawStarfieldWarp() {
  // Classic Starfield Warp - simple but spectacular!
  static float stars[60][4]; // x, y, z, color_hue
  static bool initialized = false;
  static float warp_speed = 1.0f;
  
  if (!initialized) {
    // Initialize stars in 3D space
    for (int i = 0; i < 60; i++) {
      stars[i][0] = (random(200) - 100) / 10.0f; // x: -10 to 10
      stars[i][1] = (random(200) - 100) / 10.0f; // y: -10 to 10  
      stars[i][2] = random(50, 200) / 10.0f;     // z: 5 to 20
      stars[i][3] = random(0, 360);              // color hue
    }
    initialized = true;
  }
  
  // Dark space background
  Disp.fillScreen(0x0020);
  
  // Warp speed varies for dynamic effect
  warp_speed = 2.0f + sin(millis() * 0.001f) * 1.5f;
  
  // Update and draw each star
  for (int i = 0; i < 60; i++) {
    // Move star toward camera
    stars[i][2] -= warp_speed;
    
    // Reset star when it goes behind camera
    if (stars[i][2] <= 0.1f) {
      stars[i][0] = (random(200) - 100) / 10.0f;
      stars[i][1] = (random(200) - 100) / 10.0f;
      stars[i][2] = 20.0f;
      stars[i][3] = random(0, 360);
    }
    
    // Project 3D to 2D screen coordinates
    float projected_x = (stars[i][0] / stars[i][2]) * 40 + SCREEN_WIDTH / 2;
    float projected_y = (stars[i][1] / stars[i][2]) * 40 + SCREEN_HEIGHT / 2;
    
    // Only draw if on screen
    if (projected_x >= 0 && projected_x < SCREEN_WIDTH && 
        projected_y >= 0 && projected_y < SCREEN_HEIGHT) {
      
      // Star brightness based on distance (closer = brighter)
      float brightness = 1.0f - (stars[i][2] / 20.0f);
      brightness = max(0.2f, brightness);
      
      // Star size based on distance and speed
      int star_size = 1 + (brightness * 3);
      
      // Color shifts during warp
      float hue = fmod(stars[i][3] + warp_speed * 20, 360);
      uint16_t star_color = getColorFromHSV(hue, 0.8f, brightness);
      
      // Draw star with glow
      Disp.fillCircle((int)projected_x, (int)projected_y, star_size, star_color);
      
      // Draw warp trail for fast-moving stars
      if (warp_speed > 3.0f) {
        // Calculate trail end point
        float trail_z = stars[i][2] + warp_speed * 2;
        float trail_x = (stars[i][0] / trail_z) * 40 + SCREEN_WIDTH / 2;
        float trail_y = (stars[i][1] / trail_z) * 40 + SCREEN_HEIGHT / 2;
        
        if (trail_x >= 0 && trail_x < SCREEN_WIDTH && 
            trail_y >= 0 && trail_y < SCREEN_HEIGHT) {
          uint16_t trail_color = getColorFromHSV(hue, 0.6f, brightness * 0.5f);
          Disp.drawLine((int)projected_x, (int)projected_y, 
                        (int)trail_x, (int)trail_y, trail_color);
        }
      }
    }
  }
  
  // Add some center glow during high warp
  if (warp_speed > 3.5f) {
    int center_x = SCREEN_WIDTH / 2;
    int center_y = SCREEN_HEIGHT / 2;
    
    for (int ring = 1; ring <= 3; ring++) {
      float ring_hue = fmod(millis() * 0.1f + ring * 60, 360);
      uint16_t ring_color = getColorFromHSV(ring_hue, 1.0f, 0.3f);
      Disp.drawCircle(center_x, center_y, ring * 8, ring_color);
    }
  }
}

void drawFireflySwarm() {
  // Glowing fireflies with organic movement and trails
  static float fireflies[25][6]; // x, y, vx, vy, glow_phase, hue
  static bool initialized = false;
  
  if (!initialized) {
    // Initialize fireflies
    for (int i = 0; i < 25; i++) {
      fireflies[i][0] = random(0, SCREEN_WIDTH);   // x
      fireflies[i][1] = random(0, SCREEN_HEIGHT);  // y
      fireflies[i][2] = (random(100) - 50) / 50.0f; // vx
      fireflies[i][3] = (random(100) - 50) / 50.0f; // vy
      fireflies[i][4] = random(0, 628) / 100.0f;   // glow_phase
      fireflies[i][5] = random(0, 360);            // hue
    }
    initialized = true;
  }
  
  // Fade background for beautiful trailing
  Disp.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0x0841);
  
  float swarm_time = millis() * 0.001f;
  
  // Update and draw each firefly
  for (int i = 0; i < 25; i++) {
    // Organic Perlin-like movement using multiple sine waves
    float movement_x = sin(fireflies[i][0] * 0.02f + swarm_time) * cos(swarm_time * 0.7f + i);
    float movement_y = cos(fireflies[i][1] * 0.02f + swarm_time * 0.8f) * sin(swarm_time * 0.6f + i);
    
    // Apply gentle force
    fireflies[i][2] += movement_x * 0.02f;
    fireflies[i][3] += movement_y * 0.02f;
    
    // Damping for smooth motion
    fireflies[i][2] *= 0.98f;
    fireflies[i][3] *= 0.98f;
    
    // Update position
    fireflies[i][0] += fireflies[i][2];
    fireflies[i][1] += fireflies[i][3];
    
    // Gentle edge repulsion instead of wrapping
    if (fireflies[i][0] < 10) fireflies[i][2] += 0.1f;
    if (fireflies[i][0] > SCREEN_WIDTH - 10) fireflies[i][2] -= 0.1f;
    if (fireflies[i][1] < 10) fireflies[i][3] += 0.1f;
    if (fireflies[i][1] > SCREEN_HEIGHT - 10) fireflies[i][3] -= 0.1f;
    
    // Keep in bounds
    fireflies[i][0] = constrain(fireflies[i][0], 5, SCREEN_WIDTH - 5);
    fireflies[i][1] = constrain(fireflies[i][1], 5, SCREEN_HEIGHT - 5);
    
    // Update glow and color
    fireflies[i][4] += 0.08f + sin(i) * 0.02f; // Different glow speeds
    fireflies[i][5] += 0.5f; // Slow hue drift
    if (fireflies[i][5] >= 360) fireflies[i][5] -= 360;
    
    // Calculate glow intensity
    float glow_intensity = 0.6f + 0.4f * sin(fireflies[i][4]);
    
    // Draw firefly with beautiful glow
    int fx = (int)fireflies[i][0];
    int fy = (int)fireflies[i][1];
    
    uint16_t firefly_color = getColorFromHSV(fireflies[i][5], 0.8f, glow_intensity);
    
    // Multi-layer glow effect
    Disp.fillCircle(fx, fy, 3, firefly_color);  // Core
    
    uint16_t glow_color = getColorFromHSV(fireflies[i][5], 0.6f, glow_intensity * 0.6f);
    Disp.fillCircle(fx, fy, 5, glow_color);     // Glow ring
    
    // Bright center
    uint16_t center_color = getColorFromHSV(fireflies[i][5], 0.4f, 1.0f);
    Disp.fillCircle(fx, fy, 1, center_color);
    
    // Sparkle effect when glow is high
    if (glow_intensity > 0.9f) {
      for (int sparkle = 0; sparkle < 4; sparkle++) {
        int sx = fx + random(-3, 4);
        int sy = fy + random(-3, 4);
        if (sx >= 0 && sx < SCREEN_WIDTH && sy >= 0 && sy < SCREEN_HEIGHT) {
          Disp.drawPixel(sx, sy, center_color);
        }
      }
    }
  }
  
  // Occasional magical sparkles in empty space
  for (int magic = 0; magic < 8; magic++) {
    if (random(1000) < 20) { // 2% chance per magic sparkle
      int mx = random(0, SCREEN_WIDTH);
      int my = random(0, SCREEN_HEIGHT);
      uint16_t magic_color = getColorFromHSV(random(0, 360), 1.0f, 1.0f);
      Disp.drawPixel(mx, my, magic_color);
    }
  }
}

void drawDigitalDreams() {
  // My personal creation: Digital Dreams - Where ideas are born and connect
  // Represents the beauty of creativity, connection, and infinite possibility
  static float dream_nodes[20][6]; // x, y, vx, vy, energy, connection_strength
  static float thought_waves[8][5]; // center_x, center_y, radius, expansion_speed, hue
  static int inspiration_bursts[5][4]; // x, y, size, lifetime
  static bool initialized = false;
  static float consciousness_time = 0;
  
  if (!initialized) {
    // Initialize dream nodes - these represent ideas forming
    for (int i = 0; i < 20; i++) {
      dream_nodes[i][0] = random(10, SCREEN_WIDTH - 10);   // x
      dream_nodes[i][1] = random(10, SCREEN_HEIGHT - 10);  // y
      dream_nodes[i][2] = (random(200) - 100) / 100.0f;   // vx
      dream_nodes[i][3] = (random(200) - 100) / 100.0f;   // vy
      dream_nodes[i][4] = random(50, 100) / 100.0f;       // energy
      dream_nodes[i][5] = 0;                               // connection_strength
    }
    
    // Initialize thought waves - expanding rings of consciousness
    for (int i = 0; i < 8; i++) {
      thought_waves[i][0] = random(0, SCREEN_WIDTH);  // center_x
      thought_waves[i][1] = random(0, SCREEN_HEIGHT); // center_y
      thought_waves[i][2] = 0;                        // radius
      thought_waves[i][3] = 0.5f + random(100) / 200.0f; // expansion_speed
      thought_waves[i][4] = random(0, 360);           // hue
    }
    
    // Initialize inspiration bursts
    for (int i = 0; i < 5; i++) {
      inspiration_bursts[i][3] = 0; // inactive
    }
    
    initialized = true;
  }
  
  consciousness_time += 0.03f;
  
  // Dreamy background with subtle breathing effect
  float breath = 0.2f + 0.1f * sin(consciousness_time * 2);
  uint16_t bg_color = getColorFromHSV(240, 0.3f, breath);
  Disp.fillScreen(bg_color);
  
  // Update and draw dream nodes (ideas)
  for (int i = 0; i < 20; i++) {
    // Gentle drift with attraction to center (like thoughts converging)
    float center_pull_x = (SCREEN_WIDTH / 2 - dream_nodes[i][0]) * 0.002f;
    float center_pull_y = (SCREEN_HEIGHT / 2 - dream_nodes[i][1]) * 0.002f;
    
    dream_nodes[i][2] += center_pull_x;
    dream_nodes[i][3] += center_pull_y;
    
    // Add some randomness (creativity is chaotic!)
    dream_nodes[i][2] += (random(200) - 100) / 1000.0f;
    dream_nodes[i][3] += (random(200) - 100) / 1000.0f;
    
    // Damping for smooth movement
    dream_nodes[i][2] *= 0.995f;
    dream_nodes[i][3] *= 0.995f;
    
    // Update position
    dream_nodes[i][0] += dream_nodes[i][2];
    dream_nodes[i][1] += dream_nodes[i][3];
    
    // Soft boundaries (ideas don't disappear, they reflect)
    if (dream_nodes[i][0] < 5 || dream_nodes[i][0] > SCREEN_WIDTH - 5) {
      dream_nodes[i][2] *= -0.8f;
      dream_nodes[i][0] = constrain(dream_nodes[i][0], 5, SCREEN_WIDTH - 5);
    }
    if (dream_nodes[i][1] < 5 || dream_nodes[i][1] > SCREEN_HEIGHT - 5) {
      dream_nodes[i][3] *= -0.8f;
      dream_nodes[i][1] = constrain(dream_nodes[i][1], 5, SCREEN_HEIGHT - 5);
    }
    
    // Update energy (ideas pulse with life)
    dream_nodes[i][4] = 0.5f + 0.5f * sin(consciousness_time * 3 + i * 0.7f);
    
    // Calculate connections to nearby nodes (ideas connecting)
    dream_nodes[i][5] = 0; // Reset connection strength
    
    for (int j = 0; j < 20; j++) {
      if (i != j) {
        float dx = dream_nodes[j][0] - dream_nodes[i][0];
        float dy = dream_nodes[j][1] - dream_nodes[i][1];
        float distance = sqrt(dx * dx + dy * dy);
        
        // Draw connections between close ideas
        if (distance < 40) {
          float connection_strength = 1.0f - (distance / 40.0f);
          dream_nodes[i][5] += connection_strength;
          
          // Color based on connection strength and consciousness time
          float connection_hue = fmod(consciousness_time * 50 + distance * 3, 360);
          uint16_t connection_color = getColorFromHSV(connection_hue, 0.8f, connection_strength * 0.6f);
          
          Disp.drawLine((int)dream_nodes[i][0], (int)dream_nodes[i][1],
                        (int)dream_nodes[j][0], (int)dream_nodes[j][1], connection_color);
        }
      }
    }
    
    // Draw the dream node (idea) with energy-based appearance
    int node_x = (int)dream_nodes[i][0];
    int node_y = (int)dream_nodes[i][1];
    
    // Color shifts through spectrum of creativity
    float node_hue = fmod(consciousness_time * 40 + i * 25 + dream_nodes[i][5] * 50, 360);
    float node_brightness = dream_nodes[i][4];
    uint16_t node_color = getColorFromHSV(node_hue, 1.0f, node_brightness);
    
    // Size based on energy and connections
    int node_size = 2 + (dream_nodes[i][4] + dream_nodes[i][5] * 0.5f) * 3;
    
    Disp.fillCircle(node_x, node_y, node_size, node_color);
    
    // Add sparkle when highly energized
    if (dream_nodes[i][4] > 0.8f) {
      uint16_t sparkle_color = getColorFromHSV(node_hue + 60, 0.8f, 1.0f);
      Disp.fillCircle(node_x, node_y, 1, sparkle_color);
    }
    
    // Create inspiration bursts when ideas are highly connected
    if (dream_nodes[i][5] > 2.0f && random(1000) < 30) {
      for (int burst = 0; burst < 5; burst++) {
        if (inspiration_bursts[burst][3] <= 0) {
          inspiration_bursts[burst][0] = node_x;
          inspiration_bursts[burst][1] = node_y;
          inspiration_bursts[burst][2] = 0;
          inspiration_bursts[burst][3] = 30;
          break;
        }
      }
    }
  }
  
  // Update and draw thought waves (expanding consciousness)
  for (int i = 0; i < 8; i++) {
    thought_waves[i][2] += thought_waves[i][3]; // Expand radius
    
    // Reset wave when it gets too big
    if (thought_waves[i][2] > 80) {
      thought_waves[i][0] = random(20, SCREEN_WIDTH - 20);
      thought_waves[i][1] = random(20, SCREEN_HEIGHT - 20);
      thought_waves[i][2] = 0;
      thought_waves[i][3] = 0.3f + random(100) / 300.0f;
      thought_waves[i][4] = random(0, 360);
    }
    
    // Draw expanding ring of consciousness
    if (thought_waves[i][2] > 5 && thought_waves[i][2] < 70) {
      float wave_alpha = 1.0f - (thought_waves[i][2] / 70.0f);
      uint16_t wave_color = getColorFromHSV(thought_waves[i][4], 0.7f, wave_alpha * 0.5f);
      
      Disp.drawCircle((int)thought_waves[i][0], (int)thought_waves[i][1], 
                      (int)thought_waves[i][2], wave_color);
    }
  }
  
  // Update and draw inspiration bursts
  for (int i = 0; i < 5; i++) {
    if (inspiration_bursts[i][3] > 0) {
      inspiration_bursts[i][2] += 2; // Expand
      inspiration_bursts[i][3]--;    // Fade
      
      float burst_alpha = inspiration_bursts[i][3] / 30.0f;
      uint16_t burst_color = getColorFromHSV(45, 0.9f, burst_alpha); // Golden inspiration
      
      // Draw expanding burst
      for (int angle = 0; angle < 360; angle += 30) {
        int x = inspiration_bursts[i][0] + cos(angle * PI / 180.0f) * inspiration_bursts[i][2];
        int y = inspiration_bursts[i][1] + sin(angle * PI / 180.0f) * inspiration_bursts[i][2];
        
        if (x >= 0 && x < SCREEN_WIDTH && y >= 0 && y < SCREEN_HEIGHT) {
          Disp.drawPixel(x, y, burst_color);
        }
      }
    }
  }
  
  // Add some floating dream particles
  for (int magic = 0; magic < 12; magic++) {
    if (random(1000) < 40) {
      int mx = random(0, SCREEN_WIDTH);
      int my = random(0, SCREEN_HEIGHT);
      float magic_hue = fmod(consciousness_time * 80 + magic * 30, 360);
      uint16_t magic_color = getColorFromHSV(magic_hue, 0.6f, 0.8f);
      Disp.drawPixel(mx, my, magic_color);
    }
  }
}

// v1.1 New Functions
void switchModePrevious() {
  // Go to previous mode (wrapping around)
  if (currentMode == 0) {
    currentMode = static_cast<ScreenSaverMode>(MODE_COUNT - 1);
  } else {
    currentMode = static_cast<ScreenSaverMode>(currentMode - 1);
  }
  lastModeChange = millis();
  frame_counter = 0;
  
  // Show mode name briefly
  Disp.fillScreen(BLACK);
  
  String modeName;
  switch (currentMode) {
    case DIGITAL_DREAMS: modeName = "DIGITAL DREAMS"; break;
    case PLASMA_WAVES: modeName = "PLASMA WAVES"; break;
    case SPIRAL_COLORS: modeName = "SPIRAL COLORS"; break;
    case BOUNCING_BALLS: modeName = "BOUNCING BALLS"; break;
    case NEON_RAIN: modeName = "NEON RAIN"; break;
    case KALEIDOSCOPE: modeName = "KALEIDOSCOPE"; break;
    case LIQUID_METAL: modeName = "LIQUID METAL"; break;
    case CAMPFIRE: modeName = "CAMPFIRE"; break;
    case DRAGON_CURVE: modeName = "DRAGON CURVE"; break;
    case GLYPH_RAIN: modeName = "GLYPH RAIN"; break;
    case HEAVY_RAIN: modeName = "HEAVY RAIN"; break;
    case JULIA_SET: modeName = "JULIA SET"; break;
    case MANDELBROT: modeName = "MANDELBROT"; break;
    case MATRIX_BINARY: modeName = "MATRIX BINARY"; break;
    case MICRO_DOTS: modeName = "MICRO DOTS"; break;
    case RAINDROPS: modeName = "RAINDROPS"; break;
    case RETRO_GEOMETRY: modeName = "RETRO GEOMETRY"; break;
    case SIERPINSKI: modeName = "SIERPINSKI"; break;
    case SIMPLE_FLAMES: modeName = "SIMPLE FLAMES"; break;
    case WALKING_TRIANGLE: modeName = "WALKING TRIANGLE"; break;
    case WALKING_SQUARE: modeName = "WALKING SQUARE"; break;
    case WALKING_STAR: modeName = "WALKING STAR"; break;
    case SPIROGRAPH: modeName = "SPIROGRAPH"; break;
    case RECURSIVE_POLYGONS: modeName = "RECURSIVE POLYGONS"; break;
    case FLOW_FIELD: modeName = "FLOW FIELD"; break;
    case COLOR_SHIMMER: modeName = "COLOR SHIMMER"; break;
    case STARFIELD_WARP: modeName = "STARFIELD WARP"; break;
    case FIREFLY_SWARM: modeName = "FIREFLY SWARM"; break;
  }
  
  Disp.drawString("< " + modeName, 5, 10, 1);
  Serial.println("🎨 Previous Mode: " + modeName);
}

void cycleSpeed() {
  // Cycle through 10 speed levels
  speedLevel++;
  if (speedLevel > 10) {
    speedLevel = 1; // Reset to slowest
  }
  
  // Silent speed control - no visual indicators
  Serial.println("⚡ Speed Level: " + String(speedLevel) + "/10");
}

void drawSpeedIndicator() {
  // Draw speed bars in top right corner
  for (int i = 0; i < 10; i++) {
    uint16_t color = (i < speedLevel) ? GREEN : 0x2104; // Dark grey color
    Disp.fillRect(SCREEN_WIDTH - 15 + i, 5, 1, 8, color);
  }
  
  // Show speed number
  Disp.drawString(String(speedLevel), SCREEN_WIDTH - 20, 15, 1);
}