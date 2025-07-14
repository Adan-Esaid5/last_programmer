import pygame
from interfaces.screen_interface import ScreenInterface


class Level1Screen(ScreenInterface):
    """
    מסך שלב ראשון במשחק – 'Code Breaker'.
    על המשתמש לנחש מילה סודית (DEBUG) באמצעות הקלדת אותיות מהמקלדת או לחיצה עליהן על המסך.
    מוצגות הודעות, רמזים, וכמות טעויות – ואם הצליח או נכשל, עובר לשלב הבא או מסך סיום.
    """

    def __init__(self):
        """
        אתחול רכיבי המשחק: פונט, צליל, מילה סודית, משתני משחק ומקלדת וירטואלית.
        """
        # פונטים
        self.font_main = pygame.font.Font("assets/fonts/code_font.ttf", 48)
        self.font_small = pygame.font.Font("assets/fonts/code_font.ttf", 28)
        self.font_title = pygame.font.Font("assets/fonts/code_font.ttf", 48)
        self.font_riddle = pygame.font.Font("assets/fonts/code_font.ttf", 24)

        # צליל רקע
        self.sound = pygame.mixer.Sound("assets/sounds/typing-on-laptop-keyboard.mp3")
        self.sound.play(-1)  # חוזר בלופ

        # חידה וטקסטים
        self.riddle = "💡 What do developers do when the code doesn't work?"
        self.hint = "Hint: It's what you do when your code doesn't work... Think like a debugger"
        self.show_hint = False
        self.hint_timer = 0  # סופר זמן הצגת הרמז

        # המקלדת הוויזואלית
        self.keyboard_buttons = []

        # הגדרות המשחק
        self.secret_word = "DEBUG"
        self.revealed_letters = ["_" for _ in self.secret_word]  # אותיות שנחשפו
        self.guessed_letters = set()
        self.errors = 0
        self.max_errors = 6
        self.next_screen = None

        self.message = "Type the correct letters to decode the word"

    def cleanup(self):
        """
        פעולה להפסקת הצליל כאשר המסך נסגר.
        """
        if hasattr(self, "sound"):
            self.sound.stop()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if pygame.K_a <= key <= pygame.K_z:
                letter = chr(key).upper()
                return self.process_letter(letter)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for letter, rect in self.keyboard_buttons:
                if rect.collidepoint(mouse_pos):
                    return self.process_letter(letter)

    def update(self):
        """
        עדכון לוגיקת המשחק – הורדת טיימר הרמז אם מוצג, בדיקת מעבר שלב.
        """
        if self.show_hint:
            self.hint_timer -= 1
            if self.hint_timer <= 0:
                self.show_hint = False

        if self.next_screen:
            result = self.next_screen
            self.next_screen = None
            return result

    def draw(self, surface):
        """
        ציור כל רכיבי המסך – כותרת, חידה, מילה, שגיאות, רמזים, מקלדת וירטואלית.
        """
        surface.fill((0, 0, 0))
        center_x = surface.get_width() // 2
        y = 30

        # כותרת
        title_surface = self.font_title.render("LEVEL 1: CODE BREAKER", True, (0, 255, 0))
        surface.blit(title_surface, (center_x - title_surface.get_width() // 2, y))
        y += title_surface.get_height() + 10

        # שאלה
        question_surface = self.font_small.render(self.riddle, True, (0, 255, 255))
        surface.blit(question_surface, (center_x - question_surface.get_width() // 2, y))
        y += question_surface.get_height() + 10

        # רמז
        if self.show_hint:
            hint1 = "Hint: It's what you do when your code doesn't work..."
            hint2 = "Think like a debugger"
            hint1_surface = self.font_riddle.render(hint1, True, (255, 255, 0))
            hint2_surface = self.font_riddle.render(hint2, True, (255, 255, 0))
            surface.blit(hint1_surface, (center_x - hint1_surface.get_width() // 2, y))
            y += hint1_surface.get_height() + 5
            surface.blit(hint2_surface, (center_x - hint2_surface.get_width() // 2, y))
            y += hint2_surface.get_height() + 10

        # הודעה על ניחוש
        msg_surface = self.font_small.render(self.message, True, (0, 200, 0))
        surface.blit(msg_surface, (center_x - msg_surface.get_width() // 2, y))
        y += msg_surface.get_height() + 20

        # המילה עצמה
        word_display = " ".join(self.revealed_letters)
        word_surface = self.font_main.render(word_display, True, (0, 255, 0))
        surface.blit(word_surface, (center_x - word_surface.get_width() // 2, y))
        y += word_surface.get_height() + 30

        # שגיאות
        err_surface = self.font_small.render(f"Errors: {self.errors} / {self.max_errors}", True, (255, 50, 50))
        surface.blit(err_surface, (80, y))

        # ציור מקלדת
        keyboard_layout = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            list("ZXCVBNM")
        ]

        key_width = 50
        key_height = 50
        spacing = 10
        start_x = center_x - (10 * (key_width + spacing)) // 2
        start_y = y + 60
        mouse_pos = pygame.mouse.get_pos()

        self.keyboard_buttons = []

        for row_index, row in enumerate(keyboard_layout):
            for col_index, letter in enumerate(row):
                x = start_x + col_index * (key_width + spacing)
                y = start_y + row_index * (key_height + spacing)
                rect = pygame.Rect(x, y, key_width, key_height)
                self.keyboard_buttons.append((letter, rect))

                # צבעים לפי מצב האות
                if letter in self.guessed_letters:
                    color = (0, 200, 0) if letter in self.secret_word else (200, 0, 0)
                else:
                    color = (0, 255, 0)

                # אפקט כשמצביעים בעכבר
                if rect.collidepoint(mouse_pos):
                    glow = tuple(min(c + 50, 255) for c in color)
                    pygame.draw.rect(surface, glow, rect, border_radius=8)
                else:
                    pygame.draw.rect(surface, color, rect, border_radius=8)

                # מסגרת וכיתוב האות
                pygame.draw.rect(surface, (0, 100, 0), rect, 2, border_radius=8)
                letter_surf = self.font_small.render(letter, True, (0, 0, 0))
                letter_rect = letter_surf.get_rect(center=rect.center)
                surface.blit(letter_surf, letter_rect)

    def process_letter(self, letter):
        """
        פעולת עיבוד לאחר שנבחרה אות.
        עדכון מצב האותיות שנחשפו, טעויות, רמזים, ומעבר שלב.
        """
        if letter in self.guessed_letters:
            return None  # כבר ניחש את האות הזאת

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            for i, ch in enumerate(self.secret_word):
                if ch == letter:
                    self.revealed_letters[i] = letter
        else:
            self.errors += 1

            # הצגת רמז אחרי טעות 2 ו־4
            if self.errors in [2, 4]:
                self.show_hint = True
                self.hint_timer = 600  # 10 שניות (ב־FPS 60)

            # אם הגיע למקסימום טעויות – מעבר לסיום
            if self.errors >= self.max_errors:
                self.next_screen = "end"

        # אם נחשפו כל האותיות – מעבר לשלב הבא
        if "_" not in self.revealed_letters:
            self.next_screen = "level2"

        return None
