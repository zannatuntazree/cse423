from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLU import *
from random import randint as random
import random
import time
import math


window_width = 500
window_height = 800 
bullet_list = [] 
bub_list = [] 
score = 0 
missed_fires = 0 
pause = False 
game_over = 0 
last_frame_time = 0 
bullet_speed = 700 
rocket_x = 0


def create_bubbles(existing_bubs):
    is_dynamic = random.random() < 0.2 
    r = random.randint(10, 20) 
    color = [0, 1, 0] 
    if is_dynamic: 
        color = [1, 0, 0]
    while True:
        x = random.randint(-220, 220)  
        y = 300 
        if not check_bubbles_collission(x, y, r, existing_bubs):
            bub = {
                'x': x, 
                'y': y, 
                'r': r, 
                'color': color,
                'is_dynamic': is_dynamic,
                'dynamic_phase': 0, 
                'dynamic_direction': 1 }
            return bub


def updateDYbubbles(bub, new_time):
    if bub.get('is_dynamic', False): 
        amp = 5 
        f = 10 
        bub['dynamic_phase'] += new_time * f * bub['dynamic_direction'] 
        rad_change = math.sin(bub['dynamic_phase']) * amp 
        new_rad = bub['r'] + rad_change 
        new_rad = max(15, min(new_rad, 35)) 
        bub['r'] = new_rad 

        if abs(rad_change) < 0.1:  
            bub['dynamic_direction'] *= -1


def check_bubbles_collission(x, y, r, other_bubs):
    for other in other_bubs:
        dist = ((x - other['x']) ** 2 + (y - other['y']) ** 2) ** 0.5
        if dist < (r + other['r']):
            return True
    return False


def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


#MIDPOINT LINE DRAWING ALGORITHM
def convert_to_zone0(x, y, Z):
    Zmap = {
        0: (x, y),
        1: (y, x),
        2: (y, -x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (-y, x),
        7: (x, -y)
    }
    return Zmap[Z]


def convert_from_zone0(x, y, Z):
    Zmap = {
        0: (x, y),
        1: (y, x),
        2: (-y, x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (y, -x),
        7: (x, -y)
    }
    return Zmap[Z]


# Midpoint line drawing algorithm.
def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    Z = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            Z = 0
        elif dx < 0 and dy >= 0:
            Z = 3
        elif dx < 0 and dy < 0:
            Z = 4
        elif dx >= 0 and dy < 0:
            Z = 7
    else:
        if dx >= 0 and dy >= 0:
            Z = 1
        elif dx < 0 and dy >= 0:
            Z = 2
        elif dx < 0 and dy < 0:
            Z = 5
        elif dx >= 0 and dy < 0:
            Z = 6


    x1, y1 = convert_to_zone0(x1, y1, Z)
    x2, y2 = convert_to_zone0(x2, y2, Z)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, Z)
    plot_point(x0, y0)
    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, Z)
        plot_point(x0, y0)


# Midpoint circle drawing algorithm.
def midpoint_circle(rad, cirX=0, cirY=0):
    glBegin(GL_POINTS)
    x = 0
    y = rad
    d = 1 - rad
    while y > x:
        glVertex2f(x + cirX, y + cirY)
        glVertex2f(x + cirX, -y + cirY)
        glVertex2f(-x + cirX, y + cirY)
        glVertex2f(-x + cirX, -y + cirY)
        glVertex2f(y + cirX, x + cirY)
        glVertex2f(y + cirX, -x + cirY)
        glVertex2f(-y + cirX, x + cirY)
        glVertex2f(-y + cirX, -x + cirY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()


def bub_x_position(bub):
    return bub['x']


def draw_bullet():
    global bullet_list
    glColor3f(1, 1, 0)
    for bullet in bullet_list:
        midpoint_circle(8, bullet[0], bullet[1]) 


def draw_bubbles():
    global bub_list
    for bub in bub_list:
        glColor3f(bub['color'][0], bub['color'][1], bub['color'][2])
        midpoint_circle(bub['r'], bub['x'], bub['y'])


def drawThings():
    global rocket_x, score, missed_fires, pause

    # Shooter
    glPointSize(2)
    glColor3f(1, 0, 0)
    
    # rocket body
    midpoint_line(rocket_x - 10, -345, rocket_x - 10, -315)
    midpoint_line(rocket_x + 10, -345, rocket_x + 10, -315)
    midpoint_line(rocket_x - 10, -315, rocket_x + 10, -315)
    
    # rocket tip
    midpoint_line(rocket_x - 10, -315, rocket_x, -295)
    midpoint_line(rocket_x + 10, -315, rocket_x, -295)
    
    # rocket fins
    midpoint_line(rocket_x - 10, -345, rocket_x - 15, -355)
    midpoint_line(rocket_x + 10, -345, rocket_x + 15, -355)
    midpoint_line(rocket_x - 15, -355, rocket_x - 10, -355)
    midpoint_line(rocket_x + 15, -355, rocket_x + 10, -355)
    
    # rocket fire
    glColor3f(1, 0.5, 0)
    midpoint_line(rocket_x - 5, -355, rocket_x, -375)
    midpoint_line(rocket_x + 5, -355, rocket_x, -375)
    midpoint_line(rocket_x - 5, -355, rocket_x + 5, -355)

    # black box around rocket for collision detection
    glColor3f(0, 0, 0)  
    midpoint_line(rocket_x - 20, -375, rocket_x + 20, -375)  # Bottom line
    midpoint_line(rocket_x - 20, -295, rocket_x + 20, -295)  # Top line
    midpoint_line(rocket_x - 20, -375, rocket_x - 20, -295)  # Left line
    midpoint_line(rocket_x + 20, -375, rocket_x + 20, -295)  # Right line

    # quit button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    # restart button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)

    # pause button
    glPointSize(4)
    glColor3f(1, 0.5, 0)

    if pause:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

    # score and missed fires
    glColor3f(1, 1, 1)
    # Score
    glRasterPos2f(-240, -390)
    for ch in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    # Missed fires
    glRasterPos2f(140, -390)
    for ch in f"Missed fires: {missed_fires}/3":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    # Missed bubbles
    glRasterPos2f(-80, -390)
    for ch in f"Missed bubbles: {game_over}/3":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def convert_coordinate(x, y):
    a = x - (window_width  / 2)
    b = (window_height  / 2) - y
    return a, b


def restart_game():
    global pause, bub_list, score, game_over, missed_fires, bullet_list, rocket_x
    pause = False
    bub_list = []
    num_starting_bubs = random.randint(3, 5)
    for _ in range(num_starting_bubs):
        new_bub = create_bubbles(bub_list)
        bub_list.append(new_bub)
    bub_list.sort(key=bub_x_position)
    score = 0
    game_over = 0
    missed_fires = 0
    bullet_list = []
    rocket_x = 0


def mouseListener(button, state, x, y):
    global pause, game_over, score, bub_list, bullet_list, missed_fires
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            restart_game()
        elif 170 < c_x < 216 and 330 < c_y < 370:
            print(f'Score: {score}')
            glutLeaveMainLoop()
        elif -25 < c_x < 25 and 325 < c_y < 375:
            pause = not pause
    glutPostRedisplay()


def keyboardListener(key, _, __):
    global bullet_list, pause, game_over, rocket_x
    if key == b' ':
        if not pause and game_over < 3:
            bullet_list.append([rocket_x, -365])
    elif key == b'a':
        if rocket_x > -230 and not pause:
            rocket_x -= 20
    elif key == b'd':
        if rocket_x < 230 and not pause:
            rocket_x += 20
    glutPostRedisplay()


def animate():
    global pause, bub_list, game_over, score, bullet_list, missed_fires, last_frame_time, rocket_x
    current_time = time.time()
    new_time = current_time - last_frame_time
    last_frame_time = current_time

    if not pause and game_over < 3 and missed_fires < 3:
        new_bullet = []
        for b in bullet_list:
            if b[1] < 400:
                new_bullet.append([b[0], b[1] + bullet_speed * new_time])
            else: 
                missed_fires += 1
        bullet_list = new_bullet

        for i in range(len(bub_list) - 1, -1, -1):
            bub = bub_list[i]
            box_left = rocket_x - 20
            box_right = rocket_x + 20
            box_top = -295
            box_bottom = -375
            closest_x = max(box_left, min(bub['x'], box_right))
            closest_y = max(box_bottom, min(bub['y'], box_top))
            dx = bub['x'] - closest_x
            dy = bub['y'] - closest_y
            dist = math.sqrt(dx**2 + dy**2)
            if dist < bub['r']:
                game_over = 3
                break

        for i in range(len(bub_list) - 1, -1, -1): 
            bub = bub_list[i]
            if bub.get('is_dynamic', False):
                updateDYbubbles(bub, new_time)
            if bub['y'] > -400:
                new_y = bub['y'] - (10 + score * 5) * new_time
                bub['y'] = new_y
                if check_bubbles_collission(bub['x'], bub['y'], bub['r'], 
                                        [b for b in bub_list if b != bub]):
                    bub['y'] = bub['y'] + (10 + score * 5) * new_time 
            else:
                game_over += 1
                bub_list.pop(i)
                new_bub = create_bubbles(bub_list)
                bub_list.append(new_bub)
        bub_list.sort(key=bub_x_position)
        
        for i in range(len(bub_list) - 1, -1, -1):
            bub = bub_list[i]
            dx = bub['x'] - rocket_x
            dy = bub['y'] - (-345)
            dist = math.sqrt(dx**2 + dy**2)
            if dist < (bub['r'] + 20):
                game_over = 3
                break  
            for j in range(len(bullet_list) - 1, -1, -1):
                bull = bullet_list[j]
                bullet_dx = bub['x'] - bull[0]
                bullet_dy = bub['y'] - bull[1]
                bullet_dist = math.sqrt(bullet_dx**2 + bullet_dy**2)
                if bullet_dist < (bub['r'] + 8):  
                    if bub.get('is_dynamic', False):
                        score += 2
                        print(f" Dynamic Score: {score}")
                    else:
                        score += 1
                        print(f"Score: {score}")
                    bub_list.pop(i)
                    bullet_list.pop(j)
                    new_bub = create_bubbles(bub_list)
                    bub_list.append(new_bub)
                    break  
    if (game_over >= 3 or missed_fires >= 3) and not pause:
        print(f"Game Over. Score: {score}")
        pause = True
        bub_list = []  
    glutPostRedisplay()


def display():   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawThings()
    draw_bullet()
    draw_bubbles()
    glutSwapBuffers()


def init():
    global last_frame_time
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)
    last_frame_time = time.time()


glutInit()
glutInitWindowSize(window_width , window_height )
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Circle Shooter Game")
init()
num_starting_bubs = random.randint(3, 5)
for _ in range(num_starting_bubs):
    new_bub = create_bubbles(bub_list)
    bub_list.append(new_bub)
bub_list.sort(key=bub_x_position)
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()



