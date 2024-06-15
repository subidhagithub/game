import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

PI = 3.14159265

vertices = np.array([
    [-0.5, -0.5, -0.5, 1.0],
    [0.5, -0.5, -0.5, 1.0],
    [0.5, 0.5, -0.5, 1.0],
    [-0.5, 0.5, -0.5, 1.0],
    [-0.5, -0.5, 0.5, 1.0],
    [0.5, -0.5, 0.5, 1.0],
    [0.5, 0.5, 0.5, 1.0],
    [-0.5, 0.5, 0.5, 1.0]
], dtype=float)

colors = np.array([
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0]
], dtype=float)

def multiplyMatrix(mat, vec):
    return np.dot(mat, vec)

def transform(mat):
    global vertices
    temp = np.dot(vertices, mat.T)
    vertices[:] = temp

def translationMatrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=float)

def scalingMatrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotationMatrixX(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), -math.sin(angle), 0],
        [0, math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotationMatrixY(angle):
    return np.array([
        [math.cos(angle), 0, math.sin(angle), 0],
        [0, 1, 0, 0],
        [-math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1]
    ], dtype=float)

def rotationMatrixZ(angle):
    return np.array([
        [math.cos(angle), -math.sin(angle), 0, 0],
        [math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def shearingMatrix(shx, shy, shz):
    return np.array([
        [1, shx, shx, 0],
        [shy, 1, shy, 0],
        [shz, shz, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def drawCube():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -1.0)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()

    glBegin(GL_QUADS)
    for i, face in enumerate([(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)]):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex4fv(vertices[vertex])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawCube()
    glfw.swap_buffers(window)

def key_callback(window, key, scancode, action, mods):
    mat = np.identity(4, dtype=float)
    if action == glfw.PRESS:
        if key == glfw.KEY_T:
            mat = translationMatrix(1.0, 1.0, 1.0)
        elif key == glfw.KEY_S:
            mat = scalingMatrix(2.0, 2.0, 2.0)
        elif key == glfw.KEY_X:
            mat = rotationMatrixX(PI / 4)
        elif key == glfw.KEY_Y:
            mat = rotationMatrixY(PI / 4)
        elif key == glfw.KEY_Z:
            mat = rotationMatrixZ(PI / 4)
        elif key == glfw.KEY_J:
            mat = shearingMatrix(0.0, 0.0, 0.5)
        transform(mat)
        display()

if not glfw.init():
    raise Exception("GLFW initialization failed")

window = glfw.create_window(500, 500, "3D Transformations using Homogeneous Coordinates", None, None)

if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed")

glfw.set_window_pos(window, 100, 100)
glfw.make_context_current(window)
glfw.set_key_callback(window, key_callback)

glClearColor(0.0, 0.0, 0.0, 0.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(60, 1, 1, 10)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

while not glfw.window_should_close(window):
    display()
    glfw.poll_events()

glfw.terminate()