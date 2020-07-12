from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Materials, Categorys
import logging
# from .views import RecipeEditFormView

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


# レシピ投稿新規作成フォーム
class RecipeCreateForm(forms.Form):
    recipe_title = forms.CharField(label='タイトル', required=True)
    recipe_sentence = forms.CharField(label='説明文', \
                                      widget=forms.Textarea, \
                                      required=True)

    category_id_choice = forms.ChoiceField(
        label='カテゴリー', 
        required=True
    )

    material_id_multi_choice = forms.MultipleChoiceField(
        label='材料',
        widget=forms.CheckboxSelectMultiple()
    )

    recipe_image = forms.ImageField(
        label="レシピ画像"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_list = [(0, 'カテゴリーを選択')]
        for category in Categorys.objects.all():
            category_list.append((category.id, category.category_name))
        self.fields['category_id_choice'].choices = category_list

        self.fields['material_id_multi_choice'].choices = \
            lambda: [(material.id, material.material_name) for material in Materials.objects.all()]

    def clean_category_id_choice(self):
        data = self.cleaned_data['category_id_choice']
        print('validate category',data, type(data))
        if data == '0':
            print('raise error')
            raise forms.ValidationError("いずれかのカテゴリーを選択してください。")
        return data

    def clean_recipe_image(self):
        data = self.cleaned_data['recipe_image']
        # print('validate image', data, type(data))

        return data

class RecipeUpdateForm(RecipeCreateForm):

    def __init__(self, *args, **kwargs):
        #viewからの値を取得
        title = kwargs.pop('recipe_title')
        recipe_sentence = kwargs.pop('recipe_sentence')
        recipe_image = kwargs.pop('recipe_image')
        category_id_choice = kwargs.pop('category_id_choice')
        material_id_multi_choice = kwargs.pop('material_id_multi_choice')

        # 初期化
        super().__init__(*args, **kwargs)

        logger = logging.getLogger("consol")
        # 値を設定
        self.fields['recipe_sentence'].widget.attrs['textContent'] = recipe_sentence
        self.fields['recipe_title'].widget.attrs['value'] = title
        self.fields['category_id_choice'].initial = category_id_choice
        self.fields['material_id_multi_choice'].initial = material_id_multi_choice
        self.fields['recipe_image'].widget.attrs['src'] = '/' + recipe_image.image_path.url
