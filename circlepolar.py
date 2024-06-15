import math
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_circle(radius, num_segments):
    glBegin(GL_LINE_LOOP)
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        glVertex2f(x, y)
    glEnd()


def display(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)

    radius = 100
    num_segments = 100

    draw_circle(radius, num_segments)
    glfw.swap_buffers(window)


def main():
    if not glfw.init():
        return

    window = glfw.create_window(400, 400, "Circle Drawing using Polar Coordinates", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-200, 200, -200, 200)

    while not glfw.window_should_close(window):
        display(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
