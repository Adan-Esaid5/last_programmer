import pygame

class Enemy:
    """
    מחלקה שמייצגת את הבוס (האויב) במשחק.
    הבוס מסוגל לנוע לעבר השחקן, להתנגש בקירות, להבהב כאשר נפגע, ולהיות מצויר למסך.
    """

    def __init__(self, x, y):
        """
        אתחול הבוס עם מיקום התחלתי, מהירות, תמונה, חיים ומצב הבהוב.
        :param x: מיקום אופקי התחלתי של הבוס
        :param y: מיקום אנכי התחלתי של הבוס
        """
        self.rect = pygame.Rect(x, y, 50, 50)  # אזור ההתנגשות והציור
        self.speed = 2  # מהירות תנועה
        self.image = pygame.transform.scale(pygame.image.load("assets/images/boss.png"), (50, 50))  # תמונת הבוס
        self.flash_timer = 0  # זמן ההבהוב לאחר פגיעה
        self.health = 3  # כמות החיים של הבוס

    def follow(self, target, walls):
        """
        מזיז את הבוס לכיוון השחקן תוך בדיקת התנגשויות עם קירות.
        :param target: pygame.Rect של מיקום השחקן
        :param walls: רשימת הקירות לבדיקה נגד התנגשות
        """
        dx = target.x - self.rect.x
        dy = target.y - self.rect.y

        if abs(dx) > abs(dy):
            self.rect.move_ip(self.speed if dx > 0 else -self.speed, 0)
            if self.collides(walls):
                self.rect.move_ip(-self.speed if dx > 0 else self.speed, 0)
        else:
            self.rect.move_ip(0, self.speed if dy > 0 else -self.speed)
            if self.collides(walls):
                self.rect.move_ip(0, -self.speed if dy > 0 else self.speed)

    def collides(self, walls):
        """
        בודק אם הבוס מתנגש עם אחד הקירות.
        :param walls: רשימת קירות לבדיקה
        :return: True אם יש התנגשות, אחרת False
        """
        return any(self.rect.colliderect(w) for w in walls)

    def draw(self, screen):
        """
        מצייר את הבוס על המסך. אם הוא בפלאש אחרי פגיעה - מצויר כמלבן אדום.
        :param screen: משטח הציור (pygame.Surface)
        """
        if self.flash_timer > 0:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)  # פלאש אדום
            self.flash_timer -= 1
        else:
            screen.blit(self.image, self.rect)  # ציור רגיל
