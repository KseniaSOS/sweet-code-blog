from . import views
from django.urls import path


urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('create_recipe/', views.CreateRecipe.as_view(), name='create_recipe'),
    path('add_category/', views.AddCategory.as_view(), name='add_category'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    
]  
