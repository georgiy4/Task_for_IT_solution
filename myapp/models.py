from django.db import models
from django.core.exceptions import ValidationError

class Quote(models.Model):
    text = models.TextField(unique=True,
            error_messages={
                "unique": "Такая цитата уже существует!"
            })  # сама цитата (без дубликатов)
    source = models.CharField(max_length=200)  # источник (фильм, книга и т.д.)
    weight = models.PositiveIntegerField(default=1)  # "вес" цитаты
    likes = models.IntegerField(default=0)  # лайки
    dislikes = models.IntegerField(default=0)  # дизлайки
    views = models.IntegerField(default=0)  # сколько раз показана

    def clean(self):
        """Проверка: не больше 3 цитат у одного источника"""
        if self.pk is None:  # Только для новых объектов
            if Quote.objects.filter(source=self.source).count() >= 3:
                raise ValidationError("У одного источника не может быть больше 3 цитат")

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем проверку перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.source}'

