# Generated by Django 3.2.23 on 2023-11-13 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_describtion_recipe_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category_name']},
        ),
        migrations.RemoveField(
            model_name='category',
            name='recipe_category',
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=40, verbose_name='Category'),
        ),
    ]
