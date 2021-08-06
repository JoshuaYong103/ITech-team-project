# Generated by Django 2.1.5 on 2021-08-06 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_movieliked'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Abouts',
            },
        ),
    ]