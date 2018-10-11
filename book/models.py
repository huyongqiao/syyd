from django.db import models
from django.utils.timezone import now


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='笔名')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = "作者列表"
        ordering = ['id']

    def __str__(self):
        return self.name


class Novel(models.Model):
    name = models.CharField(max_length=64, verbose_name='名称')
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, verbose_name='作者')
    category = models.CharField(max_length=64, default='', verbose_name='分类')
    cover = models.CharField(max_length=128, default='', verbose_name='封面图片')
    intro = models.TextField(default='', verbose_name='小说简介')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    mark_num = models.IntegerField(default=0, verbose_name='收藏量')
    vote_num = models.IntegerField(default=0, verbose_name='推荐量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    chapter_num = models.IntegerField(default=0, verbose_name='小说章节数')
    is_over = models.BooleanField(default=False, verbose_name='是否完本')

    class Meta:
        verbose_name = '小说'
        verbose_name_plural= '小说列表'
        unique_together = ['name', 'author']
        ordering = ['id']

    def __str__(self):
        return self.name


class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.DO_NOTHING, verbose_name='小说')
    title = models.CharField(max_length=256, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节列表'
        ordering = ['id']

    def __str__(self):
        return self.title
