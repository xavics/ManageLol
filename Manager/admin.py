from django.contrib import admin
from models import Notice

# Register your models her
admin.site.register(Notice)
class MyModelAdmin(admin.ModelAdmin):

    def change_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['some_var'] = 'This is what I want to show'
        return super(MyModelAdmin, self).change_view(request, extra_context=extra_context)

