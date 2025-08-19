import pgzrun
from pygame.rect import Rect
import random

WIDTH = 1000
HEIGHT = 560
TITLE = "Game of Toledo"
TITLE_FONT_NAME = "game of thrones"
BUTTON_FONT_NAME = "poppins"
TILE_WIDTH = 40
GRAVITY = 0.5

PLATFORM_TYPES = [
    {'image': 'platform_1', 'length': 1},
    {'image': 'platform_2', 'length': 2},
    {'image': 'platform_3', 'length': 3},
    {'image': 'platform_4', 'length': 4},
    {'image': 'platform_5', 'length': 5},
    {'image': 'platform',   'length': 3},
]

game_state = "menu"
player = None
enemies = []
platforms = []
music_on = True
mouse_pos = (0, 0)
scroll_x = 0
farthest_x_generated = 0
last_platform_pos = (150, HEIGHT - 100)
distance_traveled = 0
final_score = 0

class AnimatedActor:
    def __init__(self, initial_frames, pos, anchor=('center', 'bottom')):
        self.frames = initial_frames
        self.actor = Actor(self.frames[0] if self.frames else 'hero_idle_right/idle1', pos=pos, anchor=anchor)
        self.initial_pos = pos
        self.hitbox = self.actor.copy()
        self.current_frame, self.animation_timer, self.animation_speed = 0, 0, 0.09
    
    def update_animation(self, dt):
        if not self.frames: 
            return
        
        self.animation_timer += dt

        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.actor.image = self.frames[self.current_frame]

    def draw(self):
        self.actor.draw()

class Player(AnimatedActor):
    def __init__(self, pos):
        self.idle_frames_right = ['hero_idle_right/idle1', 'hero_idle_right/idle2', 'hero_idle_right/idle3', 'hero_idle_right/idle4']
        self.idle_frames_left = ['hero_idle_left/idleback1', 'hero_idle_left/idleback2', 'hero_idle_left/idleback3', 'hero_idle_left/idleback4']
        self.run_frames_right = ['hero_run_right/run1', 'hero_run_right/run2', 'hero_run_right/run3', 'hero_run_right/run4', 'hero_run_right/run5', 'hero_run_right/run6', 'hero_run_right/run7']
        self.run_frames_left = ['hero_run_left/runback1', 'hero_run_left/runback2', 'hero_run_left/runback3', 'hero_run_left/runback4', 'hero_run_left/runback5', 'hero_run_left/runback6', 'hero_run_left/runback7']
        
        self.jump_frame_right = 'hero_run_right/run1'
        self.jump_frame_left = 'hero_run_left/runback1' 

        super().__init__(self.idle_frames_right, pos)
        
        self.hitbox = Rect(0, 0, self.actor.width - 5, self.actor.height - 2)
        self.hitbox.center = self.actor.center
        self.last_direction, self.vy, self.on_ground = 'right', 0, False
        self.speed, self.jump_strength = 4, -13
    
    def update(self, dt, platforms_list):
        scroll_speed = 0
        is_moving = False 

        if keyboard.left:
            if self.actor.x > self.speed: 
                self.actor.x -= self.speed

            self.last_direction = 'left'
            is_moving = True

        elif keyboard.right:
            if self.actor.x < WIDTH / 2: 
                self.actor.x += self.speed

            else: 
                scroll_speed = -self.speed

            self.last_direction = 'right'
            is_moving = True
        
        self.vy += GRAVITY
        self.actor.y += self.vy
        self.on_ground = False
        self.hitbox.centerx, self.hitbox.bottom = self.actor.centerx, self.actor.bottom

        for platform in platforms_list:
            if self.hitbox.colliderect(platform.hitbox) and self.vy > 0 and self.actor.bottom - self.vy <= platform.actor.top + 1:
                self.actor.bottom, self.vy, self.on_ground = platform.actor.top, 0, True
                break
        
        if self.on_ground:
            if is_moving:
                self.frames = self.run_frames_right if self.last_direction == 'right' else self.run_frames_left

            else:
                self.frames = self.idle_frames_right if self.last_direction == 'right' else self.idle_frames_left

        else:
            if self.last_direction == 'right':
                self.frames = [self.jump_frame_right]

            else:
                self.frames = [self.jump_frame_left]

        self.hitbox.centerx, self.hitbox.bottom = self.actor.centerx, self.actor.bottom
        self.update_animation(dt)

        return scroll_speed

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_strength

            if music_on: 
                sounds.jump.play()

class Enemy(AnimatedActor):
    def __init__(self, pos, all_platforms, behavior='patrol'):
        self.idle_frames_right = ['enemy_idle_right/idle1', 'enemy_idle_right/idle2', 'enemy_idle_right/idle3', 'enemy_idle_right/idle4', 'enemy_idle_right/idle5', 'enemy_idle_right/idle6', 'enemy_idle_right/idle7']
        self.idle_frames_left = ['enemy_idle_left/idleback1', 'enemy_idle_left/idleback2', 'enemy_idle_left/idleback3', 'enemy_idle_left/idleback4', 'enemy_idle_left/idleback5', 'enemy_idle_left/idleback6', 'enemy_idle_left/idleback7']
        self.walk_frames_right = ['enemy_walk_right/walk1', 'enemy_walk_right/walk2', 'enemy_walk_right/walk3', 'enemy_walk_right/walk4', 'enemy_walk_right/walk5', 'enemy_walk_right/walk6', 'enemy_walk_right/walk7']
        self.walk_frames_left = ['enemy_walk_left/walkback1', 'enemy_walk_left/walkback2', 'enemy_walk_left/walkback3', 'enemy_walk_left/walkback4', 'enemy_walk_left/walkback5', 'enemy_walk_left/walkback6', 'enemy_walk_left/walkback7']

        super().__init__(self.walk_frames_right, pos)

        self.hitbox = Rect(0, 0, self.actor.width - 2, self.actor.height - 2)
        self.hitbox.center, self.direction, self.speed, self.state, self.behavior = self.actor.center, random.choice([-1, 1]), 1, 'walking', behavior

        if self.behavior == 'patrol':
            self.idle_timer, self.IDLE_DURATION = 0, random.uniform(1.0, 2.5)
            self.patrol_start_x, self.patrol_end_x = self.actor.centerx - 30, self.actor.centerx + 30
            self._find_patrol_bounds(all_platforms)

        elif self.behavior == 'random':
            self.action_timer, self.action_duration = 0, random.uniform(2.0, 5.0)

    def _find_patrol_bounds(self, all_platforms):
        platforms_below = [p for p in all_platforms if p.actor.left < self.actor.centerx < p.actor.right and p.actor.top >= self.actor.bottom - 5]
        ground_platform = min(platforms_below, key=lambda p: p.actor.top) if platforms_below else None

        if ground_platform:
            self.patrol_start_x = ground_platform.actor.left
            self.patrol_end_x = ground_platform.actor.right

    def update(self, dt):
        if self.behavior == 'patrol': 
            self.update_patrol(dt)

        elif self.behavior == 'random': 
            self.update_random(dt)

        self.update_animation(dt)

    def update_patrol(self, dt):
        if self.state == 'walking':
            self.initial_pos = (self.initial_pos[0] + self.speed * self.direction, self.initial_pos[1])
            self.frames = self.walk_frames_right if self.direction > 0 else self.walk_frames_left

            if self.initial_pos[0] >= self.patrol_end_x or self.initial_pos[0] <= self.patrol_start_x:
                self.state, self.idle_timer, self.direction = 'idling', 0, self.direction * -1
       
        elif self.state == 'idling':
            self.idle_timer += dt
            self.frames = self.idle_frames_right if self.direction < 0 else self.idle_frames_left
            
            if self.idle_timer > self.IDLE_DURATION:
                self.state, self.IDLE_DURATION = 'walking', random.uniform(1.0, 2.5)

    def update_random(self, dt):
        self.action_timer += dt
        if self.action_timer > self.action_duration:
            self.action_timer = 0

            if self.state == 'walking':
                self.state, self.action_duration = 'idling', random.uniform(1.0, 3.5)

            else:
                self.state, self.direction, self.action_duration = 'walking', random.choice([-1, 1]), random.uniform(2.0, 5.0)

        if self.state == 'walking':
            self.initial_pos = (self.initial_pos[0] + self.speed * self.direction, self.initial_pos[1])
            self.frames = self.walk_frames_right if self.direction > 0 else self.walk_frames_left

        else: 
            self.frames = self.idle_frames_right if self.direction > 0 else self.idle_frames_left

def generate_chunk():
    global farthest_x_generated, last_platform_pos, platforms, enemies

    for _ in range(random.randint(4, 6)):
        gap_x = random.randint(80, 160)
        max_jump_height = 150 
        gap_y = -random.randint(20, max_jump_height) if random.random() < 0.65 else random.randint(20, 80)
        new_x = farthest_x_generated + gap_x
        new_y = last_platform_pos[1] + gap_y
        new_y = max(150, min(HEIGHT - 80, new_y))

        weighted_platform_list = [
            PLATFORM_TYPES[0], PLATFORM_TYPES[0], PLATFORM_TYPES[0],
            PLATFORM_TYPES[5], PLATFORM_TYPES[5], PLATFORM_TYPES[5],
            PLATFORM_TYPES[1], PLATFORM_TYPES[2], PLATFORM_TYPES[3], PLATFORM_TYPES[4],
        ]

        platform_data = random.choice(weighted_platform_list)
        platform_image = platform_data['image']
        
        new_platform = AnimatedActor([platform_image], pos=(new_x, new_y), anchor=('left', 'top'))

        platforms.append(new_platform)
        
        platform_width_pixels = new_platform.actor.width
        
        if platform_image == 'platform_1':
            if random.random() < 0.5:
                enemies.append(Enemy(pos=(new_x + platform_width_pixels * 0.25, new_y), all_platforms=platforms, behavior='patrol'))
                enemies.append(Enemy(pos=(new_x + platform_width_pixels * 0.75, new_y), all_platforms=platforms, behavior='patrol'))

            else:
                enemy_x = new_x + (platform_width_pixels / 2)
                enemies.append(Enemy(pos=(enemy_x, new_y), all_platforms=platforms, behavior='patrol'))

        elif platform_image == 'platform':
            enemy_x = new_x + (platform_width_pixels / 2)
            enemies.append(Enemy(pos=(enemy_x, new_y), all_platforms=platforms, behavior='patrol'))
        
        last_platform_pos = (new_x, new_y)
        farthest_x_generated = new_x + platform_width_pixels

def setup_game():
    global player, enemies, platforms, scroll_x, farthest_x_generated, last_platform_pos, distance_traveled, final_score
    scroll_x, distance_traveled, final_score = 0, 0, 0
    platforms, enemies = [], []
    farthest_x_generated = WIDTH
    ground_y = HEIGHT - 40

    for x in range(-TILE_WIDTH, WIDTH + TILE_WIDTH, TILE_WIDTH):
        platforms.append(AnimatedActor(['ground_middle'], pos=(x, HEIGHT), anchor=('left', 'bottom')))

    last_platform_pos = (150, ground_y)
    player = Player(pos=(150, ground_y))

    if music_on: 
        music.play('background_music'), music.set_volume(0.4)

start_button = Rect((WIDTH/2 - 150, 250), (350, 50))
sound_button = Rect((WIDTH/2 - 150, 320), (350, 50))
exit_button = Rect((WIDTH/2 - 150, 390), (350, 50))

def draw_button(rect, text):
    color, text_color = ((50,50,50,230), (255,255,255)) if rect.collidepoint(mouse_pos) else ((30,30,30,190), (220,220,220))
    screen.draw.filled_rect(rect.inflate(4, 4), (10,10,10,220))
    screen.draw.filled_rect(rect, color)
    screen.draw.text(text, center=rect.center, fontsize=26, color=text_color, fontname=BUTTON_FONT_NAME, owidth=0.5, ocolor="black")

def draw_menu():
    screen.blit('backgrounds/menu_background', (0, 0))
    screen.draw.text(TITLE, center=(WIDTH/2, 100), fontsize=80, color="white", owidth=1.5, ocolor="black", fontname=TITLE_FONT_NAME)
    draw_button(start_button, "Iniciar Jogo")
    draw_button(sound_button, f"Música/Sons: {'LIGADO' if music_on else 'DESLIGADO'}")
    draw_button(exit_button, "Sair")

def draw_game():
    screen.fill((80, 140, 200))
    for obj in platforms + enemies:
        obj.actor.x = obj.initial_pos[0] + scroll_x
        obj.draw()

    player.draw()

def draw_game_over():
    screen.fill((80, 0, 0))
    screen.draw.text("FIM DE JOGO", center=(WIDTH/2, HEIGHT/2-80), fontsize=80, color="white", fontname=TITLE_FONT_NAME)
    screen.draw.text(f"Distância Percorrida: {final_score}m", center=(WIDTH/2, HEIGHT/2), fontsize=40, color="white", fontname=BUTTON_FONT_NAME)
    screen.draw.text("Pressione ENTER para voltar ao menu", center=(WIDTH/2, HEIGHT/2+80), fontsize=30, color="white", fontname=BUTTON_FONT_NAME)

def draw():
    if game_state == "menu": 
        draw_menu()

    elif game_state == "playing": 
        draw_game()

    else: 
        draw_game_over()

def update(dt):
    global game_state, scroll_x, final_score, distance_traveled

    if game_state == "playing":
        scroll_speed = player.update(dt, platforms)
        scroll_x += scroll_speed
        
        if player.actor.x - scroll_x > farthest_x_generated - WIDTH * 1.5:
            generate_chunk()

        for p in platforms:
            p.actor.x = p.initial_pos[0] + scroll_x
            p.hitbox.center = p.actor.center

        for e in enemies:
            e.update(dt)
            e.actor.x = e.initial_pos[0] + scroll_x
            e.hitbox.center = e.actor.center
            
        current_distance = player.actor.x - scroll_x

        if current_distance > distance_traveled: 
            distance_traveled = current_distance

        if player.hitbox.collidelist([e.hitbox for e in enemies]) != -1 or player.actor.top > HEIGHT:
            if music_on: 
                sounds.hit.play(); music.stop()

            final_score = int(distance_traveled / 10)
            game_state = "game_over"

def on_mouse_move(pos):
    global mouse_pos; mouse_pos = pos

def on_key_down(key):
    global game_state
    if game_state == "playing" and (key == keys.SPACE or key == keys.UP): 
        player.jump()

    elif game_state == "game_over" and key == keys.RETURN:
        game_state = "menu"

        if music_on: 
            music.play('background_music'); music.set_volume(0.4)

def on_mouse_down(pos):
    global game_state, music_on

    if game_state == "menu":
        if start_button.collidepoint(pos): 
            game_state = "playing"
            setup_game()

        elif sound_button.collidepoint(pos):
            music_on = not music_on

            if music_on: 
                music.play('background_music'); music.set_volume(0.4)

            else: 
                music.stop()

        elif exit_button.collidepoint(pos): 
            quit()

if music_on: 
    music.play('background_music'); music.set_volume(0.4)

pgzrun.go()