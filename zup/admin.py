from django.contrib import admin
from zup.models import Url, Job

class JobAdmin(admin.ModelAdmin):
  search_fields = ['name']


class UrlAdmin(admin.ModelAdmin):
  search_fields = ['url']


admin.site.register(Job, JobAdmin)
admin.site.register(Url, UrlAdmin)