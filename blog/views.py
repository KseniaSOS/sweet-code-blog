from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Recipe, Category
from .forms import CommentForm, CreateRecipeForm, AddCategoryForm
from django.urls import reverse_lazy


class CategoryMenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryMenuMixin, self).get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        return context


def CategoryView(request, cats):
    category_recipes = Recipe.objects.filter(category=cats)
    category_menu = Category.objects.all()
    return render(request, 'categories.html', {
        'cats': cats.title(),
        'category_recipes': category_recipes,
        'category_menu': category_menu
    })


class RecipeList(CategoryMenuMixin, generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    category = Category.objects.all()
    template_name = 'index.html'


class RecipeDetail(CategoryMenuMixin, View):
 
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects
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
                "slug": slug,
                "comments": comments,
                "commented": False,                
                "liked": liked,
                "comment_form": CommentForm(),
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
                "comment_form": CommentForm(),
                "slug": slug,
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


class UserRecipeView(CategoryMenuMixin, generic.ListView):
    """
    This class filters out all the objects from the Recipe model where
    the author is equal to the logged in user.
    """
    model = Recipe
    template_name = 'user_recipes.html'
    queryset = Recipe.objects.order_by('-created_on')
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(
            author__id=self.request.user.id).order_by('-created_on')
        return queryset


class CreateRecipe(CategoryMenuMixin, generic.CreateView):
    """
    This form allows user create a new recipe.
    """
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'create_recipe.html'

    
    def post(self, request, *arg, **kwargs): 
        
        recipe_form = CreateRecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe_form.instance.author = request.user
            recipe_form.instance.slug = slugify(recipe_form.instance.title)
            recipe = recipe_form.save(commit=False)
            recipe.approved = False
            recipe.save()            
        else:
            recipe_form = CreateRecipeForm

        return HttpResponseRedirect(reverse('create_recipe'))

    def form_valid(self, form):
        """
        Help method to add author and slug to the Post model.
        """

        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)
        


class UpdateRecipe(CategoryMenuMixin, generic.UpdateView):
    """
    This form allows user update own recipe"
    """
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'update_recipe.html'

    
    def post(self, request, *arg, **kwargs): 
        
        recipe_form = CreateRecipeForm(data=request.POST)
        if recipe_form.is_valid():
            recipe_form.instance.author = request.user
            recipe_form.instance.slug = slugify(recipe_form.instance.title)
            recipe = recipe_form.save(commit=False)
            recipe.approved = False
            recipe.save()            
        else:
            recipe_form = CreateRecipeForm

        return HttpResponseRedirect(reverse('create_recipe'))


class DeleteRecipe(CategoryMenuMixin, generic.DeleteView):
    """
    This form allows user delete own recipe.
    """
    model = Recipe    
    template_name = 'delete_recipe.html'   
    success_url = reverse_lazy('user_recipes')


class AddCategory(CategoryMenuMixin, generic.CreateView):
    """
    This form allows admin create a new category.
    No need to override the get and post methods unless you have specific logic
    that needs to be handled in these methods. The CreateView's default
    implementation should suffice for typical use cases.
    """
    model = Category
    form_class = AddCategoryForm
    template_name = 'add_category.html'
    success_url = reverse_lazy('home')  
