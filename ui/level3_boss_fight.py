import pygame
from interfaces.screen_interface import ScreenInterface
from logic.boss_logic import BossFightLogic

# --- אירוע מותאם אישית לאזהרה (לא חובה יותר כי נשלוט בזה ידנית) ----------
MY_CUSTOM_EVENT = pygame.USEREVENT + 1

class Level3BossScreen(ScreenInterface):
    """
    שלב 3 – קרב בוס. השחקן יורה (SPACE) ומנסה להביס את הבוס.
    - לשחקן 3-חיים; COLLISION מוריד חיים אחת בכל פעם.
    - ALERT נשמע רק בהתנגשות / קרבה (<120px).
    """

    def __init__(self):
        # === אתחול בסיסי ===
        self.logic = BossFightLogic()
        self.lives = 3  # כמות החיים
        self.player_hits = 0  # כמה פעמים נפגע
        self.damage_cooldown = 30  # כדי שלא ימות מיד (½ שנייה ב-60 FPS)

        self.game_over = False
        self.win = False
        self.paused = False

        self.font = pygame.font.SysFont("consolas", 24)

        # -------------------------------------------------
        #  טעינת סאונדים עם Error-Handling
        # -------------------------------------------------
        def safe_load(path: str):
            """מנסה לטעון סאונד; אם נכשל - מחזיר None ולא מפיל את המשחק."""
            try:
                return pygame.mixer.Sound(path)
            except pygame.error:
                print(f"⚠️  לא נמצא/נטען: {path}")
                return None

        self.alert_sound = safe_load("assets/sounds/alert.mp3")
        self.win_sound = safe_load("assets/sounds/win.mp3")
        self.lose_sound = safe_load("assets/sounds/lose_game.mp3")

        # מוזיקת רקע
        try:
            pygame.mixer.music.load("assets/sounds/fight_sound.mp3")
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("⚠️  קובץ fight_sound.mp3 לא נטען – ממשיכים בלי מוזיקת רקע")

        # הודעת אזהרה על המסך
        self.alert_msg = ""
        self.alert_timer = 0  # כמה פריימים עוד נשאר להציג Alert

    # ------------------------------------------------------------------ #
    #                   event-loop  –  מקלדת / עכבר                      #
    # ------------------------------------------------------------------ #
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # PAUSE / MENU
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.paused = not self.paused
                return

            if self.paused:
                if event.key == pygame.K_r:          # חזרה ממשחק עצור
                    self.paused = False
                elif event.key == pygame.K_ESCAPE:   # יציאה לתפריט
                    pygame.mixer.music.stop()
                    return "menu"
                return

            # ירי
            if not self.game_over and event.key == pygame.K_SPACE:
                self.logic.fire_bullet()

            # מעבר מסך אחרי סיום
            if self.game_over:
                return "victory" if self.win else "end"

    # ------------------------------------------------------------------ #
    #                               update                               #
    # ------------------------------------------------------------------ #
    def update(self):
        if self.paused or self.game_over:
            return

        self.logic.update(pygame.key.get_pressed())

        # ↓↓↓ COOL-DOWN למניעת ספאם פגיעות
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # 1️⃣  טיפול בהתנגשות / קרבה מסוכנת
        dist = self.logic.boss.rect.centerx - self.logic.player.rect.centerx
        dist **= 2
        dist += (self.logic.boss.rect.centery - self.logic.player.rect.centery) ** 2
        close_enough = (dist ** 0.5) < 120

        if (self.logic.boss.rect.colliderect(self.logic.player.rect) or close_enough) and self.damage_cooldown == 0:
            # -- ALARM
            self.alert_sound.play()
            self.alert_msg   = "⚠ MEMORY LEAK DETECTED!"
            self.alert_timer = 180          # ~3 שניות
            # -- מוריד חיים רק בהתנגשות בפועל
            if self.logic.boss.rect.colliderect(self.logic.player.rect):
                self.player_hits  += 1
                self.lives        = max(0, 3 - self.player_hits)
                self.damage_cooldown = 30   # 0.5 שניה חסינות

        # 2️⃣  כיבוי הודעת האזהרה
        if self.alert_timer > 0:
            self.alert_timer -= 1
        else:
            self.alert_msg = ""

        # 3️⃣  ניצחון / הפסד
        if self.logic.boss.health <= 0:
            self._finish(victory=True)
            return "victory"

        if self.lives <= 0:
            self._finish(victory=False)
            return "end"

    # ------------------------------------------------------------------ #
    #                               draw                                 #
    # ------------------------------------------------------------------ #
    def draw(self, screen):
        screen.fill((0, 0, 0))

        if self.paused:
            pause_txt = self.font.render("Game Paused  |  R-Resume  ESC-Menu", True, (255, 255, 0))
            screen.blit(pause_txt, (screen.get_width()//2 - pause_txt.get_width()//2,
                                    screen.get_height()//2))
            return

        # קירות, שחקן, בוס, קליעים
        for wall in self.logic.walls:
            pygame.draw.rect(screen, (0, 255, 0), wall, 1)

        self.logic.player.draw(screen)
        self.logic.boss.draw(screen)

        for bullet in self.logic.bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)

        # HUD
        hud = self.font.render(
            f"Lives: {self.lives}    Enemy HP: {self.logic.boss.health}", True, (0, 255, 0))
        screen.blit(hud, (20, 15))

        # ALERT
        if self.alert_msg:
            alert = self.font.render(self.alert_msg, True, (255, 0, 0))
            screen.blit(alert, (screen.get_width()//2 - alert.get_width()//2, 60))

    # ------------------------------------------------------------------ #
    #                    פעולת סיום (ניצחון / הפסד)                     #
    # ------------------------------------------------------------------ #
    def _finish(self, *, victory: bool):
        """
        פעולה אחודה לסיום הקרב.
        - עוצרת מוזיקת-רקע ו-Alert.
        - משמיעה סאונד ניצחון/הפסד.
        - שומרת סטטוסים (game_over / win).
        """
        self.game_over = True
        self.win = victory

        # 1) עוצר מוזיקה קיימת
        pygame.mixer.music.stop()

        # 2) עוצר Alert  (אם עדיין מתנגן/מופיע)
        if self.alert_sound:  # ייתכן שה-safe_load החזיר None
            self.alert_sound.stop()  # מפסיק את הצליל מיד
        self.alert_msg = ""  # מוחק הודעה על המסך
        self.alert_timer = 0  # מאפס את הטיימר

        # 3) מכבה טיימר מותאם-אישית (למקרה שהשתמשנו בו)
        pygame.time.set_timer(MY_CUSTOM_EVENT, 0)

        # 4) משמיע סאונד ניצחון / הפסד
        snd = self.win_sound if victory else self.lose_sound
        if snd:  # שוב—יכול להיות None אם לא נטען
            snd.play()

        # ✨ (לא חובה) –‐ אם תרצה גם מוזיקת-רקע חדשה בניצחון:
        if victory:
            try:
                pygame.mixer.music.load("assets/sounds/victory_theme.mp3")
                pygame.mixer.music.play()
            except pygame.error:
                print("⚠️ קובץ victory_theme.mp3 לא נטען")
