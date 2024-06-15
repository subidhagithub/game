import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Clipping window
x_min, y_min = -0.5, -0.5
x_max, y_max = 0.5, 0.5


def inside(p, edge):
    x, y = p
    if edge == "left":
        return x >= x_min
    elif edge == "right":
        return x <= x_max
    elif edge == "bottom":
        return y >= y_min
    elif edge == "top":
        return y <= y_max


def intersect(p1, p2, edge):
    x1, y1 = p1
    x2, y2 = p2

    if edge == "left":
        x = x_min
        y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
    elif edge == "right":
        x = x_max
        y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
    elif edge == "bottom":
        y = y_min
        x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
    elif edge == "top":
        y = y_max
        x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)

    return x, y


def clip_polygon(polygon, edge):
    clipped_polygon = []
    prev_vertex = polygon[-1]

    for curr_vertex in polygon:
        if inside(curr_vertex, edge):
            if not inside(prev_vertex, edge):
                clipped_polygon.append(intersect(prev_vertex, curr_vertex, edge))
            clipped_polygon.append(curr_vertex)
        elif inside(prev_vertex, edge):
            clipped_polygon.append(intersect(prev_vertex, curr_vertex, edge))

        prev_vertex = curr_vertex

    return clipped_polygon


def sutherland_hodgman_clip(polygon):
    edges = ["left", "right", "bottom", "top"]
    clipped_polygon = polygon[:]

    for edge in edges:
        clipped_polygon = clip_polygon(clipped_polygon, edge)

    return clipped_polygon


def draw_polygon(polygon):
    glBegin(GL_LINE_LOOP)
    for vertex in polygon:
        glVertex2f(*vertex)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Example polygon to be clipped
    polygon = [
        (-0.7, -0.7),
        (-0.7, 0.7),
        (0.7, 0.7),
        (0.7, -0.7)
    ]

    glColor3f(1.0, 0.0, 0.0)
    draw_polygon(polygon)

    glColor3f(0.0, 1.0, 0.0)
    clipped_polygon = sutherland_hodgman_clip(polygon)
    draw_polygon(clipped_polygon)

    glFlush()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Sutherland-Hodgman Polygon Clipping", None, None)
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
