import random

from django.shortcuts import render

from book.models import Author, Novel, Chapter
from book.utils import category_map

# Create your views here.
def home(request):
    novel_list = Novel.objects.all()
    novels_new = Novel.objects.all().order_by('-create_time')
    context = {
        'novel_list': novel_list[:8],
        'novels_new': novels_new[:16],
    }
    return render(request, 'book/home.html', context=context)


def dir(request, novel_id):
    novel_id = int(novel_id)
    novel = Novel.objects.get(pk=novel_id)
    chapters = novel.chapter_set.all().order_by('create_time')
    chapters_num = chapters.count()
    latest_chapter = chapters[chapters_num-1]
    context = {
        'novel': novel,
        'chapters': chapters,
        'latest_chapter': latest_chapter,
        'chapters_num': chapters_num,
    }
    return render(request, 'book/dir.html', context=context)


def read_chapter(request, novel_id, chapter_num):
    novel_id = int(novel_id)
    chapter_num = int(chapter_num)
    novel = Novel.objects.get(pk=novel_id)
    chapters = novel.chapter_set.all()
    chapter = chapters[chapter_num-1]
    nums = Chapter.objects.filter(novel=novel).count()

    pre_chapter = next_chapter = None
    if chapter_num > 1 and chapter_num < nums:
        pre_chapter = chapters[chapter_num-2]
        next_chapter = chapters[chapter_num]
    elif chapter_num == 1:
        next_chapter = chapters[chapter_num]
    elif chapter_num == nums:
        pre_chapter = chapters[chapter_num - 2]

    context = {
        'chapter_num': chapter_num,
        'nums': nums,
        'novel': novel,
        'chapter': chapter,
        'pre_chapter': pre_chapter,
        'next_chapter': next_chapter,
    }
    return render(request, 'book/chapter.html', context=context)


def search(request):
    searchtype = request.GET.get('searchtype', 'novelname')
    keywords = request.GET.get('searchkey')

    if searchtype == 'novelname':
        novels = Novel.objects.filter(name__contains=keywords)
    else:
        novels = Novel.objects.filter(author__name__contains=keywords)

    context = {
        'keywords': keywords,
        'novels': novels,
    }
    return render(request, 'book/search.html', context=context)


def author_novels(request, author_id):
    author_id = int(author_id)
    author = Author.objects.get(pk=author_id)
    novels = author.novel_set.all()
    context = {
        'author': author,
        'novels': novels,
    }
    return render(request, 'book/author_novels.html', context=context)


def sort(request):
    xuanhuan_novels = Novel.objects.filter(category='玄幻')
    qihuan_novels = Novel.objects.filter(category='奇幻')
    wuxia_novels = Novel.objects.filter(category='武侠')
    xianxia_novels = Novel.objects.filter(category='仙侠')
    dushi_novels = Novel.objects.filter(category='都市')
    lishi_novels = Novel.objects.filter(category='历史')
    junshi_novels = Novel.objects.filter(category='军事')
    youxi_novels = Novel.objects.filter(category='游戏')
    jingji_novels = Novel.objects.filter(category='竞技')
    kehuan_novels = Novel.objects.filter(category='科幻')
    lingyi_novels = Novel.objects.filter(category='灵异')
    qita_novels = Novel.objects.filter(category='其他')

    context = {
        'xuanhuan_novels': xuanhuan_novels[:10],
        'qihuan_novels': qihuan_novels[:10],
        'wuxia_novels': wuxia_novels[:10],
        'xianxia_novels': xianxia_novels[:10],
        'dushi_novels': dushi_novels[:10],
        'lishi_novels': lishi_novels[:10],
        'junshi_novels': junshi_novels[:10],
        'youxi_novels': youxi_novels[:10],
        'jingji_novels': jingji_novels[:10],
        'kehuan_novels': kehuan_novels[:10],
        'lingyi_novels': lingyi_novels[:10],
        'qita_novels': qita_novels[:10],
    }
    return render(request, 'book/sort.html', context=context)


def sort_category(request, category):
    if category == 'all':
        category_hanzi = '全部'
        novels = Novel.objects.all()
    else:
        category_hanzi = category_map[category]
        novels = Novel.objects.filter(category=category_hanzi)

    context = {
        'category': category,
        'category_hanzi': category_hanzi,
        'novels': novels[:15],
    }
    return render(request, 'book/sort_category.html', context=context)
