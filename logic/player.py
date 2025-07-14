import pygame

class Player:
    """
    מחלקה שמייצגת את השחקן במשחק.
    השחקן יכול לנוע בעזרת מקשי החצים, להתנגש בקירות, ולהיות מוצג על המסך.
    """

    def __init__(self, x, y):
        """
        אתחול השחקן עם מיקום, מהירות, תמונה וכמות חיים.
        :param x: קואורדינת X התחלתית של השחקן
        :param y: קואורדינת Y התחלתית של השחקן
        """
        self.rect = pygame.Rect(x, y, 40, 40)  # מיקום וגודל השחקן
        self.speed = 10  # מהירות תנועה
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/player.png"), (40, 40))  # טעינת תמונת השחקן
        self.lives = 3  # מספר החיים של השחקן

    def move(self, keys, walls):
        """
        מזיז את השחקן לפי הקלט מהמקלדת, כולל טיפול בהתנגשויות עם קירות.
        :param keys: רשימת מקשים לחוצים (pygame.key.get_pressed())
        :param walls: רשימת קירות לבדוק התנגשות מולם
        """
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        # תזוזה אופקית ובדיקה
        self.rect.move_ip(dx, 0)
        if self.collides(walls):
            self.rect.move_ip(-dx, 0)  # חזרה אחורה אם התנגש

        # תזוזה אנכית ובדיקה
        self.rect.move_ip(0, dy)
        if self.collides(walls):
            self.rect.move_ip(0, -dy)  # חזרה אחורה אם התנגש

    def collides(self, walls):
        """
        בודק אם השחקן מתנגש עם אחד הקירות.
        :param walls: רשימת קירות
        :return: True אם יש התנגשות, אחרת False
        """
        return any(self.rect.colliderect(w) for w in walls)

    def draw(self, screen):
        """
        מצייר את השחקן על המסך.
        :param screen: משטח הציור (pygame.Surface)
        """
        screen.blit(self.image, self.rect)
