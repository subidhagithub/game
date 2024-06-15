import math
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_ellipse(a, b):
    x = 0
    y = b
    a_sqr = a * a
    b_sqr = b * b
    d1 = b_sqr - a_sqr * b + 0.25 * a_sqr
    dx = 2 * b_sqr * x
    dy = 2 * a_sqr * y

    points = []

    while dx < dy:
        points.extend([(x, y), (-x, y), (x, -y), (-x, -y)])
        if d1 < 0:
            x += 1
            dx = 2 * b_sqr * x
            d1 += dx + b_sqr
        else:
            x += 1
            y -= 1
            dx = 2 * b_sqr * x
            dy = 2 * a_sqr * y
            d1 += dx - dy + b_sqr

    d2 = b_sqr * (x + 0.5) * (x + 0.5) + a_sqr * (y - 1) * (y - 1) - a_sqr * b_sqr
    while y >= 0:
        points.extend([(x, y), (-x, y), (x, -y), (-x, -y)])
        if d2 > 0:
            y -= 1
            dy = 2 * a_sqr * y
            d2 += a_sqr - dy
        else:
            y -= 1
            x += 1
            dx = 2 * b_sqr * x
            dy = 2 * a_sqr * y
            d2 += dx - dy + a_sqr

    return points


def draw_pixel(x, y):
    glVertex2f(x, y)


def display_ellipse(a, b):
    points = draw_ellipse(a, b)

    glBegin(GL_POINTS)
    for point in points:
        draw_pixel(*point)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2.0)

    a = 150
    b = 100

    display_ellipse(a, b)
    glfw.swap_buffers(window)


def main():
    if not glfw.init():
        return

    global window
    window = glfw.create_window(400, 400, "Midpoint Ellipse Drawing Algorithm", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-200, 200, -200, 200)

    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
