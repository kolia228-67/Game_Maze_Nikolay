import pygame
import traceback
from menu import Menu
from minigame.game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Проект Ави")
clock = pygame.time.Clock()

menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
game = None  # объект игры создаётся только при старте

running = True
while running:
    # --- САМАЯ ВАЖНАЯ ПРОВЕРКА: если pygame уже выключен, выходим сразу ---
    if not pygame.get_init():
        break

    # Теперь безопасно обрабатывать события (get_init проверено)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # обработка событий меню — только если не в игре
        if not menu.play_pressed:
            menu.handle_event(event)

    # Попытаемся залить экран; если surface уже недоступен, выйдем аккуратно
    try:
        screen.fill(BLACK)
    except pygame.error:
        # display surface уже закрыт — выйдем из цикла
        break

    if not menu.play_pressed:
        # Отрисовка меню
        menu.update()
        try:
            menu.draw(screen)
        except pygame.error:
            break
        # удостоверимся, что старый объект игры сброшен
        game = None

    else:
        # если нажали Play — создаём игру один раз
        if game is None:
            # небольшая диагностика: выведем тип аватарки (если нужно)
            # print("DEBUG: selected_avatar =", menu.selected_avatar, type(menu.selected_avatar))
            try:
                # Game конструктор в этой версии ожидает (nickname, avatar)
                game = Game(menu.nickname, menu.selected_avatar)
            except Exception:
                print("Ошибка при создании Game():")
                traceback.print_exc()
                input("Нажми Enter чтобы закрыть...")
                # вернёмся в меню, чтобы избежать бесконечного падения
                menu.play_pressed = False
                game = None
                continue

        # Запускаем игровой цикл и ловим исключения, чтобы они были видимы в консоли
        try:
            game.run()
        except Exception:
            print("Ошибка внутри game.run():")
            traceback.print_exc()
            # останавливаемся и ждём подтверждения, чтобы увидеть трассировку
            input("Нажми Enter чтобы закрыть...")
        finally:
            # после окончания (или при ошибке) — вернуться в меню
            # если pygame уже упал — выйдем
            if not pygame.get_init():
                running = False
                break

            menu.play_pressed = False
            game = None

    # Дополнительная защита перед flip
    if not pygame.get_init():
        break

    # безопасный вызов flip (на случай, если surface внезапно умирает)
    try:
        pygame.display.flip()
    except pygame.error:
        break

    clock.tick(60)

pygame.quit()