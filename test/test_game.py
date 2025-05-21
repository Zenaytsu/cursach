import pytest
from mob_classes import Mob, Enemy, Gamer, Inventar
import pygame
from unittest.mock import patch

@pytest.mark.parametrize("x, y, hp, damage, expected", [
    (0, 0, 100, 30, 70),
    (10, 20, 200, 50, 150),
    (5, 5, 50, 60, 0),
])
def test_mob_take_damage(x, y, hp, damage, expected):
    mob = Mob(x, y, hp)
    mob.take_damage(damage)
    assert mob.hp == expected

def test_enemy_attack_cooldown():
    pygame.init()
    enemy = Enemy(attack_cooldown=2000)
    gamer = Gamer(0, 0, 100, 10)
    
    enemy.last_attack_time = pygame.time.get_ticks()
    assert enemy.perform_attack(gamer) is False
    
    enemy.last_attack_time = pygame.time.get_ticks() - 2500
    assert enemy.perform_attack(gamer) is True

def test_gamer_reset():
    gamer = Gamer(0, 0, 100, 10)
    gamer.take_damage(30)
    gamer.reset()
    assert gamer.hp == 100
    assert gamer.has_potion is True
    assert gamer.has_poison is True

@patch('pygame.time.get_ticks')
def test_enemy_attack_animation(mock_ticks):
    enemy = Enemy(attack_cooldown=2000)
    mock_ticks.return_value = 1000
    enemy.start_attack_animation(None)
    assert enemy.attack_animation_active

    mock_ticks.return_value = 1000 + 2000
    enemy.update_attack_animation()
    assert not enemy.attack_animation_active

def test_use_health_potion():
    inventar = Inventar(0, 0, 100, 10)
    inventar.health_potion_count = 1
    gamer = Gamer(0, 0, 50, 10)
    inventar.use_health_potion(gamer)
    assert gamer.hp == 60

def test_use_poison_potion():
    inventar = Inventar(0, 0, 100, 10)
    enemy = Enemy(hp=100)
    inventar.poison_potion_count = 1
    inventar.use_poison_potion(enemy)
    assert enemy.hp == 75

def test_poison_potion_no_charges():
    inventar = Inventar(0, 0, 100, 10)
    inventar.poison_potion_count = 0
    enemy = Enemy(hp=100)
    inventar.use_poison_potion(enemy)
    assert enemy.hp == 100 