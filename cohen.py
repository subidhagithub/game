import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Region codes
INSIDE = 0  # 0000
LEFT = 1 # 0001
RIGHT = 2 # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000

# Define the clipping window
x_min, y_min = -0.5, -0.5
x_max, y_max = 0.5, 0.5

def compute_code(x, y):
    code = INSIDE
    if x < x_min:
        code |= LEFT
    elif x > x_max:
        code |= RIGHT
    if y < y_min:
        code |= BOTTOM
    elif y > y_max:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif code1 & code2 != 0:
            break
        else:
            x, y = 0.0, 0.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            if code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)

    if accept:
        return x1, y1, x2, y2
    else:
        return None

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Example lines to be clipped
    lines = [
        (-0.7, -0.7, 0.7, 0.7),
        (-0.7, 0.7, 0.7, -0.7),
        (-0.3, -0.3, 0.3, 0.3)
    ]

    glColor3f(1.0, 0.0, 0.0)
    for line in lines:
        clipped_line = cohen_sutherland_clip(*line)
        if clipped_line:
            draw_line(*clipped_line)

    glFlush()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Cohen-Sutherland Line Clipping", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(-1, 1, -1, 1)

    while not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
