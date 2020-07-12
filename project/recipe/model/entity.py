
class RecipeListEntity:
    """
    レシピ一覧画面へ表示時に渡すデータ構造
    """
    def __init__(self,
                 recipe_id,
                 user_id,
                 user_name,
                 recipe_title,
                 recipe_sentents,
                 created_sum,
                 material_info_str,
                 category_name,
                 favorite_sum,
                 recipe_image):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.user_name = user_name
        self.recipe_title = recipe_title
        self.recipe_sentents = recipe_sentents
        self.created_sum = created_sum
        self.material_info_str = material_info_str
        self.category_name = category_name
        self.favorite_sum = favorite_sum
        self.recipe_image = recipe_image


    def __str__(self):
        return self.user_name + self.recipe_title

class SearchFormList:
    def __init__(self, categorys, materials):
        self.categorys = categorys
        self.materials = materials


class RecipeDetailEntity:
    """
    レシピ詳細表示用エンティティ
    """
    def __init__(self,
                 recipe_id,
                 user_name,
                 recipe_title,
                 recipe_sentents,
                 created_sum,
                 material,
                 category_name,
                 favorite_sum,
                 recipe_image):
        self.recipe_id = recipe_id
        self.user_name = user_name
        self.recipe_title = recipe_title
        self.recipe_sentents = recipe_sentents
        self.created_sum = created_sum
        self.material = material
        self.category_name = category_name
        self.favorite_sum = favorite_sum
        self.recipe_image = recipe_image
            

        
