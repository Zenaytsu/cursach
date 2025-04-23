from mob_classes import Inventar, Enemy, Gamer  # Импортируем классы
import unittest
import time

class TestGame(unittest.TestCase):

    def test_gamer_take_damage(self):
        """Проверяем, правильно ли отнимается здоровье игроку"""
        gamer = Gamer(x=0, y=0, hp=100, power=15)
        gamer.take_damage(20)
        self.assertEqual(gamer.hp, 80, "Здоровье должно уменьшиться на 20")

    def test_enemy_attack(self):
        """Проверяем, правильно ли работает атака врага"""
        enemy = Enemy(x=0, y=0, hp=100, power=10)
        gamer = Gamer(x=0, y=0, hp=100, power=15)

        # Эмуляция атаки врага
        enemy.enemy_attack(gamer)
        self.assertEqual(gamer.hp, 90, "После атаки врага здоровье игрока должно быть уменьшено на 10")

    def test_health_potion(self):
        """Проверяем, правильно ли восстанавливается здоровье с зельем"""
        gamer = Gamer(x=0, y=0, hp=80, power=15)
        gamer.inventory.use_health_potion(gamer)  # Используем зелье
        self.assertEqual(gamer.hp, 92, "Здоровье должно восстановиться на 15%")

    def test_poison_effect(self):
        """Проверяем, правильно ли работает эффект отравления"""
        enemy = Enemy(x=0, y=0, hp=100, power=10)
        gamer = Gamer(x=0, y=0, hp=100, power=15)

        # Применяем зелье отравления
        gamer.inventory.use_poison_potion(enemy)

        time.sleep(6)  # Подождем 6 секунд, чтобы эффект отравления завершился
        self.assertTrue(enemy.hp < 100, "Враг должен потерять здоровье из-за отравления")
        self.assertEqual(enemy.hp, 75, "После 5 секунд отравления враг должен потерять 25 HP")

    def test_no_more_health_potion_after_use(self):
        """Проверяем, что зелье исчезает после использования"""
        gamer = Gamer(x=0, y=0, hp=100, power=15)
        gamer.inventory.use_health_potion(gamer)
        self.assertFalse(gamer.inventory.has_potion, "После использования зелья оно должно исчезнуть")

if __name__ == "__main__":
    unittest.main()
