import threading
import time
import pygame

class Mob:
    def __init__(self, x, y, hp, power=None):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.power = power
        self.damage = 0

    def attack(self):
        pass

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        self.damage = damage  

class Enemy(Mob):
    def __init__(self, x=0, y=0, hp=100, power=10, level=1):
        super().__init__(x, y, hp, power)
        self.last_attack_time = pygame.time.get_ticks() 
        self.original_x = x 
        self.original_y = y
        self.attack_cooldown = 2000
        self.attack_food = {
            1: "капуста.png",
            2: "пельмень.png", 
            3: "морковка.png"
        }
        self.attack_animation_active = False
        self.attack_start_time = 0
        self.attack_frames = []  
        self.level = level  # Добавлено

    def load_attack_frames(self, frame_paths):
        self.attack_frames = [pygame.image.load(p) for p in frame_paths]

    def start_attack_animation(self, target):  # Правильное имя метода
        self.attack_animation_active = True
        self.attack_start_time = pygame.time.get_ticks()

    def perform_attack(self, target):
        current_time = pygame.time.get_ticks()  # Используем pygame.time
        if (current_time - self.last_attack_time) >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.start_attack_animation(target)
            return True
        return False
    def update_attack_animation(self):
        if self.attack_animation_active:
            elapsed = pygame.time.get_ticks() - self.attack_start_time
    
class Gamer(Mob):
    def __init__(self, x, y, hp, power):
        super().__init__(x, y, hp, power)
        self.has_potion = True
        self.has_poison = True
        self.max_hp = hp

    def take_damage(self, damage):
        self.hp -= damage
        self.hp = max(0, self.hp)
        return self.hp
    
    def reset(self):
        self.hp = self.max_hp
        self.has_potion = True
        self.has_poison = True
        self.damage = 0

class Inventar(Mob):
    def __init__(self, x, y, hp, power):
        super().__init__(x, y, hp, power)
        self.health_potion_count = 1
        self.poison_potion_count = 1
        self.has_potion = True

    def use_health_potion(self, gamer): 
        if self.health_potion_count > 0:
            heal_amount = gamer.hp * 0.2
            gamer.hp += heal_amount
            if gamer.hp > 100:
                gamer.hp = 100
            self.health_potion_count -= 1
            self.has_potion = self.health_potion_count > 0

    def use_poison_potion(self, enemy):
        if self.poison_potion_count > 0:
            poison_damage = 5
            for _ in range(5):
                time.sleep(1)
                enemy.hp = max(0, enemy.hp - poison_damage)
            self.poison_potion_count -= 1