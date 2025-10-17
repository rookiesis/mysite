from django import forms

from pybo.models import Lecture

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['subject', 'content']
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }