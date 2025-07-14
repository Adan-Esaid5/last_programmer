import pygame
from interfaces.screen_interface import ScreenInterface

class VictoryScreen(ScreenInterface):
    """
    מסך ניצחון המוצג בסיום המשחק לאחר שהשחקן ניצח את הבוס:
    - מציג הודעת ניצחון וכפתורים לפעולה.
    - מאפשר יציאה מהמשחק או התחלה מחדש דרך המקלדת.
    - מנגן צליל ניצחון בעת הופעת המסך.
    """

    def __init__(self):
        # אתחול פונטים
        self.font_big = pygame.font.Font("assets/fonts/code_font.ttf", 60)
        self.font_small = pygame.font.Font("assets/fonts/code_font.ttf", 28)

        self.exit = False
        self.restart = False

        # מוסיקת ניצחון 🎵
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")
        self.win_sound.play()

    def handle_event(self, event):
        """
        עיבוד אירועי מקלדת:
        - ESC: יציאה מהמשחק
        - R: התחלה מחדש (מעבר למסך התפריט)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_r:
                self.restart = True
                return "menu"

    def update(self):
        """אין צורך בעדכון שוטף במסך זה."""
        pass

    def draw(self, screen):
        """
        ציור אלמנטי הניצחון:
        - טקסט ראשי, תיאור, והוראות המשך.
        """
        screen.fill((0, 0, 0))  # רקע שחור

        # טקסט ראשי של ניצחון
        victory_text = self.font_big.render("✔ YOU SAVED THE SYSTEM!", True, (0, 255, 0))

        # טקסט תיאורי
        desc_text = self.font_small.render(
            "The last programmer restored balance to the digital world.",
            True, (0, 255, 0)
        )

        # טקסט הדרכה לפעולה
        esc_text = self.font_small.render(
            "Press ESC to quit or R to restart",
            True, (255, 255, 255)
        )

        # מיקום מרכזי
        screen.blit(victory_text, (screen.get_width() // 2 - victory_text.get_width() // 2, 200))
        screen.blit(desc_text, (screen.get_width() // 2 - desc_text.get_width() // 2, 280))
        screen.blit(esc_text, (screen.get_width() // 2 - esc_text.get_width() // 2, 340))
