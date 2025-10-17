from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count

from pybo.models import Lecture


def index(request):
    # request.GET: URL의 쿼리스트링(?뒤에 값)을 가져오는 부분
    # http://127.0.0.1/pybo/?page=1
    # page=3 이라는 요청이 들어오면 page에 3이 저장됨
    # 입력 인자
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')    # 정렬 기준

    # 정렬
    if so == 'recommend':
        lecture_list = Lecture.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        lecture_list = Lecture.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
        lecture_list = Lecture.objects.order_by('-create_date')

    # 조회
    if kw:
        lecture_list = lecture_list.filter(
            # Q 함수를 이용하여 검색
            # __icontains: 대소문자 구별 없이 부분문자열 검색(sql구문에서는 LIKE "%kw%")
            Q(subject__icontains=kw) |                  # 제목 검색
            Q(content__icontains=kw) |                  # 내용 검색
            # lecture_list에서 filter 함수를 적용
            # Lecture -> author -> username
            Q(author__username__icontains=kw) |        # 질문 글쓴이 검색
            # Lecture -> reverse FK(Answer) -> author -> username
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct() # 중복 제거
        """
        -> sql 쿼리 구문으로 바꿔보기
        select dictinct q.*
        from pybo_lecture q
        left join pybo_answer a on a.lecture_id = q.id
        right join customuser c on c.id = a.author_id
        where q.subject ilike "%kw%"
            or q.content ilike "%kw%"
            or c.username ilike "%kw%"
        """
    
    # 쿼리셋으로 조회됨
    # 페이징 처리
    paginator = Paginator(lecture_list, 10) # 페이지당 10개씩 보여 주기
    # 데이터 묶음을 전달해주기 위한 가공
    # get_page() 메서드는 유효하지 않은 번호를 넣어도 자동으로 처리(999를 넣으면 마지막 페이지 처리)
    page_obj = paginator.get_page(page)
    
    current_page = page_obj.number
    start_index = max(current_page -5, 1)
    end_index = min(current_page +5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {
        'lecture_list': page_obj,
        'page_range': page_range,
        'page': page,
        'kw': kw,
        'so': so
        }
    return render(request, 'lecture/lecture_list.html', context)

def detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id) # pk는 id와 동일
    context = {
        'lecture': lecture,
    }

    return render(request, 'lecture/lecture_detail.html', context)