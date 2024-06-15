import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

width, height = 800, 600

def triangle():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    glPointSize(3.0)
    p1 = np.array([0, 0, 1])
    p2 = np.array([300, 100, 1])
    p3 = np.array([200, 400, 1])
    glBegin(GL_TRIANGLES)
    glVertex2d(p1[0], p1[1])
    glVertex2d(p2[0], p2[1])
    glVertex2d(p3[0], p3[1])
    glEnd()


    transformation_matrix = translate(100, 100, rotate(np.pi/4, scale(0.5, 0.5, np.identity(3))))
    p1_prime = apply_transformation(transformation_matrix, p1)
    p2_prime = apply_transformation(transformation_matrix, p2)
    p3_prime = apply_transformation(transformation_matrix, p3)

    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2d(p1_prime[0], p1_prime[1])
    glVertex2d(p2_prime[0], p2_prime[1])
    glVertex2d(p3_prime[0], p3_prime[1])
    glEnd()

    glfw.swap_buffers(window)

def translate(t_x, t_y, P):
    T = np.array([[1, 0, t_x],
                  [0, 1, t_y],
                  [0, 0, 1]])
    return np.matmul(T, P)

def scale(s_x, s_y, P):
    T = np.array([[s_x, 0, 0],
                  [0, s_y, 0],
                  [0, 0, 1]])
    return np.matmul(T, P)

def rotate(theta, P):
    T = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])
    return np.matmul(T, P)

def apply_transformation(transformation_matrix, point):
    return np.matmul(transformation_matrix, point)

if not glfw.init():
    glfw.terminate()
    exit()

window = glfw.create_window(width, height, "Composite Transformation", None, None)
if not window:
    glfw.terminate()
    exit()

glfw.make_context_current(window)
glOrtho(0, width, 0, height, -1, 1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    triangle()

glfw.terminate()
