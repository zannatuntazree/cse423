import random
from OpenGL.GL import*
from OpenGL.GLUT import*
from OpenGL.GLU import*

w_width, w_height = 600, 600
points = []
speed = 0.3
pause = False
blinking = False

class Point:
    def __init__(self, x, y, x_dir, y_dir, clr):
        self.x = x
        self.y = y
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.clr = clr
        self.original_clr = clr  # blinking
        self.is_visible = True  # blinking state
def convert_coordinates(x, y):
    global w_width, w_height
    opengl_x = x - (w_width / 2)
    opengl_y = (w_height / 2) - y
    return opengl_x, opengl_y
def draw_points():
    global points, blinking
    glPointSize(10)
    glBegin(GL_POINTS)
    for point in points:
        if not blinking or point.is_visible:
            glColor3f(*point.clr)
            glVertex2f(point.x, point.y)
    glEnd()
def mouse_listener(button, state, x, y):
    global points, pause, blinking
    directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if not pause:
            gl_x, gl_y = convert_coordinates(x, y)
            x_dir, y_dir = random.choice(directions)
            color = [random.random(), random.random(), random.random()]
            new_point = Point(gl_x, gl_y, x_dir, y_dir, color)
            points.append(new_point)
            print(f"New Point: {gl_x, gl_y, x_dir, y_dir}")
        else:
            print("Paused - No new points.")
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not pause:
            blinking = not blinking
            print(f"blinking {'enabled' if blinking else 'disabled'}.")
    glutPostRedisplay()
def special_key_listener(key, x, y):
    global speed, pause
    if key == GLUT_KEY_UP and not pause:
        speed *= 5
        print("increased the speed.")

    if key == GLUT_KEY_DOWN and not pause:
        speed = max(0.1, speed / 2.0) 
        print("decreased the speed.")
    glutPostRedisplay()
def keyboard_listener(key, x, y):
    global pause
    if key == b' ':
        pause = not pause
        print(f"{'paused' if pause else 'not paused'}.")
    glutPostRedisplay()
def animate():
    global points, speed, pause, blinking
    if not pause:
        for point in points:
            point.x += point.x_dir * speed
            point.y += point.y_dir * speed
            if point.x >= w_width / 2 or point.x <= -w_width / 2:
                point.x_dir *= -1
            if point.y >= w_height / 2 or point.y <= -w_height / 2:
                point.y_dir *= -1
        if blinking:
            for point in points:
                point.is_visible = not point.is_visible 
    glutPostRedisplay()


def show_screen():
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_boundary()
    draw_points()
    glutSwapBuffers()
def draw_boundary():
    glColor3f(1.0, 1.0, 1.0) 
    glBegin(GL_LINE_LOOP)
    glVertex2f(-w_width / 2, -w_height / 2)
    glVertex2f(-w_width / 2, w_height / 2)
    glVertex2f(w_width / 2, w_height / 2)
    glVertex2f(w_width / 2, -w_height / 2)
    glEnd()
def setup_opengl():
    glViewport(0, 0, w_width, w_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-w_width / 2, w_width / 2, -w_height / 2, w_height / 2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(w_width, w_height)
    glutCreateWindow(b"Building the Amazing Box")
    setup_opengl()
    glutDisplayFunc(show_screen)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_listener)
    glutSpecialFunc(special_key_listener)
    glutKeyboardFunc(keyboard_listener)
    glutMainLoop()

if __name__ == "__main__":
    main()






