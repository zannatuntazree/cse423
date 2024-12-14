import random
from OpenGL.GL import*
from OpenGL.GLUT import*
from OpenGL.GLU import*


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




