from django.db import models

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    rubrics = models.JSONField()  # Для хранения массива рубрик
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']  # Сортировка по дате создания (последние сначала)

    def __str__(self):
        return f'Document {self.id}'
