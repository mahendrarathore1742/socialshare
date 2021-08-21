# Generated by Django 3.1.5 on 2021-07-31 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_auto_20210729_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='position',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='Profileimage',
            field=models.ImageField(blank=True, default='userimage/user.png', null=True, upload_to='userimage'),
        ),
    ]