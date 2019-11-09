from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# this is the recommended convention for converting strings in python to human
# readable text. it passes through the translation engine if you want to
# support multiple languages. it sets up the translation files and convert the
# text appropriately
from django.utils.translation import gettext as _

from account import models


class UserAdmin(BaseUserAdmin):
    ordering = ['name']
    list_display = ['email', 'name']
    # cada () é uma seção
    # primeira seção: title
    # segunda: personal info
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # if you are providing just on field it has to have the comma after
        # 'name' otherwise it thinks this is just a string and it wont work
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    # the user admin by default takes an add field sets which defines the
    # fields that you include on the add page (is the same as create page)
    # includes email address, password and password 2
    # 'classes': that are assigned to the form. got the defaults form the user
    # admin documentation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
