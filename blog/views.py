from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Recipe, Category
from .forms import CommentForm, CreateRecipeForm, AddCategoryForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class RecipeDetail(View):
 
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by("-created_on")        
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True        

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,                
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by("-created_on")        
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True  

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,             
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

class RecipeLike(View):
    """
    This class handles the like functionality on the site.
    """

    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.likes.filter(id=self.request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))
   

class CreateRecipe(generic.CreateView):
    """
    This form allows user create a new recipe"
    """
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'create_recipe.html'

    
    def post(self, request, *arg, **kwargs): 
        
        recipe_form = CreateRecipeForm(data=request.POST)
        if recipe_form.is_valid():
            recipe_form.instance.author = request.user
            recipe = recipe_form.save(commit=False)
            recipe.approved = False
            recipe.save()            
        else:
            recipe_form = CreateRecipeForm

        return HttpResponseRedirect(reverse('create_recipe'))


class AddCategory(generic.CreateView):
    """
    This form allows admin create a new category"
    """
    model = Category
    form_class = AddCategoryForm
    template_name = 'add_category.html'

    def get(self, request, *arg, **kwargs):
        category = Category.objects.all()

        return render(
            request,
            "add_category.html",
            {
                "category": category,
                "category_form": AddCategoryForm()
            },
        )

    def post(self, request, *arg, **kwargs):
        category = Category.objects.all()

        category_form = AddCategoryForm(data=request.POST)

        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.approved = False
            category.save()            
        else:
            category_form = AddCategoryForm

        return HttpResponseRedirect(reverse('add_category'))


def CategoryView(request):
    categorys = Category.objects.all()
    context = {'categorys': categorys}
    template = 'base.html'

    return render(request, template, context)