from django.contrib import admin
from .models import Recipe, Comment, Category
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """
    This class adds fields from the Recipe model to the admin
    panel and performs a function like approving a recipe to a dropdown list of actions.
    """

    list_display = ('title', 'slug', 'status', 'created_on', 'approved')
    search_fields = ['title', 'category', 'author']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'description', 'excerpt')
    actions = ['approve_recipe', 'unapprove']

    def approve_recipe(self, request, queryset):
        queryset.update(approved=True)


    def unapprove(self, request, queryset):       
        queryset.update(approved=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    This class adds fields from the Comment model to the admin
    panel and performs a function like approving a recipe to a dropdown list of actions.
    """
    list_display = ('name', 'body', 'recipe', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    This class adds fields from the Category model to the admin
    panel
    """
    list_display = ('category_name',)
   