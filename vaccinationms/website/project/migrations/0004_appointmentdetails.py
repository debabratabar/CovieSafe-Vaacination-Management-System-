# Generated by Django 4.0.4 on 2022-05-23 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_searchbypinordistrinct_delete_searchbydistrict_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='appointmentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=50)),
                ('hospital_name', models.CharField(default='', max_length=60)),
                ('Date', models.DateField(default='')),
                ('Time', models.TimeField(default='')),
            ],
        ),
    ]