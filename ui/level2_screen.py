import pygame
from interfaces.screen_interface import ScreenInterface

class CodeBlock:
    """
    מייצג בלוק של קוד שניתן לגרור על המסך.
    כולל טקסט, מיקום, ותמיכה ב־drag and drop.
    """
    def __init__(self, text, x, y, font):
        self.text = text
        self.font = font

        # יצירת משטח טקסט וחשב גודל המלבן
        text_surface = self.font.render(self.text, True, (0, 255, 0))
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()

        # רוחב מינימלי 300 פיקסלים
        width = max(300, text_width + 20)
        height = text_height + 20

        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        """
        מצייר את הבלוק עם גבול וטקסט ממורכז.
        """
        pygame.draw.rect(surface, (0, 80, 0), self.rect)
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, (0, 255, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Level2Screen(ScreenInterface):
    """
    שלב 2 – פאזל גרירה: סידור בלוקים של קוד בסדר הנכון.
    משתמש צריך לגרור את השורות למיקום הנכון וללחוץ ENTER.
    """
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/code_font.ttf", 28)

        # סדר קוד נכון (התשובה)
        self.code_order = [
            "def hack():",
            "if safe == False:",
            "    print('Alert')",
            "else:",
            "    print('Access granted')"
        ]

        # צלילים
        self.drag_sound = pygame.mixer.Sound("assets/sounds/reload-and-jump-81124.mp3")
        self.success_sound = pygame.mixer.Sound("assets/sounds/win.mp3")
        self.fail_sound = pygame.mixer.Sound("assets/sounds/error_beep.mp3")

        # ערבוב סדר בלוקים
        import random
        shuffled = self.code_order[:]
        random.shuffle(shuffled)

        # יצירת הבלוקים ומיקומם
        start_y = 100
        spacing = 20
        self.blocks = []
        for i, txt in enumerate(shuffled):
            block = CodeBlock(txt, 100, start_y, self.font)
            self.blocks.append(block)
            start_y += block.rect.height + spacing

        self.selected_block = None
        self.success = False
        self.failed = False

    def handle_event(self, event):
        """
        טיפול באירועי עכבר ומקלדת: גרירה ובדיקה בלחיצת ENTER.
        """
        # התחלת גרירה
        if event.type == pygame.MOUSEBUTTONDOWN:
            for block in self.blocks:
                if block.rect.collidepoint(event.pos):
                    block.dragging = True
                    block.offset_x = event.pos[0] - block.rect.x
                    block.offset_y = event.pos[1] - block.rect.y
                    self.selected_block = block
                    self.drag_sound.play()

        # סיום גרירה
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selected_block:
                self.selected_block.dragging = False
                self.selected_block = None

        # תנועה תוך כדי גרירה
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_block and self.selected_block.dragging:
                self.selected_block.rect.x = event.pos[0] - self.selected_block.offset_x
                self.selected_block.rect.y = event.pos[1] - self.selected_block.offset_y

        # לחיצה על ENTER לבדיקה
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            sorted_blocks = sorted(self.blocks, key=lambda b: b.rect.y)
            player_order = [b.text for b in sorted_blocks]

            if player_order == self.code_order:
                self.success = True
                self.success_sound.play()
                return "hacker_test"  # מעבר למסך הבא
            else:
                self.failed = True
                self.fail_sound.play()

    def update(self):
        """
        לא נדרש עדכון ממושך – כל העדכונים מבוצעים באירועים.
        """
        pass

    def draw(self, surface):
        """
        מצייר את הבלוקים והוראות ההפעלה, כולל הודעת כישלון אם יש.
        """
        surface.fill((0, 0, 0))

        for block in self.blocks:
            block.draw(surface)

        # טקסט הוראה
        instructions = self.font.render("Arrange the code blocks correctly, then press [ENTER]", True, (0, 200, 0))
        surface.blit(instructions, (50, 30))

        if self.failed:
            msg = self.font.render("❌ Incorrect order, try again!", True, (255, 50, 50))
            surface.blit(msg, (50, 600))
