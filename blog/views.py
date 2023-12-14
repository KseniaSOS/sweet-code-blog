from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Recipe, Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CommentForm, CreateRecipeForm, AddCategoryForm
from django.urls import reverse_lazy
from django.contrib import messages


def CategoryView(request, cats):
    category_recipes = Recipe.objects.filter(approved=True, category=cats)
    category_menu = Category.objects.all()
    return render(request, 'categories.html', {
        'cats': cats.title(),
        'category_recipes': category_recipes,
        'category_menu': category_menu
    })


class AddCategory(generic.CreateView):
    """
    This form allows admin create a new category.
    No need to override the get and post methods unless you have specific logic
    that needs to be handled in these methods. The CreateView's default
    implementation should suffice for typical use cases.
    """
    model = Category
    form_class = AddCategoryForm
    template_name = 'add_category.html'
    success_url = '/sweetcode/submit-success/'


def category_submition(request):
    """
    A basic function that just returns category_submition.html to be rendered.
    """
    return render(request, 'category_submition.html')


def about(request):
    """
    A basic function that just returns about.html to be rendered.
    """
    return render(request, 'about.html')


def category_menu_context_processor(request):
    '''
    A context processor provides category(dropdown menu) across all templates.
    '''
    return {
        'category_menu': Category.objects.all()
    }


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(approved=True).order_by('-created_on')
    category = Category.objects.all()
    template_name = 'index.html'


class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(
            approved=True).order_by("-created_on")
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
        comments = recipe.comments.filter(
            approved=True).order_by("-created_on")
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


class UserRecipeView(generic.ListView):
    """
    This class filters out all the objects from the Recipe model where
    the author is equal to the logged in user.
    """
    model = Recipe
    template_name = 'user_recipes.html'
    queryset = Recipe.objects.filter(approved=True).order_by('-created_on')

    def get_queryset(self):
        queryset = Recipe.objects.filter(
            approved=True,
            author__id=self.request.user.id
        ).order_by('-created_on')
        return queryset


class CreateRecipe(generic.CreateView):
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
            messages.success(
                request, 'Recipe created and pending admin approval!')
        else:
            recipe_form = CreateRecipeForm

        return HttpResponseRedirect(reverse('user_recipes'))

    def form_valid(self, form):
        """
        Help method to add author and slug to the Post model.
        """

        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class UpdateRecipe(UpdateView):
    """
    This form allows user update own recipe"
    """
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'update_recipe.html'
    success_url = reverse_lazy('user_recipes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        form.instance.approved = False
        form.save()
        msg = 'Your recipe updated and pending admin approval!'
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(UpdateView, self).form_valid(form)


class DeleteRecipe(generic.DeleteView):
    """
    This form allows user delete own recipe.
    """
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('user_recipes')

    def delete(self, request, *args, **kwargs):
        """
        Delete method in the deleteview for displaying the success message.
        https://rb.gy/icpfyv
        """
        msg = "Your Recipe has been deleted"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(DeleteView, self).delete(request, *args, **kwargs)
