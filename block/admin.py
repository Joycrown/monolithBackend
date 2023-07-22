from django.contrib import admin

from .models import Block, Post, Comment, Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'value', 'post', 'comment')

admin.site.register(Block)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote, VoteAdmin)
