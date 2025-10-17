from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from django.contrib import messages

from pybo.forms import AnswerForm
from pybo.models import Answer

from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated # 인증여부확인
from rest_framework.response import Response
from pybo.serializer import AnswerSerializer


# 답변 페이징과 정렬 기능
# 페이징
from django.core.paginator import Paginator
from django.db.models import Q, Count

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer_create(request):
    serializer = AnswerSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(author = request.user, create_date = timezone.now())
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def answer_modify(request, answer_id):
    answer = Answer.objects.get(id = answer_id)

    if request.user != answer.author:
        return Response({"detail": "수정권한이 없습니다."}, status=403)

    serializer = AnswerSerializer(Answer, data = request.data, partial = True) # 변경이 일어나는 부분에 대해서만
    if serializer.is_valid():
        serializer.save(modify_date = timezone.now())
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def answer_delete(request, answer_id):
    answer = Answer.objects.get(id = answer_id)

    if request.user != answer.author:
        return Response({"detail": "삭제권한이 없습니다."}, status=403)
    
    answer.delete()
    return Response({"index": "삭제 완료"}, status=204)