import pygame
from interfaces.screen_interface import ScreenInterface

class EndScreen(ScreenInterface):
    """
    מסך סיום המשחק שמוצג לאחר ניצחון או הפסד.
    מציג הודעות, מפעיל סאונד מתאים, ומאפשר לשחקן להתחיל מחדש או לצאת.
    """

    def __init__(self, victory):
        """
        אתחול מסך הסיום.
        :param victory: בוליאני שמציין אם השחקן ניצח (True) או הפסיד (False)
        """
        self.victory = victory
        self.font_title = pygame.font.Font("assets/fonts/code_font.ttf", 48)
        self.font_text = pygame.font.Font("assets/fonts/code_font.ttf", 28)
        self.font_small = pygame.font.Font("assets/fonts/code_font.ttf", 20)
        self.clock = 0  # מד זמן פנימי

        # 🎵 טעינת הסאונד לפי תוצאה
        if self.victory:
            self.sound = pygame.mixer.Sound("assets/sounds/win.mp3")
        else:
            self.sound = pygame.mixer.Sound("assets/sounds/lose_game.mp3")

        self.sound.play()

    def handle_event(self, event):
        """
        מטפל בלחיצות מקשים במסך הסיום.
        :param event: אירוע pygame
        :return: "menu" אם לחצו על R (להתחיל מחדש), אחרת None או יציאה מהמשחק
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "menu"  # התחלה מחדש
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def update(self):
        """
        עדכון פנימי של טיימר או אנימציות עתידיות (כרגע רק סופר).
        """
        self.clock += 1

    def draw(self, surface):
        """
        מצייר את מסך הסיום: כותרת, הודעות, הנחיות וקרדיטים.
        :param surface: משטח pygame עליו מציירים
        """
        surface.fill((0, 0, 0))  # רקע שחור

        # כותרת "GAME OVER"
        title = self.font_title.render("GAME OVER", True, (255, 255, 0))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 30))

        # הודעות בהתאם לניצחון או הפסד
        if self.victory:
            lines = [
                "✔ SYSTEM STABILIZED",
                "✔ EARTH REBOOTED",
                "✔ YOU ARE THE LAST PROGRAMMER",
                "",
                "THE WORLD IS IN YOUR HANDS NOW"
            ]
            color = (0, 255, 0)
        else:
            lines = [
                "✖ THEY DEFEATED YOU",
                "✖ BUT THE FIGHT ISN'T OVER",
                "✖ YOU CAN STILL TRY AGAIN",
                "",
                "RESTART AND DEFEAT THE SYSTEM"
            ]
            color = (255, 0, 0)

        # ציור ההודעות בשורות
        for i, line in enumerate(lines):
            rendered = self.font_title.render(line, True, color)
            surface.blit(rendered, (
                surface.get_width() // 2 - rendered.get_width() // 2,
                100 + i * 60
            ))

        # הוראות לחיצה
        restart_msg = self.font_text.render("Press [R] to Play Again", True, (0, 200, 0))
        exit_msg = self.font_text.render("Press [ESC] to Exit", True, (0, 200, 0))
        surface.blit(restart_msg, (surface.get_width() // 2 - restart_msg.get_width() // 2, 500))
        surface.blit(exit_msg, (surface.get_width() // 2 - exit_msg.get_width() // 2, 550))

        # קרדיט קטן בתחתית
        credits = self.font_small.render("Designed in The Void | 2099", True, (0, 100, 0))
        surface.blit(credits, (20, surface.get_height() - 30))

    def cleanup(self):
        """
        עוצר את הסאונד של המסך בסיום (למשל כשעוברים מסך).
        """
        if hasattr(self, 'sound'):
            self.sound.stop()
