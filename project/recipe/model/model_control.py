from django.db import connection
from collections import namedtuple
import logging


class ModelBaseControl:
    """
    生クエリでデータを取得するためのベースクラス
    """
    def namedtuplefetchall(self, cursor):
        "Return all rows from a cursor as a namedtuple"
        nt_result = namedtuple('Result', [col[0] for col in cursor.description])
        # logger = logging.getLogger("consol")
        # logger.info(nt_result)
        # logger.info("nt_result")
        return [nt_result(*row) for row in cursor.fetchall()]

    def execute(self, select_text, parameter_array=[]):
        if parameter_array:
            with connection.cursor() as cursor:
                cursor.execute(select_text, parameter_array)
                result_tuple = self.namedtuplefetchall(cursor)
        else:
            with connection.cursor() as cursor:
                cursor.execute(select_text)
                result_tuple = self.namedtuplefetchall(cursor)

        return result_tuple

class RecipeControl(ModelBaseControl):
    """
    RecipeテーブルSelectクラス
    """
    def get_all(self):
        return self.execute(
            """
            select 
            recipes.*
            from recipes
            left join categorys
            on recipes.category_id = categorys.id 
            """)

    def get_recipe_all_info(self):
        sql = """
            select
                user.id as user_id,
                user.user_name,
                recipes.id as recipe_id,
                recipes.recipe_title,
                recipes.recipe_sentents,
                recipes.created_sum,
                categorys.category_name,
                materials.material_name
            from recipes
            inner join user on user.id = recipes.user_id
            left join categorys on recipes.category_id = categorys.id
            left join material_control on material_control.recipe_id = recipes.id
            left join materials on materials.id = material_control.material_id
            """
        result_tuple = self.execute(sql)
        return result_tuple
        
