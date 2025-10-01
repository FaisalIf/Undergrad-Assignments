from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from math import cos, sin, radians, sqrt, pi
import random
import time

camera_follow_first_person = False
fovY = 100
GRID_LENGTH = 600
GRID_TILES = 12
WALL_HEIGHT = 120.0
camera_radius = GRID_LENGTH + 150.0
camera_angle_deg = -90.0
camera_height = 480.0
player_pos = [0.0, 0.0, 30.0]
player_speed = 8.0
gun_angle_deg = 0.0
turn_speed = 4.0
player_alive = True
life = 5
score = 0
missed = 0
game_over = False
bullets = []
bullet_speed = 25.0
bullet_cooldown_frames = 8
frames_since_last_shot = bullet_cooldown_frames
GUN_BASE_OFFSET_X = 50.0
GUN_LENGTH = 50.0
GUN_TIP_MARGIN = 6.0
GUN_Z = 48.0
random.seed(42)
ENEMY_COUNT = 5
ENEMY_BASE_R = 30.0
enemy_speed = 1.1
enemies = []
respawn_margin = 100.0
cheat_mode = False
cheat_spin_speed = 3.0
cheat_vision = False
stable_fp_angle = 0.0
rand_var = 423
TARGET_FPS = 60.0
TARGET_DT = 1.0 / TARGET_FPS
last_update_time = 0.0


class CameraOps:
    def get_first_person(self):
        head_z = self.head_z()
        ang = self.fp_angle()
        fx, fy = self.forward(ang)
        ex, ey, ez = self.eye_fp(fx, fy, head_z)
        cx, cy, cz = self.center_fp(ex, ey, fx, fy, head_z)
        return (ex, ey, ez, cx, cy, cz, 1.0)

    def get_orbit(self):
        ex, ey, ez = self.orbit_eye()
        return (ex, ey, ez, 0.0, 0.0, 0.0, 1.0)

    def current(self):
        if camera_follow_first_person:
            return self.get_first_person()
        return self.get_orbit()

    def setup_projection(self):
        self.proj_begin()
        self.apply_perspective()

    def setup_view(self):
        self.mv_begin()
        ex, ey, ez, cx, cy, cz, upz = self.current()
        self.apply_look_at(ex, ey, ez, cx, cy, cz, upz)

    def proj_begin(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def apply_perspective(self):
        gluPerspective(fovY, 1.25, 0.1, 2600)

    def mv_begin(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def apply_look_at(self, ex, ey, ez, cx, cy, cz, upz):
        gluLookAt(ex, ey, ez, cx, cy, cz, 0, 0, upz)

    def head_z(self):
        return player_pos[2] + 66.0

    def fp_angle(self):
        if cheat_mode and cheat_vision:
            return stable_fp_angle
        return gun_angle_deg

    def forward(self, ang):
        return cos(radians(ang)), sin(radians(ang))

    def eye_fp(self, fx, fy, head_z):
        back_offset = 8.0
        ex = player_pos[0] - back_offset * fx
        ey = player_pos[1] - back_offset * fy
        ez = head_z
        return ex, ey, ez

    def center_fp(self, ex, ey, fx, fy, head_z):
        look_distance = 160.0
        cx = ex + look_distance * fx
        cy = ey + look_distance * fy
        cz = head_z
        return cx, cy, cz

    def orbit_eye(self):
        ang = camera_angle_deg
        ex = camera_radius * cos(radians(ang))
        ey = camera_radius * sin(radians(ang))
        ez = camera_height
        return ex, ey, ez


class ArenaRenderer:
    def draw_floor_tiles(self):
        tile = (2 * GRID_LENGTH) / GRID_TILES
        self.begin_tiles()
        self.draw_grid(tile)
        self.end_tiles()

    def begin_tiles(self):
        glBegin(GL_QUADS)

    def draw_grid(self, tile):
        i = 0
        while i < GRID_TILES:
            self.draw_row(i, tile)
            i += 1

    def draw_row(self, i, tile):
        j = 0
        while j < GRID_TILES:
            TILES.draw_tile(i, j, tile)
            j += 1

    def end_tiles(self):
        glEnd()

    def draw_boundaries(self):
        WALLS.draw_all()

    def draw(self):
        self.draw_floor_tiles()
        self.draw_boundaries()


class PlayerRenderer:
    def draw_body(self):
        self.body_color()
        cx, cy, cz = self.body_center()
        sx, sy, sz = self.body_size()
        GEOM.draw_cuboid(cx, cy, cz, sx, sy, sz)

    def draw_leg(self, q, y_offset):
        glPushMatrix()
        glTranslatef(0, y_offset, 0)
        gluCylinder(q, 4.5, 7.0, 28, 10, 10)
        glPopMatrix()

    def draw_legs(self, q):
        glColor3f(0.1, 0.3, 1.0)
        self.draw_leg(q, 10)
        self.draw_leg(q, -10)

    def draw_arm(self, q, y_offset):
        glPushMatrix()
        glTranslatef(30, y_offset, 50)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(q, 5.0, 7.5, 30, 10, 10)
        glPopMatrix()

    def draw_arms(self, q):
        glColor3f(0.96, 0.87, 0.70)
        self.draw_arm(q, -15)
        self.draw_arm(q, 15)

    def draw_head(self, q):
        if self.should_draw_head():
            self.head_color()
            glPushMatrix()
            self.head_transform()
            self.head_sphere(q)
            glPopMatrix()

    def draw_gun(self, q):
        glColor3f(0.6, 0.6, 0.6)
        glPushMatrix()
        glTranslatef(GUN_BASE_OFFSET_X, 0, GUN_Z)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(q, 2.0, 6.0, GUN_LENGTH, 14, 10)
        glPopMatrix()

    def draw(self):
        self.push()
        self.move_to_player()
        self.rotate_if_dead()
        self.apply_yaw()
        q = self.quadric()
        self.draw_parts(q)
        self.pop()

    def push(self):
        glPushMatrix()

    def move_to_player(self):
        glTranslatef(player_pos[0], player_pos[1], player_pos[2])

    def rotate_if_dead(self):
        if game_over:
            glRotatef(90, 0, 1, 0)

    def apply_yaw(self):
        glRotatef(gun_angle_deg, 0, 0, 1)

    def quadric(self):
        return gluNewQuadric()

    def draw_parts(self, q):
        self.draw_body()
        self.draw_legs(q)
        self.draw_arms(q)
        self.draw_head(q)
        self.draw_gun(q)

    def pop(self):
        glPopMatrix()

    def body_color(self):
        glColor3f(0.42, 0.55, 0.14)

    def body_center(self):
        return 0.0, 0.0, 43

    def body_size(self):
        return 10.0, 16.0, 15.0

    def should_draw_head(self):
        return not camera_follow_first_person

    def head_color(self):
        glColor3f(0, 0, 0)

    def head_transform(self):
        glTranslatef(0, 0, 68)

    def head_sphere(self, q):
        gluSphere(q, 13, 12, 12)


class EnemyRenderer:
    def draw(self, e):
        q = self.quadric()
        r = self.radius(e)
        self.push()
        self.translate(e)
        red_r = self.draw_body(q, r)
        self.draw_eye(q, red_r)
        self.pop()

    def quadric(self):
        return gluNewQuadric()

    def radius(self, e):
        return ENEMY_BASE_R * (0.85 + 0.15 * (1.0 + sin(e["pulse_t"])))

    def push(self):
        glPushMatrix()

    def translate(self, e):
        glTranslatef(e["x"], e["y"], e["z"])

    def draw_body(self, q, r):
        red_r = r * 0.8
        glColor3f(1, 0, 0)
        gluSphere(q, red_r, 14, 14)
        return red_r

    def draw_eye(self, q, red_r):
        glTranslatef(0, 0, red_r * 1.25)
        glColor3f(0, 0, 0)
        black_r = red_r * 0.5
        gluSphere(q, black_r, 12, 12)

    def pop(self):
        glPopMatrix()


class BulletRenderer:
    def draw(self, b):
        self.push()
        self.translate(b)
        self.color()
        q = self.quadric()
        self.sphere(q)
        self.pop()

    def push(self):
        glPushMatrix()

    def translate(self, b):
        glTranslatef(b["x"], b["y"], b["z"])

    def color(self):
        glColor3f(1, 0, 0)

    def quadric(self):
        return gluNewQuadric()

    def sphere(self, q):
        gluSphere(q, 6, 10, 10)

    def pop(self):
        glPopMatrix()


class EnemiesRenderer:
    def draw_all(self):
        if self.should_draw():
            self.loop_draw()

    def should_draw(self):
        return not game_over

    def loop_draw(self):
        i = 0
        while i < len(enemies):
            self.draw_enemy_at(i)
            i += 1

    def draw_enemy_at(self, i):
        ENEMY_DRAW.draw(enemies[i])


class BulletsRenderer:
    def draw_all(self):
        j = 0
        while j < len(bullets):
            self.draw_bullet_at(j)
            j += 1

    def draw_bullet_at(self, j):
        BULLET_DRAW.draw(bullets[j])


class EntitiesRenderer:
    def draw(self):
        self.draw_enemies()
        self.draw_bullets()
        self.draw_player()

    def draw_enemies(self):
        ENEMIES_R.draw_all()

    def draw_bullets(self):
        BULLETS_R.draw_all()

    def draw_player(self):
        PLAYER.draw()


class CheatOps:
    def auto_fire_if_los(self):
        if self.skip_auto_fire():
            return
        fx, fy = self.compute_forward()
        px, py = self.player_xy()
        self.loop_enemies_auto_fire(px, py, fx, fy)

    def skip_auto_fire(self):
        return (not cheat_mode) or game_over

    def compute_forward(self):
        return self.forward(gun_angle_deg)

    def player_xy(self):
        return player_pos[0], player_pos[1]

    def loop_enemies_auto_fire(self, px, py, fx, fy):
        i = 0
        while i < len(enemies):
            if self.process_enemy_for_los(px, py, fx, fy, enemies[i]):
                break
            i += 1

    def process_enemy_for_los(self, px, py, fx, fy, e):
        dx, dy = self.relative(px, py, e)
        ahead = self.ahead(dx, dy, fx, fy)
        side = self.side(dx, dy, fx, fy)
        if self.has_los(ahead, side):
            self.fire()
            return True
        return False

    def forward(self, ang):
        return cos(radians(ang)), sin(radians(ang))

    def relative(self, px, py, e):
        return e["x"] - px, e["y"] - py

    def ahead(self, dx, dy, fx, fy):
        return dx * fx + dy * fy

    def side(self, dx, dy, fx, fy):
        return abs(-fy * dx + fx * dy)

    def has_los(self, ahead, side):
        side_thresh = 20.0
        ahead_min = 40.0
        return ahead > ahead_min and side < side_thresh

    def fire(self):
        GAME.try_fire()


class BulletOps:
    def spawn_position(self, angle_deg):
        dist = GUN_BASE_OFFSET_X + GUN_LENGTH + GUN_TIP_MARGIN
        sx = player_pos[0] + dist * cos(radians(angle_deg))
        sy = player_pos[1] + dist * sin(radians(angle_deg))
        sz = player_pos[2] + GUN_Z
        return sx, sy, sz

    def step(self, b):
        self.wrap_step(b)

    def wrap_step(self, b):
        self.step_x(b)
        self.step_y(b)
        self.age(b)

    def step_x(self, b):
        b["x"] += bullet_speed * cos(radians(b["angle"]))

    def step_y(self, b):
        b["y"] += bullet_speed * sin(radians(b["angle"]))

    def age(self, b):
        b["age"] += 1

    def hit_enemy_index(self, b):
        return self.scan_hits(b)

    def scan_hits(self, b):
        hit_index = -1
        j = 0
        while j < len(enemies):
            if self.is_hit(b, enemies[j]):
                hit_index = j
                break
            j += 1
        return hit_index

    def is_hit(self, b, e):
        return COLLISION.bullet_hits_enemy(b, e)

    def should_remove(self, b):
        if self.out_of_bounds(b):
            return True
        if self.too_old(b):
            return True
        return False

    def out_of_bounds(self, b):
        return not MATH.within_arena(b["x"], b["y"], pad=10.0)

    def too_old(self, b):
        return b["age"] > 200


class EnemyOps:
    def pulse(self, e):
        e["pulse_t"] += 0.12

    def move_toward_player(self, e):
        dx = self.dx(e)
        dy = self.dy(e)
        nx, ny = self.normalize(dx, dy)
        self.step(e, nx, ny)

    def touches_player(self, e):
        return COLLISION.enemy_hits_player(e)

    def respawn(self, e):
        nx, ny, nz = SPAWNER.random_spawn_point()
        e["x"], e["y"], e["z"] = nx, ny, nz

    def dx(self, e):
        return player_pos[0] - e["x"]

    def dy(self, e):
        return player_pos[1] - e["y"]

    def normalize(self, dx, dy):
        L = sqrt(dx * dx + dy * dy) + 1e-6
        return dx / L, dy / L

    def step(self, e, nx, ny):
        e["x"] += enemy_speed * nx
        e["y"] += enemy_speed * ny


class FrameOps:
    def should_skip(self):
        now = self.now()
        dt = self.dt(now)
        if self.should_sleep(dt):
            self.sleep(dt)
            return True
        self.update_last(now)
        return False

    def apply_cheat(self):
        if self.should_spin():
            self.spin()
        self.apply_auto_fire()

    def cool_down(self):
        self.inc_cooldown()

    def check_miss_game_over(self):
        if self.too_many_misses():
            self.end_game()

    def now(self):
        return time.perf_counter()

    def dt(self, now):
        return now - last_update_time

    def should_sleep(self, dt):
        return dt < TARGET_DT

    def sleep(self, dt):
        time.sleep(max(0.0, TARGET_DT - dt))

    def update_last(self, now):
        global last_update_time
        last_update_time = now

    def should_spin(self):
        return cheat_mode and not game_over

    def spin(self):
        global gun_angle_deg
        gun_angle_deg = (gun_angle_deg + cheat_spin_speed) % 360.0

    def apply_auto_fire(self):
        CHEAT.auto_fire_if_los()

    def inc_cooldown(self):
        global frames_since_last_shot
        frames_since_last_shot += 1

    def too_many_misses(self):
        return missed >= 10

    def end_game(self):
        global game_over
        if not game_over:
            game_over = True
            print("Game Over", flush=True)


class TextRenderer:
    def draw(self, x, y, text, font=None):
        if font is None:
            font = GLUT_BITMAP_HELVETICA_18
        glColor3f(1, 1, 1)
        self.begin_ortho()
        self.draw_text(x, y, text, font)
        self.end_ortho()

    def begin_ortho(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

    def draw_text(self, x, y, text, font):
        glRasterPos2f(x, y)
        i = 0
        while i < len(text):
            glutBitmapCharacter(font, ord(text[i]))
            i += 1

    def end_ortho(self):
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


class GeometryRenderer:
    def draw_cuboid(self, cx, cy, cz, sx, sy, sz):
        x0, x1, y0, y1, z0, z1 = self.box_coords(cx, cy, cz, sx, sy, sz)
        self.begin_box()
        self.draw_faces(x0, x1, y0, y1, z0, z1)
        self.end_box()

    def box_coords(self, cx, cy, cz, sx, sy, sz):
        x0, x1 = cx - sx, cx + sx
        y0, y1 = cy - sy, cy + sy
        z0, z1 = cz - sz, cz + sz
        return x0, x1, y0, y1, z0, z1

    def begin_box(self):
        glBegin(GL_QUADS)

    def end_box(self):
        glEnd()

    def draw_faces(self, x0, x1, y0, y1, z0, z1):
        self.face_px(x0, x1, y0, y1, z0, z1)
        self.face_nx(x0, x1, y0, y1, z0, z1)
        self.face_py(x0, x1, y0, y1, z0, z1)
        self.face_ny(x0, x1, y0, y1, z0, z1)
        self.face_pz(x0, x1, y0, y1, z0, z1)
        self.face_nz(x0, x1, y0, y1, z0, z1)

    def face_px(self, x0, x1, y0, y1, z0, z1):
        glVertex3f(x1, y0, z0); glVertex3f(x1, y1, z0); glVertex3f(x1, y1, z1); glVertex3f(x1, y0, z1)

    def face_nx(self, x0, x1, y0, y1, z0, z1):
        glVertex3f(x0, y0, z0); glVertex3f(x0, y0, z1); glVertex3f(x0, y1, z1); glVertex3f(x0, y1, z0)

    def face_py(self, x0, x1, y0, y1, z0, z1):
        glVertex3f(x0, y1, z0); glVertex3f(x1, y1, z0); glVertex3f(x1, y1, z1); glVertex3f(x0, y1, z1)

    def face_ny(self, x0, x1, y0, y1, z0, z1):
        glVertex3f(x0, y0, z0); glVertex3f(x0, y0, z1); glVertex3f(x1, y0, z1); glVertex3f(x1, y0, z0)

    def face_pz(self, x0, x1, y0, y1, z0, z1):
        glVertex3f(x0, y0, z1); glVertex3f(x1, y0, z1); glVertex3f(x1, y1, z1); glVertex3f(x0, y1, z1)

    def face_nz(self, x0, x1, y0, y1, z0, z1):
        glVertex3f(x0, y0, z0); glVertex3f(x0, y1, z0); glVertex3f(x1, y1, z0); glVertex3f(x1, y0, z0)


class TileRenderer:
    def draw_tile(self, i, j, tile):
        x0, y0, x1, y1 = self.coords(i, j, tile)
        self.color(i, j)
        self.draw_vertices(x0, y0, x1, y1)

    def coords(self, i, j, tile):
        x0 = -GRID_LENGTH + i * tile
        y0 = -GRID_LENGTH + j * tile
        x1 = x0 + tile
        y1 = y0 + tile
        return x0, y0, x1, y1

    def color(self, i, j):
        if (i + j) % 2 == 0:
            glColor3f(1, 1, 1)
        else:
            glColor3f(0.7, 0.5, 0.95)

    def draw_vertices(self, x0, y0, x1, y1):
        glVertex3f(x0, y1, 0); glVertex3f(x1, y1, 0); glVertex3f(x1, y0, 0); glVertex3f(x0, y0, 0)


class WallsRenderer:
    def draw_top(self, L, H):
        glColor3f(0.0, 1.0, 1.0)
        self.begin()
        self.verts_top(L, H)
        self.end()

    def draw_bottom(self, L, H):
        glColor3f(1.0, 1.0, 1.0)
        self.begin()
        self.verts_bottom(L, H)
        self.end()

    def draw_right(self, L, H):
        glColor3f(0.0, 1.0, 0.0)
        self.begin()
        self.verts_right(L, H)
        self.end()

    def draw_left(self, L, H):
        glColor3f(0.0, 0.0, 1.0)
        self.begin()
        self.verts_left(L, H)
        self.end()

    def draw_all(self):
        L = GRID_LENGTH
        H = WALL_HEIGHT
        self.draw_top(L, H)
        self.draw_bottom(L, H)
        self.draw_right(L, H)
        self.draw_left(L, H)

    def begin(self):
        glBegin(GL_QUADS)

    def end(self):
        glEnd()

    def verts_top(self, L, H):
        glVertex3f(-L, L, 0); glVertex3f(L, L, 0); glVertex3f(L, L, H); glVertex3f(-L, L, H)

    def verts_bottom(self, L, H):
        glVertex3f(-L, -L, 0); glVertex3f(L, -L, 0); glVertex3f(L, -L, H); glVertex3f(-L, -L, H)

    def verts_right(self, L, H):
        glVertex3f(L, -L, 0); glVertex3f(L, L, 0); glVertex3f(L, L, H); glVertex3f(L, -L, H)

    def verts_left(self, L, H):
        glVertex3f(-L, -L, 0); glVertex3f(-L, L, 0); glVertex3f(-L, L, H); glVertex3f(-L, -L, H)


class MathOps:
    def clamp(self, v, lo, hi):
        return lo if v < lo else hi if v > hi else v

    def dist2(self, x1, y1, x2, y2):
        dx, dy = x1 - x2, y1 - y2
        return dx * dx + dy * dy

    def within_arena(self, x, y, pad=40.0):
        L = GRID_LENGTH - pad
        return -L <= x <= L and -L <= y <= L


class CollisionOps:
    def bullet_hits_enemy(self, b, e):
        return MATH.dist2(b["x"], b["y"], e["x"], e["y"]) <= (ENEMY_BASE_R * ENEMY_BASE_R)

    def enemy_hits_player(self, e):
        return MATH.dist2(e["x"], e["y"], player_pos[0], player_pos[1]) < (ENEMY_BASE_R + 25) ** 2


class Spawner:
    def random_spawn_point(self):
        side = self.choose_side()
        return self.spawn_from_side(side)

    def choose_side(self):
        return random.choice([0, 1, 2, 3])

    def spawn_from_side(self, side):
        L = GRID_LENGTH - respawn_margin
        if side == 0:
            return self.left(L)
        if side == 1:
            return self.right(L)
        if side == 2:
            return self.bottom(L)
        return self.top(L)

    def left(self, L):
        return [-L, random.uniform(-L, L), ENEMY_BASE_R]

    def right(self, L):
        return [L, random.uniform(-L, L), ENEMY_BASE_R]

    def bottom(self, L):
        return [random.uniform(-L, L), -L, ENEMY_BASE_R]

    def top(self, L):
        return [random.uniform(-L, L), L, ENEMY_BASE_R]


class HUDStatsRenderer:
    def draw(self):
        self.life()
        self.score()
        self.missed()

    def life(self):
        TEXT.draw(10, 770, f"Player Life Remaining: {life}")

    def score(self):
        TEXT.draw(10, 740, f"Game Score: {score}")

    def missed(self):
        TEXT.draw(10, 710, f"Player Bullet Missed: {missed}")


class HUDOverRenderer:
    def draw(self):
        if self.should_show():
            self.draw_msg()

    def should_show(self):
        return game_over

    def draw_msg(self):
        TEXT.draw(10, 770, f"Game is Over. Your Score is {score}.")
        TEXT.draw(10, 740, 'Press "R" to RESTART the Game')


class HUDRenderer:
    def draw(self):
        if game_over:
            self.draw_over()
        else:
            self.draw_stats()

    def draw_over(self):
        HUD_OVER.draw()

    def draw_stats(self):
        HUD_STATS.draw()


class SceneRenderer:
    def draw_world(self):
        ARENA.draw()

    def draw_entities(self):
        ENTITIES.draw()

    def draw_hud(self):
        HUD.draw()

    def render(self):
        self.pre_entities()
        self.render_entities()
        self.post_entities()
        self.render_hud()

    def pre_entities(self):
        self.render_world()

    def post_entities(self):
        pass

    def render_world(self):
        self.draw_world()

    def render_entities(self):
        self.draw_entities()

    def render_hud(self):
        self.draw_hud()


class InputOps:
    def move_forward(self):
        fx = self.fx()
        fy = self.fy()
        self.move(fx, fy)

    def move_backward(self):
        fx = self.fx()
        fy = self.fy()
        self.move(-fx, -fy)

    def rotate_left(self):
        self.turn(-turn_speed)

    def rotate_right(self):
        self.turn(turn_speed)

    def toggle_cheat(self):
        self.toggle_cheat_flag()

    def toggle_cheat_vision(self):
        self.flip_cheat_vision()
        self.sync_stable_angle_after_toggle()

    def restart(self):
        GAME.reset()

    def after_move(self):
        GAME.keep_player_in_bounds()

    def fx(self):
        return cos(radians(gun_angle_deg))

    def fy(self):
        return sin(radians(gun_angle_deg))

    def move(self, fx, fy):
        player_pos[0] += player_speed * fx
        player_pos[1] += player_speed * fy

    def turn(self, delta):
        global gun_angle_deg
        gun_angle_deg += delta

    def toggle_cheat_flag(self):
        global cheat_mode
        cheat_mode = not cheat_mode

    def flip_cheat_vision(self):
        global cheat_vision
        cheat_vision = not cheat_vision

    def sync_stable_angle_after_toggle(self):
        global stable_fp_angle
        if cheat_mode and cheat_vision:
            stable_fp_angle = gun_angle_deg
        if (not cheat_vision) and cheat_mode:
            stable_fp_angle = gun_angle_deg


class CameraControl:
    def orbit_left(self):
        self.orbit(-2.5)

    def orbit_right(self):
        self.orbit(2.5)

    def move_up(self):
        self.height(10.0)

    def move_down(self):
        self.height(-10.0)
        self.enforce_min_height()

    def orbit(self, delta):
        global camera_angle_deg
        camera_angle_deg += delta

    def height(self, delta):
        global camera_height
        camera_height += delta

    def enforce_min_height(self):
        global camera_height
        if camera_height < 120.0:
            camera_height = 120.0


class MouseOps:
    def left_down(self):
        GAME.try_fire()

    def right_down(self):
        CAMMODE.toggle_follow()


class CameraModeOps:
    def toggle_follow(self):
        global camera_follow_first_person
        camera_follow_first_person = not camera_follow_first_person


class GameOps:
    def reset(self):
        self.reset_counters()
        self.reset_flags()
        self.reset_player()
        self.clear_collections()
        self.reset_cooldown()
        self.spawn_initial_enemies()

    def keep_player_in_bounds(self):
        self.bound_x()
        self.bound_y()

    def bound_x(self):
        player_pos[0] = MATH.clamp(player_pos[0], -GRID_LENGTH + 25, GRID_LENGTH - 25)

    def bound_y(self):
        player_pos[1] = MATH.clamp(player_pos[1], -GRID_LENGTH + 25, GRID_LENGTH - 25)

    def try_fire(self):
        if not self.can_fire():
            return
        ang = gun_angle_deg
        self.consume_cooldown()
        sx, sy, sz = BULLET.spawn_position(ang)
        self.spawn_bullet(sx, sy, sz, ang)
        print("Player Bullet Fired!", flush=True)

    def can_fire(self):
        if game_over:
            return False
        return frames_since_last_shot >= bullet_cooldown_frames

    def consume_cooldown(self):
        global frames_since_last_shot
        frames_since_last_shot = 0

    def spawn_bullet(self, sx, sy, sz, ang):
        bullets.append({"x": sx, "y": sy, "z": sz, "angle": ang, "age": 0})

    def reset_counters(self):
        global life, score, missed
        life, score, missed = 5, 0, 0

    def reset_flags(self):
        global game_over, player_alive, cheat_mode, cheat_vision
        game_over = False
        player_alive = True
        cheat_mode = False
        cheat_vision = False

    def reset_player(self):
        global gun_angle_deg
        player_pos[:] = [0.0, 0.0, 30.0]
        gun_angle_deg = 0.0

    def clear_collections(self):
        bullets.clear()
        enemies.clear()

    def reset_cooldown(self):
        global frames_since_last_shot
        frames_since_last_shot = bullet_cooldown_frames

    def spawn_initial_enemies(self):
        k = 0
        while k < ENEMY_COUNT:
            x, y, z = SPAWNER.random_spawn_point()
            enemies.append({"x": x, "y": y, "z": z, "pulse_t": random.uniform(0, 6.28)})
            k += 1


class UpdateOps:
    def bullets(self):
        BULLET_UPD.update()

    def enemies(self):
        ENEMY_UPD.update()


class BulletsUpdateOps:
    def update(self):
        to_remove = self.collect_removals()
        self.apply_removals(to_remove)

    def collect_removals(self):
        to_remove = self.init_removal_list()
        self.loop_bullets_collect(to_remove)
        return self.finalize_removals(to_remove)

    def add_removal(self, to_remove, idx):
        to_remove.append(idx)

    def init_removal_list(self):
        return []

    def loop_bullets_collect(self, to_remove):
        i = 0
        while i < len(bullets):
            b = bullets[i]
            BULLET.step(b)
            if self.handle_bullet(i, b):
                self.add_removal(to_remove, i)
            i += 1

    def finalize_removals(self, to_remove):
        to_remove.sort(reverse=True)
        return to_remove

    def handle_bullet(self, idx_b, b):
        hit_idx = BULLET.hit_enemy_index(b)
        if hit_idx >= 0:
            return self.on_hit_path(hit_idx)
        if BULLET.should_remove(b):
            return self.on_miss_path()
        return False

    def on_hit_path(self, enemy_index):
        self.on_hit(enemy_index)
        return True

    def on_miss_path(self):
        self.on_miss()
        return True

    def on_hit(self, enemy_index):
        global score
        score += 1
        nx, ny, nz = SPAWNER.random_spawn_point()
        enemies[enemy_index] = {"x": nx, "y": ny, "z": nz, "pulse_t": 0.0}

    def on_miss(self):
        global missed
        missed += 1
        print(f"Bullet missed: {missed}", flush=True)

    def apply_removals(self, to_remove):
        k = 0
        while k < len(to_remove):
            bullets.pop(to_remove[k])
            k += 1


class EnemiesUpdateOps:
    def update(self):
        self.loop()

    def loop(self):
        i = 0
        while i < len(enemies):
            self.update_enemy(enemies[i])
            i += 1

    def update_enemy(self, e):
        ENEMY_OP.pulse(e)
        ENEMY_OP.move_toward_player(e)
        if self.should_touch_player(e):
            self.touch_player(e)

    def should_touch_player(self, e):
        return ENEMY_OP.touches_player(e) and not game_over

    def touch_player(self, e):
        global life, game_over, player_alive
        self.dec_life()
        self.respawn_enemy(e)
        self.handle_death()

    def dec_life(self):
        global life
        life -= 1
        print(f"Remaining Player Life: {life}", flush=True)

    def respawn_enemy(self, e):
        ENEMY_OP.respawn(e)

    def handle_death(self):
        global life, game_over, player_alive
        if life <= 0:
            game_over = True
            player_alive = False
            print("Game Over", flush=True)


class ScreenRenderOps:
    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def identity(self):
        glLoadIdentity()

    def viewport(self):
        glViewport(0, 0, 1000, 800)

    def project_and_view(self):
        CAM.setup_projection()
        CAM.setup_view()

    def draw_scene(self):
        SCENE.render()

    def swap(self):
        glutSwapBuffers()

    def pre(self):
        self.clear()
        self.identity()
        self.viewport()
        self.project_and_view()

    def post(self):
        self.swap()

    def show(self):
        self.pre()
        self.draw_scene()
        self.post()


def keyboardListener(key, x, y):
    KEYDISP.handle(key)


def specialKeyListener(key, x, y):
    SPDISP.handle(key)


def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        MOUSE.left_down()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        MOUSE.right_down()


def idle():
    IDLE.run()


class KeyboardDispatch:
    def handle(self, key):
        if self.game_over_restart(key):
            return
        self.movement(key)
        self.rotation(key)
        self.cheats(key)
        self.restart(key)

    def game_over_restart(self, key):
        if game_over and key == b'r':
            GAME.reset()
            return True
        if game_over:
            return True
        return False

    def movement(self, key):
        if key == b'w':
            self.move_w()
        if key == b's':
            self.move_s()

    def move_w(self):
        INPUT.move_forward(); INPUT.after_move()

    def move_s(self):
        INPUT.move_backward(); INPUT.after_move()

    def rotation(self, key):
        if key == b'a':
            self.rot_a()
        if key == b'd':
            self.rot_d()

    def rot_a(self):
        INPUT.rotate_right()

    def rot_d(self):
        INPUT.rotate_left()

    def cheats(self, key):
        if key == b'c':
            self.cheat_toggle()
        if key == b'v':
            self.cheat_vision_toggle()

    def cheat_toggle(self):
        INPUT.toggle_cheat()

    def cheat_vision_toggle(self):
        INPUT.toggle_cheat_vision()

    def restart(self, key):
        if key == b'r':
            self.restart_r()

    def restart_r(self):
        INPUT.restart()


class SpecialKeyDispatch:
    def handle(self, key):
        if key == GLUT_KEY_LEFT:
            self.left()
        if key == GLUT_KEY_RIGHT:
            self.right()
        if key == GLUT_KEY_UP:
            self.up()
        if key == GLUT_KEY_DOWN:
            self.down()

    def left(self):
        CAMCTL.orbit_left()

    def right(self):
        CAMCTL.orbit_right()

    def up(self):
        CAMCTL.move_up()

    def down(self):
        CAMCTL.move_down()


class IdleOps:
    def run(self):
        if FRAME.should_skip():
            return
        self.cheat_and_stable_angle()
        self.updates()
        self.frame_housekeeping()
        self.redisplay()

    def cheat_and_stable_angle(self):
        global stable_fp_angle
        FRAME.apply_cheat()
        if cheat_mode and not cheat_vision:
            stable_fp_angle = gun_angle_deg

    def updates(self):
        UPD.bullets()
        UPD.enemies()

    def frame_housekeeping(self):
        FRAME.cool_down()
        FRAME.check_miss_game_over()

    def redisplay(self):
        glutPostRedisplay()


def showScreen():
    SCREEN.show()


TEXT = TextRenderer()
GEOM = GeometryRenderer()
TILES = TileRenderer()
WALLS = WallsRenderer()
MATH = MathOps()
COLLISION = CollisionOps()
SPAWNER = Spawner()
HUD = HUDRenderer()
HUD_STATS = HUDStatsRenderer()
HUD_OVER = HUDOverRenderer()
SCENE = SceneRenderer()
INPUT = InputOps()
CAMCTL = CameraControl()
MOUSE = MouseOps()
CAMMODE = CameraModeOps()
GAME = GameOps()
BULLET = BulletOps()
ENEMY_OP = EnemyOps() 
BULLET_UPD = BulletsUpdateOps()
ENEMY_UPD = EnemiesUpdateOps()
UPD = UpdateOps()
CAM = CameraOps()
ARENA = ArenaRenderer()
PLAYER = PlayerRenderer()
ENEMY_DRAW = EnemyRenderer()
BULLET_DRAW = BulletRenderer()
ENEMIES_R = EnemiesRenderer()
BULLETS_R = BulletsRenderer()
ENTITIES = EntitiesRenderer()
FRAME = FrameOps()
SCREEN = ScreenRenderOps()
KEYDISP = KeyboardDispatch()
SPDISP = SpecialKeyDispatch()
IDLE = IdleOps()
CHEAT = CheatOps()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy - PyOpenGL")
    global last_update_time
    last_update_time = time.perf_counter()
    GAME.reset()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()