import glfw
from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
import random
import sys
import numpy as np

bspd = 0.02  # block dx value
name = input("Enter your name to play: ")
b1x, b1y = 50.0, 0.0  # block 1 initial position
hm = 0.0  # copter moving dy value
i, sci = 0, 1  # score integer
scf = 1  # score float
scs, slevel = "", ""  # score string, level string
level, lflag, wflag = 1, 1, 1
game_started = False

def init():
    global b1y
    b1y = random.randint(10, 54)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLoadIdentity()
    glOrtho(0.0, 100.0, 0.0, 100.0, -1.0, 1.0)

def draw_copter():
    glColor3f(0.7, 1.0, 1.0)
    glRectf(10, 49.8, 19.8, 44.8)  # body
    glRectf(2, 46, 10, 48)  # tail
    glRectf(2, 46, 4, 51)  # tail up
    glRectf(14, 49.8, 15.8, 52.2)  # propeller stand
    glRectf(7, 53.6, 22.8, 52.2)  # propeller

# Function to render text using Pillow
def render_text(position, text_string, font_size=18, color=(255, 255, 255)):
    font_path = "C:/Windows/Fonts/arial.ttf"  # Change path to a valid font file
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found. Please check the path and try again.")
        sys.exit(1)

    text_image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)
    text_bbox = draw.textbbox((0, 0), text_string, font=font)
    text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

    text_image = Image.new('RGBA', text_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text_string, font=font, fill=color + (255,))

    text_data = np.array(text_image)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_size[0], text_size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(position[0], position[1])
    glTexCoord2f(1, 1)
    glVertex2f(position[0] + text_size[0] / 10, position[1])
    glTexCoord2f(1, 0)
    glVertex2f(position[0] + text_size[0] / 10, position[1] + text_size[1] / 10)
    glTexCoord2f(0, 0)
    glVertex2f(position[0], position[1] + text_size[1] / 10)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDeleteTextures([texture_id])

# Function to display the game
def display():
    global i, scf, sci, level, lflag, wflag, b1x, b1y, bspd, hm, scs, slevel, game_started

    glClear(GL_COLOR_BUFFER_BIT)

    if not game_started:
        glPushMatrix()
        glColor3f(0.0, 0.5, 0.7)
        glRectf(0.0, 0.0, 100.0, 10.0)  # ceiling
        glRectf(0.0, 100.0, 100.0, 90.0)  # floor
        render_text((35, 85), "Kathmandu University")
        render_text((41, 80), "Dhulikhel, Kavre")
        render_text((20, 65), "a mini project of Computer Graphics", 13, (255, 255, 0))
        render_text((45.5, 70), "Helicopter", 24)
        render_text((40, 45), "Welcome", 24, (255, 0, 0))
        render_text((53, 45), name, 24, (255, 0, 0))
        render_text((43, 30), "Click To Start", 24)


        glPopMatrix()
        glfw.swap_buffers(window)
    else:
        # Game Over Checking
        if ((i == 730 or i == -700)  # top and bottom checking
                or (((int(b1x) in {10, 7, 4, 1}) and int(b1y) < 53 + int(hm) and int(b1y) + 35 > 53 + int(
                    hm))  # propeller front checking
                    or ((int(b1x) in {9, 3, 6}) and int(b1y) < 45 + int(hm) and int(b1y) + 35 > 45 + int(
                            hm))  # lower body checking
                    or (int(b1x) == 0 and int(b1y) < 46 + int(hm) and int(b1y) + 35 > 46 + int(
                            hm)))):  # lower tail checking
            glColor3f(0.0, 0.0, 1.0)
            glRectf(0.0, 0.0, 100.0, 100.0)
            render_text((40, 70), "GAME OVER!!!", 24, (255, 0, 0))
            render_text((25, 58), "You", 24, (255, 255, 255))
            render_text((45, 58), "scored:", 24, (255, 255, 255))
            render_text((70, 58), scs, 24, (255, 255, 255))
            glfw.swap_buffers(window)
            print("\nGAME OVER\n\n")
            print(f"{name}, you scored {scs}")
            print("\n\nClose the console window to exit...\n")
            glfw.terminate()
            sys.exit(0)
        else:
            # On every increase by 50 in score in each level
            if sci % 50 == 0 and lflag == 1:
                lflag = 0  # make level_flag=0
                level += 1  # increase level by 1
                bspd += 0.01  # increase block_dx_speed by 0.01
            # Within every level make level_flag=1
            elif sci % 50 != 0 and lflag != 1:
                lflag = 1

            glPushMatrix()
            glColor3f(0.0, 0.5, 0.7)
            glRectf(0.0, 0.0, 100.0, 10.0)  # ceiling
            glRectf(0.0, 100.0, 100.0, 90.0)  # floor
            render_text((1, 3), "Distance:")
            slevel = str(level)  # level
            render_text((80, 3), "Level:")
            render_text((93, 3), slevel)
            scf += 0.025
            sci = int(scf)
            scs = str(sci)
            render_text((20, 3), scs)
            glTranslatef(0.0, hm, 0.0)
            draw_copter()
            glPopMatrix()

            glPushMatrix()
            # If the block crosses left out of the projection volume
            if b1x < -10:
                b1x = 50  # total width is 50
                b1y = random.randint(20, 45)
            else:
                b1x -= bspd
            # Draw the block independent of copter's movement
            glColor3f(1.0, 0.0, 0.0)
            glRectf(b1x, b1y, b1x + 5, b1y + 35)  # Red block
            glPopMatrix()

            glfw.swap_buffers(window)

# Function to handle keyboard input
def key_callback(window, key, scancode, action, mods):
    global hm, game_started
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            hm += 0.5
        elif key == glfw.KEY_DOWN:
            hm -= 0.5
        game_started = True


def main():
    global window
    if not glfw.init():
        return

    window = glfw.create_window(1200, 800, "Helicopter Game", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    init()

    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
