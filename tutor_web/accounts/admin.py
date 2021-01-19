from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models

#######################################################################################################################


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'get_profile_link')
    search_fields = ('email', )
    readonly_fields = ('id', 'date_joined', 'last_login', 'get_profile_link')
    exclude = ('username', 'password', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def get_profile_link(self, obj: models.CustomUser):
        return mark_safe(
            f"""<a href="{reverse('admin:accounts_profile_change', args=(obj.profile.pk,))}">{obj.full_name}</a>"""
        )

    get_profile_link.short_description = 'profile link'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_link')
    readonly_fields = ('id', 'get_user_link')
    exclude = ('USERNAME_FIELD', 'user')
    search_fields = ('user__email', 'user__last_name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()

    def get_user_link(self, obj: models.Profile):
        return mark_safe(
            f"""<a href="{reverse('admin:accounts_customuser_change', args=(obj.pk,))}">{obj}</a>"""
        )

    get_user_link.short_description = 'user link'


#######################################################################################################################


admin.site.register(models.CustomUser, CustomUserAdmin)

admin.site.register(models.Profile, ProfileAdmin)



