import threading
import time

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
        self.last_attack_time = time.time() 

    def enemy_attack(self, target):
        current_time = time.time()
        time_since_last_attack = current_time - self.last_attack_time

class Gamer(Mob):
    def __init__(self, x, y, hp, power):
        
        super().__init__(x, y, hp, power)
        self.has_potion = True
        self.has_poison = True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

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
                enemy.hp -= poison_damage
                if enemy.hp < 0:
                    enemy.hp = 0
            self.poison_potion_count -= 1
