from django.db import models


class CreatedModel(models.Model):
    text = models.TextField(
        'Text',
        null=False,
        blank=False,
        help_text='Введите текст.'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
