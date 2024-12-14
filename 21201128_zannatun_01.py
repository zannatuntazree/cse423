import random
from OpenGL.GL import*
from OpenGL.GLUT import*
from OpenGL.GLU import*


########  task1  ##########
window_width, window_height = 600, 600
rain_drops = []
rain_direction = 0 
background_color = [0, 0, 0]  # black
def initialize_rain():
    global rain_drops
    rain_drops = [[random.randint(0, window_width), random.randint(0, window_height)] for _ in range(100)]


def draw_house():
    # Roof
    glColor3f(1, 0, 0)  # red 
    glBegin(GL_TRIANGLES)
    glVertex2f(300, 450)  # top
    glVertex2f(180, 350)  # bottom-left
    glVertex2f(420, 350)  # bottom-right
    glEnd()

    # house base
    glColor3f(0.9, 0.7, 0.5)  # light brown
    glBegin(GL_TRIANGLES)
    glVertex2f(200, 350)  # top-left
    glVertex2f(400, 350)  # top-right
    glVertex2f(200, 200)  # bottom-left
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(200, 200)  # bottom-left
    glVertex2f(400, 200)  # bottom-right
    glVertex2f(400, 350)  # top-right
    glEnd()

    # door
    glColor3f(0.5, 0.3, 0.2)  # brown
    glBegin(GL_TRIANGLES)
    glVertex2f(280, 200)  # bottom-left
    glVertex2f(320, 200)  # bottom-right
    glVertex2f(280, 270)  # top-left
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(320, 200)  # bottom-right
    glVertex2f(320, 270)  # top-right
    glVertex2f(280, 270)  # top-left
    glEnd()

    # window
    glColor3f(1.0, 0.0, 0.0)  # red 
    glBegin(GL_TRIANGLES)
    glVertex2f(360, 320)  # top-left
    glVertex2f(390, 320)  # top-right
    glVertex2f(360, 290)  # bottom-left
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(360, 290)  # bottom-left
    glVertex2f(390, 290)  # bottom-right
    glVertex2f(390, 320)  # top-right
    glEnd()
    
    # door knob
    glColor3f(0.1, 0.1, 0.1)  # Dark grey for the door knob
    glPointSize(4.5)
    glBegin(GL_POINTS)
    glVertex2f(312, 230)  # Position of the door knob
    glEnd()

def draw_rain():
    glColor3f(0, 0.5, 1.0)  # baby blue for the rain
    glBegin(GL_LINES)
    for drop in rain_drops:
        glVertex2f(drop[0], drop[1])
        glVertex2f(drop[0] + rain_direction * 5, drop[1] - 10)
    glEnd()
def update_rain():
    global rain_drops
    for drop in rain_drops:
        drop[0] += rain_direction
        drop[1] -= 5
        if drop[1] < 0 or drop[0] < 0 or drop[0] > window_width:
            drop[0] = random.randint(0, window_width)
            drop[1] = window_height

def display():
    global background_color
    glClearColor(*background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_house()
    draw_rain()
    glutSwapBuffers()
def keyboard(key, x, y):
    global rain_direction, background_color
    if key == b'd':  # day
        background_color = [1.0, 1.0, 1.0]  # white
    elif key == b'n':  # night
        background_color = [0.0, 0.0, 0.0]  # black
    elif key == b'l':  # left side flow of the rain
        rain_direction = -1
    elif key == b'r':  # right side flow of the rain
        rain_direction = 1
    elif key == b's':  # straight rain
        rain_direction = 0

def timer(value):
    update_rain()
    glutPostRedisplay() 
    glutTimerFunc(25, timer, 0)

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Building a House in Rainfall")
    initialize_rain()
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(25, timer, 0)
    glutMainLoop()
if __name__ == "__main__":
    main()














########### task 2 ##########
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






