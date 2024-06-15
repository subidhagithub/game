import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math

window_width = 1000
window_height = 1000

if not glfw.init():
    raise Exception("GLFW can not be initialized!")


window = glfw.create_window(window_width, window_height, "3D Rotation", None, None)


if not window:
    glfw.terminate()
    raise Exception("GLFW window can not be created!")

# Set the window's context
glfw.make_context_current(window)

# Set the viewport
glViewport(0, 0, window_width, window_height)
glClearColor(1, 1, 1, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, window_width / window_height, 0.0, 400.0)
glMatrixMode(GL_MODELVIEW)

# Camera settings
camera_view_x = 5
camera_view_y = 0.5
camera_view_z = -2

look_view_x = 0
look_view_y = 0
look_view_z = 0

up_x = 0
up_y = 1
up_z = 0


def draw_cube(faces, color=(1, 0.6, 0)):
    glColor3fv(color)
    for face in faces:
        glBegin(GL_POLYGON)
        for vertex in face:
            glVertex3fv(vertex)
        glEnd()


def transform(T, faces):
    new_faces = []
    for face in faces:
        new_vertices = []
        for vertex in face:
            vertex = np.array([
                vertex[0],
                vertex[1],
                vertex[2],
                1
            ])

            new_vertex = np.matmul(T, vertex)
            new_vertices.append((new_vertex[0], new_vertex[1], new_vertex[2]))

        new_faces.append(new_vertices)

    return new_faces


def rotate(faces, about, by=0):
    by = math.radians(by)  # convert degree to radian
    T = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    if about == "x-axis":
        T[1][1] = T[2][2] = math.cos(by)
        T[1][2] = -math.sin(by)
        T[2][1] = math.sin(by)
    elif about == "y-axis":
        T[0][0] = T[2][2] = math.cos(by)
        T[0][2] = math.sin(by)
        T[2][0] = -math.sin(by)
    elif about == "z-axis":
        T[0][0] = T[1][1] = math.cos(by)
        T[0][1] = -math.sin(by)
        T[1][0] = math.sin(by)

    return transform(T, faces)


def draw_axes():
    glLoadIdentity()
    gluLookAt(camera_view_x, camera_view_y, camera_view_z, look_view_x, look_view_y, look_view_z, up_x, up_y, up_z)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(110, 0, 1, 0)

    glBegin(GL_LINES)

    # X-axis (Red)
    glColor3f(1, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(10, 0, 0)

    # Y-axis (Green)
    glColor3f(0, 1, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(0, 10, 0)

    # Z-axis (Blue)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -40)
    glVertex3f(0, 0, 40)

    glEnd()


def draw():
    vertices = [
        [-0.5, -0.5, -0.5],  # Bottom-left-back
        [0.5, -0.5, -0.5],  # Bottom-right-back
        [0.5, 0.5, -0.5],  # Top-right-back
        [-0.5, 0.5, -0.5],  # Top-left-back
        [-0.5, -0.5, 0.5],  # Bottom-left-front
        [0.5, -0.5, 0.5],  # Bottom-right-front
        [0.5, 0.5, 0.5],  # Top-right-front
        [-0.5, 0.5, 0.5]  # Top-left-front
    ]
    cube = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Back face
        [vertices[1], vertices[5], vertices[6], vertices[2]],  # Right face
        [vertices[5], vertices[4], vertices[7], vertices[6]],  # Front face
        [vertices[4], vertices[0], vertices[3], vertices[7]],  # Left face
        [vertices[3], vertices[2], vertices[6], vertices[7]],  # Top face
        [vertices[0], vertices[4], vertices[5], vertices[1]]  # Bottom face
    ]

    rotated_x = rotate(cube, by=45, about="x-axis")
    rotated_y = rotate(cube, by=180, about="y-axis")
    rotated_z = rotate(cube, by=60, about="z-axis")

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_axes()

        draw_cube(cube, color=(1, 0.6, 0))
        draw_cube(rotated_x, color=(1, 0, 0))
        draw_cube(rotated_y, color=(0, 1, 0))
        draw_cube(rotated_z, color=(0, 0, 1))

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    draw()
