from django.contrib import admin
from .models import UserVideoList, Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    pass

class UserVideoListResource(resources.ModelResource):

    class Meta:
        model = UserVideoList

@admin.register(UserVideoList)
class VideoAdmin(ImportExportModelAdmin):
    pass
