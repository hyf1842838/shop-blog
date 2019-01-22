from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10, unique=True,
                                verbose_name='姓名')
    password = models.CharField(max_length=255, verbose_name='密码')
    icon = models.ImageField(upload_to='upload', null=True, verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user'


class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name='名称')
    other_name = models.CharField(max_length=10, verbose_name='别名')

    class Meta:
        db_table='cats'


class Articles(models.Model):
    title = models.CharField(max_length=10, verbose_name='标题')
    content = models.TextField()
    keywords = models.CharField(max_length=20, null=True, verbose_name='关键字')
    describ = models.CharField(max_length=300, null=True, verbose_name='描述')
    category = models.CharField(max_length=2, default=1, verbose_name='栏目')
    tags = models.CharField(max_length=20, default='PHP、javascript', verbose_name='标签')
    titlepic = models.ImageField(upload_to='upload', null=True, verbose_name='标题图片')
    visibility = models.BooleanField(default=0, verbose_name='公开度')
    creat_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = 'articles'
