import pygame
from logic.player import Player
from logic.enemy import Enemy

class BossFightLogic:
    """
    לוגיקה של קרב הבוס האחרון במשחק.
    מנהל את השחקן, הבוס, קליעים, תזוזות, התנגשות בקירות ובבוס.
    """

    def __init__(self):
        """
        מאתחל את מיקום השחקן, הבוס, הקירות, קליעים, משתני מצב.
        """
        self.WIDTH, self.HEIGHT = 1000, 700
        self.player = Player(50, 50)
        self.boss = Enemy(900, 600)
        self.bullets = []
        self.bullet_speed = 10
        self.boss_defeated = False

        # קירות המפה שמונעים מהשחקן והבוס לעבור
        self.walls = [
            pygame.Rect(0, 0, self.WIDTH, 20),
            pygame.Rect(0, 0, 20, self.HEIGHT),
            pygame.Rect(0, self.HEIGHT - 20, self.WIDTH, 20),
            pygame.Rect(self.WIDTH - 20, 0, 20, self.HEIGHT),
            pygame.Rect(100, 100, 800, 20),
            pygame.Rect(100, 100, 20, 500),
            pygame.Rect(100, 580, 600, 20),
            pygame.Rect(680, 200, 20, 400),
            pygame.Rect(200, 200, 500, 20),
            pygame.Rect(200, 300, 20, 200),
            pygame.Rect(300, 300, 400, 20),
            pygame.Rect(400, 400, 20, 180),
            pygame.Rect(500, 500, 200, 20),
        ]

    def collide_with_walls(rect):
        """
        פונקציה סטטית (לא בשימוש כרגע) שבודקת האם ריבוע מתנגש באחד הקירות.
        :param rect: pygame.Rect לבדיקה
        :return: True אם יש התנגשות, אחרת False
        """
        for wall in walls:
            if rect.colliderect(wall):
                return True
        return False

    def update(self, keys):
        """
        מעדכן את מצב השחקן, הבוס והקליעים בכל פריים.
        :param keys: לחיצות המקלדת (pygame.key.get_pressed())
        """
        self.player.move(keys, self.walls)
        self.boss.follow(self.player.rect, self.walls)

        for bullet in self.bullets[:]:
            bullet.x += self.bullet_speed
            if bullet.colliderect(self.boss.rect):
                self.boss.health -= 1
                self.boss.flash_timer = 5
                self.bullets.remove(bullet)
            elif bullet.x > self.WIDTH:
                self.bullets.remove(bullet)

    def fire_bullet(self):
        """
        יוצר קליע חדש שיוצא מהשחקן.
        """
        bullet = pygame.Rect(self.player.rect.centerx, self.player.rect.centery, 8, 4)
        self.bullets.append(bullet)

    def take_damage(self):
        """
        מפחית חיים מהבוס ומפעיל אפקט הבהוב זמני (כרגע לא בשימוש ישיר).
        """
        if self.health > 0:
            self.health -= 1
            self.flash_timer = 5
