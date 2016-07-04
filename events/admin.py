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


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'gender',
        'dob',
        'is_cohen',
        'is_single',
        'is_matchmaker',
    )
    list_filter = (
        'gender',
        'dob',
        'status',
        'is_cohen',
        'is_single',
        'is_matchmaker',
    )


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Profile, ProfileAdmin)
