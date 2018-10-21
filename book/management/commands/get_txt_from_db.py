from django.core.management.base import BaseCommand

from book.models import Author, Novel, Chapter

class Command(BaseCommand):
    help = '从数据库获取小说txt'

    def handle(self, *args, **options):
        novel_name = '圣墟'
        author_name = '辰东'

        novel = Novel.objects.get(
            author__name__contains=author_name,
            name__contains=novel_name
        )

        chapters = novel.chapter_set.all()

        file_path = 'logs'
        with open('%s/%s.txt' % (file_path, novel_name), 'w') as f:
            print('start to generate %s.txt' % novel_name)
            for chapter in chapters:
                f.write(chapter.title)
                f.write('\n')
                f.write(chapter.content)
            print('generate %s.txt over' % novel_name)
