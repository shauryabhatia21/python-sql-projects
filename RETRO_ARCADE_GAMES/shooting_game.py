"""
=============================================================================
               CYBER NOVA: GALAXY STRIKER (Python Edition)
=============================================================================
An advanced, action-packed 2D sci-fi space shooting game in pure Python.
Features multi-tier weapon upgrades, homing missiles, fracturing asteroids,
intelligent alien formations, an epic Mothership Dreadnought boss battle,
screen shake, dynamic starfield parallax, and procedural sound synthesis.
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
# INITIALIZATION & DISPLAY CONFIG
# ---------------------------------------------------------------------------
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    AUDIO_ENABLED = True
except Exception:
    AUDIO_ENABLED = False

WIDTH, HEIGHT = 850, 750
FPS = 60

# Palette
COLOR_BG = (8, 10, 18)
COLOR_NEON_CYAN = (0, 240, 255)
COLOR_NEON_BLUE = (30, 140, 255)
COLOR_NEON_RED = (255, 45, 75)
COLOR_NEON_ORANGE = (255, 140, 20)
COLOR_NEON_PURPLE = (175, 55, 255)
COLOR_NEON_GREEN = (46, 230, 113)
COLOR_GOLD = (255, 215, 20)

SAVE_FILE = os.path.join(os.path.dirname(__file__), "galaxy_striker_save.json")
ASSETS_DIR = os.path.dirname(__file__)


# ---------------------------------------------------------------------------
# SOUND & AUDIO MANAGER (Hybrid: Local WAVs + NumPy Synth)
# ---------------------------------------------------------------------------
class AudioManager:
    """Combines user audio files with procedural NumPy synthesized SFX."""
    def __init__(self):
        self.muted = False
        self.sounds = {}
        if not AUDIO_ENABLED:
            return

        self.sample_rate = 44100
        # 1. Try loading local WAV assets
        self._load_local_or_synth('laser', 'laser.wav', self._synth_laser)
        self._load_local_or_synth('explosion', 'explosion.wav', self._synth_explosion)
        # 2. Synthesize additional rich arcade effects
        self.sounds['missile'] = self._synth_missile()
        self.sounds['emp'] = self._synth_emp()
        self.sounds['powerup'] = self._synth_powerup()
        self.sounds['shield_hit'] = self._synth_shield_hit()
        self.sounds['boss_alarm'] = self._synth_boss_alarm()

        # Optional background music
        bg_music = os.path.join(ASSETS_DIR, 'background.wav')
        if os.path.exists(bg_music):
            try:
                pygame.mixer.music.load(bg_music)
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(-1)
            except Exception:
                pass

    def _load_local_or_synth(self, name, filename, synth_fn):
        filepath = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(filepath):
            try:
                snd = pygame.mixer.Sound(filepath)
                snd.set_volume(0.35)
                self.sounds[name] = snd
                return
            except Exception:
                pass
        self.sounds[name] = synth_fn()

    def _array_to_sound(self, wave):
        wave = np.clip(wave, -1.0, 1.0)
        audio_int16 = (wave * 32767).astype(np.int16)
        stereo = np.column_stack((audio_int16, audio_int16))
        snd = pygame.sndarray.make_sound(stereo)
        snd.set_volume(0.35)
        return snd

    def _synth_laser(self):
        dur = 0.12
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        freq = np.linspace(950, 220, len(t))
        wave = np.sin(2 * np.pi * freq * t) * np.linspace(0.6, 0.0, len(t))
        return self._array_to_sound(wave)

    def _synth_explosion(self):
        dur = 0.5
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        noise = np.random.uniform(-1, 1, len(t))
        env = np.exp(-5.0 * t)
        rumble = np.sin(2 * np.pi * 60 * t) * env
        wave = (noise * 0.7 + rumble * 0.5) * env * 0.7
        return self._array_to_sound(wave)

    def _synth_missile(self):
        dur = 0.28
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        freq = np.linspace(250, 700, len(t))
        noise = np.random.uniform(-0.3, 0.3, len(t))
        wave = (np.sin(2 * np.pi * freq * t) + noise) * np.linspace(0.4, 0.0, len(t))
        return self._array_to_sound(wave)

    def _synth_emp(self):
        dur = 0.85
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        freq = np.linspace(700, 70, len(t))
        wave = np.sin(2 * np.pi * freq * t) * np.linspace(0.8, 0.0, len(t))
        return self._array_to_sound(wave)

    def _synth_powerup(self):
        dur = 0.35
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        chords = [523.25, 659.25, 783.99, 1046.50]  # C major arpeggio
        seg = len(t) // len(chords)
        wave = np.zeros_like(t)
        for i, f in enumerate(chords):
            idx1 = i * seg
            idx2 = len(t) if i == len(chords) - 1 else (i + 1) * seg
            sub_t = t[idx1:idx2]
            wave[idx1:idx2] = np.sin(2 * np.pi * f * sub_t) * np.linspace(0.6, 0.2, len(sub_t))
        return self._array_to_sound(wave)

    def _synth_shield_hit(self):
        dur = 0.15
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        wave = np.sin(2 * np.pi * 420 * t) * np.linspace(0.5, 0.0, len(t))
        return self._array_to_sound(wave)

    def _synth_boss_alarm(self):
        dur = 0.6
        t = np.linspace(0, dur, int(self.sample_rate * dur), False)
        freq = 350 + 200 * np.sin(2 * np.pi * 5 * t)
        wave = np.sin(2 * np.pi * freq * t) * 0.5
        return self._array_to_sound(wave)

    def play(self, sound_name):
        if self.muted or not AUDIO_ENABLED:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            snd.play()

    def toggle_mute(self):
        self.muted = not self.muted
        if pygame.mixer.get_init():
            if self.muted:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()
        return self.muted


# ---------------------------------------------------------------------------
# ASSET LOADER WITH PROCEDURAL FALLBACKS
# ---------------------------------------------------------------------------
class AssetManager:
    """Loads existing PNG images or procedurally generates high-tech sprites."""
    @staticmethod
    def get_player_sprite(w=56, h=64):
        p_file = os.path.join(ASSETS_DIR, 'player.png')
        if os.path.exists(p_file):
            try:
                img = pygame.image.load(p_file).convert_alpha()
                return pygame.transform.smoothscale(img, (w, h))
            except Exception:
                pass

        # Procedural Fighter Jet / Spaceship
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # Main fuselage
        pts = [(w // 2, 2), (w - 8, h - 14), (w // 2, h - 8), (8, h - 14)]
        pygame.draw.polygon(surf, (30, 160, 255), pts)
        # Outer delta wings
        wings = [(w // 2, 16), (w - 2, h - 8), (w // 2 + 10, h - 16), (w // 2, h - 4),
                 (w // 2 - 10, h - 16), (2, h - 8)]
        pygame.draw.polygon(surf, (15, 100, 200), wings)
        # Cockpit canopy
        canopy = [(w // 2, 10), (w // 2 + 6, 26), (w // 2, 34), (w // 2 - 6, 26)]
        pygame.draw.polygon(surf, (0, 240, 255), canopy)
        pygame.draw.polygon(surf, (220, 255, 255), canopy, 1)
        # Wingtip laser cannons
        pygame.draw.rect(surf, (220, 230, 245), (4, h - 22, 4, 16), border_radius=2)
        pygame.draw.rect(surf, (220, 230, 245), (w - 8, h - 22, 4, 16), border_radius=2)
        return surf

    @staticmethod
    def get_scout_sprite(w=44, h=40):
        ufo_file = os.path.join(ASSETS_DIR, 'ufo.png')
        if os.path.exists(ufo_file):
            try:
                img = pygame.image.load(ufo_file).convert_alpha()
                return pygame.transform.smoothscale(img, (w, h))
            except Exception:
                pass

        # Procedural Flying Saucer / Scout
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # Saucer Dome
        pygame.draw.ellipse(surf, (0, 230, 180), (w // 2 - 10, 2, 20, 16))
        # Saucer Disk
        pygame.draw.ellipse(surf, (80, 50, 150), (2, 12, w - 4, 18))
        pygame.draw.ellipse(surf, (130, 90, 220), (6, 14, w - 12, 12))
        # Glowing emitter lights
        for lx in [8, 16, 24, 32]:
            pygame.draw.circle(surf, (255, 230, 50), (lx, 22), 2)
        return surf

    @staticmethod
    def get_enemy_sprite(w=48, h=48):
        e_file = os.path.join(ASSETS_DIR, 'enemy.png')
        if os.path.exists(e_file):
            try:
                img = pygame.image.load(e_file).convert_alpha()
                return pygame.transform.smoothscale(img, (w, h))
            except Exception:
                pass

        # Procedural Alien Fighter Drone
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pts = [(w // 2, h - 2), (w - 4, 8), (w // 2 + 8, 16), (w // 2, 6), (w // 2 - 8, 16), (4, 8)]
        pygame.draw.polygon(surf, (235, 45, 75), pts)
        pygame.draw.polygon(surf, (150, 20, 45), pts, 2)
        # Menacing eye/core
        pygame.draw.circle(surf, (255, 220, 40), (w // 2, 22), 5)
        return surf

    @staticmethod
    def get_heavy_sprite(w=68, h=68):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # Armored hull
        pygame.draw.rect(surf, (70, 75, 95), (12, 10, w - 24, h - 20), border_radius=6)
        # Side armor plating
        pygame.draw.polygon(surf, (120, 40, 160), [(2, 20), (14, 10), (14, h - 14), (2, h - 24)])
        pygame.draw.polygon(surf, (120, 40, 160), [(w - 2, 20), (w - 14, 10), (w - 14, h - 14), (w - 2, h - 24)])
        # Dual heavy cannons
        pygame.draw.rect(surf, (200, 50, 50), (18, h - 12, 8, 12), border_radius=2)
        pygame.draw.rect(surf, (200, 50, 50), (w - 26, h - 12, 8, 12), border_radius=2)
        # Power core
        pygame.draw.circle(surf, (255, 120, 20), (w // 2, h // 2), 9)
        return surf

    @staticmethod
    def get_boss_sprite(w=260, h=140):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # Main Mothership Chassis
        body_pts = [
            (w // 2, h - 6), (w - 20, h - 45), (w - 6, 20), (w // 2 + 40, 8),
            (w // 2, 22), (w // 2 - 40, 8), (6, 20), (20, h - 45)
        ]
        pygame.draw.polygon(surf, (35, 40, 55), body_pts)
        pygame.draw.polygon(surf, (80, 95, 130), body_pts, 3)

        # Wings & Engines
        pygame.draw.polygon(surf, (180, 40, 70), [(30, 20), (10, h - 50), (60, h - 35)])
        pygame.draw.polygon(surf, (180, 40, 70), [(w - 30, 20), (w - 10, h - 50), (w - 60, h - 35)])

        # Command Bridge
        bridge = pygame.Rect(w // 2 - 30, 32, 60, 22)
        pygame.draw.rect(surf, (0, 240, 255), bridge, border_radius=6)
        pygame.draw.rect(surf, (255, 255, 255), bridge, 2, border_radius=6)

        # Giant Plasma Core
        pygame.draw.circle(surf, (255, 45, 90), (w // 2, h - 42), 20)
        pygame.draw.circle(surf, (255, 200, 220), (w // 2, h - 42), 10)

        # Quad Turrets
        for tx in [w // 2 - 80, w // 2 - 40, w // 2 + 40, w // 2 + 80]:
            pygame.draw.rect(surf, (220, 220, 230), (tx - 5, h - 22, 10, 18), border_radius=3)
            pygame.draw.circle(surf, (255, 140, 0), (tx, h - 4), 4)

        return surf


# ---------------------------------------------------------------------------
# PARTICLE & EFFECT ENGINE
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
        self.radius = max(0.4, self.radius - 0.05)
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


class Shockwave:
    def __init__(self, x, y, max_radius=180, speed=12, color=(0, 240, 255)):
        self.x = x
        self.y = y
        self.radius = 8
        self.max_radius = max_radius
        self.speed = speed
        self.color = color
        self.alpha = 255

    def update(self):
        self.radius += self.speed
        self.alpha = max(0, int(255 * (1.0 - (self.radius / self.max_radius))))
        return self.radius < self.max_radius and self.alpha > 0

    def draw(self, surface):
        if self.radius <= 0 or self.alpha <= 0:
            return
        surf = pygame.Surface((int(self.radius * 2 + 4), int(self.radius * 2 + 4)), pygame.SRCALPHA)
        r, g, b = self.color[:3]
        pygame.draw.circle(surf, (r, g, b, self.alpha), (int(self.radius + 2), int(self.radius + 2)), int(self.radius), width=4)
        surface.blit(surf, (self.x - self.radius - 2, self.y - self.radius - 2))


class FloatingNotice:
    def __init__(self, text, x, y, color=COLOR_GOLD, size=22, duration=50):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont("Impact, Arial Black, Trebuchet MS", size)
        self.lifetime = duration
        self.max_lifetime = duration

    def update(self):
        self.y -= 1.1
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        txt = self.font.render(self.text, True, self.color)
        txt.set_alpha(alpha)
        # Shadow
        shadow = self.font.render(self.text, True, (0, 0, 0))
        shadow.set_alpha(int(alpha * 0.75))
        surface.blit(shadow, (self.x - txt.get_width() // 2 + 2, self.y + 2))
        surface.blit(txt, (self.x - txt.get_width() // 2, self.y))


# ---------------------------------------------------------------------------
# PARALLAX STARFIELD & NEBULAE
# ---------------------------------------------------------------------------
class Starfield:
    def __init__(self):
        self.stars = []
        # Layer 1 (Distant faint stars)
        for _ in range(65):
            self.stars.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': 0.6, 'size': 1, 'color': (140, 155, 185)})
        # Layer 2 (Mid-distance bright stars)
        for _ in range(45):
            self.stars.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': 1.6, 'size': 2, 'color': (200, 220, 255)})
        # Layer 3 (Fast foreground blue stars)
        for _ in range(25):
            self.stars.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'speed': 3.4, 'size': 3, 'color': (0, 240, 255)})

        # Atmospheric Nebula clouds
        self.nebulae = [
            {'x': 180, 'y': 150, 'radius': 160, 'color': (45, 20, 80, 35)},
            {'x': 620, 'y': 480, 'radius': 190, 'color': (15, 45, 90, 40)},
        ]

    def update(self, boost=1.0):
        for s in self.stars:
            s['y'] += s['speed'] * boost
            if s['y'] > HEIGHT:
                s['y'] = -4
                s['x'] = random.randint(0, WIDTH)

    def draw(self, surface):
        surface.fill(COLOR_BG)

        # Draw soft glowing nebulae
        for neb in self.nebulae:
            neb_surf = pygame.Surface((neb['radius'] * 2, neb['radius'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(neb_surf, neb['color'], (neb['radius'], neb['radius']), neb['radius'])
            surface.blit(neb_surf, (neb['x'] - neb['radius'], neb['y'] - neb['radius']))

        # Draw stars
        for s in self.stars:
            pygame.draw.circle(surface, s['color'], (int(s['x']), int(s['y'])), s['size'])


# ---------------------------------------------------------------------------
# PROJECTILES (Player Lasers, Missiles, Alien Plasma)
# ---------------------------------------------------------------------------
class Projectile:
    def __init__(self, x, y, vx, vy, is_player=True, p_type="laser", damage=25):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.is_player = is_player
        self.type = p_type  # 'laser', 'missile', 'plasma', 'enemy_orb'
        self.damage = damage
        self.target = None

    def update(self, enemies=None):
        # Homing Missile tracking logic
        if self.type == "missile" and enemies:
            if not self.target or self.target not in enemies:
                # Pick closest enemy
                closest = None
                min_dist = 9999
                for e in enemies:
                    d = math.hypot(e.x - self.x, e.y - self.y)
                    if d < min_dist:
                        min_dist = d
                        closest = e
                self.target = closest

            if self.target:
                angle_to = math.atan2(self.target.y - self.y, self.target.x - self.x)
                curr_angle = math.atan2(self.vy, self.vx)
                diff = (angle_to - curr_angle + math.pi) % (2 * math.pi) - math.pi
                new_angle = curr_angle + math.copysign(min(abs(diff), 0.14), diff)
                spd = 12.0
                self.vx = math.cos(new_angle) * spd
                self.vy = math.sin(new_angle) * spd

        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        if self.type == "laser":
            # Bright cyan plasma bolt with glow
            pygame.draw.line(surface, (0, 240, 255), (cx, cy - 8), (cx, cy + 8), 4)
            pygame.draw.line(surface, (255, 255, 255), (cx, cy - 6), (cx, cy + 6), 2)
        elif self.type == "missile":
            # Sleek guided rocket with orange tip
            pygame.draw.rect(surface, (230, 230, 235), (cx - 3, cy - 7, 6, 14), border_radius=2)
            pygame.draw.circle(surface, COLOR_NEON_ORANGE, (cx, cy - 7), 3)
        elif self.type == "plasma":
            # Heavy green/purple energy sphere
            pygame.draw.circle(surface, COLOR_NEON_PURPLE, (cx, cy), 6)
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 3)
        elif self.type == "enemy_orb":
            # Hostile red plasma blast
            pygame.draw.circle(surface, COLOR_NEON_RED, (cx, cy), 5)
            pygame.draw.circle(surface, (255, 230, 180), (cx, cy), 2)

    def get_hitbox(self):
        r = 6 if self.type in ["plasma", "missile"] else 4
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)


# ---------------------------------------------------------------------------
# ASTEROIDS (Fracturing Physics)
# ---------------------------------------------------------------------------
class Asteroid:
    def __init__(self, x, y, size_tier=3):
        self.x = x
        self.y = y
        self.size_tier = size_tier  # 3: Large, 2: Medium, 1: Small
        self.radius = 14 * self.size_tier
        self.max_health = 20 * self.size_tier
        self.health = self.max_health
        self.vx = random.uniform(-0.8, 0.8)
        self.vy = random.uniform(1.2, 2.5) / (0.8 * self.size_tier)
        self.rot = 0
        self.rot_speed = random.uniform(-2.5, 2.5)

        # Generate rugged polygon points
        self.poly_pts = []
        num_pts = random.randint(8, 12)
        for i in range(num_pts):
            ang = (i / num_pts) * 2 * math.pi
            dist = self.radius * random.uniform(0.78, 1.15)
            self.poly_pts.append((dist * math.cos(ang), dist * math.sin(ang)))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot += self.rot_speed

    def draw(self, surface):
        self.rot += self.rot_speed
        rad_rot = math.radians(self.rot)
        cos_r = math.cos(rad_rot)
        sin_r = math.sin(rad_rot)

        pts = []
        for px, py in self.poly_pts:
            rx = px * cos_r - py * sin_r + self.x
            ry = px * sin_r + py * cos_r + self.y
            pts.append((rx, ry))

        # Rocky crater coloring
        pygame.draw.polygon(surface, (95, 95, 105), pts)
        pygame.draw.polygon(surface, (150, 150, 165), pts, 2)
        # Small crater
        cx = self.x + (self.radius * 0.3 * cos_r)
        cy = self.y + (self.radius * 0.3 * sin_r)
        pygame.draw.circle(surface, (70, 70, 80), (int(cx), int(cy)), max(2, int(self.radius * 0.25)))

    def get_hitbox(self):
        return pygame.Rect(self.x - self.radius * 0.85, self.y - self.radius * 0.85, self.radius * 1.7, self.radius * 1.7)


# ---------------------------------------------------------------------------
# ENEMIES & BOSSES
# ---------------------------------------------------------------------------
class Enemy:
    def __init__(self, enemy_type, x, y):
        self.type = enemy_type  # 'scout', 'fighter', 'heavy', 'boss'
        self.x = x
        self.y = y
        self.shoot_timer = random.randint(30, 90)
        self.tick = random.randint(0, 100)

        if self.type == 'scout':
            self.width, self.height = 44, 40
            self.surface = AssetManager.get_scout_sprite(self.width, self.height)
            self.health = 35
            self.max_health = 35
            self.speed_y = 2.4
            self.points = 100

        elif self.type == 'fighter':
            self.width, self.height = 48, 48
            self.surface = AssetManager.get_enemy_sprite(self.width, self.height)
            self.health = 70
            self.max_health = 70
            self.speed_y = 1.8
            self.points = 250

        elif self.type == 'heavy':
            self.width, self.height = 68, 68
            self.surface = AssetManager.get_heavy_sprite(self.width, self.height)
            self.health = 180
            self.max_health = 180
            self.speed_y = 1.1
            self.points = 600

        elif self.type == 'boss':
            self.width, self.height = 260, 140
            self.surface = AssetManager.get_boss_sprite(self.width, self.height)
            self.health = 1800
            self.max_health = 1800
            self.speed_y = 0.8
            self.points = 5000
            self.boss_phase = 1
            self.strafe_dir = 1

    def update(self, player_x, projectiles, audio):
        self.tick += 1

        if self.type == 'scout':
            # Fast sine wave dive
            self.y += self.speed_y
            self.x += math.sin(self.tick * 0.06) * 3.5

        elif self.type == 'fighter':
            self.y += self.speed_y
            # Track player horizontally
            dx = player_x - (self.x + self.width // 2)
            self.x += math.copysign(min(abs(dx), 1.6), dx)

            # Fire aimed plasma bolts
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = random.randint(85, 130)
                cx = self.x + self.width // 2
                cy = self.y + self.height
                projectiles.append(Projectile(cx, cy, 0, 5.5, is_player=False, p_type="enemy_orb"))

        elif self.type == 'heavy':
            self.y += self.speed_y
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = random.randint(70, 110)
                # Twin cannon burst
                projectiles.append(Projectile(self.x + 18, self.y + self.height, -1.2, 5.0, is_player=False, p_type="enemy_orb"))
                projectiles.append(Projectile(self.x + self.width - 18, self.y + self.height, 1.2, 5.0, is_player=False, p_type="enemy_orb"))

        elif self.type == 'boss':
            # Boss enters and hovers at top of screen
            if self.y < 50:
                self.y += self.speed_y
            else:
                # Strafe left and right
                self.x += self.strafe_dir * 1.8
                if self.x < 30:
                    self.strafe_dir = 1
                elif self.x > WIDTH - self.width - 30:
                    self.strafe_dir = -1

            # Boss attack patterns
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = 50 if self.health > 800 else 35
                cx = self.x + self.width // 2
                cy = self.y + self.height - 15

                # Spiral barrage or multi-laser
                for angle_deg in [-30, -15, 0, 15, 30]:
                    rad = math.radians(angle_deg + 90)
                    spd = 5.2
                    projectiles.append(Projectile(cx, cy, math.cos(rad) * spd, math.sin(rad) * spd, is_player=False, p_type="enemy_orb", damage=20))

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))

        # Health bar for heavy cruisers
        if self.type == 'heavy' and self.health < self.max_health:
            bar_w = self.width
            pygame.draw.rect(surface, (30, 30, 30), (self.x, self.y - 8, bar_w, 4))
            fill = max(0, int((self.health / self.max_health) * bar_w))
            pygame.draw.rect(surface, COLOR_NEON_RED, (self.x, self.y - 8, fill, 4))

    def get_hitbox(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)


# ---------------------------------------------------------------------------
# POWER-UP COLLECTIBLES
# ---------------------------------------------------------------------------
class Powerup:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.type = p_type  # 'WEAPON', 'SHIELD', 'BOMB', 'HEAL'
        self.vy = 2.0
        self.tick = random.randint(0, 100)

    def update(self):
        self.y += self.vy
        self.tick += 1

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        box_size = 28
        rect = pygame.Rect(cx - box_size // 2, cy - box_size // 2, box_size, box_size)

        color_map = {
            'WEAPON': COLOR_GOLD,
            'SHIELD': COLOR_NEON_CYAN,
            'BOMB': COLOR_NEON_ORANGE,
            'HEAL': COLOR_NEON_GREEN
        }
        col = color_map.get(self.type, COLOR_GOLD)

        # Glowing box
        glow = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*col, 70 + int(30 * math.sin(self.tick * 0.15))), (22, 22), 20)
        surface.blit(glow, (cx - 22, cy - 22))

        pygame.draw.rect(surface, (20, 24, 35), rect, border_radius=5)
        pygame.draw.rect(surface, col, rect, 2, border_radius=5)

        # Icon Letter
        font = pygame.font.SysFont("Arial Black", 13, bold=True)
        txt = font.render(self.type[0], True, col)
        surface.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))

    def get_hitbox(self):
        return pygame.Rect(self.x - 14, self.y - 14, 28, 28)


# ---------------------------------------------------------------------------
# PLAYER SPACESHIP
# ---------------------------------------------------------------------------
class PlayerShip:
    def __init__(self):
        self.width = 56
        self.height = 64
        self.surface = AssetManager.get_player_sprite(self.width, self.height)
        self.reset()

    def reset(self):
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 110
        self.vx = 0
        self.vy = 0
        self.speed = 6.2

        # Defense: Shield + Hull
        self.max_health = 100.0
        self.health = 100.0
        self.max_shield = 100.0
        self.shield = 100.0
        self.shield_recharge_delay = 0

        # Offense: Weapon upgrades
        self.weapon_tier = 1  # 1 to 5
        self.bombs = 2
        self.fire_cooldown = 0
        self.missile_cooldown = 0
        self.invulnerable_frames = 0

    def update(self, keys, mouse_pressed, projectiles, particles, audio):
        # 1. 8-Directional Movement
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx * self.speed
        self.y += dy * self.speed

        # Screen boundaries
        self.x = max(10, min(WIDTH - self.width - 10, self.x))
        self.y = max(40, min(HEIGHT - self.height - 15, self.y))

        # Thruster particle trails
        if random.random() < 0.85:
            # Dual engine exhaust
            particles.append(Particle(self.x + 16, self.y + self.height - 4, random.uniform(-0.4, 0.4), random.uniform(3.5, 7), (0, 210, 255), 4, 20))
            particles.append(Particle(self.x + self.width - 16, self.y + self.height - 4, random.uniform(-0.4, 0.4), random.uniform(3.5, 7), (0, 210, 255), 4, 20))

        # 2. Shooting
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1

        shooting = keys[pygame.K_SPACE] or mouse_pressed[0]
        if shooting and self.fire_cooldown <= 0:
            self.fire_weapon(projectiles, audio)

        # 3. Shield passive regeneration
        if self.shield_recharge_delay > 0:
            self.shield_recharge_delay -= 1
        else:
            if self.shield < self.max_shield:
                self.shield = min(self.max_shield, self.shield + 0.12)

        if self.invulnerable_frames > 0:
            self.invulnerable_frames -= 1

    def fire_weapon(self, projectiles, audio):
        audio.play('laser')
        cx = self.x + self.width // 2
        cy = self.y + 4

        if self.weapon_tier == 1:
            # Dual Lasers
            self.fire_cooldown = 11
            projectiles.append(Projectile(self.x + 12, cy, 0, -14, is_player=True, p_type="laser", damage=25))
            projectiles.append(Projectile(self.x + self.width - 12, cy, 0, -14, is_player=True, p_type="laser", damage=25))

        elif self.weapon_tier == 2:
            # Heavy Rapid Dual Lasers
            self.fire_cooldown = 8
            projectiles.append(Projectile(self.x + 10, cy, 0, -16, is_player=True, p_type="laser", damage=32))
            projectiles.append(Projectile(self.x + self.width - 10, cy, 0, -16, is_player=True, p_type="laser", damage=32))

        elif self.weapon_tier == 3:
            # 3-Way Plasma Spread
            self.fire_cooldown = 10
            projectiles.append(Projectile(cx, cy, 0, -15, is_player=True, p_type="laser", damage=35))
            projectiles.append(Projectile(cx - 10, cy, -3.2, -14, is_player=True, p_type="laser", damage=30))
            projectiles.append(Projectile(cx + 10, cy, 3.2, -14, is_player=True, p_type="laser", damage=30))

        elif self.weapon_tier == 4:
            # 5-Way Plasma Spread
            self.fire_cooldown = 9
            for vx in [-5.5, -2.8, 0, 2.8, 5.5]:
                projectiles.append(Projectile(cx, cy, vx, -15, is_player=True, p_type="laser", damage=32))

        elif self.weapon_tier >= 5:
            # Overdrive: 5-way lasers + Seeking Homing Missiles!
            self.fire_cooldown = 8
            for vx in [-5.0, -2.5, 0, 2.5, 5.0]:
                projectiles.append(Projectile(cx, cy, vx, -16, is_player=True, p_type="laser", damage=36))

            if self.missile_cooldown <= 0:
                self.missile_cooldown = 24
                audio.play('missile')
                projectiles.append(Projectile(self.x + 4, cy + 12, -4, -6, is_player=True, p_type="missile", damage=60))
                projectiles.append(Projectile(self.x + self.width - 4, cy + 12, 4, -6, is_player=True, p_type="missile", damage=60))

    def take_damage(self, amount, audio):
        if self.invulnerable_frames > 0:
            return False

        self.shield_recharge_delay = 180  # 3 seconds delay before recharge
        audio.play('shield_hit')

        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
            else:
                remaining = amount - self.shield
                self.shield = 0
                self.health = max(0, self.health - remaining)
        else:
            self.health = max(0, self.health - amount)

        self.invulnerable_frames = 20
        return self.health <= 0

    def draw(self, surface):
        if self.invulnerable_frames > 0 and (self.invulnerable_frames // 4) % 2 == 1:
            return

        surface.blit(self.surface, (self.x, self.y))

        # Energy Shield Dome Effect
        if self.shield > 10:
            s_radius = int(self.width * 0.72)
            cx, cy = self.x + self.width // 2, self.y + self.height // 2
            shield_surf = pygame.Surface((s_radius * 2, s_radius * 2), pygame.SRCALPHA)
            alpha = int(70 * (self.shield / self.max_shield))
            pygame.draw.circle(shield_surf, (0, 240, 255, alpha), (s_radius, s_radius), s_radius, 3)
            pygame.draw.circle(shield_surf, (0, 180, 255, alpha // 2), (s_radius, s_radius), s_radius - 2)
            surface.blit(shield_surf, (cx - s_radius, cy - s_radius))

    def get_hitbox(self):
        return pygame.Rect(self.x + 8, self.y + 10, self.width - 16, self.height - 18)


# ---------------------------------------------------------------------------
# MAIN GAME CONTROLLER
# ---------------------------------------------------------------------------
class CyberNovaGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CYBER NOVA: GALAXY STRIKER")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_huge = pygame.font.SysFont("Impact, Arial Black", 64)
        self.font_large = pygame.font.SysFont("Impact, Arial Black", 36)
        self.font_medium = pygame.font.SysFont("Trebuchet MS, Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Trebuchet MS, Arial", 16, bold=True)
        self.font_digital = pygame.font.SysFont("Consolas, Courier", 28, bold=True)

        self.audio = AudioManager()
        self.starfield = Starfield()

        self.high_score = 0
        self.high_wave = 1
        self.load_save_data()

        self.state = 'MENU'
        self.player = PlayerShip()
        self.enemies = []
        self.asteroids = []
        self.projectiles = []
        self.powerups = []
        self.particles = []
        self.shockwaves = []
        self.notices = []

        self.score = 0
        self.wave = 1
        self.wave_enemies_to_spawn = 0
        self.wave_spawn_timer = 0
        self.boss_active = False
        self.screen_shake = 0

    def load_save_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.high_wave = data.get("high_wave", 1)
            except Exception:
                pass

    def save_data(self):
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump({
                    "high_score": max(self.high_score, int(self.score)),
                    "high_wave": max(self.high_wave, self.wave)
                }, f)
        except Exception:
            pass

    def start_new_game(self):
        self.player.reset()
        self.enemies.clear()
        self.asteroids.clear()
        self.projectiles.clear()
        self.powerups.clear()
        self.particles.clear()
        self.shockwaves.clear()
        self.notices.clear()

        self.score = 0
        self.wave = 1
        self.boss_active = False
        self.screen_shake = 0
        self.init_wave(self.wave)

        self.state = 'PLAYING'

    def init_wave(self, wave_num):
        self.wave = wave_num
        self.wave_spawn_timer = 0

        # Boss wave every 5 waves
        if self.wave % 5 == 0:
            self.boss_active = True
            self.audio.play('boss_alarm')
            self.notices.append(FloatingNotice(f"WARNING: DREADNOUGHT BOSS INCOMING!", WIDTH // 2, HEIGHT // 2 - 80, COLOR_NEON_RED, size=30, duration=90))
            self.enemies.append(Enemy('boss', (WIDTH - 260) // 2, -160))
            self.wave_enemies_to_spawn = 0
        else:
            self.boss_active = False
            self.wave_enemies_to_spawn = 12 + wave_num * 4
            self.notices.append(FloatingNotice(f"--- WAVE {self.wave} ---", WIDTH // 2, HEIGHT // 2 - 50, COLOR_NEON_CYAN, size=32, duration=70))

    def trigger_smart_bomb(self):
        if self.player.bombs <= 0:
            return
        self.player.bombs -= 1
        self.screen_shake = 22
        self.audio.play('emp')
        self.shockwaves.append(Shockwave(self.player.x + self.player.width // 2, self.player.y + self.player.height // 2, max_radius=WIDTH, speed=22, color=COLOR_NEON_CYAN))
        self.notices.append(FloatingNotice("EMP SMART BOMB DETONATED!", WIDTH // 2, self.player.y - 35, COLOR_NEON_CYAN, size=24))

        # Destroy all enemy bullets
        self.projectiles = [p for p in self.projectiles if p.is_player]

        # Heavy damage to all enemies on screen
        for e in self.enemies:
            e.health -= 250
            for _ in range(12):
                self.particles.append(Particle(e.x + e.width // 2, e.y + e.height // 2, random.uniform(-5, 5), random.uniform(-5, 5), COLOR_NEON_CYAN, 4, 18))

        # Shatter asteroids
        for ast in self.asteroids[:]:
            self.destroy_asteroid(ast)

    def destroy_asteroid(self, ast):
        self.audio.play('explosion')
        self.score += 50 * ast.size_tier
        for _ in range(8 * ast.size_tier):
            self.particles.append(Particle(ast.x, ast.y, random.uniform(-4, 4), random.uniform(-4, 4), (130, 130, 140), random.randint(2, 5), 18))

        # Fragment into smaller pieces
        if ast.size_tier > 1:
            for _ in range(2):
                child = Asteroid(ast.x + random.randint(-15, 15), ast.y + random.randint(-15, 15), size_tier=ast.size_tier - 1)
                self.asteroids.append(child)

        if ast in self.asteroids:
            self.asteroids.remove(ast)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            keys = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.audio.toggle_mute()

                    if self.state == 'MENU':
                        if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                            self.start_new_game()

                    elif self.state == 'PLAYING':
                        if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                            self.state = 'PAUSED'
                        elif event.key in [pygame.K_e, pygame.K_b]:
                            self.trigger_smart_bomb()

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

                elif event.type == pygame.MOUSEBUTTONDOWN and self.state == 'PLAYING':
                    if event.button == 3:  # Right Click = Smart Bomb
                        self.trigger_smart_bomb()

            # States update & render
            if self.state == 'MENU':
                self.update_menu()
                self.draw_menu()
            elif self.state == 'PLAYING':
                self.update_playing(keys, mouse_pressed)
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

    # -----------------------------------------------------------------------
    # PLAYING STATE UPDATE & RENDER
    # -----------------------------------------------------------------------
    def update_playing(self, keys, mouse_pressed):
        self.starfield.update(boost=1.4)

        # Update Player
        self.player.update(keys, mouse_pressed, self.projectiles, self.particles, self.audio)

        # Spawning wave enemies
        if self.wave_enemies_to_spawn > 0:
            self.wave_spawn_timer += 1
            if self.wave_spawn_timer >= 50:
                self.wave_spawn_timer = 0
                self.wave_enemies_to_spawn -= 1
                e_type = random.choices(['scout', 'fighter', 'heavy'], weights=[0.55, 0.35, 0.10])[0]
                self.enemies.append(Enemy(e_type, random.randint(30, WIDTH - 80), -60))

        # Spawning random asteroids
        if random.random() < 0.012 and len(self.asteroids) < 5:
            self.asteroids.append(Asteroid(random.randint(20, WIDTH - 50), -80, size_tier=random.choice([1, 2, 3])))

        # Check wave clear
        if self.wave_enemies_to_spawn <= 0 and len(self.enemies) == 0:
            self.init_wave(self.wave + 1)

        # Update Projectiles
        for p in self.projectiles[:]:
            p.update(self.enemies)
            if p.y < -30 or p.y > HEIGHT + 30 or p.x < -30 or p.x > WIDTH + 30:
                self.projectiles.remove(p)

        # Update Asteroids
        for ast in self.asteroids[:]:
            ast.update()
            if ast.y > HEIGHT + 80:
                self.asteroids.remove(ast)

        # Update Enemies
        player_hitbox = self.player.get_hitbox()
        for e in self.enemies[:]:
            e.update(self.player.x, self.projectiles, self.audio)

            # Check collision with player
            if player_hitbox.colliderect(e.get_hitbox()):
                self.screen_shake = 16
                is_dead = self.player.take_damage(35, self.audio)
                e.health -= 80
                for _ in range(16):
                    self.particles.append(Particle(e.x + e.width // 2, e.y + e.height // 2, random.uniform(-4, 4), random.uniform(-4, 4), COLOR_NEON_ORANGE, 4, 16))
                if is_dead:
                    self.trigger_game_over()
                    return

            if e.health <= 0:
                self.kill_enemy(e)
            elif e.y > HEIGHT + 80:
                self.enemies.remove(e)

        # Projectile Hits against Enemies & Asteroids
        for p in self.projectiles[:]:
            if p.is_player:
                # Vs Enemies
                hit_enemy = False
                for e in self.enemies:
                    if e.get_hitbox().collidepoint(p.x, p.y):
                        e.health -= p.damage
                        hit_enemy = True
                        for _ in range(4):
                            self.particles.append(Particle(p.x, p.y, random.uniform(-2, 2), random.uniform(-2, 2), COLOR_NEON_CYAN, 3, 22))
                        if e.health <= 0:
                            self.kill_enemy(e)
                        break

                if hit_enemy:
                    if p in self.projectiles:
                        self.projectiles.remove(p)
                    continue

                # Vs Asteroids
                hit_ast = False
                for ast in self.asteroids[:]:
                    if ast.get_hitbox().collidepoint(p.x, p.y):
                        ast.health -= p.damage
                        hit_ast = True
                        for _ in range(4):
                            self.particles.append(Particle(p.x, p.y, random.uniform(-2, 2), random.uniform(-2, 2), (180, 180, 190), 3, 20))
                        if ast.health <= 0:
                            self.destroy_asteroid(ast)
                        break

                if hit_ast and p in self.projectiles:
                    self.projectiles.remove(p)

            else:
                # Hostile projectile hits player
                if player_hitbox.collidepoint(p.x, p.y):
                    self.screen_shake = 10
                    is_dead = self.player.take_damage(p.damage, self.audio)
                    for _ in range(8):
                        self.particles.append(Particle(p.x, p.y, random.uniform(-3, 3), random.uniform(-3, 3), COLOR_NEON_RED, 3, 20))
                    if p in self.projectiles:
                        self.projectiles.remove(p)
                    if is_dead:
                        self.trigger_game_over()
                        return

        # Player vs Asteroid collision
        for ast in self.asteroids[:]:
            if player_hitbox.colliderect(ast.get_hitbox()):
                self.screen_shake = 18
                is_dead = self.player.take_damage(30 * ast.size_tier, self.audio)
                self.destroy_asteroid(ast)
                if is_dead:
                    self.trigger_game_over()
                    return

        # Update Powerups
        for pu in self.powerups[:]:
            pu.update()
            if player_hitbox.colliderect(pu.get_hitbox()):
                self.collect_powerup(pu)
            elif pu.y > HEIGHT + 50:
                self.powerups.remove(pu)

        # Update Particles & FX
        self.particles = [pt for pt in self.particles if pt.update()]
        self.shockwaves = [sw for sw in self.shockwaves if sw.update()]
        self.notices = [nt for nt in self.notices if nt.update()]

        if self.screen_shake > 0:
            self.screen_shake -= 1

    def kill_enemy(self, e):
        self.audio.play('explosion')
        self.score += e.points
        cx, cy = e.x + e.width // 2, e.y + e.height // 2

        # Explosion burst
        num_p = 45 if e.type == 'boss' else (25 if e.type == 'heavy' else 14)
        for _ in range(num_p):
            self.particles.append(Particle(cx, cy, random.uniform(-6, 6), random.uniform(-6, 6), random.choice([COLOR_NEON_ORANGE, COLOR_NEON_RED, (255, 230, 80)]), random.randint(3, 7), 16))

        # Chance to drop power-up
        drop_chance = 0.22 if e.type != 'boss' else 1.0
        if random.random() < drop_chance:
            ptype = random.choices(['WEAPON', 'SHIELD', 'BOMB', 'HEAL'], weights=[0.40, 0.30, 0.15, 0.15])[0]
            self.powerups.append(Powerup(cx, cy, ptype))

        if e.type == 'boss':
            self.boss_active = False
            self.screen_shake = 30
            self.shockwaves.append(Shockwave(cx, cy, max_radius=300, speed=16, color=COLOR_GOLD))
            self.notices.append(FloatingNotice("DREADNOUGHT DESTROYED! +5000 PTS", WIDTH // 2, cy, COLOR_GOLD, size=28, duration=90))

        if e in self.enemies:
            self.enemies.remove(e)

    def collect_powerup(self, pu):
        self.audio.play('powerup')
        if pu.type == 'WEAPON':
            if self.player.weapon_tier < 5:
                self.player.weapon_tier += 1
                self.notices.append(FloatingNotice(f"WEAPON UPGRADE! TIER {self.player.weapon_tier}", pu.x, pu.y, COLOR_GOLD))
            else:
                self.score += 500
                self.notices.append(FloatingNotice("+500 OVERDRIVE BONUS", pu.x, pu.y, COLOR_GOLD))
        elif pu.type == 'SHIELD':
            self.player.shield = self.player.max_shield
            self.notices.append(FloatingNotice("SHIELD FULLY CHARGED!", pu.x, pu.y, COLOR_NEON_CYAN))
        elif pu.type == 'BOMB':
            self.player.bombs += 1
            self.notices.append(FloatingNotice("+1 SMART BOMB", pu.x, pu.y, COLOR_NEON_ORANGE))
        elif pu.type == 'HEAL':
            self.player.health = min(self.player.max_health, self.player.health + 40)
            self.notices.append(FloatingNotice("+40 HULL REPAIRED", pu.x, pu.y, COLOR_NEON_GREEN))

        for _ in range(14):
            self.particles.append(Particle(pu.x, pu.y, random.uniform(-3, 3), random.uniform(-3, 3), COLOR_GOLD, 3, 18))
        if pu in self.powerups:
            self.powerups.remove(pu)

    def trigger_game_over(self):
        self.state = 'GAMEOVER'
        self.audio.play('explosion')
        if self.score > self.high_score:
            self.high_score = int(self.score)
        if self.wave > self.high_wave:
            self.high_wave = self.wave
        self.save_data()

    def update_gameover(self):
        self.particles = [pt for pt in self.particles if pt.update()]
        self.notices = [nt for nt in self.notices if nt.update()]

    def draw_playing(self):
        shake_x, shake_y = 0, 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)

        surf = pygame.Surface((WIDTH, HEIGHT))

        # 1. Starfield
        self.starfield.draw(surf)

        # 2. Asteroids
        for ast in self.asteroids:
            ast.draw(surf)

        # 3. Powerups
        for pu in self.powerups:
            pu.draw(surf)

        # 4. Enemies
        for e in self.enemies:
            e.draw(surf)

        # 5. Projectiles
        for p in self.projectiles:
            p.draw(surf)

        # 6. Player
        self.player.draw(surf)

        # 7. Shockwaves & Particles
        for sw in self.shockwaves:
            sw.draw(surf)
        for pt in self.particles:
            pt.draw(surf)

        # 8. Floating Notices
        for nt in self.notices:
            nt.draw(surf)

        # 9. Futuristic HUD
        self.draw_hud(surf)

        self.screen.blit(surf, (shake_x, shake_y))

    def draw_hud(self, surface):
        # Top HUD Bar
        hud_bar = pygame.Surface((WIDTH, 52), pygame.SRCALPHA)
        pygame.draw.rect(hud_bar, (12, 16, 26, 210), (0, 0, WIDTH, 52))
        pygame.draw.line(hud_bar, (35, 50, 75), (0, 51), (WIDTH, 51), 2)
        surface.blit(hud_bar, (0, 0))

        # Left: Shield & Health Bars
        bar_x, bar_y, bar_w, bar_h = 20, 10, 140, 12
        # Shield Bar (Cyan)
        pygame.draw.rect(surface, (25, 35, 45), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        s_fill = max(0, int((self.player.shield / self.player.max_shield) * bar_w))
        pygame.draw.rect(surface, COLOR_NEON_CYAN, (bar_x, bar_y, s_fill, bar_h), border_radius=3)
        s_txt = self.font_small.render("SHIELD", True, (170, 220, 255))
        surface.blit(s_txt, (bar_x + bar_w + 8, bar_y - 2))

        # Health Bar (Green/Red)
        pygame.draw.rect(surface, (25, 35, 45), (bar_x, bar_y + 18, bar_w, bar_h), border_radius=3)
        h_fill = max(0, int((self.player.health / self.player.max_health) * bar_w))
        h_col = COLOR_NEON_GREEN if self.player.health > 40 else COLOR_NEON_RED
        pygame.draw.rect(surface, h_col, (bar_x, bar_y + 18, h_fill, bar_h), border_radius=3)
        h_txt = self.font_small.render("HULL", True, (210, 220, 230))
        surface.blit(h_txt, (bar_x + bar_w + 8, bar_y + 16))

        # Center: Score & Wave
        sc_val = self.font_digital.render(f"{int(self.score):06d}", True, (255, 255, 255))
        sc_lbl = self.font_small.render("SCORE", True, (150, 160, 180))
        surface.blit(sc_lbl, (WIDTH // 2 - 80, 6))
        surface.blit(sc_val, (WIDTH // 2 - 80, 20))

        w_val = self.font_digital.render(f"WAVE {self.wave}", True, COLOR_GOLD)
        surface.blit(w_val, (WIDTH // 2 + 70, 14))

        # Right: Weapon Tier & Bombs
        wpn_txt = self.font_medium.render(f"WEAPON: TIER {self.player.weapon_tier}", True, COLOR_GOLD)
        surface.blit(wpn_txt, (WIDTH - 240, 6))

        bomb_txt = self.font_small.render(f"BOMBS (E/R-CLICK): {self.player.bombs}", True, COLOR_NEON_ORANGE)
        surface.blit(bomb_txt, (WIDTH - 240, 28))

        # Boss Health Bar (Top Center overlay when boss is alive)
        for e in self.enemies:
            if e.type == 'boss':
                bw, bh = 420, 18
                bx = (WIDTH - bw) // 2
                by = 64
                pygame.draw.rect(surface, (20, 25, 35), (bx - 2, by - 2, bw + 4, bh + 4), border_radius=4)
                pygame.draw.rect(surface, (180, 40, 60), (bx - 2, by - 2, bw + 4, bh + 4), 2, border_radius=4)
                fill = max(0, int((e.health / e.max_health) * bw))
                pygame.draw.rect(surface, COLOR_NEON_RED, (bx, by, fill, bh), border_radius=3)
                b_lbl = self.font_small.render("DREADNOUGHT MOTHERSHIP", True, (255, 220, 220))
                surface.blit(b_lbl, (WIDTH // 2 - b_lbl.get_width() // 2, by + 1))
                break

    # -----------------------------------------------------------------------
    # OVERLAYS (Paused & Game Over)
    # -----------------------------------------------------------------------
    def draw_paused_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 22, 190))
        self.screen.blit(overlay, (0, 0))

        title = self.font_huge.render("MISSION PAUSED", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

        info1 = self.font_medium.render("PRESS ESC TO RESUME MISSION", True, COLOR_NEON_CYAN)
        info2 = self.font_medium.render("PRESS R TO RESTART", True, COLOR_GOLD)
        info3 = self.font_medium.render("PRESS Q FOR MAIN MENU", True, (200, 205, 215))

        self.screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 + 0))
        self.screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 40))
        self.screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT // 2 + 80))

    def draw_gameover_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((25, 8, 12, 205))
        self.screen.blit(overlay, (0, 0))

        card_w, card_h = 500, 390
        cx = (WIDTH - card_w) // 2
        cy = (HEIGHT - card_h) // 2
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (18, 22, 32, 245), (0, 0, card_w, card_h), border_radius=12)
        pygame.draw.rect(card_surf, COLOR_NEON_RED, (0, 0, card_w, card_h), 2, border_radius=12)
        self.screen.blit(card_surf, (cx, cy))

        title = self.font_huge.render("SHIP DESTROYED!", True, COLOR_NEON_RED)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, cy + 24))

        stats = [
            ("FINAL SCORE", f"{int(self.score):,}", COLOR_GOLD),
            ("WAVE REACHED", f"WAVE {self.wave}", (255, 255, 255)),
            ("WEAPON TIER", f"TIER {self.player.weapon_tier}", COLOR_NEON_CYAN),
            ("BEST SCORE", f"{self.high_score:,}", (180, 255, 180)),
        ]

        stat_y = cy + 120
        for lbl, val, col in stats:
            l_surf = self.font_medium.render(lbl, True, (160, 170, 190))
            v_surf = self.font_medium.render(val, True, col)
            self.screen.blit(l_surf, (cx + 50, stat_y))
            self.screen.blit(v_surf, (cx + card_w - 50 - v_surf.get_width(), stat_y))
            stat_y += 38

        prompt = self.font_medium.render("PRESS R TO RETRY   |   M FOR MAIN MENU", True, (255, 255, 255))
        self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, cy + card_h - 48))

    # -----------------------------------------------------------------------
    # MENU STATE
    # -----------------------------------------------------------------------
    def update_menu(self):
        self.starfield.update(boost=0.6)

    def draw_menu(self):
        self.starfield.draw(self.screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 24, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.font_huge.render("CYBER NOVA", True, COLOR_NEON_CYAN)
        subtitle = self.font_large.render("GALAXY STRIKER", True, COLOR_GOLD)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 150))

        # Showcase Fighter Ship in center
        ship_w, ship_h = int(self.player.width * 1.8), int(self.player.height * 1.8)
        scaled_ship = pygame.transform.smoothscale(self.player.surface, (ship_w, ship_h))
        self.screen.blit(scaled_ship, (WIDTH // 2 - ship_w // 2, 230))

        # Instructions
        inst_y = 390
        inst_lines = [
            ("PILOT CONTROLS:", COLOR_NEON_CYAN),
            ("W / A / S / D  or  ARROWS : 8-Way Flight Navigation", (230, 235, 245)),
            ("SPACEBAR  or  LEFT CLICK : Primary Plasma Cannons", (230, 235, 245)),
            ("E  or  RIGHT CLICK       : EMP Smart Bomb Shockwave", COLOR_NEON_ORANGE),
            ("P  or  ESC               : Pause Tactical Mission", (170, 180, 195)),
            ("M                        : Toggle Sound Mute", (170, 180, 195)),
        ]
        curr_y = inst_y
        for text, color in inst_lines:
            line_surf = self.font_small.render(text, True, color)
            self.screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, curr_y))
            curr_y += 24

        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
        start_col = (int(255 * pulse), 255, int(150 + 105 * pulse))
        start_txt = self.font_large.render("PRESS SPACE OR ENTER TO LAUNCH!", True, start_col)
        self.screen.blit(start_txt, (WIDTH // 2 - start_txt.get_width() // 2, 600))

        if self.high_score > 0:
            rec_surf = self.font_small.render(f"TOP PILOT SCORE: {self.high_score:,}   |   HIGHEST WAVE: {self.high_wave}", True, COLOR_GOLD)
            self.screen.blit(rec_surf, (WIDTH // 2 - rec_surf.get_width() // 2, 670))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    game = CyberNovaGame()
    game.run()
