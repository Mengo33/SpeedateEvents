from django.contrib import admin

from . import models


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = (
        'id',
        'title',
        'description',
        'link',
        'date',
        'singles_num',
    )
    list_filter = (
        'date',
        'singles_num',
    )
    search_fields = (
        'id',
        'title',
        'date',
        'singles_num',
    )


class ProfileUserAdmin(admin.ModelAdmin):
    list_display = (
        'profile_user_id',
        'is_matchmaker',
        'is_single',
    )


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.ProfileUser, ProfileUserAdmin)
