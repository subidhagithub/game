from OpenGL.GL import *
import glfw
import numpy as np

def triangle():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)  # Set color to blue
    glPointSize(3.0)
    p1 = [0, 0, 1]
    p2 = [300, 100, 1]
    p3 = [200, 400, 1]
    glBegin(GL_TRIANGLES)
    glVertex2d(p1[0], p1[1])
    glVertex2d(p2[0], p2[1])
    glVertex2d(p3[0], p3[1])
    glEnd()


    reflection_matrix = np.array([[1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]])


    p1_prime = apply_transformation(reflection_matrix, p1)
    p2_prime = apply_transformation(reflection_matrix, p2)
    p3_prime = apply_transformation(reflection_matrix, p3)

    glColor3f(1.0, 0.0, 1.0)  # Set color to purple
    glBegin(GL_TRIANGLES)
    glVertex2d(p1_prime[0], p1_prime[1])
    glVertex2d(p2_prime[0], p2_prime[1])
    glVertex2d(p3_prime[0], p3_prime[1])
    glEnd()

    glfw.swap_buffers(window)

def apply_transformation(transformation_matrix, point):
    return np.matmul(transformation_matrix, point)

if not glfw.init():
    raise Exception("GLFW initialization failed")

window = glfw.create_window(800, 600, "2D Reflection on X-axis", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed")

glfw.make_context_current(window)

glClearColor(0.0, 0.0, 0.0, 1.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 800, 0, 600, -1, 1)
glMatrixMode(GL_MODELVIEW)

while not glfw.window_should_close(window):
    glfw.poll_events()
    triangle()

glfw.terminate()
