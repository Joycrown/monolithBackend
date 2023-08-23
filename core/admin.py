from django.contrib import admin
from .models import User, Feedback

 
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'name',
        'call_code',
        'phone',
        'sex',
        'otp',
        'avatar',
        'active',
        'is_verified',
        'is_active',
        'is_staff',
        'is_admin',
        'is_banned',
        'slug',
        'tos',
        'created_at'
    ]
    list_filter = [
        'active',
        'is_verified',
        'is_active',
        'is_staff',
        'is_admin',
        'is_banned',
        'tos']
    search_fields = [
        'created_at', 'username', 'email', 'first_name', 'last_name']


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ('id', 'title', 'text', 'user', 'created_on')
    search_fields = ['title']



admin.site.register(User, UserAdmin)
admin.site.register(Feedback, FeedbackAdmin)