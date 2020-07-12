from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipes'),
    path('mypage/<int:user_id>', views.MypageView.as_view(), name='mypage'),
    # path('recipe_create', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe_create', views.RecipeCreateFormView.as_view(), name='recipe_create'),
    path('recipe/<int:recipe_id>', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('recipe/edit/<int:recipe_id>', views.RecipeEditFormView.as_view(), name='recipe_edit')
]