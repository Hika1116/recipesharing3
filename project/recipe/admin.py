from django.contrib import admin

from .models import Recipes,RecipeImage,RecipeProcess,RecipeProcessImage,MaterialControl,Materials,Categorys,User


from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm


admin.site.register(Recipes)

admin.site.register(RecipeImage)

admin.site.register(RecipeProcess)

admin.site.register(RecipeProcessImage)

admin.site.register(MaterialControl)

admin.site.register(Materials)

admin.site.register(Categorys)


class UserAdmin(BaseUserAdmin):
    """
    管理画面ユーザー登録クラス
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
