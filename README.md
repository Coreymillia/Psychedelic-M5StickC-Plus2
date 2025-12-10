# Psychedelic M5StickC Plus2 Screensavers

XScreensaver-inspired psychedelic effects for the M5StickC Plus2 device.

## Features

- **6 Core Effects**: Matrix Rain, Plasma Wave, Spiral Colors, Bouncing Balls, Fire Effect, Kaleidoscope  
- **Auto-cycling**: Effects change every 10 seconds
- **Manual control**: Press Button A to cycle through effects
- **Optimized**: Smooth 20 FPS animation with proper color palette
- **Extensible**: Easy to add new effects based on XScreensaver classics

## Hardware Requirements

- M5StickC Plus2 device
- USB-C cable for programming/power

## Quick Start

1. **Clone and Build**:
   ```bash
   git clone <this-repo>
   cd Psychedelic-M5StickC-Plus2
   pio run --target upload
   ```

2. **Usage**:
   - Device boots with "Psychedelic Screens" splash
   - Effects auto-cycle every 10 seconds  
   - Press Button A to manually change effects
   - Current effect name displayed briefly on change

## Current Effects

| Effect | Description |
|--------|-------------|
| Matrix Rain | Digital rain drops inspired by The Matrix |
| Plasma Wave | Mathematical plasma wave with rainbow colors |
| Spiral Colors | Rotating colorful spiral pattern |
| Bouncing Balls | Physics-based bouncing balls with trails |
| Fire Effect | Animated fire simulation |
| Kaleidoscope | Rotating geometric kaleidoscope pattern |

## Development

Based on lessons learned from:
- **ESP32-2432S028 XScreens project** (touch, web interface patterns)
- **Original M5 Psychedelic release** (M5StickC Plus2 optimization)  
- **XScreensaver classics** (algorithmic approach to visual effects)

### Adding New Effects

1. Add new enum value to `EffectMode`
2. Increment `MODE_COUNT`
3. Add case in `runCurrentEffect()`
4. Add name in `getEffectName()`  
5. Implement effect function following the pattern

### Project Structure

```
src/main.cpp          # Main application with 6 effects
platformio.ini        # M5StickC Plus2 configuration  
Psychedelic-M5-GitHub-Release/  # Reference implementation
```

## Memory Usage

- **RAM**: 10.4% (33,944 bytes)
- **Flash**: 34.6% (453,445 bytes)
- Plenty of room for additional effects

## Future Plans

- Add more XScreensaver classics (Sierpinski, Mandelbrot, etc.)
- WiFi web interface for remote control
- Effect parameter customization
- Sound-reactive modes using built-in microphone

## Credits

Built on M5StickCPlus2 library and inspired by the XScreensaver collection.
28 different screens, L or R to select, M5 for speed control - Everything you  need to trip out your M5StickC Plus2
