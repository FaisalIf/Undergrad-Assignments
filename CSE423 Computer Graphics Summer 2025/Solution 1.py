# Task 1: Building a House in Rainfall

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class HouseRenderer:
   def draw_house_structure(self):
      glColor3f(1.0, 0.98, 0.8)
      glBegin(GL_TRIANGLES)
      glVertex2f(-100, -100)
      glVertex2f(100, -100)
      glVertex2f(-100, 50)
      glVertex2f(100, -100)
      glVertex2f(100, 50)
      glVertex2f(-100, 50)
      glEnd()

   def draw_rooftop(self):
      glColor3f(0.5, 0.0, 0.5)
      glBegin(GL_TRIANGLES)
      glVertex2f(-120, 50)
      glVertex2f(120, 50)
      glVertex2f(0, 150)
      glEnd()

   def draw_doorway(self):
      glColor3f(0.0, 1.0, 1.0)
      glBegin(GL_TRIANGLES)
      glVertex2f(-25, -100)
      glVertex2f(25, -100)
      glVertex2f(-25, 0)
      glVertex2f(25, -100)
      glVertex2f(25, 0)
      glVertex2f(-25, 0)
      glEnd()

   def draw_doorknob(self):
      glColor3f(1.0, 1.0, 1.0)
      glPointSize(5)
      glBegin(GL_POINTS)
      glVertex2f(15, -50)
      glEnd()

   def draw_all_windows(self):
      self.draw_single_window(-80, -40, -40, 0)
      self.draw_single_window(40, -40, 80, 0)

   def draw_single_window(self, x1, y1, x2, y2):
      glColor3f(0.0, 1.0, 1.0)
      glBegin(GL_TRIANGLES)
      glVertex2f(x1, y1)
      glVertex2f(x2, y1)
      glVertex2f(x1, y2)
      glVertex2f(x2, y1)
      glVertex2f(x2, y2)
      glVertex2f(x1, y2)
      glEnd()

   def draw_window_barriers(self):
      glColor3f(0.2, 0.2, 0.2)
      glLineWidth(2)
      glBegin(GL_LINES)
      glVertex2f(-60, -40)
      glVertex2f(-60, 0)
      glVertex2f(-80, -20)
      glVertex2f(-40, -20)
      glVertex2f(60, -40)
      glVertex2f(60, 0)
      glVertex2f(40, -20)
      glVertex2f(80, -20)
      glEnd()

   def draw(self):
      self.draw_house_structure()
      self.draw_rooftop()
      self.draw_doorway()
      self.draw_doorknob()
      self.draw_all_windows()
      self.draw_window_barriers()

class SceneryRenderer:
   def __init__(self, width, height):
      self.W_Width = width
      self.W_Height = height

   def draw_terrain(self):
      glColor3f(0.5, 0.35, 0.05)
      glBegin(GL_TRIANGLES)
      glVertex2f(-self.W_Width / 2, -self.W_Height / 2)
      glVertex2f(self.W_Width / 2, -self.W_Height / 2)
      glVertex2f(-self.W_Width / 2, -self.W_Height / 2 + 0.7 * self.W_Height)
      glVertex2f(-self.W_Width / 2, -self.W_Height / 2 + 0.7 * self.W_Height)
      glVertex2f(self.W_Width / 2, -self.W_Height / 2)
      glVertex2f(self.W_Width / 2, -self.W_Height / 2 + 0.7 * self.W_Height)
      glEnd()

   def draw_background_trees(self):
      y_base = -self.W_Height / 2 + 0.6 * self.W_Height
      tree_height = 60
      glBegin(GL_TRIANGLES)
      for x_start in range(int(-self.W_Width / 2) - 20, int(self.W_Width / 2) + 20, 40):
         glColor3f(0.0, 0.4, 0.0)
         glVertex2f(x_start, y_base)
         glVertex2f(x_start + 40, y_base)
         glColor3f(0.5, 1.0, 0.5)
         glVertex2f(x_start + 20, y_base + tree_height)
      glEnd()

   def draw(self):
      self.draw_terrain()
      self.draw_background_trees()

class WeatherController:
   def __init__(self, width, height, max_drops):
      self.W_Width = width
      self.W_Height = height
      self.MAX_RAINDROPS = max_drops
      self.raindrops = []
      self.rain_tilt = 0.0
      self.create_raindrops()

   def create_raindrops(self):
      for i in range(self.MAX_RAINDROPS):
         x = random.uniform(-self.W_Width / 2, self.W_Width / 2)
         y = random.uniform(0, self.W_Height / 2)
         self.raindrops.append([x, y])

   def render_rain(self):
      glColor3f(0.7, 0.8, 1.0)
      glLineWidth(1)
      glBegin(GL_LINES)
      for drop in self.raindrops:
         x, y = drop
         glVertex2f(x, y)
         glVertex2f(x + self.rain_tilt, y - 5)
      glEnd()

   def update_rain_physics(self):
      for i in range(len(self.raindrops)):
         self.update_single_raindrop(i)

   def update_single_raindrop(self, index):
      self.raindrops[index][0] += self.rain_tilt * 0.1
      self.raindrops[index][1] -= 2.0
      self.reset_raindrop_if_offscreen(index)

   def reset_raindrop_if_offscreen(self, index):
      if self.raindrops[index][1] < -self.W_Height / 2:
         self.raindrops[index][0] = random.uniform(-self.W_Width / 2, self.W_Width / 2)
         self.raindrops[index][1] = self.W_Height / 2
      
      if self.raindrops[index][0] > self.W_Width / 2:
         self.raindrops[index][0] = -self.W_Width / 2
      elif self.raindrops[index][0] < -self.W_Width / 2:
         self.raindrops[index][0] = self.W_Width / 2

class Scene:
   def __init__(self, width, height):
      self.light_level = 1.0
      self.house = HouseRenderer()
      self.scenery = SceneryRenderer(width, height)
      self.weather = WeatherController(width, height, 200)

   def render(self):
      glClearColor(0.5 * self.light_level, 0.7 * self.light_level, 1.0 * self.light_level, 1.0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()
      self.scenery.draw()
      self.house.draw()
      self.weather.render_rain()
      glutSwapBuffers()

   def update_animation(self):
      self.weather.update_rain_physics()
      glutPostRedisplay()

class InputHandler:
   def __init__(self, scene):
      self.scene = scene

   def handle_special_input(self, key, x, y):
      self.handle_rain_tilt(key)
      self.handle_light_level(key)
      glutPostRedisplay()

   def handle_rain_tilt(self, key):
      if key == GLUT_KEY_LEFT:
         self.scene.weather.rain_tilt -= 0.5
      if key == GLUT_KEY_RIGHT:
         self.scene.weather.rain_tilt += 0.5

   def handle_light_level(self, key):
      if key == GLUT_KEY_UP:
         self.scene.light_level += 0.05
         if self.scene.light_level > 1.0:
            self.scene.light_level = 1.0
      if key == GLUT_KEY_DOWN:
         self.scene.light_level -= 0.05
         if self.scene.light_level < 0.0:
            self.scene.light_level = 0.0

class WindowManager:
   def __init__(self, width, height, title):
      self.W_Width = width
      self.W_Height = height
      self.title = title
      self.scene = Scene(width, height)
      self.input_handler = InputHandler(self.scene)

   def initialize_graphics(self):
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glOrtho(-self.W_Width / 2, self.W_Width / 2, -self.W_Height / 2, self.W_Height / 2, -1.0, 1.0)
      glMatrixMode(GL_MODELVIEW)

   def run_application(self):
      glutInit()
      glutInitWindowSize(self.W_Width, self.W_Height)
      glutInitWindowPosition(100, 100)
      glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
      glutCreateWindow(self.title)
      self.initialize_graphics()
      glutDisplayFunc(self.scene.render)
      glutIdleFunc(self.scene.update_animation)
      glutSpecialFunc(self.input_handler.handle_special_input)
      glutMainLoop()

main_window = WindowManager(700, 700, b"Task 1: House in Rainfall")
main_window.run_application()




# Task 2: Building the Amazing Box

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random

# class Particle:
#    def __init__(self, x, y, speed):
#       self.x = x
#       self.y = y
#       self.dx = random.choice([-1, 1]) * speed
#       self.dy = random.choice([-1, 1]) * speed
#       self.r = random.random()
#       self.g = random.random()
#       self.b = random.random()

#    def move(self):
#       self.x += self.dx
#       self.y += self.dy

#    def check_wall_collision(self, max_x, max_y):
#       if self.x > max_x or self.x < -max_x:
#          self.dx *= -1
#       if self.y > max_y or self.y < -max_y:
#          self.dy *= -1

#    def set_speed(self, speed):
#       current_dx_sign = 1 if self.dx >= 0 else -1
#       current_dy_sign = 1 if self.dy >= 0 else -1
#       self.dx = current_dx_sign * speed
#       self.dy = current_dy_sign * speed

# class ParticleEngine:
#    def __init__(self, width, height):
#       self.W_Width = width
#       self.W_Height = height
#       self.particles = []
#       self.current_speed = 1.0

#    def spawn_particle(self, x, y):
#       gl_x = x - self.W_Width / 2
#       gl_y = self.W_Height / 2 - y
#       new_particle = Particle(gl_x, gl_y, self.current_speed)
#       self.particles.append(new_particle)
      
#    def update_all_particle_positions(self):
#       for p in self.particles:
#          p.move()
#          p.check_wall_collision(self.W_Width / 2, self.W_Height / 2)

#    def draw_all_particles(self, blinking_effect):
#       glPointSize(7)
#       glBegin(GL_POINTS)
#       for p in self.particles:
#          if blinking_effect.is_active and not blinking_effect.is_visible:
#             glColor3f(0.0, 0.0, 0.0)
#          else:
#             glColor3f(p.r, p.g, p.b)
#          glVertex2f(p.x, p.y)
#       glEnd()

#    def change_particle_speed(self, factor):
#       self.current_speed *= factor
#       for p in self.particles:
#          p.set_speed(self.current_speed)

# class VisualEffects:
#    def __init__(self):
#       self.is_active = False
#       self.is_visible = True
#       self.frame_counter = 0
#       self.BLINK_CYCLE = 30

#    def toggle_blinking(self):
#       self.is_active = not self.is_active
#       if not self.is_active:
#          self.is_visible = True
#          self.frame_counter = 0

#    def process_blinking_frame(self):
#       if self.is_active:
#          self.frame_counter += 1
#          if self.frame_counter > self.BLINK_CYCLE:
#             self.is_visible = not self.is_visible
#             self.frame_counter = 0

# class AppStateManager:
#    def __init__(self):
#       self.is_paused = False

#    def toggle_pause_state(self):
#       self.is_paused = not self.is_paused

# class InputController:
#    def __init__(self, engine, effects, state):
#       self.particle_engine = engine
#       self.visual_effects = effects
#       self.app_state = state

#    def handle_mouse_input(self, button, state, x, y):
#       if self.app_state.is_paused:
#          return
#       if state == GLUT_DOWN:
#          if button == GLUT_RIGHT_BUTTON:
#             self.particle_engine.spawn_particle(x, y)
#          elif button == GLUT_LEFT_BUTTON:
#             self.visual_effects.toggle_blinking()

#    def handle_keyboard_input(self, key, x, y):
#       if key == b' ':
#          self.app_state.toggle_pause_state()

#    def handle_special_key_input(self, key, x, y):
#       if self.app_state.is_paused:
#          return
#       if key == GLUT_KEY_UP:
#          self.particle_engine.change_particle_speed(1.2)
#       elif key == GLUT_KEY_DOWN:
#          self.particle_engine.change_particle_speed(1/1.2)

# class ApplicationRunner:
#    def __init__(self, width, height, title):
#       self.W_Width = width
#       self.W_Height = height
#       self.title = title
#       self.state = AppStateManager()
#       self.effects = VisualEffects()
#       self.engine = ParticleEngine(width, height)
#       self.inputs = InputController(self.engine, self.effects, self.state)

#    def display_frame(self):
#       glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#       glMatrixMode(GL_MODELVIEW)
#       glLoadIdentity()
#       self.engine.draw_all_particles(self.effects)
#       glutSwapBuffers()

#    def run_animation_logic(self):
#       if self.state.is_paused:
#          return
#       self.effects.process_blinking_frame()
#       self.engine.update_all_particle_positions()
#       glutPostRedisplay()

#    def handle_window_resize(self, new_width, new_height):
#       self.W_Width = new_width
#       self.W_Height = new_height
#       if self.W_Height == 0:
#          self.W_Height = 1
#       self.engine.W_Width = new_width
#       self.engine.W_Height = new_height
#       glViewport(0, 0, self.W_Width, self.W_Height)
#       glMatrixMode(GL_PROJECTION)
#       glLoadIdentity()
#       glOrtho(-self.W_Width / 2, self.W_Width / 2, -self.W_Height / 2, self.W_Height / 2, -1.0, 1.0)
#       glMatrixMode(GL_MODELVIEW)
#       glLoadIdentity()

#    def initialize_environment(self):
#       glClearColor(0.0, 0.0, 0.0, 1.0)

#    def execute(self):
#       glutInit()
#       glutInitWindowSize(self.W_Width, self.W_Height)
#       glutInitWindowPosition(150, 150)
#       glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
#       glutCreateWindow(self.title)
#       self.initialize_environment()
#       glutDisplayFunc(self.display_frame)
#       glutIdleFunc(self.run_animation_logic)
#       glutReshapeFunc(self.handle_window_resize)
#       glutMouseFunc(self.inputs.handle_mouse_input)
#       glutKeyboardFunc(self.inputs.handle_keyboard_input)
#       glutSpecialFunc(self.inputs.handle_special_key_input)
#       glutMainLoop()

# app = ApplicationRunner(500, 500, b"Task 2: The Amazing Box")
# app.execute()