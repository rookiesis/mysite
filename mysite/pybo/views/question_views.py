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

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    
    serializer = QuestionSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(author = request.user, create_date = timezone.now())
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=401)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')