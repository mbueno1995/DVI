from django.contrib import admin
from .models import Video, CUser, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'displayname', 'emailID')
    list_editable = ('password', 'displayname', 'emailID')
admin.site.register(CUser, UserAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('category', 'videotitle', 'videodesc', 'videofile', 'thumbnailimg', 'vusername', 'created', 'updated')
    list_filter =  ('category', 'videotitle', 'videodesc', 'vusername', 'created', 'updated')
    list_editable = ('videotitle', 'videodesc', 'videofile', 'thumbnailimg')
admin.site.register(Video, VideoAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('v_id', 'cname', 'content', 'created_on')
    list_filter = ("created_on",)
admin.site.register(Comment, CommentAdmin)