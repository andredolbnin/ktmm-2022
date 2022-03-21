import glfw
import pyrr
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from ModelLoader import ModelLoader


class ModelViewer:
    def __init__(self, width=800, height=400):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = width, height
        self.is_W, self.is_A, self.is_S, self.is_D = False, False, False, False

        self.vertex_source = """
        # version 330
        
        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec3 a_color;
        
        uniform mat4 projection;
        uniform mat4 model;
        
        out vec3 v_color;
        
        void main()
        {
            gl_Position = projection * model * vec4(a_position, 1.0);
            v_color = a_color;
        }
        """

        self.fragment_source = """
        # version 330
        
        in vec3 v_color;
        out vec4 out_color;
        
        void main()
        {
            out_color = vec4(v_color, 1.0);
        }
        """

        if not glfw.init():
            raise Exception("Error")

        self.window = glfw.create_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Model", None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("Error")

        glfw.set_window_pos(self.window, 500, 200)

        glfw.set_window_size_callback(self.window, self.window_size_callback)
        glfw.set_key_callback(self.window, self.key_callback)

        glfw.make_context_current(self.window)
        
        
    def window_size_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 1000)
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        

    def key_callback(self, window, key, scancode, action, mode):
        if key == glfw.KEY_W and action == glfw.PRESS:
            self.is_W = True
        elif key == glfw.KEY_W and action == glfw.RELEASE:
            self.is_W = False

        if key == glfw.KEY_A and action == glfw.PRESS:
            self.is_A = True
        elif key == glfw.KEY_A and action == glfw.RELEASE:
            self.is_A = False
            
        if key == glfw.KEY_S and action == glfw.PRESS:
            self.is_S = True
        elif key == glfw.KEY_S and action == glfw.RELEASE:
            self.is_S = False
            
        if key == glfw.KEY_D and action == glfw.PRESS:
            self.is_D = True
        elif key == glfw.KEY_D and action == glfw.RELEASE:
            self.is_D = False
            
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

        
    def rotate(self):
        angle = 0.005
        if self.is_W:
            self.rotation *= pyrr.Matrix44.from_x_rotation(angle)
            self.model = pyrr.matrix44.multiply(self.rotation, self.translation)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
            
        if self.is_A:
            self.rotation *= pyrr.Matrix44.from_y_rotation(angle)
            self.model = pyrr.matrix44.multiply(self.rotation, self.translation)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
            
        if self.is_S:
            self.rotation *= pyrr.Matrix44.from_x_rotation(-angle)
            self.model = pyrr.matrix44.multiply(self.rotation, self.translation)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
            
        if self.is_D:
            self.rotation *= pyrr.Matrix44.from_y_rotation(-angle)
            self.model = pyrr.matrix44.multiply(self.rotation, self.translation)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)


    def main_loop(self):
        ML = ModelLoader("model2.obj")
        ML.load_all()
        vertices = ML.v;
        indices = ML.f;

        l = int(len(vertices))
        vertices.extend([0.1, 0.1, 0.1] * l)

        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        shader = compileProgram(compileShader(self.vertex_source, GL_VERTEX_SHADER), 
                                compileShader(self.fragment_source, GL_FRAGMENT_SHADER))

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        offset = int(len(vertices) / 6 * 3 * 4)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(offset))

        glUseProgram(shader)
        glClearColor(0.8, 0.8, 0.8, 1)
        glEnable(GL_DEPTH_TEST)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.WINDOW_WIDTH / self.WINDOW_HEIGHT, 0.1, 1000)

        self.proj_loc = glGetUniformLocation(shader, "projection")
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        
        self.model_loc = glGetUniformLocation(shader, "model")
        self.translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -35]))
        self.model = self.translation
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
        
        self.rotation = pyrr.Matrix44.identity()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.rotate()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
            glfw.swap_buffers(self.window)

        glfw.terminate()
    