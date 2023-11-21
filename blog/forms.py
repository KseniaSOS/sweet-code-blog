from .models import Comment, Recipe
from django import forms
from django_summernote.widgets import SummernoteWidget

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
        based on the post model. It also adds a number
        of widgets to customize and add functionality
        to the form.
        """

        model = Recipe
        fields = ('title', 'excerpt', 'featured_image', 'cooking_time',
                  'category', 'ingredients', 'description',  'status',)

        widgets = {
                        'excerpt': SummernoteWidget(),
                        'category': forms.Select(
                            attrs={'class': 'form-select'}),
                        'ingredients': SummernoteWidget(),
                        'description': SummernoteWidget(),
                        'cooking_time': forms.NumberInput(),                                               
                        'status': forms.Select(attrs={'class': 'form-select'}),
                        }
        
