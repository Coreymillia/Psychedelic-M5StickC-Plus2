#!/bin/bash
# Quick build script for Psychedelic M5StickC Plus2

echo "🎨 Building Psychedelic M5StickC Plus2 Screensavers..."
echo "==============================================="

# Clean and build
echo "Building project..."
pio run

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📊 Memory usage:"
    pio run --target checkprogsize | grep -E "(RAM|Flash)"
    
    echo ""
    echo "🔌 To upload to device:"
    echo "   pio run --target upload"
    echo ""
    echo "🎮 Usage:"
    echo "   - Auto-cycles effects every 10s"
    echo "   - Press Button A to manually cycle"
    echo "   - 6 effects: Matrix, Plasma, Spiral, Balls, Fire, Kaleidoscope"
else
    echo "❌ Build failed!"
    exit 1
fi