from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

#
# class Tag_recipes(models.TextChoices):
#     BREAKFAST = 'breakfast', 'Завтрак'
#     LUNCH = 'lunch', 'Обед'
#     DINNER = 'dinner', 'Ужин'
#     TAGS = [BREAKFAST, LUNCH, DINNER]
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
        'Ingredient',
        through='IngredientValue',
        verbose_name='Ингридиенты',
    )
    # tags = models.CharField(
    #     max_length=10,
    #     choices=Tag_recipes.choices,
    # )
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


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    dimension = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
    )
    portion = models.ManyToManyField(
        Recipe,
        through='IngredientValue'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.title


class IngredientValue(models.Model):
    ingridient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingridient_values',
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingridient_values',
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_list'
    )


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
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
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    created = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
