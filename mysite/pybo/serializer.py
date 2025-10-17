# JWT 토큰의 범위를 지정하는 파일
# JWT 토큰의 형식처럼 Json 형식으로 값들을 지정
from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Question
        fields = ['id', 'author', 'subject', 'content', 'create_date', 'modify_date', 'voter']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        models = Answer
        fields = ['id', 'author', 'question', 'content', 'create_date', 'modify_date', 'voter']