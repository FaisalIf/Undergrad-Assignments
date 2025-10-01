import time
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
glutInit()

screen_width = 500
screen_height = 700
window_title = b"Gem Catcher"

catcher_top_width = 110
catcher_bottom_width = 70
catcher_height = 20
catcher_base_y = 15
catcher_speed = 15

item_width = 30
item_height = 40
item_initial_speed = 160.0
item_speed_increase = 1.04

color_black = (0.0, 0.0, 0.0)
color_white = (1.0, 1.0, 1.0)
color_red = (1.0, 0.2, 0.2)
color_teal = (0.0, 0.8, 0.8)
color_amber = (1.0, 0.75, 0.0)
item_colors = [
    (1.0, 1.0, 0.2), (0.2, 1.0, 1.0), (1.0, 0.2, 1.0),
    (1.0, 0.6, 0.2), (0.2, 1.0, 0.2)
]

class LineRenderer:
   def draw_pixel(self, x, y, color):
      glColor3f(color[0], color[1], color[2])
      glBegin(GL_POINTS)
      glVertex2f(x, y)
      glEnd()

   def find_zone(self, dx, dy):
      if abs(dx) > abs(dy):
         if dx >= 0 and dy >= 0: return 0
         if dx < 0 and dy >= 0: return 3
         if dx < 0 and dy < 0: return 4
         if dx >= 0 and dy < 0: return 7
      else:
         if dx >= 0 and dy >= 0: return 1
         if dx < 0 and dy >= 0: return 2
         if dx < 0 and dy < 0: return 5
         if dx >= 0 and dy < 0: return 6
      return 0

   def convert_to_zone_zero(self, x, y, zone):
      if zone == 0: return x, y
      if zone == 1: return y, x
      if zone == 2: return y, -x
      if zone == 3: return -x, y
      if zone == 4: return -x, -y
      if zone == 5: return -y, -x
      if zone == 6: return -y, x
      if zone == 7: return x, -y
      return x, y

   def revert_from_zone_zero(self, x, y, zone):
      if zone == 0: return x, y
      if zone == 1: return y, x
      if zone == 2: return -y, x
      if zone == 3: return -x, y
      if zone == 4: return -x, -y
      if zone == 5: return -y, -x
      if zone == 6: return y, -x
      if zone == 7: return x, -y
      return x, y

   def draw_line(self, x1, y1, x2, y2, color):
      dx, dy = x2 - x1, y2 - y1
      zone = self.find_zone(dx, dy)
      x1_z0, y1_z0 = self.convert_to_zone_zero(x1, y1, zone)
      x2_z0, y2_z0 = self.convert_to_zone_zero(x2, y2, zone)

      if x1_z0 > x2_z0:
         x1_z0, x2_z0 = x2_z0, x1_z0
         y1_z0, y2_z0 = y2_z0, y1_z0

      dx_z0, dy_z0 = x2_z0 - x1_z0, y2_z0 - y1_z0
      d = 2 * dy_z0 - dx_z0
      inc_e = 2 * dy_z0
      inc_ne = 2 * (dy_z0 - dx_z0)
      
      y = y1_z0
      for x in range(x1_z0, x2_z0 + 1):
         original_point = self.revert_from_zone_zero(x, y, zone)
         self.draw_pixel(original_point[0], original_point[1], color)
         if d > 0:
            d += inc_ne
            y += 1
         else:
            d += inc_e

class PlayerCatcher:
   def __init__(self):
      self.x = screen_width / 2
      self.color = color_white
      self.max_width = max(catcher_top_width, catcher_bottom_width)

   def render(self, renderer):
      x1 = self.x - catcher_bottom_width / 2
      x2 = self.x + catcher_bottom_width / 2
      x3 = self.x + catcher_top_width / 2
      x4 = self.x - catcher_top_width / 2
      y1 = catcher_base_y
      y2 = y1 + catcher_height
      renderer.draw_line(int(x1), int(y1), int(x2), int(y1), self.color)
      renderer.draw_line(int(x2), int(y1), int(x3), int(y2), self.color)
      renderer.draw_line(int(x3), int(y2), int(x4), int(y2), self.color)
      renderer.draw_line(int(x4), int(y2), int(x1), int(y1), self.color)

   def move(self, direction):
      self.x += direction * catcher_speed
      half_width = self.max_width / 2
      self.x = max(half_width, self.x)
      self.x = min(screen_width - half_width, self.x)
      
   def get_aabb(self):
      return { "x": self.x - self.max_width / 2, "y": catcher_base_y, 
               "w": self.max_width, "h": catcher_height }

class FallingItem:
   def __init__(self):
      self.x = 0
      self.y = 0
      self.color = color_white
      self.respawn()

   def respawn(self):
      self.x = random.randint(int(item_width/2), int(screen_width - item_width/2))
      self.y = screen_height
      self.color = random.choice(item_colors)

   def update_position(self, delta_t, speed):
      self.y -= speed * delta_t

   def render(self, renderer):
      p1 = (self.x, self.y)
      p2 = (self.x + item_width/2, self.y - item_height/2)
      p3 = (self.x, self.y - item_height)
      p4 = (self.x - item_width/2, self.y - item_height/2)
      renderer.draw_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), self.color)
      renderer.draw_line(int(p2[0]), int(p2[1]), int(p3[0]), int(p3[1]), self.color)
      renderer.draw_line(int(p3[0]), int(p3[1]), int(p4[0]), int(p4[1]), self.color)
      renderer.draw_line(int(p4[0]), int(p4[1]), int(p1[0]), int(p1[1]), self.color)
      
   def get_aabb(self):
      return { "x": self.x - item_width/2, "y": self.y - item_height, 
               "w": item_width, "h": item_height }

class GemCatcherGame:
   def __init__(self):
      self.score = 0
      self.is_over = False
      self.is_paused = False
      self.item_speed = item_initial_speed
      self.last_time = 0.0
      self.renderer = LineRenderer()
      self.catcher = PlayerCatcher()
      self.item = FallingItem()
      self.setup_window()
      self.set_callbacks()
      self.start_game()

   def setup_window(self):
      glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
      glutInitWindowSize(screen_width, screen_height)
      glutInitWindowPosition(100, 100)
      glutCreateWindow(window_title)
      glViewport(0, 0, screen_width, screen_height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glOrtho(0.0, screen_width, 0.0, screen_height, 0.0, 1.0)
      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()
      glClearColor(color_black[0], color_black[1], color_black[2], 1.0)
      glPointSize(2.0)

   def set_callbacks(self):
      glutDisplayFunc(self.game_loop)
      glutIdleFunc(self.animation_trigger)
      glutSpecialFunc(self.keyboard_listener)
      glutMouseFunc(self.mouse_listener)

   def start_game(self):
      print("New game started.")
      self.score = 0
      self.is_over = False
      self.is_paused = False
      self.item_speed = item_initial_speed
      self.catcher.x = screen_width / 2
      self.catcher.color = color_white
      self.item.respawn()
      self.last_time = time.time()

   def update_logic(self, delta_t):
      if self.is_paused or self.is_over:
         return
      
      self.item.update_position(delta_t, self.item_speed)
      
      if self.is_colliding(self.item.get_aabb(), self.catcher.get_aabb()):
         self.score += 1
         print("Score:", self.score)
         self.item_speed *= item_speed_increase
         self.item.respawn()
         
      elif (self.item.get_aabb()['y'] + self.item.get_aabb()['h']) < 0:
         print("Game Over. Final Score:", self.score)
         self.is_over = True
         self.catcher.color = color_red

   def is_colliding(self, box1, box2):
      return (box1['x'] < box2['x'] + box2['w'] and
              box1['x'] + box1['w'] > box2['x'] and
              box1['y'] < box2['y'] + box2['h'] and
              box1['y'] + box1['h'] > box2['y'])

   def render_scene(self):
      self.catcher.render(self.renderer)
      if not self.is_over:
         self.item.render(self.renderer)
      self.render_buttons()
      
   def render_buttons(self):
      self.renderer.draw_line(50, 670, 20, 670, color_teal)
      self.renderer.draw_line(20, 670, 35, 680, color_teal)
      self.renderer.draw_line(20, 670, 35, 660, color_teal)
      if self.is_paused:
         self.renderer.draw_line(240, 660, 240, 680, color_amber)
         self.renderer.draw_line(240, 680, 260, 670, color_amber)
         self.renderer.draw_line(260, 670, 240, 660, color_amber)
      else:
         self.renderer.draw_line(240, 660, 240, 680, color_amber)
         self.renderer.draw_line(255, 660, 255, 680, color_amber)
      self.renderer.draw_line(450, 680, 470, 660, color_red)
      self.renderer.draw_line(450, 660, 470, 680, color_red)

   def game_loop(self):
      current_time = time.time()
      delta_t = current_time - self.last_time
      self.last_time = current_time
      self.update_logic(delta_t)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      self.render_scene()
      glutSwapBuffers()

   def animation_trigger(self):
      glutPostRedisplay()

   def keyboard_listener(self, key, x, y):
      if self.is_over or self.is_paused:
         return
      if key == GLUT_KEY_LEFT:
         self.catcher.move(-1)
      elif key == GLUT_KEY_RIGHT:
         self.catcher.move(1)

   def mouse_listener(self, button, state, x, y):
      if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
         gl_y = screen_height - y
         if 20 <= x <= 50 and 655 <= gl_y <= 685:
            self.start_game()
         elif 235 <= x <= 265 and 655 <= gl_y <= 685:
            if not self.is_over:
               self.is_paused = not self.is_paused
               self.last_time = time.time()
         elif 445 <= x <= 475 and 655 <= gl_y <= 685:
            print("Goodbye! Your score was:", self.score)
            glutLeaveMainLoop()

   def run(self):
      print("Launching Game...")
      glutMainLoop()

game_instance = GemCatcherGame()
game_instance.run()