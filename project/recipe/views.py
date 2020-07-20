import datetime
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView, ListView, CreateView,FormView
from .models import Recipes, Categorys, Materials, User, MaterialControl, RecipeImage
import logging

from .model.model_control import RecipeControl
from .model.entity import RecipeListEntity, SearchFormList, RecipeDetailEntity

from django.urls import reverse_lazy
from django.db import transaction
from .forms import RecipeCreateForm, RecipeUpdateForm

from django.http import HttpResponse
import datetime
import os

class RecipeDetail(TemplateView):
    """
    レシピ詳細画面ビュークラス
    """
    template_name = 'recipe/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = Recipes.objects.get(pk=self.kwargs.get('recipe_id'));
        context['recipe'] = recipe

        result = Recipes.objects\
                    .select_related("category") \
                    .select_related("user") \
                    .select_related("recipe_image") \
                    .prefetch_related('material') \
                    .get(pk=self.kwargs.get('recipe_id'))

        context['detail'] = self.create_detail_data(result)
        return context

    def create_detail_data(self, result):
        recipe_detail_entity = RecipeDetailEntity(
            result.id,
            result.user.user_name,
            result.recipe_title,
            result.recipe_sentents,
            result.created_sum,
            result.material.all(),
            result.category.category_name,
            0,
            result.recipe_image
        )
        return recipe_detail_entity

class RecipeListView(ListView):
    """
    レシピ一覧画面ビュークラス
    """
    template_name = 'recipe/recipe_list.html'
    context_object_name = "recipe_list"

    def get_queryset(self):
        parameter = self.request.GET
        # logを出力
        logger = logging.getLogger("consol")

        if parameter:
            # クエリパラメータの設定
            category_para = parameter.get('categorys')
            material_para = parameter.get('materials').split(',')
            is_category_para = (int(category_para) > 0)
            is_material_para = (len(material_para[0]) > 0)

            # レシピ情報の検索
            if is_category_para and is_material_para:
                # 検索条件が全て揃う場合
                result = Recipes.objects \
                    .select_related("category") \
                    .select_related("user") \
                    .select_related("recipe_image") \
                    .prefetch_related('material') \
                    .filter(
                        recipe_title__contains=parameter.get('title'),
                        category=category_para,
                        material__id__in=material_para
                )
            elif not is_category_para and is_material_para:
                # 検索条件にカテゴリーがない場合
                result = Recipes.objects \
                    .select_related("category") \
                    .select_related("user") \
                    .select_related("recipe_image") \
                    .prefetch_related('material') \
                    .filter(
                        recipe_title__contains=parameter.get('title'),
                        material__id__in=material_para
                )
            elif is_category_para and not is_material_para:
                # 検索条件に材料がない場合
                result = Recipes.objects \
                    .select_related("category") \
                    .select_related("user") \
                    .select_related("recipe_image") \
                    .prefetch_related('material') \
                    .filter(
                        recipe_title__contains=parameter.get('title'),
                        category=category_para
                )
            else:
                result = Recipes.objects \
                    .select_related("category") \
                    .select_related("user") \
                    .select_related("recipe_image") \
                    .prefetch_related('material') \
                    .filter(
                        recipe_title__contains=parameter.get('title')
                    )
            recipe_edited_info = createRecipeListInfo(result)
        else:
            # クエリパラメータがない場合
            logger.info("all queryset")
            result = Recipes.objects.all()\
                .select_related("category")\
                .select_related("user")\
                .prefetch_related('material')

            recipe_edited_info = createRecipeListInfo(result)
        return recipe_edited_info

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameter = self.request.GET
        logger = logging.getLogger("consol")
        logger.info(parameter)

        search_form_list = SearchFormList(
            Categorys.objects.all(),
            Materials.objects.all()
        )
        context['search_form_list'] = search_form_list

        # クエリパラメータの有無を判定
        if len(parameter) <= 0:
            return context
        print(parameter)

        context['parameter'] = parameter
        return context
        
    

class MypageView(TemplateView):
    """
    マイページビュークラス
    """
    template_name = 'recipe/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('user_id'))
        context['user'] = user

        result = Recipes.objects\
            .select_related("category")\
            .select_related("user")\
            .prefetch_related('material')\
            .filter(
                user_id=self.kwargs.get('user_id')
            )

        recipe_edited_info = createRecipeListInfo(result)

        context['recipe_list'] = recipe_edited_info


        return context


class RecipeCreateFormView(FormView):
    """
    レシピ投稿画面
    """
    template_name = 'recipe/recipe_create.html'
    form_class = RecipeCreateForm
    success_url = reverse_lazy('recipe:recipes')
    # logを出力
    logger = logging.getLogger("consol")

    def form_invalid(self, form):
        logger = logging.getLogger("consol")
        logger.info(type(form))
        # form_get = self.get_form()
        # logger.info(form_get.recipe_title)
        return super().form_invalid(form)

    def form_valid(self, form):
        post_data = self.request.POST
        logger = logging.getLogger("consol")
        logger.info("post_data")

        # Recipeの保存
        # トランザクション開始
        with transaction.atomic():
            recipe = Recipes()
            recipe.user = User.objects.get(pk=1)
            recipe.category = Categorys.objects.get(
                pk=int(post_data.get('category_id_choice')[0])
                )
            recipe.recipe_title = post_data.get('recipe_title')
            recipe.recipe_sentents = post_data.get('recipe_sentence')
            recipe.created_sum = 0
    
            # レシピ画像の作成、保存
            recipe_image = RecipeImage(
                image_path=self.request.FILES['recipe_image']
            )
            recipe_image.save()

            recipe.recipe_image = recipe_image
            recipe.save()

            for material_choice_id in post_data.getlist('material_id_multi_choice'):
                material_controll = MaterialControl.objects.create(
                    recipe=recipe,
                    material=Materials.objects.get(pk=int(material_choice_id)),
                    amount='g'
                )

        return super().form_valid(form)


class RecipeEditFormView(FormView):
    # レシピ編集画面ビュー
    template_name = 'recipe/recipe_edit.html'
    form_class = RecipeUpdateForm
    success_url = reverse_lazy('recipe:mypage', kwargs={'user_id': 1})

    def get_form_kwargs(self):
        kwargs = super(RecipeEditFormView, self).get_form_kwargs()
        
        recipe = Recipes.objects\
            .select_related("category")\
            .select_related("user") \
            .select_related("recipe_image") \
            .prefetch_related('material') \
            .filter(
                id= self.kwargs.get('recipe_id')
            )

        logger = logging.getLogger("consol")
        logger.info(recipe)
        logger.info(self.kwargs.get('recipe_id'))

        kwargs['recipe_title'] = recipe[0].recipe_title
        kwargs['recipe_sentence'] = recipe[0].recipe_sentents
        kwargs['recipe_image'] = recipe[0].recipe_image
        kwargs['category_id_choice'] = [recipe[0].category.id]
        kwargs['material_id_multi_choice'] = [material.id for material in recipe[0].material.all()]
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def form_invalid(self, form):
        logger = logging.getLogger("consol")
        logger.info(type(form))
        return super().form_invalid(form)

    def form_valid(self, form):
        post_data = self.request.POST
        logger = logging.getLogger("consol")
        logger.info("update recipe data")

        with transaction.atomic():
            # レシピテーブル更新
            recipe = Recipes.objects.get(pk=self.kwargs.get('recipe_id'))
            recipe.category = Categorys.objects.get(
                pk=int(post_data.get('category_id_choice')[0])
            )
            recipe.recipe_title = post_data.get('recipe_title')
            recipe.recipe_sentents = post_data.get('recipe_sentence')
            recipe.created_sum = 0
            
            # レシピ画像の削除
            recipe_image_delete = recipe.recipe_image
            if os.path.exists(recipe_image_delete.image_path.name):
                os.remove(recipe_image_delete.image_path.name)

            # レシピ画像テーブルの更新
            recipe_image = RecipeImage(
                image_path=self.request.FILES['recipe_image']
            )
            recipe_image.save()

            recipe.recipe_image = recipe_image
            recipe.save()

            # 材料の紐付け削除
            MaterialControl.objects.filter(recipe_id=recipe.id).delete()

            for material_choice_id in post_data.getlist('material_id_multi_choice'):
                material_controll = MaterialControl.objects.update_or_create(
                    recipe=recipe,
                    material=Materials.objects.get(pk=int(material_choice_id)),
                    amount='g'
                )

        return super().form_valid(form)



def createRecipeListInfo(recipe_list):
    """
    レシピ一覧表示用データ整形メソッド
    """
    recipe_edited_info = list()
    for recipe in recipe_list:
        material_info_str = ""
        is_first_matrial = True
        for material in recipe.material.all():
            if is_first_matrial:
                material_info_str = material.material_name
                is_first_matrial = False
                continue
            material_info_str += "," + material.material_name

        recipe_entity = RecipeListEntity(
            recipe.id,
            recipe.user.id,
            recipe.user.user_name,
            recipe.recipe_title,
            recipe.recipe_sentents,
            recipe.created_sum,
            material_info_str,
            recipe.category.category_name,
            0,
            recipe.recipe_image
        )
        recipe_edited_info.append(recipe_entity)
        
    return recipe_edited_info


def get_test_response(request, test_id):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
