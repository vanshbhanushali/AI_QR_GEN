from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, QRCodeHistory

# -----------------------------------------------------------
# 1. Register UserProfile (Inlining it with the built-in User)
# -----------------------------------------------------------

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    
# Extend the default UserAdmin to include the profile inline
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    # Add mobile number to the list display (optional)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff') 

# Re-register User with the custom UserAdmin
# Must unregister the old one before registering the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# -----------------------------------------------------------
# 2. Register QRCodeHistory
# -----------------------------------------------------------

@admin.register(QRCodeHistory)
class QRCodeHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'generated_at', 'data_content', 'prompt_used')
    search_fields = ('user__username', 'data_content', 'data_content')
    list_filter = ('generated_at',)
    # Makes sure these fields cannot be changed via the admin
    readonly_fields = ('generated_at', 'qr_code_path')

# End of File