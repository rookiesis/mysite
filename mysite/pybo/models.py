from django.db import models
from common.models import CustomUser

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField() # null=True: 공백 허용
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(CustomUser, related_name='voter_question') # voter 추가

    def __str__(self):
        return self.subject # question 호출하면 object(1)대신 subject 이름 나오게 하기

class Answer(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(CustomUser, related_name='voter_answer') # voter 추가

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)