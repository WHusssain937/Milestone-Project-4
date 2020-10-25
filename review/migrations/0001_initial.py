# Generated by Django 3.1.1 on 2020-10-25 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0003_auto_20200914_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=254)),
                ('model', models.CharField(max_length=254)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('fuel_type', models.CharField(blank=True, max_length=254, null=True)),
                ('transmission', models.CharField(blank=True, max_length=254, null=True)),
                ('review_by', models.CharField(max_length=254)),
                ('car_review', models.CharField(max_length=254)),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.brand')),
            ],
        ),
    ]
