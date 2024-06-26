# Generated by Django 2.2.28 on 2024-06-03 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('image_1', models.ImageField(upload_to='images/')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_6', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_7', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_8', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('video_1', models.FileField(blank=True, null=True, upload_to='videos/')),
            ],
        ),
    ]
