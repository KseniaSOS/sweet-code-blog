from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('create_recipe/', views.CreateRecipe.as_view(), name='create_recipe'),
    path('user_recipes/', views.UserRecipeView.as_view(), name='user_recipes'),
    path('add_category/', views.AddCategory.as_view(), name='add_category'),
    path('category/<str:cats>/', views.CategoryView, name='category'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    path('<slug:slug>/edit/', views.UpdateRecipe.as_view(), name='update_recipe'),
    path('<slug:slug>/delete/', views.DeleteRecipe.as_view(), name='delete_recipe'),
    path('sweetcode/submit-success/', views.category_submition, name='category_submit_success'),    
]  
