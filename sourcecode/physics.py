import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import math
import emitter

if not glfw.init():
    raise Exception("GLFW fail")

windowX=800
windowY=800
window = glfw.create_window(windowX,windowY, "3D Viewer with Transparent Red Ground", None, None)



glfw.make_context_current(window) 
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
glEnable(GL_LIGHTING)
yaw = 0 
pitch = 0  
camera_distance = 50 
mouse_held = False 
last_x = 400
last_y = 300


gravity = np.array([0.0, -9.81, 0.0], dtype=float)
Ground_restitution = 0.8
friction = 0.05
dt = 0.016
obj = []
release_interval = 0.1
#last_release_time = glfw.get_time()


class Create_Sphere:
    def __init__(self, initial_position, initial_velocity):
        self.position = initial_position#np.array(initial_position, dtype=float)
        self.velocity = initial_velocity#np.array(initial_velocity, dtype=float)
        self.random_XZforce = np.array([random.uniform(-1, 1), 0, random.uniform(-1, 1)], dtype=float)
        self.XZVelocity = random.uniform(0, 1)
        self.density = 0.3
        #self.e_Ball = 0.8
        self.radius=random.uniform(1,3)
        self.mass=4/3*math.pi*self.radius*self.density
        self.miu=0.8

    def update_physics(self, dt, gravity):
        if self.position[1] < self.radius:
            self.velocity[1] = -self.velocity[1] * ground_restitution
            self.position[1] = self.radius

        velocity_magnitude = np.linalg.norm(self.velocity)
        velocity_unit_vector = self.velocity / velocity_magnitude if velocity_magnitude != 0 else np.array([0, 0, 0])
        afriction=-self.miu*gravity*[velocity_unit_vector[0],0,velocity_unit_vector[2]]
        self.velocity += gravity * dt + afriction
        self.position += self.velocity * dt * 8 + self.random_XZforce * self.XZVelocity


def setup_lighting(camera_pos):
    glEnable(GL_LIGHT0)
    light_pos = [camera_pos[0] - 2, camera_pos[1] + 2, camera_pos[2] - 2, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

def set_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,windowX/ windowY, 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    camera_pos = np.array([
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch))
    ]) * camera_distance
    
    gluLookAt(*camera_pos, 0, 0, 0, 0, 1, 0)
    return camera_pos

def resolve_collision(sphere1, sphere2):
    normal = sphere1.position - sphere2.position
    normal = normal / np.linalg.norm(normal)

    relative_velocity = sphere1.velocity - sphere2.velocity
    velocity_along_normal = np.dot(relative_velocity, normal)
    
    if velocity_along_normal > 0:
        return
    
    restitution = min(ground_restitution, ground_restitution)
    
    j = -(1 + restitution) * velocity_along_normal
    j /= 1/sphere1.mass + 1/sphere2.mass  


    impulse = j * normal
    sphere1.velocity += impulse / sphere1.mass
    sphere2.velocity -= impulse / sphere2.mass

def check_collision(sphere1, sphere2):
    distance = np.linalg.norm(sphere1.position - sphere2.position)
    if distance < sphere1.radius+sphere2.radius:
        return True
    return False

def on_mouse_button(window, button, action, mods):
    global mouse_held
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_held = (action == glfw.PRESS)

def on_cursor_pos(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, mouse_held
    if mouse_held:
        xoffset = xpos - last_x
        yoffset = last_y - ypos  
        sensitivity = 0.2
        yaw += xoffset * sensitivity
        pitch += yoffset * sensitivity
        pitch = max(-89, min(89, pitch))
    last_x = xpos
    last_y = ypos

def hex_to_rgba(hex_color):

    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return (r / 255.0, g / 255.0, b / 255.0)


glfw.set_mouse_button_callback(window, on_mouse_button)
glfw.set_cursor_pos_callback(window, on_cursor_pos)

ground_vertices = [
    [-100, -1, -100], [100, -1, -100], [100, -1, 100], [-100, -1, 100]
]


glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1])
glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
glMaterialf(GL_FRONT, GL_SHININESS, 32.0)

def run(params):
    last_release_time = glfw.get_time()
    global obj_quantity,release_interval,sphere_restitution,ground_restitution
    obj_quantity = params['obj_quantity']
    release_interval = params['release_interval']
    sphere_color = params['sphere_color']  
    sphere_restitution = params['sphere_restitution']
    ground_restitution = params['ground_restitution']
    #print(release_interval,obj_quantity,sphere_color,sphere_restitution,ground_restitution)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        camera_pos = set_camera()
        setup_lighting(camera_pos)

        glColor4f(0.5, 0.5, 0.5, 1)
        glBegin(GL_QUADS)
        for vertex in ground_vertices:
            glVertex3f(*vertex)
        glEnd()

        current_time = glfw.get_time()
        if current_time - last_release_time >= release_interval:
            emitter.generate()
            last_release_time = current_time

        for sphere in obj:
            sphere.update_physics(dt, gravity)

        for sphere in obj:
            glPushMatrix()
            glTranslatef(sphere.position[0], sphere.position[1], sphere.position[2])
            glColor3f(hex_to_rgba(sphere_color)[0],hex_to_rgba(sphere_color)[1],hex_to_rgba(sphere_color)[2])
            sphere.radius
            gluSphere(gluNewQuadric(), sphere.radius, 16, 16)
            glPopMatrix()

        for i in range(len(obj)):
            for j in range(i + 1, len(obj)):
                if check_collision(obj[i], obj[j]):
                    resolve_collision(obj[i], obj[j])

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
