from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib import messages

from pybo.forms import QuestionForm
from pybo.models import Question

from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated # 인증여부확인
from rest_framework.response import Response
from pybo.serializer import QuestionSerializer

# POST 방식의 요청만 받음
@api_view(['POST'])
# JWT 토큰으로 인증받은 사용자인지 검증(검증되지 않은 사용자는 401 응답 코드)
@permission_classes([IsAuthenticated])
def question_create(request):
    serializer = QuestionSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(author = request.user, create_date = timezone.now())
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def question_modify(request, question_id):
    question = Question.objects.get(id = question_id)

    if request.user != question.author:
        return Response({"detail": "수정권한이 없습니다."}, status=403)
        
    serializer = QuestionSerializer(Question, data = request.data, partial = True) # 변경이 일어나는 부분에 대해서만
    if serializer.is_valid():
        serializer.save(modify_date = timezone.now())
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def question_delete(request, question_id):
    question = Question.objects.get(id = question_id)

    if request.user != question.author:
        return Response({"detail": "삭제권한이 없습니다."}, status=403)
    
    question.delete()
    return Response({"index": "삭제 완료"}, status=204)