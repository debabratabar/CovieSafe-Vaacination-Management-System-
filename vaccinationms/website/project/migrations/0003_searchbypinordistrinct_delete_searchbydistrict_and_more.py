# Generated by Django 4.0.4 on 2022-05-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_searchbydistrict_searchbypin'),
    ]

    operations = [
        migrations.CreateModel(
            name='searchByPinorDistrinct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('District_name', models.CharField(default='', max_length=6)),
                ('pin_code', models.CharField(default='', max_length=6)),
                ('hospital_name', models.CharField(default='', max_length=60)),
            ],
            options={
                'verbose_name_plural': 'searchByPin',
            },
        ),
        migrations.DeleteModel(
            name='searchByDistrict',
        ),
        migrations.DeleteModel(
            name='searchByPin',
        ),
    ]
