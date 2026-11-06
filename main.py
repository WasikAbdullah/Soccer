from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


mouseX = 0
mouseY = 0

def mouse_input(x,y):

    global mouseX,mouseY

    mouseX = x
    mouseY = y
    pass


def render():
    glColor4f(0,1,1,1)

    glPushMatrix()
    glRotate(mouseX,1,0,0)
    glTranslate(256,256,64)


    glutSolidTeapot( 128 )
    glPopMatrix()

    pass

def display():

    #glClearColor(1,1,1,1)
    glClear(GL_COLOR_BUFFER_BIT)
    glViewport(0,0,1600,1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,1600,0,1000,-128,128)
    #glMatrixMode(GL_PROJECTION)








    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0,GL_DIFFUSE, [1,1,1,1])
    glLightfv(GL_LIGHT0, GL_POSITION, [128,128,128,0])
    #glLighti(GL_LIGHT0,GL_LIGH)

    render()

    glFlush()

    pass




glutInit()
glutInitWindowSize(1600,1000)
glutCreateWindow(b"Soccer")
glutDisplayFunc(display)
glutMotionFunc(mouse_input)
glutMainLoop()