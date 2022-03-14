# download OpenGL:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

# install OpenGL:
# pip install <file.whl> 
# (версия как у анаконды)


import sys
from random import random
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

pointdata = [[0, 0.5, 0], 
             [-0.5, -0.5, 0], 
             [0.5, -0.5, 0]]

pointcolor = [[1, 1, 0], 
              [0, 1, 1], 
              [1, 0, 1]]

vertex_source = """
varying vec4 vertex_color;
void main(){
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    vertex_color = gl_Color;
}
"""

fragment_source = """
varying vec4 vertex_color;
void main() {
    gl_FragColor = vertex_color;
}
"""

def create_shader(sh_type, sh_source):
    sh = gl.glCreateShader(sh_type)
    gl.glShaderSource(sh, sh_source)
    gl.glCompileShader(sh)
    return sh

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
    gl.glEnableClientState(gl.GL_COLOR_ARRAY)
    gl.glVertexPointer(3, gl.GL_FLOAT, 0, pointdata)
    gl.glColorPointer(3, gl.GL_FLOAT, 0, pointcolor)
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
    gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
    gl.glDisableClientState(gl.GL_COLOR_ARRAY)
    glut.glutSwapBuffers()
    
def specialkeys(key, x, y):
    global pointcolor
    if key == glut.GLUT_KEY_UP:
        gl.glRotatef(5, 1, 0, 0)
    if key == glut.GLUT_KEY_DOWN:
        gl.glRotatef(-5, 1, 0, 0)
    if key == glut.GLUT_KEY_LEFT:
        gl.glRotatef(5, 0, 1, 0)
    if key == glut.GLUT_KEY_RIGHT:
        gl.glRotatef(-5, 0, 1, 0)
    if key == glut.GLUT_KEY_END:
        pointcolor = [[random(), random(), random()], 
                      [random(), random(), random()], 
                      [random(), random(), random()]]

def initialize():
    vertex = create_shader(gl.GL_VERTEX_SHADER, vertex_source)
    fragment = create_shader(gl.GL_FRAGMENT_SHADER, fragment_source)
    
    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex)
    gl.glAttachShader(program, fragment)
    gl.glLinkProgram(program)
    gl.glUseProgram(program)


def run():
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize(640, 480)
    glut.glutInitWindowPosition(50, 50)
    window = glut.glutCreateWindow(b"example")
    glut.glutDisplayFunc(display)
    glut.glutIdleFunc(display)
    glut.glutSpecialFunc(specialkeys)
    gl.glClearColor(0.2, 0.2, 0.2, 1)
    
    try:
        initialize()
    except:
        print("Error")
        
    glut.glutMainLoop()
    

print("Press `End` to change color")
run()
