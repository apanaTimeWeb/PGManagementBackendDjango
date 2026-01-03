from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TenantProfile, OwnerProfile, StaffProfile, ParentStudentMapping, ActivityLog

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_photo_url', 'date_of_birth', 'gender', 'language_code')}),
    )

@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'total_properties_count', 'created_at')

@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pg_credit_score', 'wallet_balance', 'created_at')
    # Note: property/room/bed fields commented out in list_display until properties app exists
    # list_display += ('property', 'room')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'employment_status', 'joined_at')

@admin.register(ParentStudentMapping)
class ParentStudentMappingAdmin(admin.ModelAdmin):
    list_display = ('parent_user', 'student_tenant', 'relationship')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'severity', 'timestamp', 'ip_address')
    list_filter = ('severity', 'timestamp', 'action')
    readonly_fields = ('timestamp',)
