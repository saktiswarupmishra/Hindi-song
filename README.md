# 🎬 Retro Bollywood Terminal Player — Animated Gradient Edition

Welcome to the **Retro Bollywood Terminal Player**! This is a highly visual, fully animated, 24-bit true color terminal-based music player. This specific edition is configured to play the classic Bollywood track **"Zulfon Ko Girake"** from the movie *Jaaneman (1999)*, featuring a synchronized, cinematic lyric experience directly in your command line.

## ✨ Features & Visual Aesthetics

- **Animated Gradient Text Engine:** Custom-built per-character gradient engine that flows and animates smoothly across text in real-time.
- **Dynamic Two-Column UI:** 
  - *Left Column:* Displays custom ASCII movie poster art for *Jaaneman (1999)*, along with animated song metadata.
  - *Right Column:* Features a dynamic visualizer that transitions through multiple phases: a boot sequence, a typing "Python code" lyric effect, and a Matrix rain zoom-out glitch effect.
- **Neon Blue Dynamic Lyrics Engine:** Lyrics are synchronized to the exact millisecond, highlighted using a pulsing neon cyberpunk theme and a typing cursor effect.
- **Built-in Synchronization Tool:** Includes an interactive mode that allows you to easily resync lyrics manually by tapping the spacebar.
- **Audio Visualizers:** Features a mini equalizer and volume bar display that react to the aesthetic flow of the player.
- **Double-Buffered Rendering:** Ensures a 100% flicker-free, smooth terminal animation.

## 🛠️ Prerequisites

To run this project, you will need:
- **Python 3.6+** installed on your system.
- The **pygame** library for audio playback.

You can install the required library using pip:
```bash
pip install pygame
```

## 🚀 How to Run

### Play the Song
Run the Python script directly from your terminal to launch the player:
```bash
python player.py
```

### Run Sync Mode (Lyrics Synchronization)
If you wish to manually re-time the lyrics to the music, you can call the `run_sync_mode()` function within the script. This provides an interactive UI to tap the spacebar to the beat and records the millisecond-perfect timing.

## 📂 Project Structure

- `player.py`: The main script containing the gradient rendering engine, UI layout, lyric timestamps, and animation loops.
- `julfo ko girake.mpeg`: The audio track used by the application.
- `click.wav`: A mechanical keyboard typing sound effect generated on the fly (or read from disk) to accompany the typing animation.
- `README.md`: This documentation file.

## 🎨 Customization

You can personalize the player by editing `player.py`:
- **Change the Song:** Update the `AUDIO_FILE` variable at the top of the file to point to your own `.mpeg` or `.mp3` file.
- **Update Metadata:** Modify the `SONG` dictionary to reflect your new track's title, movie, singers, and credits.
- **Adjust Lyrics:** Change the `LYRICS_STANZA_1` and `LYRICS_STANZA_2` arrays with your new lyrics and timestamps.
- **Tweak Gradients:** Explore and modify the `GRAD_*` lists to create your own color schemes.

## 🐛 Troubleshooting

- **Terminal displays weird codes (e.g., `[38;2;...`):** Your terminal does not support 24-bit ANSI colors. Please use a modern terminal emulator like **Windows Terminal**, **iTerm2**, or **VS Code's integrated terminal**.
- **No Sound:** Ensure your volume is up and that the audio file `julfo ko girake.mpeg` is located in the exact same folder as the script.

## 🎬 Credits

- **Song:** Zulfon Ko Girake
- **Movie:** Jaaneman (1999)
- **Singers:** Udit Narayan & Alka Yagnik
- **Music:** Nadeem Shravan

---
*Keep Smiling... Keep Creating....*
