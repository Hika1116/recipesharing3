from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



## ユーザー情報定義
class UserManager(BaseUserManager):
    """
    ユーザー生成のためのヘルパークラス
    """

    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    ユーザー情報モデル
    """
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    user_name = models.CharField(max_length=150, null=True)# ユーザの名前
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='images', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = "user"


class RecipeImage(models.Model):
    """
    レシピ記事の画像情報モデル
    """
    image_path = models.ImageField(upload_to='images',blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_image"
        verbose_name = "RecipeImage"

class Categorys(models.Model):
    """
    カテゴリー情報モデル
    """
    category_name = models.CharField(max_length=150)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "categorys"
        verbose_name = "Categorys"



class Materials(models.Model):
    """
    材料情報モデル
    """
    material_name = models.CharField(max_length=150)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.material_name

    class Meta:
        db_table = "materials"
        verbose_name = "Materials"


class Recipes(models.Model):
    """
    レシピ情報モデル
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    
    category = models.ForeignKey(
        Categorys,
        on_delete=models.CASCADE
    )

    recipe_image = models.ForeignKey(
        RecipeImage,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    material = models.ManyToManyField(
        Materials,
        through="MaterialControl"
    )

    recipe_title = models.CharField(max_length=150)
    recipe_sentents = models.TextField(blank=True)
    created_sum = models.IntegerField()

    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe_title

    class Meta:
        db_table = "recipes"
        verbose_name = "Recipes"


class MaterialControl(models.Model):
    """
    材料情報中間テーブルモデル
    """
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Materials,
        on_delete=models.CASCADE
    )
    amount = models.CharField(max_length=150, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "material_control"
        verbose_name = "MaterialControl"

    
class RecipeProcessImage(models.Model):
    """
    レシピ工程画像情報モデル
    """
    image_path = models.ImageField(upload_to='images',blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_process_image"
        verbose_name = "RecipeProcessImage"

class RecipeProcess(models.Model):
    """
    レシピ工程情報モデル
    """
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    process_image = models.ForeignKey(
        RecipeProcessImage,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    process_order = models.IntegerField()
    process_text = models.TextField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "ProcessOrderNum:" + self.process_order

    class Meta:
        db_table = "recipe_process"
        verbose_name = "RecipeProcess"
    

class Favorites(models.Model):
    """
    お気に入り管理モデル
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "favorites"
        verbose_name = "Favorites"
