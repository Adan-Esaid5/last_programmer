from typing import Optional
import pygame
from abc import ABC, abstractmethod

class ScreenInterface(ABC):
    """
    ממשק אבסטרקטי עבור כל המסכים במשחק.
    כל מסך (כמו מסך תפריט, הוראות, שלב, ניצחון וכו') צריך לממש את המחלקה הזו.
    """

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        מטפל באירועים (כגון לחיצות מקלדת/עכבר).
        :param event: האירוע שהתקבל מפייגיים
        :return: מחרוזת עם שם המסך הבא, אם יש צורך לעבור מסך, אחרת None
        """
        pass

    @abstractmethod
    def update(self) -> Optional[str]:
        """
        מעדכן את הלוגיקה של המסך (למשל תנועה, בדיקות תנאים וכו').
        :return: מחרוזת עם שם המסך הבא, אם יש מעבר מסך, אחרת None
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את תוכן המסך על גבי ה־Surface שנשלח.
        :param surface: משטח הציור של פייגיים (לרוב המסך הראשי)
        """
        pass
