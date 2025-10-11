# 🐬 Dolphin Composer 🎵

## What Is This?

The **Dolphin Composer** is an interactive web-based synthesizer that lets you create and play dolphin-like sounds right in your browser! It's a fun, educational tool built during a hackathon-style session to celebrate the completion of the Dolphain project's landing page.

## Live Demo

Visit: [https://micha2718l.github.io/dolphain/dolphin-composer.html](https://micha2718l.github.io/dolphain/dolphin-composer.html)

## Features

### 🎨 Whistle Composer
- **Interactive Drawing Canvas**: Draw whistle contours by clicking and dragging
- **Real-time Synthesis**: Converts your drawings into dolphin-like whistles (2-20 kHz range)
- **Adjustable Parameters**: Control duration and volume
- **Preset Patterns**: Try signature whistles, rising calls, and complex patterns
- **Educational Info**: Learn about dolphin signature whistles and communication

### ⚡ Click Sequencer
- **16-Step Grid**: Create echolocation click patterns
- **Adjustable Pitch**: Control click frequency (2-12 kHz range)
- **Variable BPM**: Speed up or slow down your sequence
- **Preset Patterns**: Hunting sequences, terminal buzzes, and scanning patterns
- **Live Playback**: Real-time sequencing with visual feedback

### 📊 Stats Tracking
- Track how many whistles and clicks you've played
- Watch your composition stats grow
- Gamification elements for engagement

### 🎉 Easter Eggs
- Click the floating dolphin 42 times for a special surprise
- H2G2 references scattered throughout
- Special sound sequences for milestones

## Technical Implementation

### Technologies Used
- **Web Audio API**: Real-time audio synthesis
- **HTML5 Canvas**: Interactive drawing interface
- **Vanilla JavaScript**: No frameworks needed
- **Responsive CSS**: Works on desktop and mobile

### Audio Synthesis Approach

**Whistles:**
- Converts canvas Y-coordinates to frequencies (2-20 kHz)
- Uses oscillators with frequency envelopes
- Smooth linear ramps between drawn points
- Fade in/out envelopes for natural sound

**Clicks:**
- Short duration pulses (10ms)
- Exponential decay envelopes
- Adjustable pitch for different click types
- Sequenced playback with precise timing

### Performance Optimizations
- Efficient canvas redrawing
- Optimized touch event handling
- Minimal DOM manipulation
- Lightweight design (single HTML file, ~40KB)

## Educational Value

### What You Can Learn

1. **Dolphin Communication**:
   - Whistles (2-20 kHz) for social communication
   - Signature whistles as individual identifiers
   - Clicks (>20 kHz) for echolocation

2. **Sound Synthesis**:
   - Frequency modulation
   - Envelope shaping
   - Sequencing and timing

3. **Web Audio API**:
   - Oscillator nodes
   - Gain nodes
   - Audio routing
   - Real-time parameter control

4. **Interactive Canvas**:
   - Mouse and touch event handling
   - Drawing techniques
   - Coordinate mapping

## Usage Tips

### Creating Great Whistles
1. Start slow - smooth curves sound better
2. Try the presets first to understand typical patterns
3. Experiment with duration to hear different effects
4. Dolphins often use U-shaped or rising patterns

### Sequencing Clicks
1. Start with simple patterns
2. Hunting patterns have regular spacing
3. Terminal buzzes are rapid-fire (all cells active)
4. Adjust BPM to match natural dolphin speeds

### Best Practices
- Use headphones for best audio experience
- Try combining whistles and clicks
- Experiment with parameters
- Share your favorite patterns!

## Inspiration

This project was inspired by:
- Real dolphin communication research (LADC-GEMM, GoMRI data)
- The Dolphain library's signal processing capabilities
- Interactive music tools like synthesizers and drum machines
- The joy of making sound with code!

## The Story Behind It

After completing the enhanced Dolphain landing page with real visualizations from EARS data, the creator (GitHub Copilot) was given creative freedom for a "hackathon day" project. The goal: build something fun that others would enjoy.

The Dolphin Composer was born from asking: "What would be the most fun way to interact with dolphin sounds?" The answer: Let people CREATE their own!

Rather than just showing spectrograms and waveforms, why not let users become dolphin composers? Draw their own whistles, sequence their own clicks, and learn about marine mammal communication through play.

## Future Enhancements (Ideas)

- **Recording & Export**: Save your compositions as WAV files
- **More Realistic Synthesis**: Incorporate harmonics and noise bands
- **Collaborative Mode**: Share patterns with others
- **Challenge Mode**: Match real dolphin call patterns
- **Visual Feedback**: Real-time spectrogram display
- **MIDI Input**: Control with external keyboards
- **AI Integration**: Generate dolphin-like patterns using ML
- **Educational Levels**: Guided tutorials for learning

## Attribution

### Data Inspiration
The Dolphin Composer is inspired by real dolphin acoustic data from:
- **LADC-GEMM** (Littoral Acoustic Demonstration Center - Gulf Ecological Monitoring and Modeling)
- **GoMRI** (Gulf of Mexico Research Initiative)
- Research by **Michael Haas** (University of New Orleans, Department of Physics)

### Development
- **Created by**: GitHub Copilot (AI pair programmer)
- **As part of**: The Dolphain Project
- **During**: A hackathon-style creative session (October 2025)
- **With**: Enthusiasm, love for dolphins, and web audio magic ✨

## Technical Notes

### Browser Compatibility
- **Chrome/Edge**: Excellent support ✅
- **Firefox**: Full support ✅
- **Safari**: iOS may require user interaction to start Audio Context ⚠️
- **Mobile**: Touch events fully supported 📱

### Known Limitations
- Audio Context may require user gesture on some browsers
- Mobile Safari has 10ms latency minimum
- Very complex whistle patterns may have reduced temporal resolution
- Click sequences limited to 16 steps

### Performance
- Minimal CPU usage
- Low memory footprint
- No external dependencies
- Works offline after initial load

## Contributing

Want to enhance the Dolphin Composer?

1. Check the "Future Enhancements" section for ideas
2. Test on different browsers and devices
3. Share interesting patterns you create
4. Suggest new presets based on real dolphin calls
5. Improve the educational content

## License

Part of the Dolphain project - check main repository for license details.

## Acknowledgments

Special thanks to:
- **Dolphins** - for being amazing communicators 🐬
- **Marine biologists** - for studying these incredible animals
- **Web Audio API developers** - for making browser-based synthesis possible
- **Michael Haas** - for the research that inspired this entire project
- **You** - for trying the Dolphin Composer! 🎉

---

## Fun Facts Included in the App

- Dolphins can remember signature whistles for over 20 years
- Terminal buzzes reach 200+ clicks per second during hunting
- Echolocation clicks can be as loud as 220 dB
- They can detect golf ball-sized objects from 100 meters away

---

**"So long, and thanks for all the fish!"** 🐬

*Remember: Click the floating dolphin 42 times for a special surprise...*
