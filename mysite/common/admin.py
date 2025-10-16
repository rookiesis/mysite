from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

# UserAdmin을 상속받는 CustomUserAdmin 클래스를 만듭니다.
class CustomUserAdmin(UserAdmin):
    # 관리자 페이지의 사용자 목록(list)에 보여줄 필드를 설정합니다.
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    
    # 사용자를 생성하고 수정하는 페이지에 노출될 필드를 설정합니다.
    # UserAdmin.fieldsets는 튜플이므로 리스트로 변환 후 수정하고 다시 튜플로 만듭니다.
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')})
    fieldsets = tuple(fieldsets)


# admin.site.register()를 사용하여 CustomUser 모델과 CustomUserAdmin 클래스를 등록합니다.
admin.site.register(CustomUser, CustomUserAdmin)

# 이거 넣어서 우리가 만든 필드를 주면 나와