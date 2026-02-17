from django.contrib import admin
from .models import UpdateData


@admin.register(UpdateData)
class UpdateDataAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "website")
    search_fields = ("name", "email", "phone", "message")
    list_per_page = 25
