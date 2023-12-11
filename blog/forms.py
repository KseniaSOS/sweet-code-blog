from .models import Comment, Recipe, Category
from django import forms
from django_summernote.widgets import SummernoteWidget

choices = Category.objects.all().values_list('category_name', 'category_name')

choice_list = []

for item in choices:
    choice_list.append(item)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class CreateRecipeForm(forms.ModelForm):
    """
    This class creates the recipe form.
    """

    class Meta:
        """
        This meta class adds the fields to the form
        based on the recipe model. It also adds a number
        of widgets to customize and add functionality
        to the form.
        """

        model = Recipe
        fields = ('title', 'excerpt', 'featured_image', 'cooking_time',
                  'category', 'ingredients', 'description',)

        widgets = {
            'excerpt': SummernoteWidget(),
            'category': forms.Select(choices=choice_list,
                attrs={'class': 'form-select'}),
            'ingredients': SummernoteWidget(),
            'description': SummernoteWidget(),
            'cooking_time': forms.NumberInput(),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'cooking_time': 'Time in minutes',
            'featured_image': 'Image [500x500 pixels 1:1]'
        }

class AddCategoryForm(forms.ModelForm):
    """
    This class allowds admin to add a new category to the site.
    """
    class Meta:
        model= Category
        fields = ('category_name',)

        widgets = {
            'category_name': forms.TextInput(
                attrs={'placeholder': 'Enter a new category'}),
        }
