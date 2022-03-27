import glfw
import pyrr
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from ModelLoader import ModelLoader


class ModelViewer:
    def __init__(self, data, width=700, height=400):
        self.data = data
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

        glfw.set_window_pos(self.window, 650, 250)

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
        
    
    def define_color(self, temp):
        cold3 = [0.0, 0.0, 1.0]
        cold2 = [0.0, 0.2, 1.0]
        cold1 = [0.0, 0.4, 1.0]
        cold0 = [0.0, 0.6, 0.9]
        hot0 = [0.9, 0.9, 0.0]
        hot1 = [1.0, 0.8, 0.0]
        hot2 = [1.0, 0.6, 0.0]
        hot3 = [1.0, 0.4, 0.0]
        hot4 = [1.0, 0.2, 0.0]
        hot5 = [1.0, 0.0, 0.0]
        
        mn = np.amin(self.data[:, 1:6])
        mx = np.amax(self.data[:, 1:6])
        h = (mx - mn) / 10
        
        if temp >= mn and temp < mn + h: 
            return cold3
        elif temp >= mn + h and temp < mn + 2 * h:
            return cold2
        elif temp >= mn + 2 * h and temp < mn + 3 * h:
            return cold1
        elif temp >= mn + 3 * h and temp < mn + 4 * h:
            return cold0
        elif temp >= mn + 4 * h and temp < mn + 5 * h:
            return hot0
        elif temp >= mn + 5 * h and temp < mn + 6 * h:
            return hot1
        elif temp >= mn + 6 * h and temp < mn + 7 * h:
            return hot2
        elif temp >= mn + 7 * h and temp < mn + 8 * h:
            return hot3
        elif temp >= mn + 8 * h and temp < mn + 9 * h:
            return hot4
        else:
            return hot5
    
    
    def coloring(self, i):     
        temps = self.data[i]
        #part1
        arr1 = np.array(self.define_color(temps[1]) * int(self.vd[1] / 3.0), dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, self.offset, arr1.nbytes, arr1)
        #part2
        arr2 = np.array(self.define_color(temps[2]) * int((self.vd[2] - self.vd[1]) / 3.0), dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, self.offset + arr1.nbytes, arr2.nbytes, arr2)
        #part3
        arr3 = np.array(self.define_color(temps[4]) * int((self.vd[3] - self.vd[2]) / 3.0), dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, self.offset + arr1.nbytes + arr2.nbytes, arr3.nbytes, arr3)
        #part4
        arr4 = np.array(self.define_color(temps[3])* int((self.vd[4] - self.vd[3]) / 3.0), dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, self.offset + arr1.nbytes + arr2.nbytes + arr3.nbytes, arr4.nbytes, arr4)
        #part5
        arr5 = np.array(self.define_color(temps[5])* int((self.vd[5] - self.vd[4]) / 3.0), dtype=np.float32)
        glBufferSubData(GL_ARRAY_BUFFER, self.offset + arr1.nbytes + arr2.nbytes + arr3.nbytes + arr4.nbytes, 
                        arr5.nbytes, arr5)
        

    def main_loop(self):
        self.qwf = 0
        ML = ModelLoader("model2.obj")
        ML.load_all()
        self.vertices = ML.v
        indices = ML.f
        self.vd = ML.vd

        self.l = int(len(self.vertices))
        self.vertices.extend([0.1, 0.1, 0.1] * self.l)

        self.vertices = np.array(self.vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        shader = compileProgram(compileShader(self.vertex_source, GL_VERTEX_SHADER), 
                                compileShader(self.fragment_source, GL_FRAGMENT_SHADER))

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        self.offset = int(len(self.vertices) / 6 * 3 * 4)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(self.offset))

        glUseProgram(shader)
        glClearColor(0.8, 0.8, 0.8, 1)
        glEnable(GL_DEPTH_TEST)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.WINDOW_WIDTH / self.WINDOW_HEIGHT, 0.1, 1000)

        self.proj_loc = glGetUniformLocation(shader, "projection")
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        
        self.model_loc = glGetUniformLocation(shader, "model")
        self.translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 3, -33]))
        self.model = self.translation
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.model)
        
        self.rotation = pyrr.Matrix44.identity()

        i = 0
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.rotate()
            if len(self.data) > int(i) + 1:
                i += 0.2
                if int(i) % 1 == 0: self.coloring(int(i))
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
            glfw.swap_buffers(self.window)

        glfw.terminate()
    