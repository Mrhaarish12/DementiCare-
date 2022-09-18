from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'name', 'gender', 'date_of_birth', 'caretaker_relation', 'doctor_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email','password')}),
        ('Personal info', {'fields': ('name', 'gender', 'date_of_birth', 'caretaker_relation', 'doctor_name')}),
        ('Permissions', {'fields': ('is_admin',)})

    )

    #add_fieldsets override the feildsets and display the fields which user should see.
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'name','gender','date_of_birth','caretaker_relation',
                        'doctor_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

#Now register the new UserModel Admin
admin.site.register(User, UserModelAdmin)    