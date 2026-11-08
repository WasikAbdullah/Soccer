import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Ball import Ball
from Player import Player

p1 = Player(-5, (0.85, 0.15, 0.15))
p2 = Player(5, (0.15, 0.3, 0.9))
ball = Ball()
score = [0, 0]
held = set()


def box(x, y, z, w, h, d):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(w, h, d)
    glutSolidCube(1)
    glPopMatrix()


def draw_player(p, walking, kicking):
    glPushMatrix()
    glTranslatef(p.x, p.y, 0)
    swing = 30 if walking and p.y == 0 else 0
    for side in (-1, 1):
        angle = side * swing
        if kicking and side == -1:
            angle = 75 if ball.x > p.x else -75
        glPushMatrix()
        glTranslatef(side * 0.22, 0.9, 0)
        glRotatef(angle, 0, 0, 1)
        glColor3f(0.12, 0.12, 0.18)
        box(0, -0.45, 0, 0.32, 0.9, 0.32)
        glPopMatrix()
    glColor3f(*p.color)
    box(0, 1.4, 0, 0.95, 1, 0.55)
    glPushMatrix()
    glTranslatef(0, 2.35, 0)
    glColor3f(0.96, 0.8, 0.66)
    glutSolidSphere(0.4, 24, 24)
    glColor3f(0.05, 0.05, 0.05)
    for ex in (-0.14, 0.14):
        glPushMatrix()
        glTranslatef(ex, 0.07, 0.34)
        glutSolidSphere(0.07, 12, 12)
        glPopMatrix()
    glPopMatrix()
    glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-12.5, 12.5, -7.5, 7.5, -60, 60)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(20, 1, 0, 0)
    glTranslatef(0, -4.2, 0)

    glColor3f(0.3, 0.68, 0.32)
    box(0, -0.5, 0, 28, 1, 10)

    glColor3f(0.96, 0.96, 0.96)
    for side in (-1, 1):
        for z in (-1.7, 1.7):
            box(side * 10, 1.75, z, 0.16, 3.5, 0.16)
        box(side * 10, 3.5, 0, 0.16, 0.16, 3.56)

    draw_player(p1, ('a' in held) != ('d' in held), 's' in held)
    draw_player(p2, (GLUT_KEY_LEFT in held) != (GLUT_KEY_RIGHT in held), GLUT_KEY_DOWN in held)

    glPushMatrix()
    glTranslatef(ball.x, ball.y, 0)
    glColor3f(1, 1, 1)
    glutSolidSphere(0.5, 32, 32)
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glColor3f(1, 1, 1)
    glRasterPos2f(20, 560)
    for c in str(score[0]):
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
    glRasterPos2f(960, 560)
    for c in str(score[1]):
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))
    glEnable(GL_LIGHTING)

    glutSwapBuffers()
    tick()


def move(p, left, right, jump):
    p.x = max(-9.3, min(9.3, p.x + (right - left) * 0.11))
    if jump and p.y == 0:
        p.vy = 0.19
    p.vy -= 0.008
    p.y += p.vy
    if p.y < 0:
        p.y = 0
        p.vy = 0


def kick(p):
    if abs(ball.x - p.x) < 1.7 and p.y - 0.6 < ball.y < p.y + 1.8:
        ball.vx = 0.26 if ball.x > p.x else -0.26
        ball.vy = 0.22


def collide(p):
    dx = ball.x - max(p.x - 0.55, min(ball.x, p.x + 0.55))
    dy = ball.y - max(p.y, min(ball.y, p.y + 2.75))
    d = max(math.hypot(dx, dy), 0.0001)
    if d < 0.5:
        nx = dx / d
        ny = dy / d
        ball.x += nx * (0.5 - d)
        ball.y += ny * (0.5 - d)
        v = ball.vx * nx + ball.vy * ny
        if v < 0:
            ball.vx -= 1.65 * v * nx
            ball.vy -= 1.65 * v * ny


def tick():
    move(p1, 'a' in held, 'd' in held, 'w' in held)
    move(p2, GLUT_KEY_LEFT in held, GLUT_KEY_RIGHT in held, GLUT_KEY_UP in held)

    ball.vy -= 0.0064
    ball.vx *= 0.99
    ball.x += ball.vx
    ball.y += ball.vy
    if ball.y < 0.5:
        ball.y = 0.5
        ball.vy = abs(ball.vy) * 0.65

    for side in (-1, 1):
        if side * ball.x > 9.5:
            if ball.y >= 3.2:
                ball.x = side * 9.5
                ball.vx = -side * abs(ball.vx)
            elif side * ball.x > 10:
                score[0 if side == 1 else 1] += 1
                ball.reset()

    collide(p1)
    collide(p2)
    glutPostRedisplay()


def key_down(key, x, y):
    key = key.decode().lower()
    if key == 's':
        kick(p1)
    held.add(key)


def key_up(key, x, y):
    held.discard(key.decode().lower())


def kick_down(key, x, y):
    if key == GLUT_KEY_DOWN:
        kick(p2)
    held.add(key)


def kick_up(key, x, y):
    held.discard(key)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1000, 600)
glutCreateWindow(b"Soccer")

glClearColor(0.53, 0.78, 0.92, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_NORMALIZE)
glLightfv(GL_LIGHT0, GL_POSITION, (-0.4, 0.9, 0.7, 0))

glutDisplayFunc(display)
glutKeyboardFunc(key_down)
glutKeyboardUpFunc(key_up)
glutSpecialFunc(kick_down)
glutSpecialUpFunc(kick_up)
glutMainLoop()