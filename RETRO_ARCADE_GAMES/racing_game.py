"""
=============================================================================
                  TURBO RUSH: HIGHWAY RACER (Python Edition)
=============================================================================
A full-featured, high-octane 2D arcade racing game built entirely in pure Python.
Features procedural graphics, dynamic synth audio, realistic traffic AI,
nitro boosts, collectible powerups, near-miss bonuses, and particle effects.
=============================================================================
"""

import sys
import os
import math
import random
import json
import pygame
import numpy as np

# ---------------------------------------------------------------------------
# INITIALIZATION & CONSTANTS
# ---------------------------------------------------------------------------
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    AUDIO_ENABLED = True
except Exception:
    AUDIO_ENABLED = False

WIDTH, HEIGHT = 900, 700
FPS = 60

# Road geometry
ROAD_WIDTH = 480
ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
LANE_CENTERS = [ROAD_LEFT + int((i + 0.5) * LANE_WIDTH) for i in range(LANE_COUNT)]

# Color Palette
COLOR_GRASS_1 = (38, 77, 43)
COLOR_GRASS_2 = (32, 66, 36)
COLOR_ROAD = (40, 44, 52)
COLOR_ROAD_SHOULDER = (70, 75, 85)
COLOR_CURB_WHITE = (235, 235, 235)
COLOR_CURB_RED = (210, 45, 45)
COLOR_LANE_MARK = (255, 255, 255)
COLOR_NEON_CYAN = (0, 240, 255)
COLOR_NEON_ORANGE = (255, 120, 20)
COLOR_GOLD = (255, 215, 0)
COLOR_GREEN = (46, 204, 113)
COLOR_DARK_OVERLAY = (15, 17, 23, 190)

SAVE_FILE = os.path.join(os.path.dirname(__file__), "turbo_rush_save.json")


# ---------------------------------------------------------------------------
# PROCEDURAL AUDIO SYNTHESIZER
# ---------------------------------------------------------------------------
class ProceduralAudio:
    """Generates authentic arcade sound effects using NumPy and Pygame mixer."""
    def __init__(self):
        self.muted = False
        self.engine_channel = None
        self.sounds = {}
        if not AUDIO_ENABLED:
            return

        try:
            self.sample_rate = 44100
            self.sounds['coin'] = self._make_coin_sound()
            self.sounds['nitro'] = self._make_nitro_sound()
            self.sounds['crash'] = self._make_crash_sound()
            self.sounds['repair'] = self._make_repair_sound()
            self.sounds['near_miss'] = self._make_near_miss_sound()
            self.sounds['skid'] = self._make_skid_sound()
            self.engine_sound = self._make_engine_sound(frequency=65)
            self.engine_channel = pygame.mixer.Channel(0)
            self.engine_channel.play(self.engine_sound, loops=-1)
            self.engine_channel.set_volume(0.25)
        except Exception as e:
            print(f"Sound initialization notice: {e}")

    def _make_coin_sound(self):
        duration = 0.22
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        half = len(t) // 2
        f1 = 987.77
        f2 = 1318.51
        w1 = np.sin(2 * np.pi * f1 * t[:half]) * np.linspace(1.0, 0.4, half)
        w2 = np.sin(2 * np.pi * f2 * t[half:]) * np.linspace(1.0, 0.0, len(t) - half)
        wave = np.concatenate((w1, w2)) * 0.4
        return self._array_to_sound(wave)

    def _make_nitro_sound(self):
        duration = 0.7
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        envelope = np.sin(np.pi * np.linspace(0, 1, len(t))) ** 1.5
        carrier = np.sin(2 * np.pi * 120 * t)
        wave = (noise * 0.6 + carrier * 0.4) * envelope * 0.35
        return self._array_to_sound(wave)

    def _make_crash_sound(self):
        duration = 0.8
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        decay = np.exp(-4.5 * t)
        rumble = np.sin(2 * np.pi * 50 * t) * decay
        wave = (noise * 0.7 + rumble * 0.5) * decay * 0.7
        return self._array_to_sound(wave)

    def _make_repair_sound(self):
        duration = 0.35
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        freqs = [523.25, 659.25, 783.99]
        wave = np.zeros_like(t)
        for f in freqs:
            wave += np.sin(2 * np.pi * f * t)
        wave = wave / len(freqs) * np.linspace(1.0, 0.0, len(t)) * 0.4
        return self._array_to_sound(wave)

    def _make_near_miss_sound(self):
        duration = 0.25
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        freq = np.linspace(400, 750, len(t))
        wave = np.sin(2 * np.pi * freq * t) * np.sin(np.pi * np.linspace(0, 1, len(t))) * 0.3
        return self._array_to_sound(wave)

    def _make_skid_sound(self):
        duration = 0.25
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        high_pitch = np.sin(2 * np.pi * 900 * t)
        wave = (noise * 0.7 + high_pitch * 0.3) * np.linspace(0.5, 0.0, len(t)) * 0.25
        return self._array_to_sound(wave)

    def _make_engine_sound(self, frequency=60):
        duration = 0.5
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t) + \
               0.25 * np.sin(2 * np.pi * (frequency * 2) * t) + \
               0.15 * np.sin(2 * np.pi * (frequency * 3) * t) + \
               0.10 * np.random.uniform(-0.3, 0.3, len(t))
        return self._array_to_sound(wave * 0.3)

    def _array_to_sound(self, wave):
        wave = np.clip(wave, -1.0, 1.0)
        audio_int16 = (wave * 32767).astype(np.int16)
        stereo = np.column_stack((audio_int16, audio_int16))
        return pygame.sndarray.make_sound(stereo)

    def play(self, sound_name):
        if self.muted or not AUDIO_ENABLED:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            snd.play()

    def update_engine(self, speed_ratio, is_nitro=False):
        if self.muted or not AUDIO_ENABLED or not self.engine_channel:
            return
        vol = 0.18 + 0.22 * speed_ratio
        if is_nitro:
            vol = min(0.45, vol + 0.1)
        self.engine_channel.set_volume(vol)

    def toggle_mute(self):
        self.muted = not self.muted
        if self.engine_channel:
            self.engine_channel.set_volume(0.0 if self.muted else 0.25)
        return self.muted


# ---------------------------------------------------------------------------
# PROCEDURAL GRAPHICS GENERATOR
# ---------------------------------------------------------------------------
class ProceduralVehicles:
    """Generates sharp, anti-aliased sports cars, trucks, and collectibles."""
    @staticmethod
    def create_car_surface(width, height, primary_color, secondary_color, style="sports"):
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        cx = width // 2

        # Car Shadow
        shadow_rect = pygame.Rect(3, 4, width - 6, height - 4)
        pygame.draw.ellipse(surf, (15, 18, 22, 120), shadow_rect)

        # Wheels (4 black rubber tires with rim highlights)
        wheel_w, wheel_h = 7, 16
        wheel_positions = [
            (3, 10), (width - 10, 10),              # Front wheels
            (3, height - 26), (width - 10, height - 26)  # Rear wheels
        ]
        for wx, wy in wheel_positions:
            pygame.draw.rect(surf, (20, 20, 20), (wx, wy, wheel_w, wheel_h), border_radius=2)
            pygame.draw.line(surf, (120, 120, 130), (wx + 3, wy + 2), (wx + 3, wy + wheel_h - 3), 2)

        # Chassis Body
        body_rect = pygame.Rect(7, 4, width - 14, height - 10)
        pygame.draw.rect(surf, primary_color, body_rect, border_radius=10)

        # Dual Racing Stripes
        stripe_color = secondary_color
        stripe_w = 3
        pygame.draw.rect(surf, stripe_color, (cx - 5, 4, stripe_w, height - 10))
        pygame.draw.rect(surf, stripe_color, (cx + 2, 4, stripe_w, height - 10))

        # Cockpit Windshield & Windows
        windshield_y = int(height * 0.26)
        windshield_h = int(height * 0.22)
        windshield_rect = pygame.Rect(11, windshield_y, width - 22, windshield_h)
        pygame.draw.rect(surf, (22, 28, 38), windshield_rect, border_radius=6)
        # Windshield glossy reflection line
        pygame.draw.line(surf, (180, 210, 255, 160), (14, windshield_y + 3), (width - 14, windshield_y + windshield_h - 4), 2)

        # Roof
        roof_rect = pygame.Rect(12, windshield_y + windshield_h - 2, width - 24, int(height * 0.20))
        pygame.draw.rect(surf, primary_color, roof_rect, border_radius=4)
        # Roof stripes
        pygame.draw.rect(surf, stripe_color, (cx - 5, roof_rect.y, stripe_w, roof_rect.height))
        pygame.draw.rect(surf, stripe_color, (cx + 2, roof_rect.y, stripe_w, roof_rect.height))

        # Rear Window
        rear_win_y = roof_rect.bottom
        rear_win_rect = pygame.Rect(12, rear_win_y, width - 24, int(height * 0.12))
        pygame.draw.rect(surf, (25, 30, 40), rear_win_rect, border_radius=4)

        # Headlights (Front)
        hl_w, hl_h = 7, 5
        pygame.draw.rect(surf, (255, 255, 220), (9, 6, hl_w, hl_h), border_radius=2)
        pygame.draw.rect(surf, (255, 255, 220), (width - 16, 6, hl_w, hl_h), border_radius=2)

        # Taillights (Rear)
        tl_w, tl_h = 7, 4
        pygame.draw.rect(surf, (240, 30, 30), (9, height - 10, tl_w, tl_h), border_radius=2)
        pygame.draw.rect(surf, (240, 30, 30), (width - 16, height - 10, tl_w, tl_h), border_radius=2)

        # Rear Spoiler
        spoiler_rect = pygame.Rect(5, height - 8, width - 10, 4)
        pygame.draw.rect(surf, (20, 20, 25), spoiler_rect, border_radius=2)

        return surf

    @staticmethod
    def create_truck_surface(width, height, color):
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        # Shadow
        pygame.draw.rect(surf, (15, 18, 22, 130), (2, 4, width - 4, height - 4), border_radius=4)

        # 6 Heavy Wheels
        for wy in [15, height // 2, height - 25]:
            pygame.draw.rect(surf, (25, 25, 25), (1, wy, 6, 16), border_radius=2)
            pygame.draw.rect(surf, (25, 25, 25), (width - 7, wy, 6, 16), border_radius=2)

        # Truck Cab
        cab_h = 35
        pygame.draw.rect(surf, color, (6, 4, width - 12, cab_h), border_radius=6)
        # Windshield
        pygame.draw.rect(surf, (20, 30, 42), (10, 10, width - 20, 14), border_radius=3)
        # Headlights
        pygame.draw.rect(surf, (255, 255, 220), (8, 5, 8, 4), border_radius=2)
        pygame.draw.rect(surf, (255, 255, 220), (width - 16, 5, 8, 4), border_radius=2)

        # Cargo Container
        trailer_rect = pygame.Rect(5, cab_h + 8, width - 10, height - cab_h - 14)
        pygame.draw.rect(surf, (220, 225, 230), trailer_rect, border_radius=4)
        pygame.draw.rect(surf, (160, 165, 170), trailer_rect, 2, border_radius=4)
        # Container rib lines
        for y in range(trailer_rect.y + 10, trailer_rect.bottom - 8, 14):
            pygame.draw.line(surf, (190, 195, 200), (trailer_rect.x + 3, y), (trailer_rect.right - 4, y), 2)

        # Rear lights
        pygame.draw.rect(surf, (240, 20, 20), (8, height - 8, 8, 4))
        pygame.draw.rect(surf, (240, 20, 20), (width - 16, height - 8, 8, 4))

        return surf

    @staticmethod
    def create_police_surface(width, height):
        surf = ProceduralVehicles.create_car_surface(width, height, (30, 30, 35), (240, 240, 245), style="police")
        pygame.draw.rect(surf, (245, 245, 250), (9, int(height * 0.38), width - 18, int(height * 0.22)))
        bar_w = 20
        bar_x = (width - bar_w) // 2
        bar_y = int(height * 0.40)
        pygame.draw.rect(surf, (30, 30, 30), (bar_x - 1, bar_y - 1, bar_w + 2, 7), border_radius=2)
        pygame.draw.rect(surf, (255, 30, 30), (bar_x, bar_y, bar_w // 2, 5))
        pygame.draw.rect(surf, (30, 120, 255), (bar_x + bar_w // 2, bar_y, bar_w // 2, 5))
        return surf


# ---------------------------------------------------------------------------
# PARTICLE & VISUAL EFFECTS SYSTEM
# ---------------------------------------------------------------------------
class Particle:
    def __init__(self, x, y, vx, vy, color, radius, decay, shape="circle"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.alpha = 255
        self.decay = decay
        self.shape = shape

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha = max(0, self.alpha - self.decay)
        self.radius = max(0.5, self.radius - 0.05)
        return self.alpha > 0

    def draw(self, surface):
        if self.radius <= 0 or self.alpha <= 0:
            return
        r, g, b = self.color[:3]
        col = (r, g, b, int(self.alpha))
        p_surf = pygame.Surface((int(self.radius * 2 + 2), int(self.radius * 2 + 2)), pygame.SRCALPHA)
        if self.shape == "circle":
            pygame.draw.circle(p_surf, col, (int(self.radius + 1), int(self.radius + 1)), int(self.radius))
        else:
            pygame.draw.rect(p_surf, col, (0, 0, int(self.radius * 2), int(self.radius * 2)))
        surface.blit(p_surf, (self.x - self.radius, self.y - self.radius))


class FloatingText:
    def __init__(self, text, x, y, color=(255, 230, 0), font_size=24, duration=45):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont("Impact, Arial Black, Trebuchet MS", font_size)
        self.lifetime = duration
        self.max_lifetime = duration

    def update(self):
        self.y -= 1.2
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        txt_surf = self.font.render(self.text, True, self.color)
        txt_surf.set_alpha(alpha)
        shadow = self.font.render(self.text, True, (0, 0, 0))
        shadow.set_alpha(int(alpha * 0.7))
        surface.blit(shadow, (self.x - txt_surf.get_width() // 2 + 2, self.y + 2))
        surface.blit(txt_surf, (self.x - txt_surf.get_width() // 2, self.y))


# ---------------------------------------------------------------------------
# ROAD & ENVIRONMENT
# ---------------------------------------------------------------------------
class RoadEnvironment:
    """Manages animated scrolling asphalt, lane marks, curbs, and roadside scenery."""
    def __init__(self):
        self.scroll_y = 0
        self.scenery_objects = []
        for y in range(-HEIGHT, HEIGHT * 2, 140):
            self.scenery_objects.append({'type': 'tree', 'side': 'left', 'x': random.randint(30, 170), 'y': y})
            self.scenery_objects.append({'type': 'tree', 'side': 'right', 'x': random.randint(WIDTH - 180, WIDTH - 40), 'y': y + 70})
            if random.random() < 0.6:
                self.scenery_objects.append({'type': 'lamp', 'side': 'left', 'x': ROAD_LEFT - 16, 'y': y + 30})
                self.scenery_objects.append({'type': 'lamp', 'side': 'right', 'x': ROAD_RIGHT + 16, 'y': y + 30})

    def update(self, speed_pixels):
        self.scroll_y = (self.scroll_y + speed_pixels) % 80
        for obj in self.scenery_objects:
            obj['y'] += speed_pixels
            if obj['y'] > HEIGHT + 100:
                obj['y'] -= (HEIGHT + 200)
                if obj['type'] == 'tree':
                    if obj['side'] == 'left':
                        obj['x'] = random.randint(30, 170)
                    else:
                        obj['x'] = random.randint(WIDTH - 180, WIDTH - 40)

    def draw(self, surface):
        surface.fill(COLOR_GRASS_1)
        grass_stripe_h = 60
        stripe_offset = int(self.scroll_y) % (grass_stripe_h * 2)
        for y in range(-grass_stripe_h * 2 + stripe_offset, HEIGHT + grass_stripe_h, grass_stripe_h * 2):
            pygame.draw.rect(surface, COLOR_GRASS_2, (0, y, ROAD_LEFT, grass_stripe_h))
            pygame.draw.rect(surface, COLOR_GRASS_2, (ROAD_RIGHT, y, WIDTH - ROAD_RIGHT, grass_stripe_h))

        pygame.draw.rect(surface, COLOR_ROAD_SHOULDER, (ROAD_LEFT - 12, 0, ROAD_WIDTH + 24, HEIGHT))
        pygame.draw.rect(surface, COLOR_ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

        curb_seg_h = 30
        curb_offset = int(self.scroll_y) % (curb_seg_h * 2)
        curb_w = 10
        for y in range(-curb_seg_h * 2 + curb_offset, HEIGHT + curb_seg_h, curb_seg_h * 2):
            pygame.draw.rect(surface, COLOR_CURB_RED, (ROAD_LEFT - curb_w, y, curb_w, curb_seg_h))
            pygame.draw.rect(surface, COLOR_CURB_WHITE, (ROAD_LEFT - curb_w, y + curb_seg_h, curb_w, curb_seg_h))
            pygame.draw.rect(surface, COLOR_CURB_RED, (ROAD_RIGHT, y, curb_w, curb_seg_h))
            pygame.draw.rect(surface, COLOR_CURB_WHITE, (ROAD_RIGHT, y + curb_seg_h, curb_w, curb_seg_h))

        dash_length = 35
        dash_gap = 25
        cycle = dash_length + dash_gap
        lane_offset = int(self.scroll_y) % cycle
        for lane_idx in range(1, LANE_COUNT):
            lane_x = ROAD_LEFT + lane_idx * LANE_WIDTH
            for y in range(-cycle + lane_offset, HEIGHT + cycle, cycle):
                pygame.draw.line(surface, COLOR_LANE_MARK, (lane_x, y), (lane_x, y + dash_length), 3)

        for obj in self.scenery_objects:
            if obj['type'] == 'tree':
                self._draw_tree(surface, obj['x'], obj['y'])
            elif obj['type'] == 'lamp':
                self._draw_lamp(surface, obj['x'], obj['y'], obj['side'])

    def _draw_tree(self, surface, x, y):
        pygame.draw.ellipse(surface, (20, 35, 20, 110), (x - 20, y - 6, 40, 20))
        pygame.draw.rect(surface, (82, 54, 34), (x - 4, y - 10, 8, 16))
        pygame.draw.circle(surface, (28, 90, 36), (x, y - 22), 22)
        pygame.draw.circle(surface, (38, 115, 48), (x - 6, y - 26), 16)
        pygame.draw.circle(surface, (48, 138, 58), (x + 5, y - 24), 14)

    def _draw_lamp(self, surface, x, y, side):
        pygame.draw.circle(surface, (140, 145, 155), (x, y), 4)
        arm_end_x = x + (18 if side == 'left' else -18)
        pygame.draw.line(surface, (100, 105, 115), (x, y), (arm_end_x, y - 6), 3)
        glow = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 245, 180, 70), (15, 15), 14)
        pygame.draw.circle(glow, (255, 255, 220, 200), (15, 15), 4)
        surface.blit(glow, (arm_end_x - 15, y - 21))


# ---------------------------------------------------------------------------
# PLAYER CAR CLASS
# ---------------------------------------------------------------------------
CAR_PRESETS = [
    {"name": "Inferno Red", "primary": (225, 35, 35), "secondary": (250, 250, 250)},
    {"name": "Neon Cyan", "primary": (0, 210, 245), "secondary": (20, 30, 40)},
    {"name": "Viper Lime", "primary": (46, 204, 80), "secondary": (245, 245, 245)},
    {"name": "Sunset Amber", "primary": (250, 150, 20), "secondary": (40, 40, 40)},
    {"name": "Phantom Violet", "primary": (155, 45, 230), "secondary": (0, 240, 255)},
]

class PlayerCar:
    def __init__(self, color_index=0):
        self.width = 46
        self.height = 84
        self.color_idx = color_index
        self.color_data = CAR_PRESETS[self.color_idx]
        self.surface = ProceduralVehicles.create_car_surface(
            self.width, self.height, self.color_data["primary"], self.color_data["secondary"]
        )
        self.reset()

    def reset(self):
        self.x = LANE_CENTERS[1] - self.width // 2
        self.y = HEIGHT - 160
        self.vx = 0
        self.speed_kmh = 90.0
        self.max_speed = 185.0
        self.min_speed = 40.0
        self.nitro_max_speed = 245.0
        self.accel = 0.55
        self.brake_decel = 1.1
        self.natural_decel = 0.25
        self.steer_speed = 5.8
        self.tilt_angle = 0.0

        self.health = 100.0
        self.nitro = 100.0
        self.nitro_active = False
        self.invulnerable_frames = 0

    def set_color(self, index):
        self.color_idx = index % len(CAR_PRESETS)
        self.color_data = CAR_PRESETS[self.color_idx]
        self.surface = ProceduralVehicles.create_car_surface(
            self.width, self.height, self.color_data["primary"], self.color_data["secondary"]
        )

    def update(self, keys, audio, particles):
        accelerating = keys[pygame.K_UP] or keys[pygame.K_w]
        braking = keys[pygame.K_DOWN] or keys[pygame.K_s]
        nitro_key = keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        self.nitro_active = False
        if nitro_key and self.nitro > 2 and accelerating:
            self.nitro_active = True
            self.nitro = max(0, self.nitro - 0.45)
            self.speed_kmh = min(self.nitro_max_speed, self.speed_kmh + self.accel * 2.2)
            particles.append(Particle(self.x + 13, self.y + self.height - 4, random.uniform(-0.5, 0.5), random.uniform(3, 7), (0, 210, 255), 4, 18))
            particles.append(Particle(self.x + self.width - 13, self.y + self.height - 4, random.uniform(-0.5, 0.5), random.uniform(3, 7), (0, 210, 255), 4, 18))
            particles.append(Particle(self.x + self.width // 2, self.y + self.height - 4, random.uniform(-0.8, 0.8), random.uniform(4, 9), (255, 140, 20), 5, 22))
        elif accelerating:
            target_max = self.max_speed
            if self.speed_kmh < target_max:
                self.speed_kmh += self.accel
        elif braking:
            self.speed_kmh = max(self.min_speed, self.speed_kmh - self.brake_decel)
            if self.speed_kmh > 70:
                audio.play('skid')
                particles.append(Particle(self.x + 9, self.y + self.height - 8, 0, 1.5, (30, 30, 30), 3, 14, shape="rect"))
                particles.append(Particle(self.x + self.width - 9, self.y + self.height - 8, 0, 1.5, (30, 30, 30), 3, 14, shape="rect"))
        else:
            if self.speed_kmh > 90:
                self.speed_kmh -= self.natural_decel
            elif self.speed_kmh < 90:
                self.speed_kmh += self.natural_decel * 0.5

        if not self.nitro_active and self.nitro < 100:
            self.nitro = min(100.0, self.nitro + 0.08)

        steering = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steering -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steering += 1

        self.vx = steering * self.steer_speed
        self.x += self.vx

        target_angle = -steering * 4.5
        self.tilt_angle += (target_angle - self.tilt_angle) * 0.2

        on_grass = (self.x < ROAD_LEFT or self.x + self.width > ROAD_RIGHT)
        if on_grass:
            self.speed_kmh = max(35.0, self.speed_kmh - 1.2)
            particles.append(Particle(self.x + (0 if self.x < ROAD_LEFT else self.width), self.y + self.height - 10, random.uniform(-2, 2), random.uniform(-1, 3), (90, 120, 50), 3, 16))

        self.x = max(10, min(WIDTH - self.width - 10, self.x))

        if self.invulnerable_frames > 0:
            self.invulnerable_frames -= 1

        speed_ratio = (self.speed_kmh - self.min_speed) / (self.nitro_max_speed - self.min_speed)
        audio.update_engine(speed_ratio, self.nitro_active)

    def draw(self, surface):
        if self.invulnerable_frames > 0 and (self.invulnerable_frames // 4) % 2 == 1:
            return

        beam_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        beam_color = (255, 255, 210, 35)
        pts_left = [(self.x + 12, self.y + 8), (self.x - 30, self.y - 180), (self.x + 30, self.y - 180)]
        pygame.draw.polygon(beam_surf, beam_color, pts_left)
        pts_right = [(self.x + self.width - 12, self.y + 8), (self.x + self.width - 30, self.y - 180), (self.x + self.width + 30, self.y - 180)]
        pygame.draw.polygon(beam_surf, beam_color, pts_right)
        surface.blit(beam_surf, (0, 0))

        if abs(self.tilt_angle) > 0.5:
            rotated = pygame.transform.rotate(self.surface, self.tilt_angle)
            new_rect = rotated.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            surface.blit(rotated, new_rect.topleft)
        else:
            surface.blit(self.surface, (self.x, self.y))

    def get_hitbox(self):
        return pygame.Rect(self.x + 4, self.y + 6, self.width - 8, self.height - 10)


# ---------------------------------------------------------------------------
# TRAFFIC VEHICLE CLASS
# ---------------------------------------------------------------------------
TRAFFIC_TYPES = [
    {"type": "sports", "width": 44, "height": 82, "speed": 125, "p_color": (30, 140, 230), "s_color": (255, 255, 255)},
    {"type": "sedan", "width": 44, "height": 80, "speed": 100, "p_color": (210, 180, 40), "s_color": (30, 30, 30)},
    {"type": "muscle", "width": 46, "height": 84, "speed": 115, "p_color": (220, 60, 40), "s_color": (250, 250, 250)},
    {"type": "police", "width": 46, "height": 84, "speed": 135, "p_color": (20, 20, 20), "s_color": (255, 255, 255)},
    {"type": "truck", "width": 50, "height": 130, "speed": 75, "p_color": (80, 90, 110), "s_color": (200, 200, 200)},
]

class TrafficCar:
    def __init__(self, lane_index, y_pos, vehicle_type_dict):
        self.lane_idx = lane_index
        self.data = vehicle_type_dict
        self.width = self.data["width"]
        self.height = self.data["height"]
        self.speed_kmh = self.data["speed"] + random.uniform(-8, 8)
        self.x = LANE_CENTERS[self.lane_idx] - self.width // 2
        self.y = y_pos
        self.target_x = self.x
        self.is_changing_lane = False
        self.lane_change_speed = 2.2
        self.near_missed = False
        self.siren_tick = random.randint(0, 30)

        if self.data["type"] == "truck":
            self.surface = ProceduralVehicles.create_truck_surface(self.width, self.height, self.data["p_color"])
        elif self.data["type"] == "police":
            self.surface = ProceduralVehicles.create_police_surface(self.width, self.height)
        else:
            self.surface = ProceduralVehicles.create_car_surface(
                self.width, self.height, self.data["p_color"], self.data["s_color"], style=self.data["type"]
            )

    def update(self, player_speed_kmh, all_traffic):
        rel_speed_kmh = player_speed_kmh - self.speed_kmh
        pixel_dy = (rel_speed_kmh / 100.0) * 14.0
        self.y += pixel_dy

        if not self.is_changing_lane and random.random() < 0.004:
            possible_lanes = []
            if self.lane_idx > 0:
                possible_lanes.append(self.lane_idx - 1)
            if self.lane_idx < LANE_COUNT - 1:
                possible_lanes.append(self.lane_idx + 1)
            if possible_lanes:
                new_lane = random.choice(possible_lanes)
                target_center = LANE_CENTERS[new_lane]
                is_clear = True
                for other in all_traffic:
                    if other != self and abs(other.y - self.y) < 140:
                        if abs(other.x - (target_center - other.width // 2)) < 60:
                            is_clear = False
                            break
                if is_clear:
                    self.lane_idx = new_lane
                    self.target_x = LANE_CENTERS[self.lane_idx] - self.width // 2
                    self.is_changing_lane = True

        if self.is_changing_lane:
            if abs(self.x - self.target_x) <= self.lane_change_speed:
                self.x = self.target_x
                self.is_changing_lane = False
            else:
                self.x += self.lane_change_speed if self.target_x > self.x else -self.lane_change_speed

        self.siren_tick += 1

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))

        if self.data["type"] == "police":
            bar_w = 18
            bx = self.x + (self.width - bar_w) // 2
            by = self.y + int(self.height * 0.40)
            if (self.siren_tick // 8) % 2 == 0:
                glow = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.circle(glow, (255, 30, 30, 160), (12, 12), 10)
                surface.blit(glow, (bx - 8, by - 8))
            else:
                glow = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.circle(glow, (30, 120, 255, 160), (12, 12), 10)
                surface.blit(glow, (bx + bar_w - 12, by - 8))

        if self.is_changing_lane and (self.siren_tick // 6) % 2 == 0:
            blinker_x = self.x + (self.width - 6 if self.target_x > self.x else 2)
            pygame.draw.circle(surface, (255, 180, 0), (int(blinker_x), int(self.y + self.height - 10)), 4)

    def get_hitbox(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)


# ---------------------------------------------------------------------------
# COLLECTIBLES (Coins, Nitro, Repair)
# ---------------------------------------------------------------------------
class Collectible:
    def __init__(self, item_type, x, y):
        self.type = item_type
        self.x = x
        self.y = y
        self.radius = 16
        self.anim_tick = random.randint(0, 100)

    def update(self, player_speed_kmh):
        dy = (player_speed_kmh / 100.0) * 14.0
        self.y += dy
        self.anim_tick += 1

    def draw(self, surface):
        self.anim_tick += 1
        cx, cy = int(self.x), int(self.y)

        if self.type == 'coin':
            scale_x = abs(math.cos(self.anim_tick * 0.08))
            coin_w = max(4, int(26 * scale_x))
            coin_rect = pygame.Rect(cx - coin_w // 2, cy - 13, coin_w, 26)
            pygame.draw.ellipse(surface, (180, 140, 10), coin_rect.inflate(2, 2))
            pygame.draw.ellipse(surface, COLOR_GOLD, coin_rect)
            if coin_w > 12:
                pygame.draw.ellipse(surface, (255, 245, 160), (cx - coin_w // 4, cy - 8, coin_w // 2, 16))

        elif self.type == 'nitro':
            glow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow, (0, 220, 255, 80 + int(30 * math.sin(self.anim_tick * 0.15))), (20, 20), 18)
            surface.blit(glow, (cx - 20, cy - 20))
            pygame.draw.rect(surface, (0, 170, 230), (cx - 8, cy - 12, 16, 24), border_radius=4)
            pygame.draw.rect(surface, (240, 250, 255), (cx - 5, cy - 15, 10, 4), border_radius=2)
            font = pygame.font.SysFont("Arial", 9, bold=True)
            txt = font.render("N2O", True, (255, 255, 255))
            surface.blit(txt, (cx - txt.get_width() // 2, cy - 5))

        elif self.type == 'repair':
            glow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow, (46, 204, 113, 90 + int(30 * math.sin(self.anim_tick * 0.12))), (20, 20), 18)
            surface.blit(glow, (cx - 20, cy - 20))
            pygame.draw.rect(surface, (255, 255, 255), (cx - 4, cy - 12, 8, 24), border_radius=2)
            pygame.draw.rect(surface, (255, 255, 255), (cx - 12, cy - 4, 24, 8), border_radius=2)
            pygame.draw.rect(surface, (46, 204, 113), (cx - 2, cy - 10, 4, 20))
            pygame.draw.rect(surface, (46, 204, 113), (cx - 10, cy - 2, 20, 4))

    def get_hitbox(self):
        return pygame.Rect(self.x - 14, self.y - 14, 28, 28)


# ---------------------------------------------------------------------------
# MAIN GAME CONTROLLER
# ---------------------------------------------------------------------------
class TurboRushGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TURBO RUSH: Highway Racer")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_huge = pygame.font.SysFont("Impact, Arial Black", 68)
        self.font_large = pygame.font.SysFont("Impact, Arial Black", 38)
        self.font_medium = pygame.font.SysFont("Trebuchet MS, Arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("Trebuchet MS, Arial", 18, bold=True)
        self.font_digital = pygame.font.SysFont("Consolas, Courier", 32, bold=True)

        self.audio = ProceduralAudio()
        self.road = RoadEnvironment()

        self.high_score = 0
        self.high_distance = 0
        self.load_save_data()

        self.state = 'MENU'
        self.player = PlayerCar(color_index=0)
        self.traffic = []
        self.collectibles = []
        self.particles = []
        self.floating_texts = []
        self.speed_lines = []

        self.score = 0
        self.distance_m = 0.0
        self.coins_collected = 0
        self.near_misses = 0
        self.combo_multiplier = 1.0
        self.combo_timer = 0
        self.screen_shake = 0
        self.spawn_timer = 0

    def load_save_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.high_distance = data.get("high_distance", 0)
            except Exception:
                pass

    def save_data(self):
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump({
                    "high_score": max(self.high_score, int(self.score)),
                    "high_distance": max(self.high_distance, int(self.distance_m))
                }, f)
        except Exception:
            pass

    def start_new_game(self):
        self.player.reset()
        self.traffic.clear()
        self.collectibles.clear()
        self.particles.clear()
        self.floating_texts.clear()
        self.speed_lines.clear()

        self.score = 0
        self.distance_m = 0.0
        self.coins_collected = 0
        self.near_misses = 0
        self.combo_multiplier = 1.0
        self.combo_timer = 0
        self.screen_shake = 0
        self.spawn_timer = 0

        for i in range(4):
            lane = i % LANE_COUNT
            y_pos = -150 - (i * 220)
            vtype = random.choice(TRAFFIC_TYPES)
            self.traffic.append(TrafficCar(lane, y_pos, vtype))

        self.state = 'PLAYING'

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.audio.toggle_mute()

                    if self.state == 'MENU':
                        if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                            self.start_new_game()
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            self.player.set_color(self.player.color_idx - 1)
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            self.player.set_color(self.player.color_idx + 1)

                    elif self.state == 'PLAYING':
                        if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                            self.state = 'PAUSED'

                    elif self.state == 'PAUSED':
                        if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                            self.state = 'PLAYING'
                        elif event.key == pygame.K_r:
                            self.start_new_game()
                        elif event.key == pygame.K_q:
                            self.state = 'MENU'

                    elif self.state == 'GAMEOVER':
                        if event.key in [pygame.K_r, pygame.K_SPACE]:
                            self.start_new_game()
                        elif event.key in [pygame.K_m, pygame.K_ESCAPE]:
                            self.state = 'MENU'

            if self.state == 'MENU':
                self.update_menu()
                self.draw_menu()
            elif self.state == 'PLAYING':
                self.update_playing()
                self.draw_playing()
            elif self.state == 'PAUSED':
                self.draw_playing()
                self.draw_paused_overlay()
            elif self.state == 'GAMEOVER':
                self.update_gameover()
                self.draw_playing()
                self.draw_gameover_overlay()

            pygame.display.flip()

        self.save_data()
        pygame.quit()
        sys.exit()

    def update_playing(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.audio, self.particles)

        speed_mps = (self.player.speed_kmh * 1000.0) / 3600.0
        dist_frame = speed_mps / FPS
        self.distance_m += dist_frame
        self.score += (dist_frame * 1.5 * self.combo_multiplier)

        if self.combo_multiplier > 1.0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_multiplier = 1.0

        pixel_speed = (self.player.speed_kmh / 100.0) * 14.0
        self.road.update(pixel_speed)

        if self.player.speed_kmh > 175:
            if random.random() < 0.6:
                line_x = random.randint(ROAD_LEFT, ROAD_RIGHT)
                line_h = random.randint(40, 110)
                self.speed_lines.append([line_x, -line_h, line_h, random.randint(18, 30)])

        for line in self.speed_lines[:]:
            line[1] += line[3] + pixel_speed
            if line[1] > HEIGHT:
                self.speed_lines.remove(line)

        self.spawn_timer += 1
        spawn_rate = max(38, int(90 - (self.distance_m / 150)))
        if self.spawn_timer >= spawn_rate:
            self.spawn_timer = 0
            available_lanes = [l for l in range(LANE_COUNT)]
            for car in self.traffic:
                if car.y < 80 and car.lane_idx in available_lanes:
                    available_lanes.remove(car.lane_idx)
            if available_lanes:
                chosen_lane = random.choice(available_lanes)
                vtype = random.choice(TRAFFIC_TYPES)
                self.traffic.append(TrafficCar(chosen_lane, -140, vtype))

        if random.random() < 0.014 and len(self.collectibles) < 4:
            c_type = random.choices(['coin', 'nitro', 'repair'], weights=[0.65, 0.20, 0.15])[0]
            lane_c = random.choice(LANE_CENTERS)
            self.collectibles.append(Collectible(c_type, lane_c, -60))

        player_hitbox = self.player.get_hitbox()
        for car in self.traffic[:]:
            car.update(self.player.speed_kmh, self.traffic)

            if not car.near_missed and self.player.speed_kmh > 120:
                y_overlap = (car.y < self.player.y + self.player.height and car.y + car.height > self.player.y)
                dx = abs((self.player.x + self.player.width / 2) - (car.x + car.width / 2))
                if y_overlap and dx < (self.player.width / 2 + car.width / 2 + 26):
                    car.near_missed = True
                    self.near_misses += 1
                    bonus = int(250 * self.combo_multiplier)
                    self.score += bonus
                    self.combo_multiplier = min(4.0, self.combo_multiplier + 0.5)
                    self.combo_timer = 180
                    self.audio.play('near_miss')
                    self.floating_texts.append(FloatingText(f"NEAR MISS! +{bonus}", self.player.x + self.player.width // 2, self.player.y - 15, COLOR_NEON_CYAN))

            if self.player.invulnerable_frames <= 0:
                car_hitbox = car.get_hitbox()
                if player_hitbox.colliderect(car_hitbox):
                    self.screen_shake = 16
                    self.audio.play('crash')
                    damage = 25.0 if self.player.speed_kmh < 130 else 50.0
                    self.player.health -= damage
                    self.player.speed_kmh = max(40.0, self.player.speed_kmh * 0.45)
                    self.player.invulnerable_frames = 45
                    self.combo_multiplier = 1.0

                    cx = (self.player.x + car.x) / 2
                    cy = (self.player.y + car.y) / 2
                    for _ in range(25):
                        self.particles.append(Particle(cx, cy, random.uniform(-6, 6), random.uniform(-6, 6), (255, random.randint(100, 240), 20), random.randint(3, 7), 16))
                    for _ in range(15):
                        self.particles.append(Particle(cx, cy, random.uniform(-3, 3), random.uniform(-3, 3), (80, 80, 90), random.randint(5, 12), 10))

                    if self.player.health <= 0:
                        self.trigger_game_over()
                        return

            if car.y > HEIGHT + 250 or car.y < -500:
                self.traffic.remove(car)

        for item in self.collectibles[:]:
            item.update(self.player.speed_kmh)
            if player_hitbox.colliderect(item.get_hitbox()):
                if item.type == 'coin':
                    self.coins_collected += 1
                    self.score += int(150 * self.combo_multiplier)
                    self.audio.play('coin')
                    self.floating_texts.append(FloatingText("+150 COIN", item.x, item.y, COLOR_GOLD))
                elif item.type == 'nitro':
                    self.player.nitro = min(100.0, self.player.nitro + 45.0)
                    self.audio.play('repair')
                    self.floating_texts.append(FloatingText("NITRO BOOST!", item.x, item.y, COLOR_NEON_CYAN))
                elif item.type == 'repair':
                    self.player.health = min(100.0, self.player.health + 35.0)
                    self.audio.play('repair')
                    self.floating_texts.append(FloatingText("HEALTH REPAIRED!", item.x, item.y, COLOR_GREEN))

                for _ in range(12):
                    self.particles.append(Particle(item.x, item.y, random.uniform(-3, 3), random.uniform(-3, 3), (255, 255, 100), 3, 18))
                self.collectibles.remove(item)
            elif item.y > HEIGHT + 80:
                self.collectibles.remove(item)

        self.particles = [p for p in self.particles if p.update()]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

        if self.screen_shake > 0:
            self.screen_shake -= 1

    def trigger_game_over(self):
        self.state = 'GAMEOVER'
        self.audio.play('crash')
        if self.score > self.high_score:
            self.high_score = int(self.score)
        if self.distance_m > self.high_distance:
            self.high_distance = int(self.distance_m)
        self.save_data()

    def update_gameover(self):
        self.particles = [p for p in self.particles if p.update()]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

    def draw_playing(self):
        shake_x, shake_y = 0, 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)

        render_surf = pygame.Surface((WIDTH, HEIGHT))

        self.road.draw(render_surf)

        for item in self.collectibles:
            item.draw(render_surf)

        for car in self.traffic:
            car.draw(render_surf)

        self.player.draw(render_surf)

        for line in self.speed_lines:
            pygame.draw.line(render_surf, (240, 245, 255, 150), (line[0], line[1]), (line[0], line[1] + line[2]), 2)

        for p in self.particles:
            p.draw(render_surf)

        for ft in self.floating_texts:
            ft.draw(render_surf)

        self.draw_hud(render_surf)
        self.screen.blit(render_surf, (shake_x, shake_y))

    def draw_hud(self, surface):
        top_bar = pygame.Surface((WIDTH, 56), pygame.SRCALPHA)
        pygame.draw.rect(top_bar, (15, 18, 26, 210), (0, 0, WIDTH, 56))
        pygame.draw.line(top_bar, (45, 55, 75), (0, 55), (WIDTH, 55), 2)
        surface.blit(top_bar, (0, 0))

        score_txt = self.font_digital.render(f"{int(self.score):06d}", True, (255, 255, 255))
        lbl_score = self.font_small.render("SCORE", True, (150, 160, 180))
        surface.blit(lbl_score, (24, 6))
        surface.blit(score_txt, (24, 22))

        if self.combo_multiplier > 1.0:
            combo_surf = self.font_medium.render(f"x{self.combo_multiplier:.1f}", True, COLOR_NEON_CYAN)
            surface.blit(combo_surf, (150, 24))

        dist_km = self.distance_m / 1000.0
        dist_str = f"{dist_km:.2f} KM" if dist_km >= 1.0 else f"{int(self.distance_m)} M"
        dist_surf = self.font_digital.render(dist_str, True, COLOR_GOLD)
        lbl_dist = self.font_small.render("DISTANCE", True, (150, 160, 180))
        surface.blit(lbl_dist, (WIDTH // 2 - lbl_dist.get_width() // 2, 6))
        surface.blit(dist_surf, (WIDTH // 2 - dist_surf.get_width() // 2, 22))

        coin_txt = self.font_digital.render(f"{self.coins_collected}", True, COLOR_GOLD)
        lbl_coin = self.font_small.render("COINS", True, (150, 160, 180))
        surface.blit(lbl_coin, (WIDTH - 180, 6))
        surface.blit(coin_txt, (WIDTH - 180, 22))

        nm_txt = self.font_digital.render(f"{self.near_misses}", True, COLOR_NEON_CYAN)
        lbl_nm = self.font_small.render("NEAR MISS", True, (150, 160, 180))
        surface.blit(lbl_nm, (WIDTH - 95, 6))
        surface.blit(nm_txt, (WIDTH - 95, 22))

        hb_x, hb_y, hb_w, hb_h = 24, HEIGHT - 55, 180, 20
        pygame.draw.rect(surface, (25, 30, 40), (hb_x - 2, hb_y - 2, hb_w + 4, hb_h + 4), border_radius=4)
        health_fill = max(0, int((self.player.health / 100.0) * hb_w))
        h_color = COLOR_GREEN if self.player.health > 50 else (COLOR_NEON_ORANGE if self.player.health > 25 else (235, 40, 40))
        pygame.draw.rect(surface, h_color, (hb_x, hb_y, health_fill, hb_h), border_radius=3)
        h_label = self.font_small.render(f"HEALTH: {int(self.player.health)}%", True, (255, 255, 255))
        surface.blit(h_label, (hb_x, hb_y - 20))

        gauge_x = WIDTH - 220
        gauge_y = HEIGHT - 110

        bp_rect = pygame.Rect(gauge_x, gauge_y, 195, 95)
        gauge_bg = pygame.Surface((bp_rect.width, bp_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(gauge_bg, (16, 20, 28, 220), (0, 0, bp_rect.width, bp_rect.height), border_radius=10)
        pygame.draw.rect(gauge_bg, (40, 50, 65), (0, 0, bp_rect.width, bp_rect.height), 2, border_radius=10)
        surface.blit(gauge_bg, bp_rect.topleft)

        spd_num = self.font_huge.render(f"{int(self.player.speed_kmh)}", True, (255, 255, 255) if not self.player.nitro_active else COLOR_NEON_CYAN)
        kmh_lbl = self.font_small.render("KM/H", True, (160, 175, 195))
        surface.blit(spd_num, (gauge_x + 18, gauge_y + 6))
        surface.blit(kmh_lbl, (gauge_x + 130, gauge_y + 24))

        nb_x, nb_y, nb_w, nb_h = gauge_x + 18, gauge_y + 68, 160, 14
        pygame.draw.rect(surface, (30, 35, 45), (nb_x, nb_y, nb_w, nb_h), border_radius=3)
        nitro_fill = max(0, int((self.player.nitro / 100.0) * nb_w))
        n_color = COLOR_NEON_CYAN if not self.player.nitro_active else COLOR_NEON_ORANGE
        pygame.draw.rect(surface, n_color, (nb_x, nb_y, nitro_fill, nb_h), border_radius=3)
        nitro_lbl = pygame.font.SysFont("Arial", 11, bold=True).render("NITRO (SPACE / SHIFT)", True, (200, 220, 240))
        surface.blit(nitro_lbl, (nb_x, nb_y - 14))

    def draw_paused_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 22, 190))
        self.screen.blit(overlay, (0, 0))

        title = self.font_huge.render("GAME PAUSED", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

        info1 = self.font_medium.render("PRESS ESC TO RESUME", True, COLOR_NEON_CYAN)
        info2 = self.font_medium.render("PRESS R TO RESTART", True, COLOR_GOLD)
        info3 = self.font_medium.render("PRESS Q FOR MAIN MENU", True, (200, 205, 215))

        self.screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 + 0))
        self.screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 40))
        self.screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT // 2 + 80))

    def draw_gameover_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((25, 8, 8, 205))
        self.screen.blit(overlay, (0, 0))

        card_w, card_h = 520, 420
        cx = (WIDTH - card_w) // 2
        cy = (HEIGHT - card_h) // 2 - 20
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (20, 24, 32, 240), (0, 0, card_w, card_h), border_radius=14)
        pygame.draw.rect(card_surf, (220, 50, 50), (0, 0, card_w, card_h), 3, border_radius=14)
        self.screen.blit(card_surf, (cx, cy))

        title = self.font_huge.render("TOTAL WRECK!", True, (245, 50, 50))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, cy + 24))

        stats = [
            ("FINAL SCORE", f"{int(self.score):,}", COLOR_GOLD),
            ("DISTANCE", f"{self.distance_m / 1000.0:.2f} KM", (255, 255, 255)),
            ("COINS EARNED", f"{self.coins_collected}", COLOR_GOLD),
            ("NEAR MISSES", f"{self.near_misses}", COLOR_NEON_CYAN),
            ("HIGH SCORE", f"{self.high_score:,}", (180, 255, 180)),
        ]

        stat_y = cy + 115
        for lbl, val, col in stats:
            l_surf = self.font_medium.render(lbl, True, (160, 170, 190))
            v_surf = self.font_medium.render(val, True, col)
            self.screen.blit(l_surf, (cx + 50, stat_y))
            self.screen.blit(v_surf, (cx + card_w - 50 - v_surf.get_width(), stat_y))
            stat_y += 38

        prompt = self.font_medium.render("PRESS R TO RACE AGAIN   |   M FOR MENU", True, (255, 255, 255))
        self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, cy + card_h - 50))

    def update_menu(self):
        self.road.update(6.0)

    def draw_menu(self):
        self.road.draw(self.screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((12, 16, 24, 185))
        self.screen.blit(overlay, (0, 0))

        title = self.font_huge.render("TURBO RUSH", True, COLOR_NEON_CYAN)
        subtitle = self.font_large.render("HIGHWAY RACER", True, COLOR_GOLD)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 140))

        showcase_y = 230
        box_w, box_h = 320, 180
        bx = (WIDTH - box_w) // 2
        pygame.draw.rect(self.screen, (22, 28, 38, 220), (bx, showcase_y, box_w, box_h), border_radius=12)
        pygame.draw.rect(self.screen, (50, 60, 80), (bx, showcase_y, box_w, box_h), 2, border_radius=12)

        car_surf = self.player.surface
        scaled_car = pygame.transform.scale(car_surf, (int(self.player.width * 1.5), int(self.player.height * 1.5)))
        self.screen.blit(scaled_car, (WIDTH // 2 - scaled_car.get_width() // 2, showcase_y + 20))

        preset_name = self.player.color_data["name"]
        name_surf = self.font_medium.render(preset_name, True, (255, 255, 255))
        arrows_surf = self.font_medium.render("<  (A / D to change)  >", True, (140, 155, 175))
        self.screen.blit(name_surf, (WIDTH // 2 - name_surf.get_width() // 2, showcase_y + box_h - 45))
        self.screen.blit(arrows_surf, (WIDTH // 2 - arrows_surf.get_width() // 2, showcase_y + box_h - 22))

        inst_y = 440
        inst_lines = [
            ("CONTROLS:", COLOR_NEON_CYAN),
            ("W / UP ARROW  : Accelerate", (230, 235, 245)),
            ("S / DOWN ARROW: Brake & Slow Down", (230, 235, 245)),
            ("A / D or ARROWS: Steer Left & Right", (230, 235, 245)),
            ("SPACE / SHIFT : NITRO BOOST", COLOR_NEON_ORANGE),
            ("M : Toggle Sound Mute  |  ESC : Pause Game", (170, 180, 195)),
        ]
        curr_y = inst_y
        for text, color in inst_lines:
            line_surf = self.font_small.render(text, True, color)
            self.screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, curr_y))
            curr_y += 24

        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
        start_col = (int(255 * pulse), 255, int(150 + 105 * pulse))
        start_txt = self.font_large.render("PRESS SPACE OR ENTER TO RACE!", True, start_col)
        self.screen.blit(start_txt, (WIDTH // 2 - start_txt.get_width() // 2, 605))

        if self.high_score > 0:
            rec_surf = self.font_small.render(f"BEST SCORE: {self.high_score:,}  |  BEST DISTANCE: {self.high_distance / 1000.0:.2f} KM", True, COLOR_GOLD)
            self.screen.blit(rec_surf, (WIDTH // 2 - rec_surf.get_width() // 2, 660))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    game = TurboRushGame()
    game.run()
