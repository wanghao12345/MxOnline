from django.contrib import admin

from .models import EmailVerifyRecord,Banner

# Register your models here.
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    '''邮箱验证码'''
    # 显示的列
    list_display = ['code','email','send_type','send_time']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code','email','send_type']
    # 过滤
    list_filter = ['code','email','send_type','send_time']
admin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)

class BannerAdmin(admin.ModelAdmin):
    '''Banner轮播图'''
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']
admin.site.register(Banner,BannerAdmin)