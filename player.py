#!/usr/bin/env python3
"""
Retro Bollywood Terminal Player — Animated Gradient Edition
"""

import os, sys, time, math, random, wave, struct
from datetime import datetime

# ── Windows Unicode Fix ──
if sys.platform == 'win32':
    os.system('')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import shutil

# ═══════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════
AUDIO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "julfo ko girake.mpeg")

LYRICS_STANZA_1 = [
    (1.11, "Zulfon Ko Girake"),
    (1.9, "Palkon Ko Jhukana"),
    (2.56, "Sikha Hai Kahan Se"),
    (3.26, "Yeh Jadoo Chalana"),
]

LYRICS_STANZA_2 = [
    (3.85, "Aata Hai Tumhe Toh"),
    (4.47, "Yun Baatein Banana"),
    (5.11, "Jaoji Hato Bhi"),
    (5.85, "Chhodo Yun Satana"),
]

ALL_LYRICS = [(0.0, "")] + LYRICS_STANZA_1 + LYRICS_STANZA_2 + [(22.0, "")]

SONG = {
    "title": "Zulfon Ko Girake",
    "movie": "Jaaneman (1999)",
    "singers": "Udit Narayan & Alka Yagnik",
    "music": "Nadeem Shravan",
    "lyricist": "Sameer",
    "cast": "Akshay Kumar, Abhishek Bachchan & Karisma Kapoor",
    "director": "Dharmesh Darshan",
    "producer": "Suneel Darshan",
    "gfx": "Nadeem Akhtar",
    "gfx_studio": "(Paperboyz Studioz)",
}

# ═══════════════════════════════════════════════════════
#  ANSI HELPERS
# ═══════════════════════════════════════════════════════
def fg(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

RST  = '\033[0m'
BOLD = '\033[1m'
DIM  = '\033[2m'
HIDE = '\033[?25l'
SHOW = '\033[?25h'
CLR  = '\033[2J\033[H'
HOME = '\033[H'

# Static colors (for borders, controls, etc.)
NEON_GREEN   = fg(0, 255, 100)
DARK_GREEN   = fg(0, 180, 60)
GREY         = fg(120, 120, 120)
DIM_GREY     = fg(70, 70, 70)
WHITE        = fg(240, 240, 240)
RED          = fg(255, 50, 50)
YELLOW       = fg(255, 255, 0)
BRIGHT_GREEN = fg(80, 255, 80)
ORANGE       = fg(255, 165, 0)
WARM_WHITE   = fg(255, 250, 230)

# ═══════════════════════════════════════════════════════
#  GRADIENT TEXT ENGINE — Per-character animated gradients
# ═══════════════════════════════════════════════════════
def lerp(a, b, t):
    """Linear interpolate between a and b."""
    return int(a + (b - a) * t)

def gradient_text(text, colors, offset=0, speed=1.0):
    """
    Apply a smooth animated gradient to text.
    colors = list of (r,g,b) tuples — gradient stops
    offset = frame-based shift for animation
    """
    if not text or not colors:
        return text
    
    result = ''
    n = len(colors)
    text_len = max(len(text), 1)
    
    for i, ch in enumerate(text):
        if ch == ' ':
            result += ' '
            continue
        
        # Position in gradient (0..1) with animated shift
        pos = ((i / text_len) * (n - 1) + offset * speed) % (n - 1)
        idx = int(pos)
        frac = pos - idx
        
        # Clamp index
        c1 = colors[idx % n]
        c2 = colors[(idx + 1) % n]
        
        r = lerp(c1[0], c2[0], frac)
        g = lerp(c1[1], c2[1], frac)
        b = lerp(c1[2], c2[2], frac)
        
        result += fg(r, g, b) + ch
    
    return result + RST

def gradient_text_bold(text, colors, offset=0, speed=1.0):
    """Gradient text with bold."""
    if not text:
        return text
    result = ''
    n = len(colors)
    text_len = max(len(text), 1)
    
    for i, ch in enumerate(text):
        if ch == ' ':
            result += ' '
            continue
        pos = ((i / text_len) * (n - 1) + offset * speed) % (n - 1)
        idx = int(pos)
        frac = pos - idx
        c1 = colors[idx % n]
        c2 = colors[(idx + 1) % n]
        r = lerp(c1[0], c2[0], frac)
        g = lerp(c1[1], c2[1], frac)
        b = lerp(c1[2], c2[2], frac)
        result += fg(r, g, b) + BOLD + ch
    
    return result + RST

# ── Gradient Presets ──
GRAD_TITLE = [(255,50,100), (255,150,50), (255,255,0), (50,255,100), (0,200,255), (150,50,255), (255,50,100)]
GRAD_PINK_GOLD = [(255,80,150), (255,150,200), (255,220,100), (255,200,50), (255,150,200), (255,80,150)]
GRAD_CYAN_MAGENTA = [(0,255,255), (100,200,255), (200,100,255), (255,80,200), (200,100,255), (0,255,255)]
GRAD_FIRE = [(255,255,100), (255,200,50), (255,130,0), (255,60,30), (255,130,0), (255,200,50)]
GRAD_NEON = [(0,255,100), (0,255,200), (0,200,255), (100,150,255), (0,200,255), (0,255,100)]
GRAD_ROSE = [(255,100,130), (255,180,200), (255,220,230), (255,180,200), (255,100,130)]
GRAD_LYRIC_ACTIVE = [(255,255,50), (255,200,0), (255,130,50), (255,80,100), (255,50,150), (200,50,255), (100,100,255), (50,200,255), (50,255,200), (100,255,100), (200,255,50), (255,255,50)]
GRAD_LYRIC_DIM = [(100,100,110), (130,120,125), (100,100,110)]
GRAD_LYRIC_FUTURE = [(220,220,230), (240,240,250), (255,255,255), (240,240,250), (220,220,230)]
GRAD_POSTER = [(255,200,0), (255,150,0), (255,80,0), (255,50,50), (255,80,0), (255,200,0)]
GRAD_SEPARATOR = [(80,80,90), (140,100,120), (200,80,150), (140,100,120), (80,80,90)]
GRAD_HEART = [(255,50,80), (255,100,130), (255,150,180), (255,200,210), (255,150,180), (255,100,130), (255,50,80)]
GRAD_STATUS = [(255,100,180), (255,150,200), (255,200,220), (255,150,200), (255,100,180)]


# ═══════════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════════
def vlen(text):
    length = 0
    i = 0
    while i < len(text):
        if text[i] == '\033':
            while i < len(text) and text[i] != 'm':
                i += 1
            i += 1
        else:
            length += 1
            i += 1
    return length

def pad(text, width, align='left'):
    vl = vlen(text)
    if vl >= width:
        return text
    space = width - vl
    if align == 'center':
        l = space // 2
        r = space - l
        return ' ' * l + text + ' ' * r
    elif align == 'right':
        return ' ' * space + text
    else:
        return text + ' ' * space

def fmt_time(s):
    return f"{int(s)//60:02d}:{int(s)%60:02d}"

def get_active_lyric_index(elapsed):
    idx = 0
    for i, (ts, _) in enumerate(ALL_LYRICS):
        if elapsed >= ts:
            idx = i
    return idx


# ═══════════════════════════════════════════════════════
#  MOVIE POSTER ASCII ART
# ═══════════════════════════════════════════════════════
POSTER_ART = [
    "╔══════════════════╗",
    "║  ┌──────────────┐║",
    "║  │  ╔═╗         │║",
    "║  │  ║T║ SERIES   │║",
    "║  │  ╚═╝         │║",
    "║  │   SUNEEL     │║",
    "║  │  DARSHAN'S   │║",
    "║  │              │║",
    "║  │  ╦╦╦╦╦╦╦╦╦╦  │║",
    "║  │  ║JAANEMAN║  │║",
    "║  │  ╩╩╩╩╩╩╩╩╩╩  │║",
    "║  │              │║",
    "║  └──────────────┘║",
    "╚══════════════════╝",
]


# ═══════════════════════════════════════════════════════
#  EQUALIZER + VOLUME
# ═══════════════════════════════════════════════════════
def render_eq_mini(frame, width=12):
    bars = ''
    eq_chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    for i in range(width):
        h = (math.sin(frame * 0.15 + i * 0.6) + 1) / 2
        h += random.uniform(-0.1, 0.1)
        h = max(0, min(1, h))
        ci = int(h * (len(eq_chars) - 1))
        # Gradient color per bar height
        r = lerp(0, 255, h)
        g = lerp(255, 50, h)
        b = lerp(100, 50, h)
        bars += fg(r, g, b) + eq_chars[ci] + RST
    return bars

def render_volume_bars(level=80):
    total = 8
    filled = int((level / 100) * total)
    bars = ''
    for i in range(total):
        if i < filled:
            r = lerp(0, 255, i / total)
            g = lerp(255, 50, i / total)
            b = 50
            bars += fg(r, g, b) + '▮' + RST
        else:
            bars += DIM_GREY + '▯' + RST
    return bars


# ═══════════════════════════════════════════════════════
#  ANIMATED GRADIENT BORDER
# ═══════════════════════════════════════════════════════
def gradient_border_h(char, width, frame, speed=0.08):
    """Horizontal border with flowing gradient animation."""
    result = ''
    for i in range(width):
        phase = (i * 0.05 + frame * speed)
        r = int(127 + 127 * math.sin(phase))
        g = int(127 + 127 * math.sin(phase + 2.094))
        b = int(127 + 127 * math.sin(phase + 4.189))
        # Shift towards green-cyan tones
        r = max(0, r - 80)
        g = min(255, g + 50)
        result += fg(r, g, b) + char + RST
    return result

def border_v(frame, pos=0):
    """Animated vertical border character."""
    phase = (pos * 0.1 + frame * 0.1)
    r = max(0, int(80 + 80 * math.sin(phase)) - 60)
    g = min(255, int(150 + 105 * math.sin(phase + 1.0)))
    b = int(80 + 80 * math.sin(phase + 2.0))
    return fg(r, g, b) + '│' + RST


# ═══════════════════════════════════════════════════════
#  NEON BLUE DYNAMIC LYRICS ENGINE & SYNC TOOL
# ═══════════════════════════════════════════════════════

def ensure_click_sound():
    filename = "click.wav"
    if os.path.exists(filename):
        return
    sample_rate = 44100
    duration = 0.05
    num_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for i in range(num_samples):
            t = i / sample_rate
            # Sweeping frequency to simulate physical resonance
            freq = 2000 - (t * 30000)
            freq = max(150, freq)
            val = math.sin(2 * math.pi * freq * t) * math.exp(-t * 90.0)
            # Add mechanical high-frequency noise
            noise = random.uniform(-0.2, 0.2) * math.exp(-t * 220.0)
            sample = int((val + noise) * 32767 * 0.45)
            sample = max(-32768, min(32767, sample))
            f.writeframes(struct.pack('<h', sample))

class MatrixRain:
    def __init__(self, width=40, height=25):
        self.width = width
        self.height = height
        self.drops = [random.randint(-15, 0) for _ in range(width)]
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*§"
        
    def update_and_render(self, elapsed, frame, right_w, right_h):
        if frame % 2 == 0:
            for i in range(len(self.drops)):
                self.drops[i] += 1
                if self.drops[i] >= right_h:
                    self.drops[i] = random.randint(-15, 0)
        lines = []
        for y in range(right_h):
            row = ""
            for x in range(right_w):
                drop_y = self.drops[x % len(self.drops)]
                dist = y - drop_y
                if dist < 0 or dist > 12:
                    row += " "
                elif dist == 0:
                    row += fg(255, 255, 255) + BOLD + random.choice(self.chars) + RST
                elif dist < 4:
                    row += fg(0, 191, 255) + BOLD + random.choice(self.chars) + RST
                elif dist < 8:
                    row += fg(186, 85, 211) + random.choice(self.chars) + RST
                else:
                    row += fg(75, 0, 130) + random.choice(self.chars) + RST
            lines.append(row)
        return lines

class LyricsEngine:
    def __init__(self):
        self.matrix = None
        self.click_sound = None
        self.last_char_counts = [0] * 10
        self.initialized_sound = False
        
    def init_sound(self):
        if self.initialized_sound:
            return
        ensure_click_sound()
        try:
            self.click_sound = pygame.mixer.Sound("click.wav")
            self.click_sound.set_volume(0.2)
        except Exception as e:
            pass
        self.initialized_sound = True
        
    def play_click(self):
        if self.click_sound:
            self.click_sound.play()

LYRICS_ENGINE = LyricsEngine()

def highlight_code_line(line, elapsed_line, trigger_time, pulse_val):
    def mix_pulse(base_color, peak_color, weight):
        r = lerp(base_color[0], peak_color[0], weight)
        g = lerp(base_color[1], peak_color[1], weight)
        b = lerp(base_color[2], peak_color[2], weight)
        return fg(r, g, b)

    C_KEYWORD  = (186, 85, 211)  # neon purple
    C_VARIABLE = (0, 191, 255)   # neon blue
    C_STRING   = (255, 165, 0)    # glowing orange
    C_COMMENT  = (0, 250, 154)    # medium spring green
    C_DEFAULT  = (240, 240, 240)  # white
    C_PEAK     = (255, 255, 255)  # pulse peak (pure white)

    keyword_fg = mix_pulse(C_KEYWORD, C_PEAK, pulse_val * 0.4)
    var_fg     = mix_pulse(C_VARIABLE, C_PEAK, pulse_val * 0.5)
    str_fg     = mix_pulse(C_STRING, C_PEAK, pulse_val * 0.3)
    comment_fg = mix_pulse(C_COMMENT, C_PEAK, pulse_val * 0.3)
    def_fg     = mix_pulse(C_DEFAULT, C_PEAK, pulse_val * 0.2)

    if line.strip().startswith('#'):
        return comment_fg + line + RST
        
    if line.startswith("import "):
        return keyword_fg + "import " + var_fg + line[7:] + RST
    elif line.startswith("def "):
        return keyword_fg + "def " + var_fg + "love_story" + def_fg + "():" + RST
    elif " = " in line:
        indent = len(line) - len(line.lstrip())
        trimmed = line.strip()
        var_name, val = trimmed.split(" = ")
        return (
            " " * indent + 
            var_fg + var_name + 
            def_fg + " = " + 
            str_fg + val + 
            RST
        )
    elif "if " in line:
        indent = len(line) - len(line.lstrip())
        return " " * indent + keyword_fg + "if " + var_fg + "Aata_Hai_Tumhe_Toh" + def_fg + ":" + RST
    elif "return " in line:
        indent = len(line) - len(line.lstrip())
        trimmed = line.strip()
        val = trimmed[7:]
        return " " * indent + keyword_fg + "return " + str_fg + val + RST
        
    return def_fg + line + RST

def render_right_column(elapsed, frame, right_w, right_h):
    LYRICS_ENGINE.init_sound()
    if LYRICS_ENGINE.matrix is None or LYRICS_ENGINE.matrix.width != right_w or LYRICS_ENGINE.matrix.height != right_h:
        LYRICS_ENGINE.matrix = MatrixRain(right_w, right_h)
        
    lines = []
    
    # ── TIMELINE PHASES ──
    # Phase 1: Boot Cursor (0.0s to 1.5s)
    if elapsed < 1.5:
        lines = [''] * right_h
        blink = int(elapsed * 4) % 2 == 0
        cursor = fg(0, 191, 255) + "▊" + RST if blink else " "
        
        if elapsed < 0.8:
            lines[2] = " " * 2 + cursor
        else:
            txt = "# SYSTEM BOOTING..."
            typed_duration = 0.7
            prog = min(1.0, (elapsed - 0.8) / typed_duration)
            char_count = int(prog * len(txt))
            
            if char_count > LYRICS_ENGINE.last_char_counts[0]:
                LYRICS_ENGINE.play_click()
                LYRICS_ENGINE.last_char_counts[0] = char_count
                
            typed_str = fg(0, 250, 154) + txt[:char_count] + RST
            lines[2] = " " * 2 + typed_str + cursor
            
    # Phase 2: Terminal Box Zoom-In (1.5s to 3.0s)
    elif elapsed < 3.0:
        lines = [''] * right_h
        prog = (elapsed - 1.5) / 1.5
        bw = int(lerp(6, right_w - 2, prog))
        bh = int(lerp(4, right_h - 2, prog))
        
        start_x = (right_w - bw) // 2
        start_y = (right_h - bh) // 2
        
        for y in range(bh):
            row_y = start_y + y
            if row_y < 0 or row_y >= right_h:
                continue
            if y == 0:
                box_str = fg(0, 191, 255) + "╔" + "═" * (bw - 2) + "╗" + RST
            elif y == bh - 1:
                box_str = fg(0, 191, 255) + "╚" + "═" * (bw - 2) + "╝" + RST
            else:
                box_str = fg(0, 191, 255) + "║" + " " * (bw - 2) + "║" + RST
            lines[row_y] = " " * start_x + box_str

    # Phase 3: Python Code Typing & Beat Sync (3.0s to 22.0s)
    elif elapsed < 22.0:
        t_w = right_w - 2
        t_h = right_h - 2
        pulse_val = max(0.0, math.sin(elapsed * math.pi * 1.5))
        pulse_val = pulse_val ** 4
        
        r_b = lerp(0, 255, pulse_val * 0.4)
        g_b = lerp(191, 255, pulse_val * 0.4)
        b_b = lerp(255, 255, pulse_val * 0.2)
        border_color = fg(int(r_b), int(g_b), int(b_b))
        
        code_lines = [
            "import love",
            "def love_story():",
            "    # Zulfon Ko Girake",
            "    eyes = \"Palkon Ko Jhukana\"",
            "    learn = \"Sikha Hai Kahan Se\"",
            "    magic = \"Yeh Jadoo Chalana\"",
            "    if Aata_Hai_Tumhe_Toh:",
            "        banana = \"Yun Baatein Banana\"",
            "        jaoji = \"Hato Bhi\"",
            "        return \"Chhodo Yun Satana\""
        ]
        
        t_lines = [
            3.0,
            4.0,
            ALL_LYRICS[1][0],
            ALL_LYRICS[2][0],
            ALL_LYRICS[3][0],
            ALL_LYRICS[4][0],
            ALL_LYRICS[5][0],
            ALL_LYRICS[6][0],
            ALL_LYRICS[7][0],
            ALL_LYRICS[8][0],
        ]
        
        rendered_code = []
        for idx, line in enumerate(code_lines):
            t_start = t_lines[idx]
            if elapsed < t_start:
                break
                
            t_next = t_lines[idx+1] if idx + 1 < len(t_lines) else 22.0
            type_duration = min(1.2, t_next - t_start)
            prog = min(1.0, (elapsed - t_start) / type_duration)
            char_count = int(prog * len(line))
            
            if char_count > LYRICS_ENGINE.last_char_counts[idx]:
                LYRICS_ENGINE.play_click()
                LYRICS_ENGINE.last_char_counts[idx] = char_count
                
            typed_part = line[:char_count]
            color_line = highlight_code_line(typed_part, elapsed - t_start, t_start, pulse_val)
            
            if char_count < len(line):
                blink = int(elapsed * 6) % 2 == 0
                cursor = fg(0, 191, 255) + "▊" + RST if blink else " "
                color_line += cursor
                
            rendered_code.append(color_line)
            
        lines.append(border_color + "┌" + "─" * t_w + "┐" + RST)
        title_str = border_color + "│ " + fg(0, 255, 255) + BOLD + "love_player.py" + RST
        lines.append(title_str + " " * (right_w - vlen(title_str) - 1) + border_color + "│" + RST)
        lines.append(border_color + "├" + "─" * t_w + "┤" + RST)
        
        for y in range(t_h - 3):
            code_idx = y
            if code_idx < len(rendered_code):
                cline = rendered_code[code_idx]
                row_str = border_color + "│ " + RST + pad(cline, t_w - 2) + border_color + " │" + RST
            else:
                row_str = border_color + "│ " + RST + " " * (t_w - 2) + border_color + " │" + RST
            lines.append(row_str)
            
        lines.append(border_color + "└" + "─" * t_w + "┘" + RST)

    # Phase 4: Zoom Out & Matrix Rain (22.0s to 25.5s)
    elif elapsed < 25.5:
        matrix_lines = LYRICS_ENGINE.matrix.update_and_render(elapsed, frame, right_w, right_h)
        if elapsed < 23.5:
            prog = (elapsed - 22.0) / 1.5
            bw = int(lerp(right_w - 2, 6, prog))
            bh = int(lerp(right_h - 2, 4, prog))
            start_x = (right_w - bw) // 2
            start_y = (right_h - bh) // 2
            
            for y in range(bh):
                row_y = start_y + y
                if row_y < 0 or row_y >= right_h:
                    continue
                if y == 0:
                    box_edge = "╔" + "═" * (bw - 2) + "╗"
                elif y == bh - 1:
                    box_edge = "╚" + "═" * (bw - 2) + "╝"
                else:
                    box_edge = "║" + " " * (bw - 2) + "║"
                
                matrix_lines[row_y] = " " * start_x + fg(0, 191, 255) + box_edge + RST + " " * (right_w - start_x - bw)
        lines = matrix_lines

    # Phase 5: Glitch SUBSCRIBE Ending (25.5s to end)
    else:
        if elapsed < 26.0:
            lines = []
            glitch_chars = "█▓▒░*?#@$%"
            for y in range(right_h):
                row = ""
                if random.random() < 0.7:
                    row_len = right_w
                    for _ in range(row_len):
                        col = random.choice([fg(0, 191, 255), fg(186, 85, 211), fg(0, 250, 154)])
                        row += col + random.choice(glitch_chars) + RST
                else:
                    row = " " * right_w
                lines.append(row)
        else:
            lines = [''] * right_h
            is_glitching = random.random() < 0.08
            offset_x = random.choice([-2, 1, 2]) if is_glitching else 0
            
            button_lines = [
                "┌───────────────────────────────┐",
                "│    ▶   S U B S C R I B E      │",
                "├───────────────────────────────┤",
                "│    LIKE • SHARE • SUPPORT     │",
                "└───────────────────────────────┘"
            ]
            
            if is_glitching:
                bl_idx = random.randint(0, len(button_lines)-1)
                button_lines[bl_idx] = button_lines[bl_idx].replace("SUBSCRIBE", "SU█▓▒CRIBE")
                
            start_y = (right_h - len(button_lines)) // 2
            
            for y in range(right_h):
                if y >= start_y and y < start_y + len(button_lines):
                    btn_y = y - start_y
                    if btn_y == 1:
                        color = fg(0, 255, 255) + BOLD
                    elif btn_y == 3:
                        color = fg(186, 85, 211)
                    else:
                        color = fg(0, 191, 255)
                        
                    btn_line = color + button_lines[btn_y] + RST
                    pad_l = max(0, (right_w - len(button_lines[0])) // 2 + offset_x)
                    lines[y] = " " * pad_l + btn_line
                else:
                    row = ""
                    for x in range(right_w):
                        if random.random() < 0.015:
                            p_color = random.choice([fg(0, 191, 255), fg(186, 85, 211)])
                            row += p_color + random.choice(["•", "*", "∘", "✧"]) + RST
                        else:
                            row += " "
                    lines[y] = row
                    
    while len(lines) < right_h:
        lines.append('')
    return lines[:right_h]

def run_sync_mode():
    if not os.path.exists(AUDIO_FILE):
        print(f"\033[31m[ERROR] Audio file not found: {AUDIO_FILE}\033[0m")
        sys.exit(1)

    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    ensure_click_sound()
    
    lines = [
        "Zulfon Ko Girake",
        "Palkon Ko Jhukana",
        "Sikha Hai Kahan Se",
        "Yeh Jadoo Chalana",
        "Aata Hai Tumhe Toh",
        "Yun Baatein Banana",
        "Jaoji Hato Bhi",
        "Chhodo Yun Satana"
    ]
    
    sys.stdout.write('\033[2J\033[H')
    print("\033[1;36m" + "═" * 60)
    print("      RETRO TERMINAL LYRICS SYNCHRONIZATION TOOL")
    print("═" * 60 + "\033[0m")
    print("\nHow it works:")
    print("1. The song will play.")
    print("2. You will see each lyric line printed below.")
    print("3. Press \033[1;32mSPACEBAR\033[0m or Enter the exact moment the line is sung!")
    print("4. The tool will record the millisecond-perfect timing.")
    print("5. Once done, it will automatically save it directly into 'player.py'!")
    print("\nReady? Press \033[1;33mENTER\033[0m to start the music...")
    input()
    
    pygame.mixer.music.play()
    start_time = time.time()
    timestamps = []
    
    for i, line in enumerate(lines):
        sys.stdout.write('\033[2J\033[H')
        print("\033[1;36m" + "═" * 60)
        print("          LYRICS SYNCHRONIZATION RUNNING...          ")
        print("═" * 60 + "\033[0m\n")
        
        for j, l in enumerate(lines):
            if j < i:
                print(f"  \033[32m✔ [Synced at {timestamps[j]:.2f}s]\033[0m  {l}")
            elif j == i:
                print(f"  \033[1;33;5m▶▶ PRESS SPACEBAR NOW ▶▶\033[0m  \033[1;37;104m {l} \033[0m")
            else:
                print(f"    [Pending]         {l}")
                
        import msvcrt
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch in (b' ', b'\r', b'\n'):
                    ts = pygame.mixer.music.get_pos() / 1000.0
                    if ts < 0:
                        ts = time.time() - start_time
                    timestamps.append(round(ts, 2))
                    try:
                        pygame.mixer.Sound("click.wav").play()
                    except:
                        pass
                    break
            time.sleep(0.01)
            
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            content = f.read()
            
        s1_lines = []
        for idx in range(4):
            s1_lines.append(f"    ({timestamps[idx]}, \"{lines[idx]}\"),")
            
        s2_lines = []
        for idx in range(4, 8):
            s2_lines.append(f"    ({timestamps[idx]}, \"{lines[idx]}\"),")
            
        key1 = "LYRICS_STANZA_1"
        key2 = "LYRICS_STANZA_2"
        
        stanza1_str = f"{key1} = [\n" + "\n".join(s1_lines) + "\n]"
        stanza2_str = f"{key2} = [\n" + "\n".join(s2_lines) + "\n]"
        
        import re
        content = re.sub(rf'^{key1}\s*=\s*\[.*?\]', stanza1_str, content, flags=re.DOTALL | re.MULTILINE)
        content = re.sub(rf'^{key2}\s*=\s*\[.*?\]', stanza2_str, content, flags=re.DOTALL | re.MULTILINE)
        
        with open(__file__, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("\n\033[1;32m✔ SUCCESS! Timestamps successfully updated in 'player.py'!\033[0m")
        print("Updated Timestamps:")
        for idx, l in enumerate(lines):
            print(f"  - {l}: {timestamps[idx]:.2f}s")
        print("\nRun \033[1;36mpython player.py\033[0m to play the song with perfectly animated, lag-free lyrics!")
    except Exception as e:
        print(f"\033[31m[ERROR] Failed to save timestamps to file: {e}\033[0m")
        
    sys.exit(0)


# ═══════════════════════════════════════════════════════
#  BUILD FRAME
# ═══════════════════════════════════════════════════════
def build_frame(elapsed, total, frame, W, H):
    buf = []
    inner = W - 2
    f = frame  # shorthand
    
    # Helper: animated gradient top/bottom border
    def hborder(left_ch, fill_ch, right_ch):
        return gradient_border_h(left_ch, 1, f) + gradient_border_h(fill_ch, inner, f) + gradient_border_h(right_ch, 1, f)
    
    def hsep():
        return gradient_border_h('├', 1, f) + gradient_border_h('─', inner, f) + gradient_border_h('┤', 1, f)
    
    bv_idx = [0]
    def bv():
        bv_idx[0] += 1
        return border_v(f, bv_idx[0])

    # ════════ TOP BORDER ════════
    buf.append(hborder('┌', '─', '┐'))
    
    # ════════ TOP BAR ════════
    now = datetime.now()
    date_str = now.strftime("%d %b %Y | %I:%M %p")
    
    top_left  = gradient_text_bold(' ♫ Retro Bollywood Player', GRAD_NEON, f * 0.1)
    top_center = gradient_text_bold('♫ NOW PLAYING ♫', GRAD_FIRE, f * 0.15)
    top_right = gradient_text(date_str + ' ', GRAD_CYAN_MAGENTA, f * 0.08)
    
    tl = vlen(top_left)
    tc = vlen(top_center)
    tr = vlen(top_right)
    g1 = max(1, (inner - tl - tc - tr) // 2)
    g2 = max(1, inner - tl - tc - tr - g1)
    
    top_content = top_left + ' ' * g1 + top_center + ' ' * g2 + top_right
    buf.append(bv() + pad(top_content, inner) + bv())
    
    buf.append(hsep())
    
    # ════════ MAIN CONTENT: Two columns ════════
    left_w  = (W - 3) * 55 // 100
    right_w = (W - 3) - left_w
    
    # ── LEFT COLUMN ──
    left_lines = []
    poster_w = 22
    info_w = left_w - poster_w - 2
    
    # Poster with gradient animation
    for pi, line in enumerate(POSTER_ART):
        p_colored = gradient_text(line, GRAD_POSTER, f * 0.05 + pi * 0.3)
        left_lines.append(p_colored)
    
    # Song info with gradient
    info_data = [
        ('', '', None),
        (' ♫ ' + SONG["title"], GRAD_FIRE, True),
        ('   ' + SONG["movie"], GRAD_NEON, False),
        ('   ─────────────────', GRAD_SEPARATOR, False),
        ('', None, None),
        ('   ♪ Singer(s):', GRAD_CYAN_MAGENTA, False),
        ('   ' + SONG["singers"], GRAD_PINK_GOLD, False),
        ('', None, None),
        ('   ♫ Music Director:', GRAD_CYAN_MAGENTA, False),
        ('   ' + SONG["music"], GRAD_PINK_GOLD, False),
        ('', None, None),
        ('   ✎ Lyricist:', GRAD_CYAN_MAGENTA, False),
        ('   ' + SONG["lyricist"], GRAD_PINK_GOLD, False),
        ('', None, None),
        ('   ⌬ Edit & Gfx:', GRAD_CYAN_MAGENTA, False),
        ('   ' + SONG["gfx"], GRAD_PINK_GOLD, False),
        ('   ' + SONG["gfx_studio"], GRAD_PINK_GOLD, False),
    ]
    
    info_lines = []
    for txt, grad, is_bold in info_data:
        if not txt:
            info_lines.append('')
        elif grad and is_bold:
            info_lines.append(gradient_text_bold(txt, grad, f * 0.12))
        elif grad:
            info_lines.append(gradient_text(txt, grad, f * 0.1))
        else:
            info_lines.append(txt)
    
    # Merge poster + info side by side
    max_rows = max(len(POSTER_ART), len(info_lines))
    merged_left = []
    for i in range(max_rows):
        p_part = left_lines[i] if i < len(left_lines) else ' ' * 20
        i_part = info_lines[i] if i < len(info_lines) else ''
        combined = pad(p_part, poster_w) + pad(i_part, info_w)
        merged_left.append(' ' + pad(combined, left_w - 1))
    
    merged_left.append(' ' * left_w)
    
    # Cast & Crew with gradient
    cast_box_w = left_w - 4
    cast_title = gradient_text_bold(' 🎬 Movie Cast & Crew:', GRAD_FIRE, f * 0.1)
    
    cast_items = [
        ('Producer', SONG["producer"]),
        ('Director', SONG["director"]),
        ('Cast    ', SONG["cast"]),
    ]
    
    cast_lines = []
    cast_lines.append(gradient_border_h('┌', 1, f) + gradient_border_h('─', cast_box_w, f) + gradient_border_h('┐', 1, f))
    cast_lines.append(border_v(f, 90) + pad(cast_title, cast_box_w) + border_v(f, 91))
    
    for ci, (label, value) in enumerate(cast_items):
        label_g = gradient_text('  • ' + label, GRAD_CYAN_MAGENTA, f * 0.08 + ci * 0.5)
        value_g = gradient_text(' : ' + value, GRAD_ROSE, f * 0.1 + ci * 0.3)
        cast_lines.append(border_v(f, 92+ci) + pad(label_g + value_g, cast_box_w) + border_v(f, 93+ci))
    
    cast_lines.append(gradient_border_h('└', 1, f) + gradient_border_h('─', cast_box_w, f) + gradient_border_h('┘', 1, f))
    
    for cl in cast_lines:
        merged_left.append(' ' + pad(cl, left_w - 1))
    
    # ── RIGHT COLUMN (Lyrics) ──
    right_lines = render_right_column(elapsed, f, right_w, len(merged_left))
    
    # ── Merge columns ──
    max_body = max(len(merged_left), len(right_lines))
    for i in range(max_body):
        ll = merged_left[i] if i < len(merged_left) else ' ' * left_w
        rl = right_lines[i] if i < len(right_lines) else ' ' * right_w
        row = bv() + pad(ll, left_w) + bv() + pad(rl, right_w) + bv()
        buf.append(row)
    
    buf.append(hsep())
    
    # ════════ PROGRESS BAR with gradient ════════
    bar_w = W - 18
    ratio = min(elapsed / total, 1.0) if total > 0 else 0
    filled = int(ratio * bar_w)
    
    pbar = ''
    for i in range(bar_w):
        if i < filled:
            t = i / max(bar_w, 1)
            r = lerp(0, 255, t)
            g = lerp(255, 200, t)
            b = lerp(100, 0, t)
            pbar += fg(r, g, b) + '━' + RST
        elif i == filled:
            pbar += fg(255, 255, 255) + BOLD + '●' + RST
        else:
            pbar += DIM_GREY + '─' + RST
    
    tl_str = gradient_text_bold(fmt_time(elapsed), GRAD_NEON, f * 0.1)
    tr_str = gradient_text_bold(fmt_time(total), GRAD_NEON, f * 0.1 + 1)
    
    progress = ' ' + tl_str + '  ' + pbar + '  ' + tr_str + ' '
    buf.append(bv() + pad(progress, inner) + bv())
    
    buf.append(hsep())
    
    # ════════ CONTROLS BAR ════════
    vol = render_volume_bars(80)
    eq  = render_eq_mini(f, 8)
    
    controls = (
        ' ' + gradient_text('◀))', GRAD_NEON, f * 0.1) + ' ' +
        vol + ' ' +
        gradient_text('80%', GRAD_NEON, f * 0.08) +
        '      ' +
        gradient_text('⇄', GRAD_CYAN_MAGENTA, f * 0.1) + '    ' +
        gradient_text('⏮', GRAD_PINK_GOLD, f * 0.12) + '   ' +
        gradient_text_bold('⏵', GRAD_FIRE, f * 0.2) + '   ' +
        gradient_text('⏭', GRAD_PINK_GOLD, f * 0.12) + '    ' +
        gradient_text('⟳', GRAD_CYAN_MAGENTA, f * 0.1) +
        '          ' +
        gradient_text_bold('[[ STEREO ]]', GRAD_NEON, f * 0.12) +
        '   ' + eq
    )
    
    buf.append(bv() + pad(controls, inner) + bv())
    buf.append(hsep())
    
    # ════════ BOTTOM STATUS BAR ════════
    st_l = gradient_text(' Playing: ', GRAD_LYRIC_DIM, f * 0.05) + gradient_text_bold(SONG["title"], GRAD_NEON, f * 0.12)
    st_c = gradient_text('Album: ', GRAD_LYRIC_DIM, f * 0.05) + gradient_text(SONG["movie"], GRAD_CYAN_MAGENTA, f * 0.1)
    st_r = gradient_text_bold('Love Bollywood ', GRAD_STATUS, f * 0.15) + fg(255, 50, 50) + '❤' + RST + ' '
    
    sl = vlen(st_l); sc = vlen(st_c); sr = vlen(st_r)
    sg1 = max(1, (inner - sl - sc - sr) // 2)
    sg2 = max(1, inner - sl - sc - sr - sg1)
    
    status = st_l + ' ' * sg1 + st_c + ' ' * sg2 + st_r
    buf.append(bv() + pad(status, inner) + bv())
    
    buf.append(hborder('└', '─', '┘'))
    
    # Pad to H-1 lines to prevent terminal scrolling/shaking
    while len(buf) < H - 1:
        buf.append('')
    
    return '\n'.join(buf[:H-1])


# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    if "--sync" in sys.argv:
        run_sync_mode()

    if not os.path.exists(AUDIO_FILE):
        print(f"{RED}[ERROR] Audio file not found: {AUDIO_FILE}{RST}")
        sys.exit(1)

    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)

    try:
        from mutagen.mp3 import MP3
        total_duration = MP3(AUDIO_FILE).info.length
    except Exception:
        total_duration = 30.37

    # Hide cursor and clear screen completely once
    sys.stdout.write(HIDE + CLR)
    sys.stdout.flush()

    pygame.mixer.music.play()
    start = time.time()
    frame = 0

    try:
        while pygame.mixer.music.get_busy():
            # Get millisecond-perfect elapsed time from the audio mixer directly
            elapsed = pygame.mixer.music.get_pos() / 1000.0
            if elapsed < 0:
                elapsed = time.time() - start
                
            cols, rows = shutil.get_terminal_size((100, 35))

            # Subtract 1 from cols and rows to prevent Windows console auto-wrapping
            # which causes the screen to shake/flicker
            output = build_frame(elapsed, total_duration, frame, cols - 1, rows - 1)

            # Move cursor to top-left and overwrite, avoiding scroll
            sys.stdout.write(HOME + output)
            sys.stdout.flush()

            frame += 1
            time.sleep(0.08)  # Faster update for smoother karaoke

    except KeyboardInterrupt:
        pass
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        sys.stdout.write(SHOW + CLR)
        sys.stdout.flush()
        print(f"\n{NEON_GREEN}{BOLD}  ♫ Thanks for Watching!{RST}")
        print(f"{GREY}  Retro Bollywood Player — Love Bollywood {RED}❤{RST}\n")


if __name__ == '__main__':
    main()
