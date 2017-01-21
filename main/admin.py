from django.contrib import admin
from .models import SessionAccount, Person


class SessionAccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_at', 'session_time', 'person', 'is_active')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username',)


admin.site.register(SessionAccount, SessionAccountAdmin)
admin.site.register(Person, PersonAdmin)
