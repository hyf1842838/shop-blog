# Generated by Django 2.1.4 on 2019-01-22 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='标题')),
                ('content', models.TextField()),
                ('keywords', models.CharField(max_length=20, null=True, verbose_name='关键字')),
                ('describ', models.CharField(max_length=300, null=True, verbose_name='描述')),
                ('category', models.CharField(default=1, max_length=2, verbose_name='栏目')),
                ('tags', models.CharField(default='PHP、javascript', max_length=20, verbose_name='标签')),
                ('titlepic', models.ImageField(null=True, upload_to='upload', verbose_name='标题图片')),
                ('visibility', models.BooleanField(default=0, verbose_name='公开度')),
                ('creat_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('other_name', models.CharField(max_length=10, verbose_name='别名')),
            ],
            options={
                'db_table': 'cats',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='姓名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('icon', models.ImageField(null=True, upload_to='upload', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('operate_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='articles',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Category'),
        ),
        migrations.AddField(
            model_name='articles',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]
