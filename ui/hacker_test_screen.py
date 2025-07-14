import pygame
from interfaces.screen_interface import ScreenInterface

class HackerTestScreen(ScreenInterface):
    """
    מסך חידון אבטחת מידע/האקר לפני שלב הבוס.
    מציג סדרת שאלות עם אפשרויות בחירה (A/B/C) —
    אם השחקן עונה על כל השאלות נכון → עובר לבוס, אחרת למסך סיום.
    """

    def __init__(self):
        """
        מאתחל את משתני המסך, כולל רשימת השאלות, מדדים לעקוב אחרי תשובות וסטטוס המסך.
        """
        self.font = pygame.font.Font("assets/fonts/code_font.ttf", 28)
        self.font_small = pygame.font.Font("assets/fonts/code_font.ttf", 22)  # פונט קטן יותר להוראות
        self.question_index = 0
        self.correct_answers = 0
        self.finished = False
        self.failed = False
        self.option_rects = []
        self.user_input = ""

        self.questions = [
            {
                "q": "What does this return: length([1, 2, 3])?",
                "options": ["A. 2", "B. 3", "C. 4"],
                "answer": "B"
            },
            {
                "q": "Which symbol is used to define a function in Python?",
                "options": ["A. def", "B. func", "C. lambda"],
                "answer": "A"
            },
            {
                "q": "What error is raised when dividing by zero?",
                "options": ["A. NameError", "B. TypeError", "C. ZeroDivisionError"],
                "answer": "C"
            }
        ]

    def handle_event(self, event):
        """
        מטפל באירועים: לחיצות מקלדת או עכבר.
        ENTER בסיום → מעבר לשלב הבא/סיום.
        מקשים A/B/C או קליק → טיפול בתשובה.

        :param event: אירוע pygame
        :return: "level3" אם עבר את החידון, "end" אם נכשל, אחרת None
        """
        if self.finished:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "level3" if self.correct_answers == len(self.questions) else "end"
            return None

        # קלט מקלדת
        # קלט מקלדת
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.handle_answer("A")
            elif event.key == pygame.K_b:
                self.handle_answer("B")
            elif event.key == pygame.K_c:
                self.handle_answer("C")

        # קלט עכבר
        if event.type == pygame.MOUSEBUTTONDOWN and not self.finished:
            mouse_pos = event.pos
            for rect, letter in self.option_rects:
                if rect.collidepoint(mouse_pos):
                    self.handle_answer(letter)

        return None

    def handle_answer(self, letter):
        """
        בודקת האם התשובה שסופקה נכונה, ומעדכנת מדדים בהתאם.
        :param letter: תו A/B/C שנבחר
        """
        current = self.questions[self.question_index]
        if letter == current["answer"]:
            self.correct_answers += 1
        self.question_index += 1

        if self.question_index >= len(self.questions):
            self.finished = True
            if self.correct_answers < len(self.questions):
                self.failed = True

    def update(self):
        """
        אין עדכון דינאמי במסך זה (סטטי).
        """
        pass

    def draw(self, surface):
        """
        מצייר את החידון או את מסך הסיום (בהתאם להתקדמות).
        :param surface: המשטח עליו מציירים
        """
        surface.fill((0, 0, 0))  # רקע שחור
        self.option_rects = []

        if not self.finished:
            # ✍️ מציירים את השאלה הנוכחית
            q = self.questions[self.question_index]
            question = self.font.render(f"Q{self.question_index + 1}: {q['q']}", True, (0, 255, 0))
            surface.blit(question, (50, 100))

            # ✨ מציירים את אפשרויות התשובה
            for i, opt in enumerate(q["options"]):
                x, y = 80, 180 + i * 60
                rect = pygame.Rect(x, y, 600, 50)
                pygame.draw.rect(surface, (0, 80, 0), rect)
                pygame.draw.rect(surface, (0, 255, 0), rect, 2)

                opt_surf = self.font.render(opt, True, (0, 255, 0))
                surface.blit(opt_surf, (x + 10, y + 10))

                self.option_rects.append((rect, opt[0]))  # לשמירה על מיקום האות

            # 💡 רמז לשחקן
            hint = self.font.render("Press A / B / C or click to answer", True, (0, 120, 0))
            surface.blit(hint, (50, 400))

        else:
            # 🏁 מסך סיום
            if self.failed:
                # ❌ נכשל - רק הודעת כישלון
                msg = self.font.render("❌ Test failed. Press ENTER to continue...", True, (255, 50, 50))
                surface.blit(msg, (50, 280))
            else:
                # ✅ הצליח - שתי הודעות
                msg1 = self.font.render("✅ All correct! You may proceed to the BOSS FIGHT!", True, (0, 255, 0))
                msg2 = self.font.render("Press ENTER to continue...", True, (255, 255, 255))
                surface.blit(msg1, (50, 280))
                surface.blit(msg2, (50, 320))

