"""
=============================================================================
               OPERATION VANGUARD: TACTICAL COMMANDO
=============================================================================
A 2D top-down military tactical combat shooter in pure Python.
Features human soldier combat, 360-degree mouse aiming, realistic firearms
(Pistol, Assault Rifle, Shotgun, Sniper, Frag Grenades), tactical cover,
enemy squad AI, destructible crates, and procedural gunshot sound synthesis.
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
# INITIALIZATION & DISPLAY
# ---------------------------------------------------------------------------
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    AUDIO_ENABLED = True
except Exception:
    AUDIO_ENABLED = False

WIDTH, HEIGHT = 900, 700
FPS = 60

# Tactical Color Palette
COLOR_FLOOR = (35, 38, 44)
COLOR_FLOOR_GRID = (45, 49, 58)
COLOR_WALL = (65, 70, 80)
COLOR_WALL_TOP = (85, 92, 105)
COLOR_SANDBAG = (160, 135, 90)
COLOR_CRATE = (130, 95, 55)
COLOR_CRATE_BORDER = (95, 68, 38)
COLOR_HUD_BG = (18, 22, 30, 225)
COLOR_NEON_BLUE = (0, 200, 255)
COLOR_NEON_GREEN = (46, 204, 113)
COLOR_NEON_RED = (235, 50, 50)
COLOR_GOLD = (245, 190, 30)

SAVE_FILE = os.path.join(os.path.dirname(__file__), "commando_save.json")


# ---------------------------------------------------------------------------
# PROCEDURAL GUNPLAY AUDIO SYNTHESIZER
# ---------------------------------------------------------------------------
class GunAudioSynth:
    """Synthesizes authentic tactical gunshot acoustics using NumPy."""
    def __init__(self):
        self.muted = False
        self.sounds = {}
        if not AUDIO_ENABLED:
            return

        self.sample_rate = 44100
        try:
            self.sounds['pistol'] = self._synth_gunshot(duration=0.18, freq_start=950, noise_ratio=0.75, decay=28)
            self.sounds['rifle'] = self._synth_gunshot(duration=0.22, freq_start=750, noise_ratio=0.82, decay=24)
            self.sounds['shotgun'] = self._synth_gunshot(duration=0.38, freq_start=450, noise_ratio=0.90, decay=14)
            self.sounds['sniper'] = self._synth_gunshot(duration=0.45, freq_start=1100, noise_ratio=0.70, decay=12)
            self.sounds['reload'] = self._synth_reload()
            self.sounds['empty'] = self._synth_click()
            self.sounds['explosion'] = self._synth_explosion()
            self.sounds['hit'] = self._synth_hit()
            self.sounds['pickup'] = self._synth_pickup()
        except Exception as e:
            print(f"Audio init warning: {e}")

    def _array_to_sound(self, wave, volume=0.35):
        wave = np.clip(wave, -1.0, 1.0)
        audio_int16 = (wave * 32767).astype(np.int16)
        stereo = np.column_stack((audio_int16, audio_int16))
        snd = pygame.sndarray.make_sound(stereo)
        snd.set_volume(volume)
        return snd

    def _synth_gunshot(self, duration, freq_start, noise_ratio, decay):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        env = np.exp(-decay * t)
        freq = np.linspace(freq_start, 80, len(t))
        carrier = np.sin(2 * np.pi * freq * t)
        wave = (noise * noise_ratio + carrier * (1.0 - noise_ratio)) * env
        return self._array_to_sound(wave, volume=0.40)

    def _synth_reload(self):
        duration = 0.35
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        # Metallic sliding click sound
        click1 = np.sin(2 * np.pi * 1800 * t) * np.exp(-40 * t)
        click2 = np.sin(2 * np.pi * 1200 * t) * np.exp(-35 * np.maximum(0, t - 0.15))
        wave = (click1 + click2) * 0.4
        return self._array_to_sound(wave, volume=0.35)

    def _synth_click(self):
        duration = 0.08
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = np.sin(2 * np.pi * 2400 * t) * np.exp(-60 * t) * 0.3
        return self._array_to_sound(wave, volume=0.30)

    def _synth_explosion(self):
        duration = 0.8
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        env = np.exp(-4.5 * t)
        sub_bass = np.sin(2 * np.pi * 45 * t) * env
        wave = (noise * 0.75 + sub_bass * 0.6) * env
        return self._array_to_sound(wave, volume=0.55)

    def _synth_hit(self):
        duration = 0.12
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = np.sin(2 * np.pi * 320 * t) * np.exp(-30 * t) * 0.35
        return self._array_to_sound(wave, volume=0.30)

    def _synth_pickup(self):
        duration = 0.2
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = np.sin(2 * np.pi * 880 * t) * np.linspace(0.4, 0.0, len(t))
        return self._array_to_sound(wave, volume=0.30)

    def play(self, name):
        if self.muted or not AUDIO_ENABLED:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted


# ---------------------------------------------------------------------------
# PARTICLES & COMBAT FX
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
        self.radius = max(0.4, self.radius - 0.04)
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


class BloodDecal:
    """Persistent footprint/blood marks on the battlefield floor."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(5, 11)
        self.color = (random.randint(120, 160), 20, 25, random.randint(110, 180))

    def draw(self, surface):
        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.radius, self.radius), self.radius)
        surface.blit(surf, (self.x - self.radius, self.y - self.radius))


class ShellCasing:
    """Brass cartridges popping out of firearms."""
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        # Eject perpendicular to aiming angle
        eject_angle = angle + math.pi / 2 + random.uniform(-0.3, 0.3)
        spd = random.uniform(2.5, 4.5)
        self.vx = math.cos(eject_angle) * spd
        self.vy = math.sin(eject_angle) * spd
        self.alpha = 240
        self.rot = random.uniform(0, 360)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.88
        self.vy *= 0.88
        self.alpha = max(0, self.alpha - 2.5)
        return self.alpha > 0

    def draw(self, surface):
        surf = pygame.Surface((6, 3), pygame.SRCALPHA)
        surf.fill((215, 185, 60, int(self.alpha)))
        surface.blit(surf, (self.x - 3, self.y - 1))


class FloatingText:
    def __init__(self, text, x, y, color=COLOR_GOLD, size=20, duration=45):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont("Impact, Arial Black", size)
        self.lifetime = duration
        self.max_lifetime = duration

    def update(self):
        self.y -= 0.9
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        txt = self.font.render(self.text, True, self.color)
        txt.set_alpha(alpha)
        shadow = self.font.render(self.text, True, (0, 0, 0))
        shadow.set_alpha(int(alpha * 0.75))
        surface.blit(shadow, (self.x - txt.get_width() // 2 + 2, self.y + 2))
        surface.blit(txt, (self.x - txt.get_width() // 2, self.y))


# ---------------------------------------------------------------------------
# WEAPONRY ARSENAL
# ---------------------------------------------------------------------------
WEAPONS = {
    "Pistol": {
        "name": "9mm Tactical", "mag_size": 12, "damage": 28, "fire_delay": 14,
        "spread": 0.04, "pellets": 1, "speed": 22.0, "reload_time": 50, "auto": False,
        "ammo_type": "9mm", "color": (230, 230, 230)
    },
    "Assault Rifle": {
        "name": "M4A1 Carbine", "mag_size": 30, "damage": 34, "fire_delay": 7,
        "spread": 0.08, "pellets": 1, "speed": 25.0, "reload_time": 75, "auto": True,
        "ammo_type": "5.56mm", "color": (70, 75, 85)
    },
    "Shotgun": {
        "name": "12-Gauge Breacher", "mag_size": 8, "damage": 18, "fire_delay": 32,
        "spread": 0.22, "pellets": 7, "speed": 20.0, "reload_time": 95, "auto": False,
        "ammo_type": "12G", "color": (50, 50, 55)
    },
    "Sniper": {
        "name": ".50 Cal Marksman", "mag_size": 5, "damage": 160, "fire_delay": 45,
        "spread": 0.01, "pellets": 1, "speed": 34.0, "reload_time": 90, "auto": False,
        "ammo_type": ".50", "color": (40, 45, 50)
    }
}


# ---------------------------------------------------------------------------
# BULLETS & FRAG GRENADES
# ---------------------------------------------------------------------------
class Bullet:
    def __init__(self, x, y, angle, speed, damage, is_player=True):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.damage = damage
        self.is_player = is_player
        self.lifetime = 55

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        color = (255, 235, 120) if self.is_player else (255, 60, 60)
        # Bullet streak line
        tail_x = self.x - self.vx * 0.45
        tail_y = self.y - self.vy * 0.45
        pygame.draw.line(surface, color, (tail_x, tail_y), (self.x, self.y), 3)


class FragGrenade:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        angle = math.atan2(target_y - y, target_x - x)
        dist = min(280, math.hypot(target_x - x, target_y - y))
        spd = dist / 28.0
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd
        self.fuse = 60  # 1 second fuse

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.92
        self.vy *= 0.92
        self.fuse -= 1
        return self.fuse > 0

    def draw(self, surface):
        # Round dark green canister with pulsing red blinker
        pygame.draw.circle(surface, (45, 75, 45), (int(self.x), int(self.y)), 6)
        pygame.draw.circle(surface, (25, 45, 25), (int(self.x), int(self.y)), 6, 2)
        if (self.fuse // 6) % 2 == 0:
            pygame.draw.circle(surface, (255, 40, 40), (int(self.x), int(self.y)), 2)


# ---------------------------------------------------------------------------
# TACTICAL OBSTACLES & COVER
# ---------------------------------------------------------------------------
class Obstacle:
    def __init__(self, x, y, width, height, obs_type="wall"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = obs_type  # 'wall', 'sandbag', 'crate'
        self.health = 80 if obs_type == 'crate' else 9999

    def draw(self, surface):
        if self.type == 'wall':
            # Solid concrete bunker wall
            pygame.draw.rect(surface, COLOR_WALL, self.rect, border_radius=4)
            pygame.draw.rect(surface, COLOR_WALL_TOP, (self.rect.x, self.rect.y, self.rect.width, 6), border_radius=4)
            pygame.draw.rect(surface, (40, 45, 55), self.rect, 2, border_radius=4)

        elif self.type == 'sandbag':
            # Low cover sandbag barrier
            pygame.draw.rect(surface, COLOR_SANDBAG, self.rect, border_radius=5)
            # Bag seams
            for x in range(self.rect.x + 14, self.rect.right - 10, 16):
                pygame.draw.line(surface, (120, 100, 65), (x, self.rect.y), (x, self.rect.bottom), 2)
            pygame.draw.rect(surface, (110, 90, 55), self.rect, 2, border_radius=5)

        elif self.type == 'crate':
            # Destructible wooden supply crate
            pygame.draw.rect(surface, COLOR_CRATE, self.rect, border_radius=3)
            # Diagonal cross braces
            pygame.draw.line(surface, COLOR_CRATE_BORDER, self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(surface, COLOR_CRATE_BORDER, self.rect.topright, self.rect.bottomleft, 2)
            pygame.draw.rect(surface, COLOR_CRATE_BORDER, self.rect, 3, border_radius=3)


# ---------------------------------------------------------------------------
# LOOT PICKUPS (Ammo & Medkits)
# ---------------------------------------------------------------------------
class Pickup:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.type = p_type  # 'medkit', 'ammo', 'vest'
        self.tick = random.randint(0, 50)

    def draw(self, surface):
        self.tick += 1
        cx, cy = int(self.x), int(self.y)
        glow = pygame.Surface((36, 36), pygame.SRCALPHA)
        color = COLOR_NEON_GREEN if self.type == 'medkit' else (COLOR_GOLD if self.type == 'ammo' else COLOR_NEON_BLUE)
        pygame.draw.circle(glow, (*color, 65 + int(25 * math.sin(self.tick * 0.15))), (18, 18), 16)
        surface.blit(glow, (cx - 18, cy - 18))

        if self.type == 'medkit':
            # White box with red medical cross
            pygame.draw.rect(surface, (245, 245, 250), (cx - 9, cy - 9, 18, 18), border_radius=3)
            pygame.draw.rect(surface, (230, 40, 40), (cx - 2, cy - 7, 4, 14))
            pygame.draw.rect(surface, (230, 40, 40), (cx - 7, cy - 2, 14, 4))
        elif self.type == 'ammo':
            # Green military ammo can with brass bullet icon
            pygame.draw.rect(surface, (50, 75, 45), (cx - 10, cy - 8, 20, 16), border_radius=3)
            pygame.draw.rect(surface, (215, 185, 60), (cx - 4, cy - 4, 8, 8), border_radius=1)
        elif self.type == 'vest':
            # Blue armor vest
            pygame.draw.rect(surface, (20, 45, 80), (cx - 9, cy - 8, 18, 16), border_radius=4)
            pygame.draw.line(surface, COLOR_NEON_BLUE, (cx - 9, cy), (cx + 9, cy), 2)

    def get_hitbox(self):
        return pygame.Rect(self.x - 12, self.y - 12, 24, 24)


# ---------------------------------------------------------------------------
# PROCEDURAL TOP-DOWN HUMAN SOLDIER RENDERER
# ---------------------------------------------------------------------------
class HumanRenderer:
    """Renders authentic 2D top-down human commando with limbs and firearms."""
    @staticmethod
    def draw_soldier(surface, x, y, angle, uniform_color, helmet_color, weapon_name, leg_cycle=0.0, is_reloading=False):
        # Base dimensions
        radius = 16
        cx, cy = int(x), int(y)

        # 1. Animated Legs (stride back and forth when moving)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        perp_x = -sin_a
        perp_y = cos_a

        leg_offset = math.sin(leg_cycle) * 7.0
        # Left boot
        l_bx = cx - cos_a * 8 + perp_x * 9 + cos_a * leg_offset
        l_by = cy - sin_a * 8 + perp_y * 9 + sin_a * leg_offset
        pygame.draw.circle(surface, (20, 20, 25), (int(l_bx), int(l_by)), 5)

        # Right boot
        r_bx = cx - cos_a * 8 - perp_x * 9 - cos_a * leg_offset
        r_by = cy - sin_a * 8 - perp_y * 9 - sin_a * leg_offset
        pygame.draw.circle(surface, (20, 20, 25), (int(r_bx), int(r_by)), 5)

        # 2. Shoulders & Torso
        shoulder_span = 14
        left_sh_x = cx + perp_x * shoulder_span
        left_sh_y = cy + perp_y * shoulder_span
        right_sh_x = cx - perp_x * shoulder_span
        right_sh_y = cy - perp_y * shoulder_span

        # Body ellipse
        torso_pts = [
            (int(left_sh_x - cos_a * 4), int(left_sh_y - sin_a * 4)),
            (int(right_sh_x - cos_a * 4), int(right_sh_y - sin_a * 4)),
            (int(right_sh_x + cos_a * 6), int(right_sh_y + sin_a * 6)),
            (int(left_sh_x + cos_a * 6), int(left_sh_y + sin_a * 6)),
        ]
        pygame.draw.polygon(surface, uniform_color, torso_pts)

        # Tactical Kevlar Vest over chest
        vest_pts = [
            (int(left_sh_x * 0.7 + cx * 0.3), int(left_sh_y * 0.7 + cy * 0.3)),
            (int(right_sh_x * 0.7 + cx * 0.3), int(right_sh_y * 0.7 + cy * 0.3)),
            (int(cx + cos_a * 5), int(cy + sin_a * 5)),
            (int(cx - cos_a * 5), int(cy - sin_a * 5)),
        ]
        pygame.draw.polygon(surface, (30, 35, 45), vest_pts)

        # 3. Arms & Equipped Weapon
        gun_color = WEAPONS[weapon_name]["color"]
        gun_length = 26 if weapon_name == "Sniper" else (20 if weapon_name in ["Assault Rifle", "Shotgun"] else 12)

        # Gun barrel tip
        barrel_x = cx + cos_a * (gun_length + 10)
        barrel_y = cy + sin_a * (gun_length + 10)

        # Draw gun barrel
        pygame.draw.line(surface, gun_color, (cx + cos_a * 8, cy + sin_a * 8), (barrel_x, barrel_y), 4)

        # Hands gripping firearm
        h1_x = cx + cos_a * 14 + perp_x * 5
        h1_y = cy + sin_a * 14 + perp_y * 5
        h2_x = cx + cos_a * 19 - perp_x * 2
        h2_y = cy + sin_a * 19 - perp_y * 2
        pygame.draw.circle(surface, (215, 175, 140), (int(h1_x), int(h1_y)), 3)
        pygame.draw.circle(surface, (215, 175, 140), (int(h2_x), int(h2_y)), 3)

        # 4. Tactical Helmet & Head
        pygame.draw.circle(surface, helmet_color, (cx, cy), radius - 3)
        # Helmet rim / brim
        pygame.draw.arc(surface, (20, 20, 25), (cx - radius + 3, cy - radius + 3, (radius - 3) * 2, (radius - 3) * 2), angle - 0.9, angle + 0.9, 3)
        # Goggles / Visor
        visor_x = cx + cos_a * (radius - 5)
        visor_y = cy + sin_a * (radius - 5)
        pygame.draw.circle(surface, (0, 210, 255), (int(visor_x), int(visor_y)), 3)

        if is_reloading:
            # Show "RELOADING" text overhead
            font = pygame.font.SysFont("Arial Black", 10, bold=True)
            txt = font.render("RELOADING", True, COLOR_GOLD)
            surface.blit(txt, (cx - txt.get_width() // 2, cy - 28))


# ---------------------------------------------------------------------------
# PLAYER COMMANDO CLASS
# ---------------------------------------------------------------------------
class PlayerCommando:
    def __init__(self):
        self.width = 34
        self.height = 34
        self.reset()

    def reset(self):
        self.x = 120.0
        self.y = HEIGHT // 2
        self.angle = 0.0
        self.speed = 4.2
        self.leg_cycle = 0.0

        # Health & Armor
        self.max_health = 100.0
        self.health = 100.0
        self.max_armor = 100.0
        self.armor = 100.0

        # Arsenal & Ammo
        self.weapon_order = ["Pistol", "Assault Rifle", "Shotgun", "Sniper"]
        self.current_weapon_idx = 0
        self.magazines = {w: WEAPONS[w]["mag_size"] for w in WEAPONS}
        self.reserves = {
            "Pistol": 999,  # Infinite sidearm
            "Assault Rifle": 120,
            "Shotgun": 32,
            "Sniper": 15
        }

        self.fire_timer = 0
        self.reload_timer = 0
        self.grenades = 3
        self.invulnerable = 0

    @property
    def current_weapon(self):
        return self.weapon_order[self.current_weapon_idx]

    def update(self, keys, mouse_pos, obstacles, bullets, particles, shells, audio):
        # 1. Aim toward mouse cursor
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)

        # 2. Movement
        mx, my = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            my -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            my += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            mx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            mx += 1

        is_moving = (mx != 0 or my != 0)
        if is_moving:
            if mx != 0 and my != 0:
                mx *= 0.7071
                my *= 0.7071

            # Axis-independent collision resolution with obstacles
            new_x = self.x + mx * self.speed
            new_rect_x = pygame.Rect(new_x - 16, self.y - 16, 32, 32)
            can_move_x = True
            for obs in obstacles:
                if new_rect_x.colliderect(obs.rect):
                    can_move_x = False
                    break
            if can_move_x:
                self.x = max(20, min(WIDTH - 20, new_x))

            new_y = self.y + my * self.speed
            new_rect_y = pygame.Rect(self.x - 16, new_y - 16, 32, 32)
            can_move_y = True
            for obs in obstacles:
                if new_rect_y.colliderect(obs.rect):
                    can_move_y = False
                    break
            if can_move_y:
                self.y = max(20, min(HEIGHT - 20, new_y))

            self.leg_cycle += 0.28

        # 3. Weapon Timers
        if self.fire_timer > 0:
            self.fire_timer -= 1

        if self.reload_timer > 0:
            self.reload_timer -= 1
            if self.reload_timer == 0:
                # Complete reload
                wpn = self.current_weapon
                mag_max = WEAPONS[wpn]["mag_size"]
                needed = mag_max - self.magazines[wpn]
                avail = min(needed, self.reserves[wpn])
                self.magazines[wpn] += avail
                if wpn != "Pistol":
                    self.reserves[wpn] -= avail

        if self.invulnerable > 0:
            self.invulnerable -= 1

    def start_reload(self, audio):
        wpn = self.current_weapon
        if self.magazines[wpn] < WEAPONS[wpn]["mag_size"] and self.reserves[wpn] > 0 and self.reload_timer == 0:
            self.reload_timer = WEAPONS[wpn]["reload_time"]
            audio.play('reload')

    def switch_weapon(self, index, audio):
        idx = index % len(self.weapon_order)
        if idx != self.current_weapon_idx:
            self.current_weapon_idx = idx
            self.reload_timer = 0
            audio.play('reload')

    def shoot(self, bullets, particles, shells, audio):
        if self.reload_timer > 0:
            return False

        wpn_data = WEAPONS[self.current_weapon]
        if self.magazines[self.current_weapon] <= 0:
            audio.play('empty')
            self.start_reload(audio)
            return False

        if self.fire_timer <= 0:
            self.magazines[self.current_weapon] -= 1
            self.fire_timer = wpn_data["fire_delay"]

            # Sound
            if self.current_weapon == "Pistol":
                audio.play('pistol')
            elif self.current_weapon == "Assault Rifle":
                audio.play('rifle')
            elif self.current_weapon == "Shotgun":
                audio.play('shotgun')
            elif self.current_weapon == "Sniper":
                audio.play('sniper')

            # Muzzle tip origin
            muzzle_dist = 30
            mx = self.x + math.cos(self.angle) * muzzle_dist
            my = self.y + math.sin(self.angle) * muzzle_dist

            # Eject brass casing
            shells.append(ShellCasing(self.x, self.y, self.angle))

            # Muzzle Flash Particles
            for _ in range(7):
                particles.append(Particle(mx, my, random.uniform(-1, 1) + math.cos(self.angle) * 3, random.uniform(-1, 1) + math.sin(self.angle) * 3, (255, random.randint(160, 240), 40), random.randint(3, 7), 28))

            # Spawn Bullets
            for _ in range(wpn_data["pellets"]):
                spread = random.uniform(-wpn_data["spread"], wpn_data["spread"])
                b_ang = self.angle + spread
                bullets.append(Bullet(mx, my, b_ang, wpn_data["speed"], wpn_data["damage"], is_player=True))

            return True
        return False

    def throw_grenade(self, target_x, target_y, grenades_list, audio):
        if self.grenades > 0:
            self.grenades -= 1
            grenades_list.append(FragGrenade(self.x, self.y, target_x, target_y))
            return True
        return False

    def take_damage(self, amount, audio):
        if self.invulnerable > 0:
            return False
        audio.play('hit')
        self.invulnerable = 15

        # Armor absorbs 65% of damage first
        if self.armor > 0:
            absorbed = min(self.armor, amount * 0.65)
            self.armor -= absorbed
            health_dmg = amount - absorbed
            self.health = max(0, self.health - health_dmg)
        else:
            self.health = max(0, self.health - amount)

        return self.health <= 0

    def draw(self, surface):
        if self.invulnerable > 0 and (self.invulnerable // 3) % 2 == 1:
            return
        HumanRenderer.draw_soldier(
            surface, self.x, self.y, self.angle,
            uniform_color=(35, 60, 95),  # Navy Commando uniform
            helmet_color=(25, 45, 70),
            weapon_name=self.current_weapon,
            leg_cycle=self.leg_cycle,
            is_reloading=(self.reload_timer > 0)
        )

    def get_hitbox(self):
        return pygame.Rect(self.x - 14, self.y - 14, 28, 28)


# ---------------------------------------------------------------------------
# ENEMY SOLDIER CLASS
# ---------------------------------------------------------------------------
ENEMY_TYPES = {
    "Grunt": {"weapon": "Assault Rifle", "health": 75, "speed": 2.2, "color": (50, 75, 50), "points": 150},
    "Breacher": {"weapon": "Shotgun", "health": 110, "speed": 2.6, "color": (75, 55, 45), "points": 250},
    "Sniper": {"weapon": "Sniper", "health": 60, "speed": 1.7, "color": (65, 70, 75), "points": 350},
    "Juggernaut": {"weapon": "Assault Rifle", "health": 450, "speed": 1.4, "color": (30, 30, 35), "points": 1000},
}

class EnemySoldier:
    def __init__(self, enemy_type, x, y):
        self.type = enemy_type
        self.data = ENEMY_TYPES[enemy_type]
        self.x = x
        self.y = y
        self.angle = random.uniform(0, math.pi * 2)
        self.health = self.data["health"]
        self.max_health = self.data["health"]
        self.speed = self.data["speed"]
        self.weapon_name = self.data["weapon"]
        self.shoot_cooldown = random.randint(40, 90)
        self.leg_cycle = 0.0
        self.state = "patrol"  # 'patrol', 'combat'
        self.patrol_timer = random.randint(30, 90)

    def update(self, player, obstacles, bullets, particles, shells, audio):
        # Line of sight check to player
        dist_to_player = math.hypot(player.x - self.x, player.y - self.y)
        dx = player.x - self.x
        dy = player.y - self.y

        # Aim towards player if in combat range
        target_angle = math.atan2(dy, dx)
        self.angle += (target_angle - self.angle) * 0.12

        # Check line of sight (no blocking wall)
        has_los = True
        for obs in obstacles:
            if obs.type == 'wall' and obs.rect.clipline((self.x, self.y), (player.x, player.y)):
                has_los = False
                break

        # AI Behavior
        if has_los or dist_to_player < 350:
            self.state = "combat"

        if self.state == "combat":
            # Preferred engagement distance
            preferred_dist = 360 if self.type == "Sniper" else (110 if self.type == "Breacher" else 220)

            move_x, move_y = 0, 0
            if dist_to_player > preferred_dist + 40:
                # Advance
                move_x = math.cos(self.angle)
                move_y = math.sin(self.angle)
            elif dist_to_player < preferred_dist - 40:
                # Retreat / keep distance
                move_x = -math.cos(self.angle)
                move_y = -math.sin(self.angle)
            else:
                # Strafe sideways
                move_x = -math.sin(self.angle) * 0.8
                move_y = math.cos(self.angle) * 0.8

            # Try moving with collision
            new_x = self.x + move_x * self.speed
            new_y = self.y + move_y * self.speed
            rect_try = pygame.Rect(new_x - 14, new_y - 14, 28, 28)
            can_move = True
            for obs in obstacles:
                if rect_try.colliderect(obs.rect):
                    can_move = False
                    break
            if can_move:
                self.x = max(20, min(WIDTH - 20, new_x))
                self.y = max(20, min(HEIGHT - 20, new_y))
                self.leg_cycle += 0.22

            # Shoot at player if clear line of sight
            if has_los:
                self.shoot_cooldown -= 1
                if self.shoot_cooldown <= 0:
                    self.shoot(bullets, particles, shells, audio)
                    base_delay = 55 if self.type == "Sniper" else (40 if self.type == "Breacher" else 28)
                    self.shoot_cooldown = base_delay + random.randint(0, 30)

        elif self.state == "patrol":
            self.patrol_timer -= 1
            if self.patrol_timer <= 0:
                self.patrol_timer = random.randint(50, 100)
                self.angle = random.uniform(0, math.pi * 2)

    def shoot(self, bullets, particles, shells, audio):
        wpn_data = WEAPONS[self.weapon_name]
        mx = self.x + math.cos(self.angle) * 26
        my = self.y + math.sin(self.angle) * 26

        shells.append(ShellCasing(self.x, self.y, self.angle))
        if self.weapon_name == "Sniper":
            audio.play('sniper')
        elif self.weapon_name == "Shotgun":
            audio.play('shotgun')
        else:
            audio.play('rifle')

        for _ in range(wpn_data["pellets"]):
            spread = random.uniform(-wpn_data["spread"] * 1.5, wpn_data["spread"] * 1.5)
            bullets.append(Bullet(mx, my, self.angle + spread, wpn_data["speed"] * 0.85, wpn_data["damage"] * 0.65, is_player=False))

    def draw(self, surface):
        HumanRenderer.draw_soldier(
            surface, self.x, self.y, self.angle,
            uniform_color=self.data["color"],
            helmet_color=(35, 45, 35),
            weapon_name=self.weapon_name,
            leg_cycle=self.leg_cycle
        )

        # Health bar above enemy head
        if self.health < self.max_health:
            bw = 32 if self.type != "Juggernaut" else 50
            bx = self.x - bw // 2
            by = self.y - 24
            pygame.draw.rect(surface, (20, 20, 25), (bx, by, bw, 4))
            fill = max(0, int((self.health / self.max_health) * bw))
            pygame.draw.rect(surface, COLOR_NEON_RED, (bx, by, fill, 4))

    def get_hitbox(self):
        return pygame.Rect(self.x - 14, self.y - 14, 28, 28)


# ---------------------------------------------------------------------------
# MAIN GAME CONTROLLER
# ---------------------------------------------------------------------------
class CommandoGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("OPERATION VANGUARD: Tactical Commando")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_huge = pygame.font.SysFont("Impact, Arial Black", 64)
        self.font_large = pygame.font.SysFont("Impact, Arial Black", 36)
        self.font_medium = pygame.font.SysFont("Trebuchet MS, Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Trebuchet MS, Arial", 16, bold=True)
        self.font_digital = pygame.font.SysFont("Consolas, Courier", 26, bold=True)

        self.audio = GunAudioSynth()

        self.high_score = 0
        self.high_wave = 1
        self.load_save_data()

        self.state = 'MENU'
        self.player = PlayerCommando()
        self.enemies = []
        self.obstacles = []
        self.bullets = []
        self.grenades = []
        self.pickups = []
        self.particles = []
        self.shells = []
        self.decals = []
        self.notices = []

        self.score = 0
        self.wave = 1
        self.enemies_remaining = 0
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

    def build_arena_map(self):
        self.obstacles.clear()
        # Outer boundary walls
        self.obstacles.append(Obstacle(0, 0, WIDTH, 12, 'wall'))
        self.obstacles.append(Obstacle(0, HEIGHT - 12, WIDTH, 12, 'wall'))
        self.obstacles.append(Obstacle(0, 0, 12, HEIGHT, 'wall'))
        self.obstacles.append(Obstacle(WIDTH - 12, 0, 12, HEIGHT, 'wall'))

        # Concrete Bunkers & Sandbag barriers
        self.obstacles.append(Obstacle(240, 150, 18, 140, 'wall'))
        self.obstacles.append(Obstacle(240, 410, 18, 140, 'wall'))

        self.obstacles.append(Obstacle(640, 150, 18, 140, 'wall'))
        self.obstacles.append(Obstacle(640, 410, 18, 140, 'wall'))

        # Center Sandbags & Pillars
        self.obstacles.append(Obstacle(430, 220, 40, 40, 'wall'))
        self.obstacles.append(Obstacle(430, 440, 40, 40, 'wall'))

        self.obstacles.append(Obstacle(360, 330, 80, 20, 'sandbag'))
        self.obstacles.append(Obstacle(460, 330, 80, 20, 'sandbag'))

        # Destructible Supply Crates
        crate_positions = [
            (180, 120), (180, 540), (700, 120), (700, 540),
            (320, 210), (560, 450), (435, 330)
        ]
        for cx, cy in crate_positions:
            self.obstacles.append(Obstacle(cx, cy, 30, 30, 'crate'))

    def start_new_game(self):
        self.player.reset()
        self.enemies.clear()
        self.bullets.clear()
        self.grenades.clear()
        self.pickups.clear()
        self.particles.clear()
        self.shells.clear()
        self.decals.clear()
        self.notices.clear()

        self.score = 0
        self.wave = 1
        self.screen_shake = 0

        self.build_arena_map()
        self.spawn_wave(self.wave)

        self.state = 'PLAYING'

    def spawn_wave(self, wave_num):
        self.wave = wave_num
        self.notices.append(FloatingText(f"--- WAVE {self.wave}: ENEMY ASSAULT ---", WIDTH // 2, HEIGHT // 2 - 60, COLOR_GOLD, size=30, duration=75))

        # Enemy composition
        num_grunts = 3 + wave_num * 2
        num_breachers = 1 + wave_num // 2
        num_snipers = wave_num // 2
        num_juggernauts = 1 if wave_num % 4 == 0 else 0

        spawn_pool = []
        spawn_pool.extend(["Grunt"] * num_grunts)
        spawn_pool.extend(["Breacher"] * num_breachers)
        spawn_pool.extend(["Sniper"] * num_snipers)
        spawn_pool.extend(["Juggernaut"] * num_juggernauts)

        self.enemies_remaining = len(spawn_pool)

        # Spawn around edges away from player
        for etype in spawn_pool:
            side = random.choice(['top', 'bottom', 'right'])
            if side == 'top':
                ex = random.randint(400, WIDTH - 50)
                ey = random.randint(30, 90)
            elif side == 'bottom':
                ex = random.randint(400, WIDTH - 50)
                ey = random.randint(HEIGHT - 90, HEIGHT - 30)
            else:
                ex = random.randint(WIDTH - 120, WIDTH - 40)
                ey = random.randint(80, HEIGHT - 80)

            self.enemies.append(EnemySoldier(etype, ex, ey))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

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
                        elif event.key == pygame.K_r:
                            self.player.start_reload(self.audio)
                        elif event.key == pygame.K_1:
                            self.player.switch_weapon(0, self.audio)
                        elif event.key == pygame.K_2:
                            self.player.switch_weapon(1, self.audio)
                        elif event.key == pygame.K_3:
                            self.player.switch_weapon(2, self.audio)
                        elif event.key == pygame.K_4:
                            self.player.switch_weapon(3, self.audio)
                        elif event.key == pygame.K_g:
                            self.player.throw_grenade(mouse_pos[0], mouse_pos[1], self.grenades, self.audio)

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
                    if event.button == 1:  # Left Click = Shoot
                        did_shoot = self.player.shoot(self.bullets, self.particles, self.shells, self.audio)
                        if did_shoot:
                            self.screen_shake = 4 if self.player.current_weapon != "Sniper" else 8
                    elif event.button == 3:  # Right Click = Throw Grenade
                        self.player.throw_grenade(mouse_pos[0], mouse_pos[1], self.grenades, self.audio)
                    elif event.button == 4:  # Wheel Up
                        self.player.switch_weapon(self.player.current_weapon_idx - 1, self.audio)
                    elif event.button == 5:  # Wheel Down
                        self.player.switch_weapon(self.player.current_weapon_idx + 1, self.audio)

            # Auto-fire for Assault Rifle if holding mouse button
            if self.state == 'PLAYING' and mouse_pressed[0] and WEAPONS[self.player.current_weapon]["auto"]:
                did_shoot = self.player.shoot(self.bullets, self.particles, self.shells, self.audio)
                if did_shoot:
                    self.screen_shake = 3

            # States update & render
            if self.state == 'MENU':
                self.draw_menu()
            elif self.state == 'PLAYING':
                self.update_playing(keys, mouse_pos)
                self.draw_playing(mouse_pos)
            elif self.state == 'PAUSED':
                self.draw_playing(mouse_pos)
                self.draw_paused_overlay()
            elif self.state == 'GAMEOVER':
                self.update_gameover()
                self.draw_playing(mouse_pos)
                self.draw_gameover_overlay()

            pygame.display.flip()

        self.save_data()
        pygame.quit()
        sys.exit()

    # -----------------------------------------------------------------------
    # PLAYING STATE UPDATE & DRAW
    # -----------------------------------------------------------------------
    def update_playing(self, keys, mouse_pos):
        # Update Player
        self.player.update(keys, mouse_pos, self.obstacles, self.bullets, self.particles, self.shells, self.audio)

        # Update Enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.obstacles, self.bullets, self.particles, self.shells, self.audio)
            if enemy.health <= 0:
                self.kill_enemy(enemy)

        # Check wave clear
        if len(self.enemies) == 0:
            self.spawn_wave(self.wave + 1)

        # Update Bullets
        for b in self.bullets[:]:
            alive = b.update()
            if not alive:
                self.bullets.remove(b)
                continue

            # Collision with obstacles
            b_hit = False
            for obs in self.obstacles:
                if obs.rect.collidepoint(b.x, b.y):
                    b_hit = True
                    # Spark particles
                    for _ in range(4):
                        self.particles.append(Particle(b.x, b.y, random.uniform(-3, 3), random.uniform(-3, 3), (255, 210, 100), 2, 28))
                    if obs.type == 'crate':
                        obs.health -= b.damage
                        if obs.health <= 0:
                            self.destroy_crate(obs)
                    break

            if b_hit:
                if b in self.bullets:
                    self.bullets.remove(b)
                continue

            # Player bullet hits enemy
            if b.is_player:
                for enemy in self.enemies:
                    if enemy.get_hitbox().collidepoint(b.x, b.y):
                        enemy.health -= b.damage
                        # Blood splatter
                        self.decals.append(BloodDecal(b.x, b.y))
                        for _ in range(6):
                            self.particles.append(Particle(b.x, b.y, random.uniform(-3, 3), random.uniform(-3, 3), (190, 20, 20), 3, 22))
                        if enemy.health <= 0:
                            self.kill_enemy(enemy)
                        if b in self.bullets:
                            self.bullets.remove(b)
                        break
            else:
                # Enemy bullet hits player
                if self.player.get_hitbox().collidepoint(b.x, b.y):
                    self.screen_shake = 12
                    is_dead = self.player.take_damage(b.damage, self.audio)
                    self.decals.append(BloodDecal(b.x, b.y))
                    for _ in range(6):
                        self.particles.append(Particle(b.x, b.y, random.uniform(-3, 3), random.uniform(-3, 3), (190, 20, 20), 3, 22))
                    if b in self.bullets:
                        self.bullets.remove(b)
                    if is_dead:
                        self.trigger_game_over()
                        return

        # Update Frag Grenades
        for g in self.grenades[:]:
            alive = g.update()
            if not alive:
                self.detonate_grenade(g)
                self.grenades.remove(g)

        # Update Pickups
        p_hitbox = self.player.get_hitbox()
        for pu in self.pickups[:]:
            if p_hitbox.colliderect(pu.get_hitbox()):
                self.collect_pickup(pu)
                self.pickups.remove(pu)

        # Update Shells, Particles, Notices
        self.shells = [s for s in self.shells if s.update()]
        self.particles = [pt for pt in self.particles if pt.update()]
        self.notices = [nt for nt in self.notices if nt.update()]

        if self.screen_shake > 0:
            self.screen_shake -= 1

    def destroy_crate(self, crate):
        self.audio.play('hit')
        # Wood splinters
        for _ in range(14):
            self.particles.append(Particle(crate.rect.centerx, crate.rect.centery, random.uniform(-4, 4), random.uniform(-4, 4), COLOR_CRATE, random.randint(2, 5), 18))

        # Drop loot
        loot = random.choices(['medkit', 'ammo', 'vest', None], weights=[0.35, 0.35, 0.15, 0.15])[0]
        if loot:
            self.pickups.append(Pickup(crate.rect.centerx, crate.rect.centery, loot))

        if crate in self.obstacles:
            self.obstacles.remove(crate)

    def detonate_grenade(self, g):
        self.audio.play('explosion')
        self.screen_shake = 22
        # Blast shockwave & fire particles
        for _ in range(35):
            self.particles.append(Particle(g.x, g.y, random.uniform(-6, 6), random.uniform(-6, 6), random.choice([(255, 120, 20), (255, 60, 40), (240, 210, 40)]), random.randint(3, 8), 16))
        for _ in range(20):
            self.particles.append(Particle(g.x, g.y, random.uniform(-3, 3), random.uniform(-3, 3), (70, 70, 75), random.randint(4, 9), 12))

        # Area of Effect damage (radius 140px)
        radius = 140
        for enemy in self.enemies[:]:
            dist = math.hypot(enemy.x - g.x, enemy.y - g.y)
            if dist < radius:
                dmg = int((1.0 - dist / radius) * 240)
                enemy.health -= dmg
                if enemy.health <= 0:
                    self.kill_enemy(enemy)

        # Damage player if caught in blast
        p_dist = math.hypot(self.player.x - g.x, self.player.y - g.y)
        if p_dist < radius:
            p_dmg = int((1.0 - p_dist / radius) * 120)
            is_dead = self.player.take_damage(p_dmg, self.audio)
            if is_dead:
                self.trigger_game_over()

    def kill_enemy(self, enemy):
        self.audio.play('hit')
        self.score += enemy.data["points"]
        self.decals.append(BloodDecal(enemy.x, enemy.y))

        # Blood & casing particles
        for _ in range(12):
            self.particles.append(Particle(enemy.x, enemy.y, random.uniform(-4, 4), random.uniform(-4, 4), (180, 20, 20), 4, 18))

        # Chance to drop ammo or medkit
        if random.random() < 0.35:
            ptype = random.choice(['ammo', 'medkit'])
            self.pickups.append(Pickup(enemy.x, enemy.y, ptype))

        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def collect_pickup(self, pu):
        self.audio.play('pickup')
        if pu.type == 'medkit':
            self.player.health = min(self.player.max_health, self.player.health + 45)
            self.notices.append(FloatingText("+45 HEALTH RESTORED", pu.x, pu.y, COLOR_NEON_GREEN))
        elif pu.type == 'ammo':
            self.player.reserves["Assault Rifle"] += 60
            self.player.reserves["Shotgun"] += 16
            self.player.reserves["Sniper"] += 8
            self.player.grenades = min(5, self.player.grenades + 1)
            self.notices.append(FloatingText("+AMMO & GRENADE RESTOCKED", pu.x, pu.y, COLOR_GOLD))
        elif pu.type == 'vest':
            self.player.armor = self.player.max_armor
            self.notices.append(FloatingText("+BODY ARMOR REPAIRED", pu.x, pu.y, COLOR_NEON_BLUE))

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

    def draw_playing(self, mouse_pos):
        shake_x, shake_y = 0, 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)

        surf = pygame.Surface((WIDTH, HEIGHT))

        # 1. Floor Tile Grid
        surf.fill(COLOR_FLOOR)
        tile_size = 50
        for x in range(0, WIDTH, tile_size):
            pygame.draw.line(surf, COLOR_FLOOR_GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, tile_size):
            pygame.draw.line(surf, COLOR_FLOOR_GRID, (0, y), (WIDTH, y), 1)

        # 2. Blood Decals
        for d in self.decals:
            d.draw(surf)

        # 3. Shell Casings
        for s in self.shells:
            s.draw(surf)

        # 4. Obstacles (Sandbags & Crates)
        for obs in self.obstacles:
            obs.draw(surf)

        # 5. Pickups
        for pu in self.pickups:
            pu.draw(surf)

        # 6. Frag Grenades
        for g in self.grenades:
            g.draw(surf)

        # 7. Enemies
        for enemy in self.enemies:
            enemy.draw(surf)

        # 8. Player Commando
        self.player.draw(surf)

        # 9. Bullets
        for b in self.bullets:
            b.draw(surf)

        # 10. Particles & Notices
        for pt in self.particles:
            pt.draw(surf)
        for nt in self.notices:
            nt.draw(surf)

        # 11. HUD
        self.draw_hud(surf)

        # 12. Tactical Crosshair at cursor
        self.draw_crosshair(surf, mouse_pos[0], mouse_pos[1])

        self.screen.blit(surf, (shake_x, shake_y))

    def draw_crosshair(self, surface, x, y):
        # Precise tactical crosshair
        col = (255, 50, 50) if self.player.reload_timer > 0 else (0, 240, 255)
        pygame.draw.circle(surface, col, (x, y), 5, 1)
        pygame.draw.line(surface, col, (x - 12, y), (x - 6, y), 2)
        pygame.draw.line(surface, col, (x + 6, y), (x + 12, y), 2)
        pygame.draw.line(surface, col, (x, y - 12), (x, y - 6), 2)
        pygame.draw.line(surface, col, (x, y + 6), (x, y + 12), 2)

    def draw_hud(self, surface):
        # Top HUD Bar
        top_bar = pygame.Surface((WIDTH, 48), pygame.SRCALPHA)
        pygame.draw.rect(top_bar, COLOR_HUD_BG, (0, 0, WIDTH, 48))
        pygame.draw.line(top_bar, (50, 60, 75), (0, 47), (WIDTH, 47), 2)
        surface.blit(top_bar, (0, 0))

        # Score & Wave
        sc_val = self.font_digital.render(f"SCORE: {int(self.score):06d}", True, (255, 255, 255))
        surface.blit(sc_val, (24, 10))

        w_val = self.font_digital.render(f"WAVE {self.wave}  |  HOSTILES: {len(self.enemies)}", True, COLOR_GOLD)
        surface.blit(w_val, (WIDTH // 2 - w_val.get_width() // 2, 10))

        g_val = self.font_digital.render(f"GRENADES (G/R-CLICK): {self.player.grenades}", True, (255, 120, 40))
        surface.blit(g_val, (WIDTH - g_val.get_width() - 24, 10))

        # Bottom-Left: Health & Kevlar Armor
        hb_x, hb_y, hb_w, hb_h = 24, HEIGHT - 65, 160, 16
        # Health bar
        pygame.draw.rect(surface, (25, 30, 40), (hb_x, hb_y, hb_w, hb_h), border_radius=3)
        h_fill = max(0, int((self.player.health / self.player.max_health) * hb_w))
        h_col = COLOR_NEON_GREEN if self.player.health > 40 else COLOR_NEON_RED
        pygame.draw.rect(surface, h_col, (hb_x, hb_y, h_fill, hb_h), border_radius=3)
        hl = self.font_small.render(f"HEALTH: {int(self.player.health)}%", True, (240, 245, 250))
        surface.blit(hl, (hb_x, hb_y - 18))

        # Armor bar
        pygame.draw.rect(surface, (25, 30, 40), (hb_x, hb_y + 22, hb_w, hb_h), border_radius=3)
        a_fill = max(0, int((self.player.armor / self.player.max_armor) * hb_w))
        pygame.draw.rect(surface, COLOR_NEON_BLUE, (hb_x, hb_y + 22, a_fill, hb_h), border_radius=3)
        al = self.font_small.render(f"KEVLAR: {int(self.player.armor)}%", True, (200, 225, 255))
        surface.blit(al, (hb_x + hb_w + 10, hb_y + 20))

        # Bottom-Right: Active Weapon & Ammo Display
        card_w, card_h = 240, 85
        cx = WIDTH - card_w - 24
        cy = HEIGHT - card_h - 15
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, COLOR_HUD_BG, (0, 0, card_w, card_h), border_radius=8)
        pygame.draw.rect(card_surf, (50, 60, 80), (0, 0, card_w, card_h), 2, border_radius=8)
        surface.blit(card_surf, (cx, cy))

        wpn = self.player.current_weapon
        wpn_name = self.font_medium.render(wpn.upper(), True, COLOR_GOLD)
        surface.blit(wpn_name, (cx + 16, cy + 10))

        mag = self.player.magazines[wpn]
        res = self.player.reserves[wpn]
        res_str = "INF" if wpn == "Pistol" else str(res)

        if self.player.reload_timer > 0:
            ammo_str = self.font_digital.render("RELOADING...", True, (255, 120, 40))
        else:
            ammo_str = self.font_digital.render(f"{mag} / {res_str}", True, (255, 255, 255))
        surface.blit(ammo_str, (cx + 16, cy + 42))

        keys_help = self.font_small.render("1-4: SWITCH  |  R: RELOAD", True, (140, 155, 175))
        surface.blit(keys_help, (cx + 16, cy + 64))

    # -----------------------------------------------------------------------
    # OVERLAYS (Paused & Game Over)
    # -----------------------------------------------------------------------
    def draw_paused_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((12, 16, 24, 200))
        self.screen.blit(overlay, (0, 0))

        title = self.font_huge.render("MISSION PAUSED", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

        info1 = self.font_medium.render("PRESS ESC TO RESUME MISSION", True, COLOR_NEON_BLUE)
        info2 = self.font_medium.render("PRESS R TO RESTART", True, COLOR_GOLD)
        info3 = self.font_medium.render("PRESS Q FOR MAIN MENU", True, (200, 205, 215))

        self.screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 + 0))
        self.screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 40))
        self.screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT // 2 + 80))

    def draw_gameover_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((25, 10, 10, 215))
        self.screen.blit(overlay, (0, 0))

        card_w, card_h = 520, 390
        cx = (WIDTH - card_w) // 2
        cy = (HEIGHT - card_h) // 2
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (18, 22, 32, 245), (0, 0, card_w, card_h), border_radius=12)
        pygame.draw.rect(card_surf, COLOR_NEON_RED, (0, 0, card_w, card_h), 2, border_radius=12)
        self.screen.blit(card_surf, (cx, cy))

        title = self.font_huge.render("COMMANDO KIA!", True, COLOR_NEON_RED)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, cy + 24))

        stats = [
            ("FINAL SCORE", f"{int(self.score):,}", COLOR_GOLD),
            ("WAVE REACHED", f"WAVE {self.wave}", (255, 255, 255)),
            ("TOP RECORD SCORE", f"{self.high_score:,}", (180, 255, 180)),
            ("HIGHEST WAVE", f"WAVE {self.high_wave}", COLOR_NEON_BLUE),
        ]

        stat_y = cy + 120
        for lbl, val, col in stats:
            l_surf = self.font_medium.render(lbl, True, (160, 170, 190))
            v_surf = self.font_medium.render(val, True, col)
            self.screen.blit(l_surf, (cx + 50, stat_y))
            self.screen.blit(v_surf, (cx + card_w - 50 - v_surf.get_width(), stat_y))
            stat_y += 38

        prompt = self.font_medium.render("PRESS R TO DEPLOY AGAIN   |   M FOR MAIN MENU", True, (255, 255, 255))
        self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, cy + card_h - 48))

    # -----------------------------------------------------------------------
    # MENU STATE
    # -----------------------------------------------------------------------
    def draw_menu(self):
        self.screen.fill(COLOR_FLOOR)
        # Background floor grid
        for x in range(0, WIDTH, 50):
            pygame.draw.line(self.screen, COLOR_FLOOR_GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(self.screen, COLOR_FLOOR_GRID, (0, y), (WIDTH, y), 1)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((12, 16, 26, 190))
        self.screen.blit(overlay, (0, 0))

        title = self.font_huge.render("OPERATION VANGUARD", True, COLOR_NEON_BLUE)
        subtitle = self.font_large.render("TACTICAL COMMANDO", True, COLOR_GOLD)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 140))

        # Commando showcase in center
        HumanRenderer.draw_soldier(
            self.screen, WIDTH // 2, 235, -math.pi / 2,
            uniform_color=(35, 60, 95),
            helmet_color=(25, 45, 70),
            weapon_name="Assault Rifle",
            leg_cycle=0.0
        )

        # Instructions
        inst_y = 330
        inst_lines = [
            ("TACTICAL CONTROLS:", COLOR_NEON_BLUE),
            ("W / A / S / D       : Tactical 8-Way Movement", (230, 235, 245)),
            ("MOUSE CURSOR        : 360-Degree Aiming", (230, 235, 245)),
            ("LEFT CLICK / SPACE  : Fire Equipped Weapon", (230, 235, 245)),
            ("RIGHT CLICK / G     : Throw Frag Grenade", (255, 140, 40)),
            ("R                   : Reload Magazine", (230, 235, 245)),
            ("1 / 2 / 3 / 4       : Switch Weapons (Pistol, Rifle, Shotgun, Sniper)", COLOR_GOLD),
            ("P or ESC            : Pause Tactical Mission", (170, 180, 195)),
            ("M                   : Toggle Audio Mute", (170, 180, 195)),
        ]
        curr_y = inst_y
        for text, color in inst_lines:
            line_surf = self.font_small.render(text, True, color)
            self.screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, curr_y))
            curr_y += 24

        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
        start_col = (int(255 * pulse), 255, int(150 + 105 * pulse))
        start_txt = self.font_large.render("PRESS SPACE OR ENTER TO DEPLOY!", True, start_col)
        self.screen.blit(start_txt, (WIDTH // 2 - start_txt.get_width() // 2, 600))

        if self.high_score > 0:
            rec_surf = self.font_small.render(f"TOP RECORD SCORE: {self.high_score:,}   |   HIGHEST WAVE: {self.high_wave}", True, COLOR_GOLD)
            self.screen.blit(rec_surf, (WIDTH // 2 - rec_surf.get_width() // 2, 660))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    game = CommandoGame()
    game.run()
