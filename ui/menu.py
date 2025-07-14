import pygame
from interfaces.screen_interface import ScreenInterface
import random

class MenuScreen(ScreenInterface):
    """
    מסך פתיחה ראשי של המשחק:
    - מציג כותרת מרכזית.
    - מאפשר ניווט עם מקשי החיצים או עכבר בין 'Start Game' ל־'Exit'.
    - כולל גולגולת עם אפקט רטט כשעוברים עליה עם העכבר.
    - מנגן מוזיקת פתיחה בלולאה.
    """

    def __init__(self):
        # הגדרות פונטים
        self.font_title = pygame.font.Font("assets/fonts/code_font.ttf", 64)
        self.font_button = pygame.font.Font("assets/fonts/code_font.ttf", 36)
        self.font_hint = pygame.font.Font("assets/fonts/code_font.ttf", 24)

        # 🎧 מוזיקה ברקע
        pygame.mixer.music.load("assets/sounds/start_game.mp3")
        pygame.mixer.music.play(-1)  # בלולאה

        self.options = ["Start Game", "Exit"]
        self.selected_index = 0
        self.title = "THE LAST PROGRAMMER"

        self.blink_timer = 0         # טיימר למצמוץ הבחירה
        self.blink_visible = True

        # 💀 תמונת גולגולת עם אפקטים
        self.image = pygame.image.load("assets/images/skull_glitch.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image_rect = self.image.get_rect(center=(500, 550))
        self.image_shake_offset = [0, 0]

    def handle_event(self, event):
        """
        עיבוד אירועים:
        - חיצים לשינוי בחירה
        - ENTER לבחירה
        - לחיצת עכבר על כפתור
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self._select_option(self.options[self.selected_index])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(self.options):
                option_surface = self.font_button.render(option, True, (0, 255, 0))
                option_x = 500 - option_surface.get_width() // 2
                option_y = 250 + i * 60
                option_rect = pygame.Rect(option_x, option_y,
                                          option_surface.get_width(), option_surface.get_height())
                if option_rect.collidepoint(mouse_pos):
                    return self._select_option(option)

    def _select_option(self, selected):
        """
        פעולה פנימית לבחירת פעולה:
        - Start Game → מעבר למסך ההוראות
        - Exit → סגירת המשחק
        """
        pygame.mixer.music.stop()
        if selected == "Start Game":
            return "instructions"
        elif selected == "Exit":
            pygame.quit()
            exit()

    def update(self):
        """
        עדכון כללי בכל פריים:
        - מצמוץ בטקסט הבחירה
        - אפקט רטט לגולגולת
        """
        self.blink_timer += 1
        if self.blink_timer % 30 == 0:
            self.blink_visible = not self.blink_visible

        self.image_shake_offset = [random.randint(-2, 2), random.randint(-2, 2)]

    def draw(self, surface):
        """
        ציור כל אלמנטי המסך:
        - רקע, מסגרת ירוקה, כותרת, תפריט בחירה, גולגולת עם אפקטים.
        """
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (0, 255, 0), surface.get_rect(), 10)

        # כותרת עם צל
        title_surface_shadow = self.font_title.render(self.title, True, (0, 100, 0))
        title_surface = self.font_title.render(self.title, True, (0, 255, 0))
        title_x = surface.get_width() // 2 - title_surface.get_width() // 2
        title_y = 100
        surface.blit(title_surface_shadow, (title_x + 2, title_y + 2))
        surface.blit(title_surface, (title_x, title_y))

        # תפריט בחירה
        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected_index and self.blink_visible else (0, 180, 0)
            option_surface = self.font_button.render(option, True, color)
            option_x = surface.get_width() // 2 - option_surface.get_width() // 2
            option_y = 250 + i * 60
            surface.blit(option_surface, (option_x, option_y))

        # ציור הגולגולת עם רטט אם העכבר עליה
        mouse_pos = pygame.mouse.get_pos()
        hovering = self.image_rect.collidepoint(mouse_pos)

        if hovering:
            glow_img = pygame.transform.scale(self.image, (230, 230))
            glow_rect = glow_img.get_rect(center=(self.image_rect.centerx + self.image_shake_offset[0],
                                                  self.image_rect.centery + self.image_shake_offset[1]))
            surface.blit(glow_img, glow_rect)
        else:
            static_rect = self.image_rect.move(self.image_shake_offset[0], self.image_shake_offset[1])
            surface.blit(self.image, static_rect)
