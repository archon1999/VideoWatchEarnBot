import random
import datetime
import os

from django.db import models
from django.db.models import Count
from django.utils import timezone

from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


VIDEO_LIMIT_PER_DAY = 2  # Лимит видео на день
TRUE_REFERAL_VIDEOS_COUNT = 2  # Количество просмотренных видео для реферала
PAYMENT_PERMS_REFERALS_COUNT = 1  # Количество рефералов для выплаты
PAYMENT_PERMS_VIEWED_VIDEOS_COUNT = 10  # Количество видео для выплаты
BONUS_VALUE = 10  # Размер бонуса для каждого видео
CAN_GET_BONUS_TIME = 20  # Время, после которого можно получить этот бонус


class BotUser(models.Model):
    class States(models.IntegerChoices):
        NOTHING = 0

    users = models.Manager()
    full_name = models.CharField(max_length=255,
                                 verbose_name='Полное имя')
    username = models.CharField(max_length=255,
                                verbose_name='Юзернейм',
                                null=True,
                                blank=True)
    chat_id = models.CharField(max_length=255,
                               unique=True,
                               verbose_name='ИД чата')
    balance = models.IntegerField(default=0,
                                  verbose_name='Баланс')
    referals = models.ManyToManyField(to='self',
                                      symmetrical=False,
                                      blank=True,
                                      verbose_name='Рефералы')
    bot_state = models.IntegerField(default=States.NOTHING,
                                    choices=States.choices)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_today_viewed_videos(self):
        return self.videos.filter(
            sended__date=datetime.date.today(),
        )

    def check_video_limit_per_day(self):
        return self.get_today_viewed_videos().count() <= VIDEO_LIMIT_PER_DAY

    def get_next_video(self):
        last_video = self.videos.all().order_by('id').last()
        last_video_id = last_video.id if last_video else 0
        next_video = Video.videos.filter(id__gt=last_video_id).first()
        if not next_video:
            next_video = random.choice(Video.videos.all())

        return next_video

    def get_true_referals(self):
        return self.referals.annotate(
            videos_count=Count('videos'),
        ).filter(
            videos_count__gte=TRUE_REFERAL_VIDEOS_COUNT,
        )

    def check_payment_terms(self):
        ok = self.get_true_referals().count() >= PAYMENT_PERMS_REFERALS_COUNT
        ok &= self.videos.count() >= PAYMENT_PERMS_VIEWED_VIDEOS_COUNT
        return ok

    def __str__(self):
        return self.full_name


class Video(models.Model):
    videos = models.Manager()
    video = models.FileField(verbose_name='Видео',
                             upload_to='backend/videos')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создано')

    def get_data(self) -> bytes:
        app_path = os.path.dirname(os.path.dirname(__file__))
        video_path = os.path.join(app_path, self.video.name)
        with open(video_path, 'rb') as video:
            data = video.read()

        return data

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class ViewVideo(models.Model):
    user = models.ForeignKey(
        to=BotUser,
        on_delete=models.CASCADE,
        related_name='videos',
    )
    video = models.ForeignKey(
        to=Video,
        on_delete=models.CASCADE,
        related_name='views',
    )
    received = models.BooleanField(default=False)
    sended = models.DateTimeField(auto_now_add=True,
                                  verbose_name='Отправлено')

    def can_get_bonus(self):
        seconds = (timezone.now() - self.sended).total_seconds()
        return seconds >= CAN_GET_BONUS_TIME

    class Meta:
        verbose_name = 'Просмотр видео'
        verbose_name_plural = 'Просмотры видео'


def filter_tag(tag: Tag, ol_number=None):
    if isinstance(tag, NavigableString):
        text = tag
        text = text.replace('<', '&#60;')
        text = text.replace('>', '&#62;')
        return text

    html = str()
    li_number = 0
    for child_tag in tag:
        if tag.name == 'ol':
            if child_tag.name == 'li':
                li_number += 1
        else:
            li_number = None

        html += filter_tag(child_tag, li_number)

    format_tags = ['strong', 'em', 'pre', 'b', 'u', 'i', 'code']
    if tag.name in format_tags:
        return f'<{tag.name}>{html}</{tag.name}>'

    if tag.name == 'a':
        return f"""<a href="{tag.get("href")}">{tag.text}</a>"""

    if tag.name == 'li':
        if ol_number:
            return f'{ol_number}. {html}'
        return f'•  {html}'

    if tag.name == 'br':
        html += '\n'

    if tag.name == 'span':
        styles = tag.get_attribute_list('style')
        if 'text-decoration: underline;' in styles:
            return f'<u>{html}</u>'

    if tag.name == 'ol' or tag.name == 'ul':
        return '\n'.join(map(lambda row: f'   {row}', html.split('\n')))

    return html


def filter_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return filter_tag(soup)


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Template.Type.MESSAGE)


class KeyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Template.Type.KEY)


class SmileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Template.Type.SMILE)


class Template(models.Model):
    class Type(models.IntegerChoices):
        MESSAGE = 1, 'Сообщение'
        KEY = 2, 'Кнопка'
        SMILE = 3, 'Смайлик'

    templates = models.Manager()
    messages = MessageManager()
    keys = KeyManager()
    smiles = SmileManager()

    type = models.IntegerField(choices=Type.choices,
                               verbose_name='Тип (для разработчика)')
    title = models.CharField(max_length=255,
                             verbose_name='Название (для разработчика)')
    title_verbose_name = models.CharField(max_length=255,
                                          verbose_name='Название')
    body = RichTextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def gettext(self):
        return filter_html(self.body)

    def __str__(self):
        return self.title_verbose_name
