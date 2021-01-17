# Generated by Django 2.2.17 on 2021-01-16 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='index',
        ),
        migrations.AddField(
            model_name='content',
            name='pos_x',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='content',
            name='postcard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='blog.Postcard'),
        ),
    ]
