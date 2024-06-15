import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

window_width = 800
window_height = 600
window_title = "Midpoint Circle Drawing Algorithm"

radius = 200
center_x = window_width // 2
center_y = window_height // 2

def initGL():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0.0, window_width, 0.0, window_height)

def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def draw_circle(radius):
    x = 0
    y = radius
    p = 1 - radius
    plot_circle_points(x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(x, y)

def plot_circle_points(x, y):
    plot_point(x + center_x, y + center_y)
    plot_point(-x + center_x, y + center_y)
    plot_point(x + center_x, -y + center_y)
    plot_point(-x + center_x, -y + center_y)
    plot_point(y + center_x, x + center_y)
    plot_point(-y + center_x, x + center_y)
    plot_point(y + center_x, -x + center_y)
    plot_point(-y + center_x, -x + center_y)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(radius)
    glfw.swap_buffers(window)

def main():
    if not glfw.init():
        sys.exit(1)

    global window
    window = glfw.create_window(window_width, window_height, window_title, None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    initGL()

    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
