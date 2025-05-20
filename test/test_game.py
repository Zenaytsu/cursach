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
    enemy = Enemy(attack_cooldown=2000)
    current_time = 1000
    enemy.last_attack_time = current_time
    assert enemy.perform_attack(None) is False

    with patch('pygame.time.get_ticks', return_value=3000):
        assert enemy.perform_attack(None) is True

def test_enemy_attack_animation():
    enemy = Enemy()
    enemy.start_attack_animation(None)
    assert enemy.attack_animation_active is True
    assert enemy.attack_start_time > 0

    with patch('pygame.time.get_ticks', return_value=enemy.attack_start_time + 500):
        enemy.update_attack_animation()
        assert enemy.attack_animation_active is True

    with patch('pygame.time.get_ticks', return_value=enemy.attack_start_time + 2000):
        enemy.update_attack_animation()
        assert enemy.attack_animation_active is False

@pytest.mark.parametrize("max_hp, damage, expected", [
    (100, 30, 100),
    (150, 50, 150),
])
def test_gamer_reset(max_hp, damage, expected):
    gamer = Gamer(0, 0, max_hp, 10)
    gamer.take_damage(damage)
    gamer.reset()
    assert gamer.hp == expected
    assert gamer.has_potion is True
    assert gamer.has_poison is True
    assert gamer.damage == 0

@pytest.mark.parametrize("potion_count, initial_hp, expected_hp", [
    (1, 50, 60),
    (0, 50, 50),
    (2, 90, 100),
])
def test_use_health_potion(potion_count, initial_hp, expected_hp):
    inventar = Inventar(0, 0, 100, 10)
    inventar.health_potion_count = potion_count
    gamer = Gamer(0, 0, initial_hp, 10)
    inventar.use_health_potion(gamer)
    assert gamer.hp == expected_hp
    assert inventar.health_potion_count == max(0, potion_count - 1)

@patch('time.sleep')
def test_use_poison_potion(mock_sleep):
    inventar = Inventar(0, 0, 100, 10)
    enemy = Enemy(hp=100)
    inventar.poison_potion_count = 1
    inventar.use_poison_potion(enemy)
    assert enemy.hp == 75
    assert inventar.poison_potion_count == 0

def test_poison_potion_with_no_charges():
    inventar = Inventar(0, 0, 100, 10)
    inventar.poison_potion_count = 0
    enemy = Enemy(hp=100)
    inventar.use_poison_potion(enemy)
    assert enemy.hp == 100