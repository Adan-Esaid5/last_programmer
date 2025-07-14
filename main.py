import pygame
from ui.menu import MenuScreen
from ui.instructions import InstructionsScreen
from ui.level1_screen import Level1Screen
from ui.level2_screen import Level2Screen
from ui.hacker_test_screen import HackerTestScreen
from ui.level3_boss_fight import Level3BossScreen
from ui.end_screen import EndScreen
from ui.victory_screen import VictoryScreen

# 🖥️ הגדרות תצוגת המשחק
WIDTH, HEIGHT = 1000, 700
FPS = 60

pygame.init()

# 🧠 יצירת אירוע מותאם אישית שיתבצע כל 5 שניות (5000 מילישניות)
MY_CUSTOM_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MY_CUSTOM_EVENT, 5000)

# 📋 מיפוי מסכים לפי שמות
SCREENS = {
    "menu": MenuScreen,
    "instructions": InstructionsScreen,
    "level1": Level1Screen,
    "level2": Level2Screen,
    "hacker_test": HackerTestScreen,
    "level3": Level3BossScreen,
    "victory": VictoryScreen,
    "end": EndScreen
}

def load_screen(result):
    """
    טוען את המסך הבא לפי התוצאה שהוחזרה מהמסך הנוכחי.
    :param result: שם המסך הבא או tuple (שם, מידע נוסף)
    :return: מופע של המסך הבא
    """
    if isinstance(result, tuple):
        name, data = result
        if name == "end":
            return EndScreen(victory=data)
        else:
            return SCREENS[name]()
    elif result == "end":
        return EndScreen(victory=False)
    else:
        return SCREENS[result]()

def main():
    """
    נקודת ההתחלה של המשחק:
    - אתחול pygame והמסך
    - הרצת לולאת המשחק
    - טיפול באירועים, עדכונים וציור המסך
    """
    pygame.init()
    pygame.key.set_repeat(300, 50)  # ⌨ מאפשר לחיצה ממושכת על מקשים
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("THE LAST PROGRAMMER ON THE EARTH")
    clock = pygame.time.Clock()

    current_screen_name = "menu"
    current_screen = SCREENS[current_screen_name]()

    running = True
    while running:
        clock.tick(FPS)

        # 🎮 קלט משתמש
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            next_screen = current_screen.handle_event(event)
            if next_screen:
                if hasattr(current_screen, "cleanup"):
                    current_screen.cleanup()
                current_screen = load_screen(next_screen)

        # 🔁 לוגיקת המשחק
        screen_result = current_screen.update()
        if screen_result:
            if hasattr(current_screen, "cleanup"):
                current_screen.cleanup()
            current_screen = load_screen(screen_result)

        # 🖼️ ציור למסך
        current_screen.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
