# Generated by Django 3.2.4 on 2021-06-20 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_productpicture_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpicture',
            name='picture',
            field=models.ImageField(upload_to='productImages'),
        ),
    ]
