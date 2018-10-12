import os
import sys
import time
import threading
import logging
import random

import requests
import lxml.etree
from django.core.management.base import BaseCommand

from book.models import Author, Novel, Chapter

crawl_info_logger = logging.getLogger('crawl_info')
crawl_warning_logger = logging.getLogger('crawl_warning')
crawl_error_logger = logging.getLogger('crawl_error')


class Command(BaseCommand):
    help = '从快眼看书获取小说'

    # 酒神 6002
    # 斗破苍穹 4721
    # 斗罗大陆 4843

    NOVEL_PAGE = os.environ.get('NOVEL_PAGE', 5050)
    novel_url = 'https://www.kuaiyankanshu.net/' + str(NOVEL_PAGE)
    dir_url = novel_url + '/dir.html'
    novel_name = ''
    author_name = ''
    novel_category = ''
    novel_cover = ''
    novel_intro = ''
    title_list = []
    content_list = []

    def get_dir(self):
        for i in range(3):
            try:
                response = requests.get(self.dir_url, timeout=10)
                xml = lxml.etree.HTML(response.text)
                href_path = '//ul[contains(@class,"dirlist")]/li/a/@href'
                href_list = xml.xpath(href_path)
                title_path = '//ul[contains(@class,"dirlist")]/li/a/text()'
                self.title_list = xml.xpath(title_path)
                novel_name_path = '//h1/text()'
                self.novel_name = xml.xpath(novel_name_path)[0][:-5]
                author_name_path = '//div[@class="novelinfo-l"]/ul/li[1]/a/text()'
                self.author_name = xml.xpath(author_name_path)[0]

                novel_count = Novel.objects.filter(
                    author__name=self.author_name,
                    name=self.novel_name).count()
                if novel_count > 0:
                    crawl_info_logger.info('小说：%s（%s）%s 已存在，跳过爬取' % (
                    self.novel_name, self.author_name, self.dir_url))
                    sys.exit(1)

                novel_category_path = '//div[@class="novelinfo-l"]/ul/li[2]/a/text()'
                self.novel_category = xml.xpath(novel_category_path)[0]

                response = requests.get(self.novel_url, timeout=10)
                xml = lxml.etree.HTML(response.text)
                cover_path = '//div[@class="novelinfo-r"]/a/img/@src'
                self.novel_cover = xml.xpath(cover_path)[0]
                intro_path = '//div[@class="body novelintro"]/text()'
                self.novel_intro = xml.xpath(intro_path)[0]
                return href_list
            except Exception as e:
                crawl_warning_logger.warning(
                    '爬取小说目录超时：%s 第%s次' % (self.dir_url, i + 1))
                crawl_warning_logger.warning(e)
                time.sleep(1)

        crawl_error_logger.error('爬取小说目录失败：%s，程序退出！' % (self.dir_url))
        sys.exit(1)

    def get_content(self, index, content_url):
        for i in range(3):
            try:
                content_path = '//div[@id="chaptercontent"]/text()'
                response = requests.get(content_url, timeout=10)
                contents = lxml.etree.HTML(response.text).xpath(content_path)
                content = '\r\r'.join(contents)
                self.content_list.append([index, content])
                return
            except Exception as e:
                crawl_warning_logger.warning('爬取小说章节超时：%s %s 第%s次' % (
                self.novel_name, content_url, i + 1))
                crawl_warning_logger.warning(e)
                time.sleep(1)

        # 如果有1个章节，3次都没有抓取成功，程序强制退出，爬取结果不保存
        crawl_error_logger.error(
            '爬取小说章节失败：%s %s，程序退出！' % (self.novel_name, content_url))
        # 单线程中退出主程序用sys.exit，子线程中退出主程序用os._exit
        os._exit(1)

    def write_to_db(self):
        # content_list原本是无序的，多线程爬取完以后按照目录顺序进行排序
        self.content_list.sort(key=lambda e: e[0])
        chapter_num = len(self.content_list)

        # 没有章节对应的作者和小说时，对应创建
        author, _ = Author.objects.get_or_create(name=self.author_name)

        novel = Novel.objects.create(
            name=self.novel_name,
            author=author,
            category=self.novel_category,
            cover=self.novel_cover,
            intro=self.novel_intro,
            chapter_num=chapter_num,
            click_num=random.randint(10000, 200000),
            mark_num=random.randint(20, 999),
            vote_num=random.randint(20, 999),
        )

        for i in range(chapter_num):
            # 批量插入一部小说太大了，容易出错，这里改成逐章插入
            chapter = Chapter.objects.create(
                novel=novel,
                title=self.title_list[i],
                content=self.content_list[i][1],
            )

    def handle(self, *args, **options):
        t1 = time.time()

        href_list = self.get_dir()

        tlist = []
        for i in range(len(href_list)):
            # https://www.kuaiyankanshu.net/6002/read_1.html
            content_url = "https://www.kuaiyankanshu.net" + href_list[i]
            t = threading.Thread(target=self.get_content,
                                 args=(i, content_url))
            t.start()
            tlist.append(t)

        for t in tlist:
            t.join()

        self.write_to_db()

        t2 = time.time()
        crawl_info_logger.info('爬取小说：%s %s结束，程序耗时%s秒' % (
        self.novel_name, self.dir_url, int(t2 - t1)))
