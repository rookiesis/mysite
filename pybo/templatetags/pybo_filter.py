# 필터 혹은 함수를 등록하기 위해 필요한 모듈
from django import template

# 마크다운 -> html 태그로 변환
import markdown

# 장고 이스케이프에서 안전한 html 태그로 렌더링하기 위해 필요
from django.utils.safestring import mark_safe

# 필터 or 함수를 등록하기 위한 객체화
register = template.Library()


# 실제 등록
@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value):            # value는 마크다운 언어로 입력받을 값
    # nl2br(=nl to br): 줄바꿈(뉴라인을 <br>태그로 바꿔서 입력. 텍스트에서 줄바꿈을 유지)
    # fenced_code: (code fence) 코드라인을 <pre><code>...</code></pre>로 변환
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))