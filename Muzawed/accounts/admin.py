from django.contrib import admin
from .models import SupplierProfile, ProfileBeneficiary
# Register your models here.
class SupplierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'is_active')
    list_filter = ('status', 'is_active')
    search_fields = ('name', 'user__username')
    list_editable = ('status', 'is_active')

admin.site.register(SupplierProfile, SupplierProfileAdmin)
admin.site.register(ProfileBeneficiary)