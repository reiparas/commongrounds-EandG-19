from django.contrib import admin
from .models import Commission, CommissionType

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'people_required', 'created_on', 'updated_on')

@admin.register(CommissionType)
class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
