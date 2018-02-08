from django.contrib import admin

from .models import Measure, Participant

class ParticipantInline(admin.TabularInline):
    model = Participant

class MeasureAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]

admin.site.register(Measure, MeasureAdmin)