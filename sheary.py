from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import numpy as np


def triangle():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    glPointSize(3.0)
    p1 = [0, 0, 1]
    p2 = [300, 100, 1]
    p3 = [200, 400, 1]
    glBegin(GL_TRIANGLES)
    glVertex2d(p1[0], p1[1])
    glVertex2d(p2[0], p2[1])
    glVertex2d(p3[0], p3[1])
    glEnd()

    shear_factor_y = 0.5
    p1_prime = shear_y(shear_factor_y, p1)
    p2_prime = shear_y(shear_factor_y, p2)
    p3_prime = shear_y(shear_factor_y, p3)

    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2d(p1_prime[0], p1_prime[1])
    glVertex2d(p2_prime[0], p2_prime[1])
    glVertex2d(p3_prime[0], p3_prime[1])
    glEnd()
    glfw.swap_buffers(window)


def shear_y(sh_y, P):
    T = [[1, 0, 0], [sh_y, 1, 0], [0, 0, 1]]
    return np.matmul(T, P)


if not glfw.init():
    raise Exception("GLFW initialization failed")

window = glfw.create_window(800, 600, "LAB 4", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed")

glfw.make_context_current(window)

glClearColor(0.0, 0.0, 0.0, 1.0)

while not glfw.window_should_close(window):
    glfw.poll_events()
    triangle()

glfw.terminate()
