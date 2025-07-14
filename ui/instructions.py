import pygame
from interfaces.screen_interface import ScreenInterface

class InstructionsScreen(ScreenInterface):
    """
    מסך ההוראות של המשחק – מציג לשחקן את הסיפור, השלבים, ומה מטרת המשחק.
    מעבר לשלב הראשון יתבצע כאשר השחקן ילחץ על מקש [SPACE].
    """

    def __init__(self):
        """
        מאתחל פונטים, טקסטים, ומנגנון הבהוב רקע לצורך אפקט ויזואלי.
        """
        self.font_title = pygame.font.Font("assets/fonts/code_font.ttf", 52)  # לא בשימוש כרגע
        self.font_text = pygame.font.Font("assets/fonts/code_font.ttf", 30)
        self.font_small = pygame.font.Font("assets/fonts/code_font.ttf", 26)

        self.flash_timer = 0      # טיימר פנימי להבהוב
        self.flash_on = False     # דגל האם הרקע בהיר או כהה (לאפקט מהבהב)

        self.lines = [  # הטקסט שיוצג על המסך
            "--> WARNING: SYSTEM UNDER ATTACK",
            "",
            "YOU are the LAST PROGRAMMER on Earth.",
            "",
            "Mission: Solve 3 hacking challenges",
            "          to stop the system failure.",
            "",
            "1  LEVEL 1: Guess the secret word letter by letter.",
            "   You have 6 chance, Think like a programmer",
            "",
            "2  LEVEL 2: Fix the missing code pieces in the puzzle.",
            "   Think like a programmer... or the system crashes!",
            "",
            "3  FINAL BOSS: Face the memory overload monster.",
            "   Avoid code traps, survive the final attack.",
            "",
            "Press [SPACE] to begin."
        ]

    def handle_event(self, event):
        """
        מאזין לאירועים. אם SPACE נלחץ – מעבר לשלב הראשון.
        :param event: אירוע pygame
        :return: "level1" אם SPACE נלחץ, אחרת None
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return "level1"

    def update(self):
        """
        מעדכן את אפקט ההבהוב על המסך.
        הבהוב מתחלף כל 30 פריימים.
        """
        self.flash_timer += 1
        if self.flash_timer >= 30:
            self.flash_on = not self.flash_on
            self.flash_timer = 0

    def draw(self, surface):
        """
        מצייר את רקע ההוראות וכל שורות הטקסט עם עיצוב שונה לפי התוכן.
        :param surface: משטח הציור הראשי של pygame
        """
        # אפקט רקע מהבהב: בין כהה לבין כהה-אדמדם
        surface.fill((30, 0, 0) if self.flash_on else (0, 0, 0))

        # חישוב גובה כולל של כל השורות בשביל למרכז אותן
        total_height = 0
        line_heights = []
        for line in self.lines:
            font = self.font_small if "Press" in line else self.font_text
            height = font.get_height()
            line_heights.append(height)
            total_height += height + 10  # כולל רווח בין שורות

        # התחלת ציור מהאמצע האנכי של המסך
        start_y = (surface.get_height() - total_height) // 2

        for i, line in enumerate(self.lines):
            # צבעים וסוג גופן לפי תוכן השורה
            if "WARNING" in line:
                color = (255, 0, 0)
                font = self.font_text
            elif "Press [SPACE]" in line:
                color = (255, 255, 0)
                font = self.font_small
            elif "YOU are" in line:
                color = (0, 255, 0)
                font = self.font_text
            else:
                color = (0, 200, 0)
                font = self.font_text

            # יצירת המשטח לטקסט
            text_surface = font.render(line, True, color)
            text_x = surface.get_width() // 2 - text_surface.get_width() // 2
            surface.blit(text_surface, (text_x, start_y))
            start_y += line_heights[i] + 10
