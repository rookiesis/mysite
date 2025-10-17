from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from lecture.forms import LectureForm
from pybo.models import Lecture

from django.contrib.auth.decorators import login_required

@login_required(login_url='common:login')
def lecture_create(request):
    if request.method == "POST":
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.author = request.user
            lecture.create_date = timezone.now()
            lecture.save()
            return redirect('lecture:index')
    else:
        form = LectureForm()
    context = {'form': form}
    return render(request, 'lecture/lecture_form.html', context)


@login_required(login_url='common:login')
def lecture_modify(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if request.user != lecture.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('lecture:detail', lecture_id=lecture.id)
    
    if request.method == "POST":
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.author = request.user
            lecture.modify_date = timezone.now()
            lecture.save()
            return redirect('lecture:detail', lecture_id=lecture.id)
    else:
        form = LectureForm(instance=lecture)
    context = {'form': form}
    return render(request, 'lecture/lecture_form.html', context)


@login_required(login_url='common:login')
def lecture_delete(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if request.user != lecture.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('lecture:detail', lecture_id=lecture.id)
    lecture.delete()
    return redirect('lecture:index')