from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

#
# class Tags(models.TextChoices):
#     BREAKFAST = 'breakfast', 'Завтрак'
#     LUNCH = 'lunch', 'Обед'
#     DINNER = 'dinner', 'Ужин'
#
#


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True,
        max_length=100,
        blank=True,
        null=True
    )
    color = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    dimension = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_recipe',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фото',
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=5000
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientValue',
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='в минутах',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def display_favorites(self):
        return ', '.join(
            self.favorites.all().values_list(
                'user__username',
                flat=True
            )
        )

    display_favorites.short_description = 'В избранном'


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_values',
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list',
        verbose_name='Автор',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_list',
        verbose_name='Список покупок',
    )

    class Meta:
        unique_together = ('user', 'recipe',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        null=True,
    )

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_favorites',
        verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранные рецепты',
    )
    created = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-created',)
        unique_together = ('user', 'recipe',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
