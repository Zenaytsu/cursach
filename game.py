import pygame
import os
import threading
import time
from mob_classes import Inventar, Enemy, Gamer
import pygame.mixer
pygame.mixer.init()

pygame.init()

WIDTH = 1000
HEIGHT = 600
TITLE = "Game"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

background_path = os.path.join("пикчи", "фон.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


current_background = background

health_bar_width = 339
health_bar_height = 59
health_border_color = (255, 255, 255)
health_background_color = (217, 217, 217)
health_inner_width = 283
health_inner_height = 41
health_inner_color = (170, 24, 3)
poison_bar_color = (109, 140, 0)

max_hp = 100

player_skin_path = os.path.join("пикчи", "котенок-поваренок.png")
enemy_skin_path = os.path.join("пикчи", "котик-капуста.png")
explosion_path = os.path.join("пикчи", "взрыв.gif")
player = Gamer(x=100, y=100, hp=100, power=10)
inventar = Inventar(x=100, y=100, hp=100, power=10)
defeat_screen = False
defeat_playing = False


angry_player_skin_path = os.path.join("пикчи", "злой.png")
angry_player_skin = pygame.image.load(angry_player_skin_path)

original_player_x = player.x 

player_skin = pygame.image.load(player_skin_path)
enemy_skin = pygame.image.load(enemy_skin_path)

player_width = 345
player_height = 345
enemy_width = 411
enemy_height = 377

attacking = False
returning = False
attack_direction = 1
attack_step = 10
return_step = 5
attack_target_x = WIDTH - enemy_width - 30
original_player_x = player.x
damage = 0

last_poison_tick = pygame.time.get_ticks()
healing_sound = pygame.mixer.Sound("звуки/здоровье.mp3")
evil_sound = pygame.mixer.Sound("звуки/злой.mp3")
explosion_sound = pygame.mixer.Sound("звуки/взрыв.mp3")
victory_sound = pygame.mixer.Sound("звуки/победа.mp3")
damage_sound = pygame.mixer.Sound("звуки/урон.mp3")

potion_path = os.path.join("пикчи", "Колба.png")
poison_path = os.path.join("пикчи", "Колба1.png")
potion_img = pygame.image.load(potion_path)
poison_img = pygame.image.load(poison_path)

level_select_width = 665.9
level_select_height = 390
level_select_x = (WIDTH - level_select_width) // 2
level_select_y = 40

show_level_select = True
level_selected = False
show_inventory = False
confirmation_dialog = None

inventory_size = 534
inventory_color = (209, 171, 125)
slot_size = 193.3
slot_color = (99, 80, 61)
slot_spacing = (inventory_size - 2 * slot_size) / 3

enemy = Enemy(hp=100, power=15)

poison_timer = 0
poison_effect_active = False
healing_in_progress = False
explosion_playing = False 
victory_screen = False
victory_timer = 0
last_damage_time_player = pygame.time.get_ticks()
damage_interval_player = 2000
level_start_time = None

# Основной цикл игры
running = True
while running:
    screen.blit(current_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if confirmation_dialog:
                dialog_x = (WIDTH - 600) // 2
                dialog_y = 79
                yes_btn = pygame.Rect(dialog_x + 600 - 190 - 50, dialog_y + 160 + 54, 190, 66)
                no_btn = pygame.Rect(dialog_x + 50, dialog_y + 160 + 54, 190, 66)
                if yes_btn.collidepoint(mouse_x, mouse_y):
                    if confirmation_dialog == 'potion':
                        heal_target_hp = min(100, player.hp + 15)  # Восстановление здоровья на 15
                        healing_in_progress = True
                        player.has_potion = False
                        healing_sound.play()
                    if healing_in_progress:
                        if player.hp < heal_target_hp:
                            player.hp += 1
                            pygame.time.delay(10)  # Уменьшаем задержку для плавного увеличения
                        else:
                            player.hp = heal_target_hp
                            healing_in_progress = False
                    elif confirmation_dialog == 'poison':
                        poison_timer = 5
                        poison_effect_active = True
                    confirmation_dialog = None
                    inventar.has_potion = False if confirmation_dialog == 'potion' else inventar.has_potion
                    inventar.has_potion = False if confirmation_dialog == 'poison' else inventar.has_potion
                    show_inventory = False
                elif no_btn.collidepoint(mouse_x, mouse_y):
                    confirmation_dialog = None

                dialog_x = (WIDTH - 600) // 2
                dialog_y = 79
                yes_btn = pygame.Rect(dialog_x + 600 - 190 - 50, dialog_y + 160 + 54, 190, 66)
                no_btn = pygame.Rect(dialog_x + 50, dialog_y + 160 + 54, 190, 66)
                if yes_btn.collidepoint(mouse_x, mouse_y):
                    if confirmation_dialog == 'potion':
                        heal_target_hp = min(100, player.hp + 15)
                        healing_in_progress = True
                        player.has_potion = False
                        healing_sound.play()
                    if healing_in_progress:
                        if player.hp < heal_target_hp:
                            player.hp += 1
                            pygame.time.delay(10)
                        else:
                            player.hp = heal_target_hp
                            healing_in_progress = False
                    elif confirmation_dialog == 'poison':
                        poison_timer = 5
                        poison_effect_active = True
                    confirmation_dialog = None
                    inventar.has_potion = False if confirmation_dialog == 'potion' else inventar.has_potion
                    inventar.has_potion = False if confirmation_dialog == 'poison' else inventar.has_potion
                    show_inventory = False
                elif no_btn.collidepoint(mouse_x, mouse_y):
                    confirmation_dialog = None
            elif not confirmation_dialog:
                if show_level_select:
                    bx = level_select_x + (level_select_width - 228) // 2
                    by = level_select_y + 97
                    level_select_text = font.render("Выберите уровень", True, (255, 255, 255))
                    screen.blit(level_select_text, (WIDTH // 2 - level_select_text.get_width() // 2, HEIGHT // 2 - 50))
                    pygame.display.update()
                    for i in range(3):
                        if bx <= mouse_x <= bx + 228 and by + i * (60 + 22) <= mouse_y <= by + i * (60 + 22) + 60:
                            level_start_time = pygame.time.get_ticks()
                            show_level_select = False
                            level_selected = True
                            if i == 0:
                                enemy_skin_path = os.path.join("пикчи", "котик-капуста.png")
                                enemy_width = 411
                                enemy_height = 377
                                damage_interval_player = 2000
                                damage_percent = 0.1
                            elif i == 1:
                                enemy_skin_path = os.path.join("пикчи", "котик-пельмешка.png")
                                enemy_width = 411
                                enemy_height = 377
                                damage_interval_player = 2000
                                damage_percent = 0.15
                            elif i == 2:
                                enemy_skin_path = os.path.join("пикчи", "котик-морковка.png")
                                enemy_width = 448
                                enemy_height = 464
                                damage_interval_player = 1000
                                damage_percent = 0.1

                            enemy_skin = pygame.image.load(enemy_skin_path)
                            enemy_skin = pygame.transform.scale(enemy_skin, (enemy_width, enemy_height))

                            enemy_x = WIDTH - enemy_width
                            enemy_y = HEIGHT - enemy_height - 70
                elif level_selected and not show_inventory:
                    if 30 <= mouse_x <= 30 + 80 and HEIGHT - 80 <= mouse_y <= HEIGHT:
                        show_inventory = True
                elif show_inventory:
                    inventory_x = (WIDTH - inventory_size) // 2
                    inventory_y = (HEIGHT - inventory_size) // 2
                    for i in range(2):
                        for j in range(2):
                            slot_x = inventory_x + slot_spacing + j * (slot_size + slot_spacing)
                            slot_y = inventory_y + slot_spacing + i * (slot_size + slot_spacing)
                            if slot_x <= mouse_x <= slot_x + slot_size and slot_y <= mouse_y <= slot_y + slot_size:
                                if i == 0 and j == 0 and inventar.has_potion:
                                    confirmation_dialog = 'potion'
                                elif i == 0 and j == 1 and inventar.has_potion:
                                    confirmation_dialog = 'poison'
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i and level_selected and not confirmation_dialog:
                show_inventory = not show_inventory
            elif event.key == pygame.K_e:
                attacking = True
                returning = False
                attack_direction = 1
                damage = int(0.1 * enemy.max_hp)
                
            elif event.key == pygame.K_q:
                attacking = True
                returning = False
                attack_direction = 1
                damage = int(1 * enemy.max_hp)
                evil_sound.play()

                player_skin = angry_player_skin
                attack_step = (WIDTH - enemy_width - 30 - player.x) // 100 

    if not victory_screen and not defeat_screen:
        current_time = pygame.time.get_ticks()
    if level_start_time: 
        if current_time - level_start_time >= 2000:
            if current_time - last_damage_time_player >= damage_interval_player:
                enemy_damage = int(damage_percent * player.max_hp)
                player.hp = max(0, player.hp - enemy_damage)
                last_damage_time_player = current_time

    if enemy.hp <= 0 and not explosion_playing:
        enemy_skin = pygame.image.load(explosion_path)
        enemy_skin = pygame.transform.scale(enemy_skin, (enemy_width, enemy_height))
        explosion_sound.play()
        explosion_playing = True 
        
        victory_timer = pygame.time.get_ticks()

    if explosion_playing and pygame.time.get_ticks() - victory_timer >= 2000:
        explosion_playing = False
        victory_sound.play()
        victory_screen = True
        enemy.hp = 100

    if player.hp <= 0 and not defeat_playing:
        defeat_playing = True

        defeat_timer = pygame.time.get_ticks()
        defeat_screen = True

    if defeat_screen:
        defeat_background_path = os.path.join("пикчи", "Проигрыш.png")
        defeat_background = pygame.image.load(defeat_background_path)
        defeat_background = pygame.transform.scale(defeat_background, (WIDTH, HEIGHT))

        screen.blit(defeat_background, (0, 0))

        if pygame.time.get_ticks() - defeat_timer >= 10000:

            player.hp = 100
            enemy.hp = 100
            defeat_screen = False
            show_level_select = True

    if victory_screen:
        victory_image_path = os.path.join("пикчи", "Фон победа.png")
        victory_image = pygame.image.load(victory_image_path)
        victory_image = pygame.transform.scale(victory_image, (WIDTH, HEIGHT))

        screen.blit(victory_image, (0,0))
        if pygame.time.get_ticks() - victory_timer >= 8000:
            show_level_select = True
            enemy.hp = 100
            player.hp = 100
            victory_screen = False

            
    if poison_timer > 0 and poison_effect_active:
        now = pygame.time.get_ticks()
        if now - last_poison_tick >= 1000:
            last_poison_tick = now
            enemy.hp = max(0, enemy.hp - 5)
            damage_sound.play()
            poison_timer -= 1
            if poison_timer == 0:
                poison_effect_active = False
    def draw_health_bar(x, y, current_hp, max_hp, color):
        pygame.draw.rect(screen, health_border_color, (x, y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, health_background_color, (x + (health_bar_width - health_inner_width) // 2, y + (health_bar_height - health_inner_height) // 2, health_inner_width, health_inner_height))
        filled_width = int(health_inner_width * (current_hp / max_hp))
        pygame.draw.rect(screen, color, (x + (health_bar_width - health_inner_width) // 2, y + (health_bar_height - health_inner_height) // 2, filled_width, health_inner_height))

    if show_level_select:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (255, 255, 255), (level_select_x, level_select_y, level_select_width, level_select_height))

        font = pygame.font.Font(None, 32)
        text_surface = font.render("Выберите уровень", True, (0, 0, 0))
        screen.blit(text_surface, (level_select_x + (level_select_width - text_surface.get_width()) // 2, level_select_y + 50))

        button_width = 228
        button_height = 60
        button_radius = 15
        button_x = level_select_x + (level_select_width - button_width) // 2
        button_y = level_select_y + 80 + 17
        button_spacing = 22

        font = pygame.font.Font(None, 24)
        button_texts = ["Уровень 1", "Уровень 2", "Уровень 3"]

        for i, text in enumerate(button_texts):
            pygame.draw.rect(screen, (25, 80, 49), (button_x, button_y + i * (button_height + button_spacing), button_width, button_height), border_radius=button_radius)
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) // 2, button_y + i * (button_height + button_spacing) + (button_height - text_surface.get_height()) // 2))
    elif not show_inventory:
        draw_health_bar(29, 54, player.hp, player.max_hp, health_inner_color)  # Отображение здоровья игрока
        bar_color = poison_bar_color if poison_effect_active else health_inner_color
        draw_health_bar(WIDTH - 29 - health_bar_width, 54, enemy.hp, enemy.max_hp, bar_color)  # Отображение здоровья врага

        screen.blit(player_skin, (player.x, HEIGHT - player_height - 80))
        screen.blit(enemy_skin, (WIDTH - enemy_width, HEIGHT - enemy_height - 70))

    if show_inventory:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        inventory_x = (WIDTH - inventory_size) // 2
        inventory_y = (HEIGHT - inventory_size) // 2
        pygame.draw.rect(screen, inventory_color, (inventory_x, inventory_y, inventory_size, inventory_size))

        for i in range(2):
            for j in range(2):
                slot_x = inventory_x + slot_spacing + j * (slot_size + slot_spacing)
                slot_y = inventory_y + slot_spacing + i * (slot_size + slot_spacing)
                pygame.draw.rect(screen, slot_color, (slot_x, slot_y, slot_size, slot_size))

                if i == 0 and j == 0 and player.has_potion:
                    item_img = potion_img
                    item_width, item_height = 116.76, 163.18
                elif i == 0 and j == 1 and player.has_poison:
                    item_img = poison_img
                    item_width, item_height = 116.76, 163.18
                else:
                    continue 
                item_scaled = pygame.transform.scale(item_img, (int(item_width), int(item_height)))
                item_x = slot_x + (slot_size - item_width) // 2
                item_y = slot_y + (slot_size - item_height) // 2
                screen.blit(item_scaled, (item_x, item_y))

    if confirmation_dialog:
        dialog_x = (WIDTH - 600) // 2
        dialog_y = 79
        pygame.draw.rect(screen, (255, 255, 255), (dialog_x, dialog_y, 600, 320))

        font = pygame.font.Font(None, 50)
        item_name = "Зелье здоровья" if confirmation_dialog == 'potion' else "Зелье отравления"
        color = pygame.Color("#C22727") if confirmation_dialog == 'potion' else pygame.Color("#6D8C00")
        base_text = font.render("Вы хотите использовать", True, (0, 0, 0))
        item_text = font.render(f"{item_name} 1 шт?", True, color)
        screen.blit(base_text, ((WIDTH - base_text.get_width()) // 2, dialog_y + 70))
        screen.blit(item_text, ((WIDTH - item_text.get_width()) // 2, dialog_y + 110))

        no_button = pygame.Rect(dialog_x + 50, dialog_y + 160 + 54, 190, 66)
        yes_button = pygame.Rect(dialog_x + 600 - 190 - 50, dialog_y + 160 + 54, 190, 66)

        pygame.draw.rect(screen, (194, 39, 39), no_button)
        pygame.draw.rect(screen, (109, 140, 0), yes_button)

        font_btn = pygame.font.Font(None, 28)
        no_text = font_btn.render("Отмена", True, (255, 255, 255))
        yes_text = font_btn.render("Использовать", True, (255, 255, 255))

        screen.blit(no_text, (no_button.x + (190 - no_text.get_width()) // 2, no_button.y + (66 - no_text.get_height()) // 2))
        screen.blit(yes_text, (yes_button.x + (190 - yes_text.get_width()) // 2, yes_button.y + (66 - yes_text.get_height()) // 2))

        if yes_button.collidepoint(mouse_x, mouse_y):
            if confirmation_dialog == 'potion':
                player.hp = min(100, player.hp * 1.2)
                player.has_potion = False
            elif confirmation_dialog == 'poison':
                poison_timer = 5
                poison_effect_active = True
                player.has_poison = False
            confirmation_dialog = None
            show_inventory = False
        elif no_button.collidepoint(mouse_x, mouse_y):
            confirmation_dialog = None

    
    if attacking:
        if player.x < attack_target_x:
            player.x += attack_step * attack_direction
        else:
            attacking = False
            if player.x >= attack_target_x and player.x <= attack_target_x + enemy_width:
                enemy.hp -= damage
                damage_sound.play()
            returning = True 

    if returning:
        if player.x > original_player_x:
            player.x -= return_step
        else:
            player.x = original_player_x
            returning = False
            player_skin = pygame.image.load(player_skin_path)

    pygame.display.flip()

pygame.quit()