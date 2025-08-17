import math
import time
import sys
import os
import shutil
import msvcrt  # For ESC key
import pygame.midi
import threading
import ctypes
import tempfile
import atexit
import signal

# Enable reliable cross-platform ANSI color output (even on Windows cmd)
# Colorama ensures that ANSI escape sequences like green text work correctly
from colorama import init, Fore, Style
init(autoreset=True)

# Force Windows terminal to support ANSI escape sequences
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

GREEN = Fore.LIGHTGREEN_EX
DARK_GREEN = Fore.GREEN
RESET = Style.RESET_ALL

# Hex data for a simple MIDI file
midi_data = bytes.fromhex('4D546864000000060001000200604D54726B000000D500FF7F0F050F1C323032342E30382E3031010300FF7F2C050F2D4D6963726F736F66742053616E732053657269662C382E32352C46616C73652C46616C73652C312C3000FF7F34050F1203037F7F00FF010428537065616B65727320285265616C74656B204869676820446566696E6974696F6E20417564696F2900FF0122436F6D706F7365642077697468206A756D6D6275732E6269746275636B65742E696F00FF510303D09000FF58040802180800FF5902FD0100FF060A4C6F6F702053746172749800FF06084C6F6F7020456E6400FF2F004D54726B00000C1900FF7F05050F094C4800FF7F2E050F0647656E6572616C204D494449202D204D6963726F736F667420475320576176657461626C652053796E746800C05000FF58040802180800FF030F7069746368206368616E6E656C203000B0650000B0640000B0061800B0260000B0657F00B0647F00FF040C496E737472756D656E74203100B0077F00B00A4000903C5A30803C5A00B00B6D00903C5A01E0723F01E0643F01E0553F01E0473F01E0393F01E02B3F01E01C3F01E00E3F01E0003F01E0723E01E0643E01E0553E01E0473E01E0393E01E02B3E01E01C3E01E00E3E01E0003E01E0723D01E0643D01E0553D01E0473D01E0393D01E02B3D01E01C3D01E00E3D01E0003D01E0723C01E0643C01E0553C01E0473C01E0393C01E02B3C01E01C3C01E00E3C01E0003C01E0723B01E0643B01E0553B01E0473B01E0393B01E02B3B01E01C3B01E00E3B01E0003B01E0723A01E0643A01803C5A00E0004000B00B5400903C5A30803C5A00B00B7F00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00B00B5400903C5A60803C5A30B00B7F00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A30803C5A00B00B6D00903C5A30803C5A00B00B7F00903C5A0C803C5A0090485A0C80485A00903C5A0C803C5A0090485A0C80485A00B00B5400903C5A01E0723F01E0643F01E0553F01E0473F01E0393F01E02B3F01E01C3F01E00E3F01E0003F01E0723E01E0643E01E0553E01E0473E01E0393E01E02B3E01E01C3E01E00E3E01E0003E01E0723D01E0643D01E0553D01E0473D01E0393D01E02B3D01E01C3D01E00E3D01E0003D01E0723C01E0643C01E0553C01E0473C01E0393C01E02B3C01E01C3C01E00E3C01E0003C01E0723B01E0643B01E0553B01E0473B01E0393B01E02B3B01E01C3B01E00E3B01E0003B01E0723A01E0643A01803C5A00E0004000B00B7F00903C5A30803C5A00B00B6D00903C5A30803C5A00B00B7F00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00B00B5400903C5A30803C5A00B00B7F0090385A3080385A00B00B6D0090385A01E0793F01E0723F01E06B3F01E0643F01E05C3F01E0553F01E04E3F01E0473F01E0403F01E0393F01E0323F01E02B3F01E0243F01E01C3F01E0153F01E00E3F01E0073F01E0003F01E0793E01E0723E01E06B3E01E0643E01E05C3E01E0553E01E04E3E01E0473E01E0403E01E0393E01E0323E01E02B3E01E0243E01E01C3E01E0153E01E00E3E01E0073E01E0003E01E0793D01E0723D01E06B3D01E0643D01E05C3D01E0553D01E04E3D01E0473D01E0403D01E0393D01E0323D0180385A00E0004000B00B540090385A3080385A00B00B7F0090385A0680385A00903F5A06803F5A0090445A0680445A00903F5A06803F5A0090385A0680385A00903F5A06803F5A0090445A0680445A00903F5A06803F5A00B00B540090385A6080385A30B00B7F0090385A0680385A00903F5A06803F5A0090445A0680445A00903F5A06803F5A0090385A0680385A00903F5A06803F5A0090445A0680445A00903F5A06803F5A0090385A3080385A00B00B6D0090385A3080385A00B00B7F0090385A0C80385A0090445A0C80445A0090385A0C80385A0090445A0C80445A00B00B540090385A01E0793F01E0723F01E06B3F01E0643F01E05C3F01E0553F01E04E3F01E0473F01E0403F01E0393F01E0323F01E02B3F01E0243F01E01C3F01E0153F01E00E3F01E0073F01E0003F01E0793E01E0723E01E06B3E01E0643E01E05C3E01E0553E01E04E3E01E0473E01E0403E01E0393E01E0323E01E02B3E01E0243E01E01C3E01E0153E01E00E3E01E0073E01E0003E01E0793D01E0723D01E06B3D01E0643D01E05C3D01E0553D01E04E3D01E0473D01E0403D01E0393D01E0323D0180385A00E0004000B00B7F0090385A3080385A00B00B6D0090385A3080385A00B00B7F0090385A0680385A00903F5A06803F5A0090445A0680445A00903F5A06803F5A0090385A0680385A00903F5A06803F5A0090445A0680445A00903F5A06803F5A00B00B540090385A3080385A00B00B7F00903C5A30803C5A00B00B6D00903C5A01E0723F01E0643F01E0553F01E0473F01E0393F01E02B3F01E01C3F01E00E3F01E0003F01E0723E01E0643E01E0553E01E0473E01E0393E01E02B3E01E01C3E01E00E3E01E0003E01E0723D01E0643D01E0553D01E0473D01E0393D01E02B3D01E01C3D01E00E3D01E0003D01E0723C01E0643C01E0553C01E0473C01E0393C01E02B3C01E01C3C01E00E3C01E0003C01E0723B01E0643B01E0553B01E0473B01E0393B01E02B3B01E01C3B01E00E3B01E0003B01E0723A01E0643A01803C5A00E0004000B00B5400903C5A30803C5A00B00B7F00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00B00B5400903C5A60803C5A30B00B7F00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A30803C5A00B00B6D00903C5A30803C5A00B00B7F00903C5A0C803C5A0090485A0C80485A00903C5A0C803C5A0090485A0C80485A00B00B5400903C5A01E0723F01E0643F01E0553F01E0473F01E0393F01E02B3F01E01C3F01E00E3F01E0003F01E0723E01E0643E01E0553E01E0473E01E0393E01E02B3E01E01C3E01E00E3E01E0003E01E0723D01E0643D01E0553D01E0473D01E0393D01E02B3D01E01C3D01E00E3D01E0003D01E0723C01E0643C01E0553C01E0473C01E0393C01E02B3C01E01C3C01E00E3C01E0003C01E0723B01E0643B01E0553B01E0473B01E0393B01E02B3B01E01C3B01E00E3B01E0003B01E0723A01E0643A01803C5A00E0004000B00B7F00903C5A30803C5A00B00B6D00903C5A30803C5A00B00B7F00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00903C5A06803C5A0090435A0680435A0090485A0680485A0090435A0680435A00B00B5400903C5A30803C5A00B00B7F00903F5A30803F5A00B00B6D00903F5A01E0793F01E0723F01E06B3F01E0643F01E05C3F01E0553F01E04E3F01E0473F01E0403F01E0393F01E0323F01E02B3F01E0243F01E01C3F01E0153F01E00E3F01E0073F01E0003F01E0793E01E0723E01E06B3E01E0643E01E05C3E01E0553E01E04E3E01E0473E01E0403E01E0393E01E0323E01E02B3E01E0243E01E01C3E01E0153E01E00E3E01E0073E01E0003E01E0793D01E0723D01E06B3D01E0643D01E05C3D01E0553D01E04E3D01E0473D01E0403D01E0393D01E0323D01803F5A00E0004000B00B5400903F5A30803F5A00B00B7F00903F5A06803F5A0090465A0680465A00904B5A06804B5A0090465A0680465A00903F5A06803F5A0090465A0680465A00904B5A06804B5A0090465A0680465A00B00B5400903F5A60803F5A30B00B7F00904B5A06804B5A0090465A0680465A00903F5A06803F5A0090465A0680465A00904B5A06804B5A0090465A0680465A00903F5A06803F5A0090465A0680465A00903F5A30803F5A00B00B6D00903F5A30803F5A00B00B7F00903F5A0C803F5A00904B5A0C804B5A00903F5A0C803F5A00904B5A0C804B5A00B00B5400903F5A01E0793F01E0723F01E06B3F01E0643F01E05C3F01E0553F01E04E3F01E0473F01E0403F01E0393F01E0323F01E02B3F01E0243F01E01C3F01E0153F01E00E3F01E0073F01E0003F01E0793E01E0723E01E06B3E01E0643E01E05C3E01E0553E01E04E3E01E0473E01E0403E01E0393E01E0323E01E02B3E01E0243E01E01C3E01E0153E01E00E3E01E0073E01E0003E01E0793D01E0723D01E06B3D01E0643D01E05C3D01E0553D01E04E3D01E0473D01E0403D01E0393D01E0323D01803F5A00E0004000B00B7F00903F5A30803F5A00B00B6D00903F5A30803F5A00B00B7F00903F5A06803F5A0090465A0680465A00904B5A06804B5A0090465A0680465A00903F5A06803F5A0090465A0680465A00904B5A06804B5A0090465A0680465A00B00B5400903F5A30803F5A00FF2F00')

# Get system temp folder
temp_dir = tempfile.gettempdir()
midi_path = os.path.join(temp_dir, "demo.mid")

# Write MIDI file to temp
with open(midi_path, "wb") as f:
    f.write(midi_data)
print(f"MIDI Loaded: {midi_path}")

# Ensure cleanup on exit
def cleanup():
    try:
        pygame.mixer.music.stop()
    except:
        pass
    if os.path.exists(midi_path):
        os.remove(midi_path)

# Register for normal exit
atexit.register(cleanup)

# Also register for Ctrl+C or termination
for sig in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, lambda signum, frame: cleanup() or sys.exit(0))

# MIDI Setup
def play_midi_background(filename):
    try:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)  # Loop infinitely
    except Exception as e:
        print(f"[!] MIDI error: {e}")

# Start MIDI playback in background thread
midi_thread = threading.Thread(target=play_midi_background, args=(midi_path,), daemon=True)
midi_thread.start()

# Auto Maximize for Window
def maximize_console():
    # Load required Windows libraries
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32

    # Get handle to the current console window
    hWnd = kernel32.GetConsoleWindow()

    if hWnd:
        SW_MAXIMIZE = 3  # Constant for maximizing the window
        # ShowWindow applies the maximize command to the console window
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

# Set the console window title using Windows API
ctypes.windll.kernel32.SetConsoleTitleW("_--=== LEGENDARY CUBE VISUALIZER ===--_")

# Call it once at the beginning to maximize the CMD window
maximize_console()

# Cube vertex and edge definitions
cube_vertices = [
    [-1, -1, -1], [-1, -1,  1], [-1,  1, -1], [-1,  1,  1],
    [ 1, -1, -1], [ 1, -1,  1], [ 1,  1, -1], [ 1,  1,  1]
]

edges = [
    (0, 1), (1, 3), (3, 2), (2, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Dark trail buffer
trail_frames = []
TRAIL_LENGTH = 5

def rotate_point(x, y, z, ax, ay, az):
    sin_ax, cos_ax = math.sin(ax), math.cos(ax)
    y, z = y * cos_ax - z * sin_ax, y * sin_ax + z * cos_ax

    sin_ay, cos_ay = math.sin(ay), math.cos(ay)
    x, z = x * cos_ay + z * sin_ay, -x * sin_ay + z * cos_ay

    sin_az, cos_az = math.sin(az), math.cos(az)
    x, y = x * cos_az - y * sin_az, x * sin_az + y * cos_az

    return x, y, z

def project(x, y, z, offset_x, offset_y, width, height):
    distance = 3
    factor = 30 / (z + distance)
    aspect_ratio = 2.0
    x_proj = int(offset_x + factor * x * aspect_ratio)
    y_proj = int(offset_y - factor * y)
    return x_proj, y_proj

def draw_line(buf, x1, y1, x2, y2, width, height, char='*', color=''):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return
    for i in range(steps + 1):
        x = int(x1 + dx * i / steps)
        y = int(y1 + dy * i / steps)
        if 0 <= x < width and 0 <= y < height:
            buf[y][x] = color + char + RESET

def clear_screen():
    print("\033[2J\033[H", end='')  # Clear screen and move cursor to top-left

# Cube offset and speed
offset_x = 40
offset_y = 20
vel_x = 1
vel_y = 1

prev_time = time.time()
fps_display = "FPS: unknown!!!"

scroll_text = None
frame = 0
amplitude = 2       # Vertical wave height
wave_speed = 0.1    # Sine wave frequency
scroll_speed = 0.5    # Scrolling speed

try:
    while True:
        size = shutil.get_terminal_size((80, 40))
        WIDTH = size.columns
        HEIGHT = size.lines - 1

        # Initialize scroll_text after WIDTH is known
        if scroll_text is None:
            scroll_text = " " * WIDTH + "                                                         HEYA- GREETINGS! BEHOLD THE POWERFUL CUBE!!!!!!!!!                                                                                                    THIS IS GOING TO GET CRAZY!!                                                                                                                                                                                        WE ARE SOULS HERE...                                     HAVE YOU CHECKED IF YOU’RE IN FULL-SCREEN, KING?                                                                                                                                    THIS COULD ACTUALLY HAPPEN...                                                                                                         IF YOU  S T A R E  INTO MY GLORIOUSLY VISUALIZED CUBE             YOUR MIND MAY BEND!!!!!!!!!                                                                                                                                                                         THIS...             TOOK...              ME...                  2       4       H   O   U  R  S    .............................................................                                                                                                                                                                                                                                     LET’S SIT BACK TOGETHER AND WATCH YOUR               F  A  V  O  R  I  T  E         S H O W               !!!!!!!!!!!!!!!!!                                                                                                                                                                           RIGHT??                                                                                                                                                                                                                                                                                                                                             ARE     YOU     O K A Y     BUDDY?                                                                                                                                                                                                                                                                                                                                                           PROBABLY YOU’RE STILL            W  A  T  C  H  I  N  G                      THE   C U B E ?                                            OR MAYBE I SHOULD CALL IT... A   B O X?                                                                                   UHHH..............         MAYBE.... ?                    SOMETHING... ?                                                                                                                                                                                                ALRIGHT THEN.....                                                                                                                                          HAVE A    G O O D   T I M E           WATCHING   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                                                                                                                                                                                    PLEASE WELCOME TOOOOOO MYYYY   L   E   G  E   N   D   A  R   Y     C U B E  !!!                                                                                 MY LORD...                                                         WE  ARE  YOUR MEMBERS..............                                                                                               WE...       ARE...            Y  O  U  R  ...                  Q     U    E    E    N    S  !!!                                                                                                                           NOT FOR       CRIMINALS!                  Y  O  U                 M    O    N   S     T     E    R    !!!!!!                                                                              Y  O  U         R   U  I  N  E  D         M   Y                 P        Y        T         H       O       N                   S    C    R    I    P  T   ! !  !  !!!!!!!!!!!!                       I     W   I   L   L          D    E      L    E    T      E       Y  O  U  R           P   E    R   S  O  N  A  L            B     A      C      K      U       P              F  I  L  E  S     .  .  .  .  . ... ....                                                                          HAHAHA....           J U S T    KIDDING!!!                                                                                                   NO    WORRIES....                                        I'M    H E R E ....                                                                                                                                                                                                                                                            OKAY!                           LET’S GO BACK TO THE BEGINNING OF ALL WORLDS!!!                                 UHHH.... NO.....                                                                                   PHEW...                                                                                                                                                      "

        buffer = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
        projected = []

        # Rotate and project cube
        for vertex in cube_vertices:
            x, y, z = rotate_point(*vertex, angle_x := frame * 0.05, angle_y := frame * 0.03, angle_z := frame * 0.02)
            x_proj, y_proj = project(x, y, z, offset_x, offset_y, WIDTH, HEIGHT)
            projected.append((x_proj, y_proj))

        # Add current frame edges to trail
        frame_lines = []
        for edge in edges:
            x1, y1 = projected[edge[0]]
            x2, y2 = projected[edge[1]]
            frame_lines.append((x1, y1, x2, y2))
        trail_frames.append(frame_lines)
        if len(trail_frames) > TRAIL_LENGTH:
            trail_frames.pop(0)

        # Draw trails with fading effect
        for i, lines in enumerate(trail_frames):
            char = '#'
            color = GREEN if i == len(trail_frames) - 1 else DARK_GREEN
            char = '#' if i == len(trail_frames) - 1 else '.'
            for x1, y1, x2, y2 in lines:
                draw_line(buffer, x1, y1, x2, y2, WIDTH, HEIGHT, char=char, color=color)

        # Left-scrolling sine-wave text
        wave_height = int(HEIGHT * 0.9)
        wave_amplitude = int(HEIGHT * 0.08)
        wave_freq = 0.01

        for i in range(WIDTH):
            index = int((frame * scroll_speed + i)) % len(scroll_text)
            ch = scroll_text[index]
            x = i
            y = wave_height + int(math.sin((frame * wave_freq) + i * 0.3) * wave_amplitude)
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                buffer[y][x] = GREEN + ch + RESET

        clear_screen()
        buffer[0][0:len(fps_display)] = list(fps_display)
        sys.stdout.write('\033[2J\033[H' + '\n'.join(''.join(row) for row in buffer))
        sys.stdout.flush()

        offset_x += vel_x
        offset_y += vel_y
        margin_x = 30
        margin_y = 10
        if offset_x < margin_x or offset_x > WIDTH - margin_x:
            vel_x *= -1
        if offset_y < margin_y or offset_y > HEIGHT - margin_y:
            vel_y *= -1

        # FPS Calculation
        current_time = time.time()
        delta_time = current_time - prev_time
        fps_display = f"{GREEN}FPS: {1 / delta_time:.2f}{RESET}"
        prev_time = current_time

        frame += 1

        if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
            break

        time.sleep(0.02)

except KeyboardInterrupt:
    pass
finally:
    try:
        # Stop any playing MIDI music
        pygame.mixer.music.stop()
        
        # Clean up the mixer to release resources
        pygame.mixer.quit()
        
        # Check if the temporary MIDI file exists
        if os.path.exists(midi_path):
            # Delete the MIDI file from the temp folder
            os.remove(midi_path)
            print(f"Deleted MIDI: {midi_path}")
        else:
            # Inform that the file was already missing
            print("MIDI file not found!!!")
    except Exception as e:
        # Catch and display any errors during cleanup
        print(f"Failed to delete MIDI!!! : {e}")