# Generated by Django 3.2.23 on 2023-11-23 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20231113_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='category',
        ),
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.CharField(default='Uncategorized', max_length=200),
        ),
    ]