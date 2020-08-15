from accounts.models import ShumilogUser
from django.db import models


class MovieGenreM(models.Model):
    """映画ジャンルマスタ"""

    movie_genre_id = models.IntegerField(verbose_name='映画ジャンルID', primary_key=True)
    movie_genre_name = models.CharField(verbose_name='映画ジャンル', max_length=20)

    class Meta:
        verbose_name_plural = 'MovieGenreM'

    def __str__(self):
        return self.movie_genre_name


class MovieM(models.Model):
    """映画マスタ"""
    movie_id = models.IntegerField(verbose_name='映画ID', primary_key=True)
    movie_title = models.CharField(verbose_name='映画タイトル', max_length=40)
    released_date = models.DateField(verbose_name='公開日')
    movie_summary = models.TextField(verbose_name='あらすじ', blank=True, null=True)
    movie_genres = models.ManyToManyField(MovieGenreM)

    class Meta:
        verbose_name_plural = 'MovieM'

    def __str__(self):
        return self.movie_title


class MovieReviewT(models.Model):
    """映画レビューテーブル"""

    user = models.ForeignKey(ShumilogUser, verbose_name='ユーザ', on_delete=models.PROTECT)
    movie = models.ForeignKey(MovieM, verbose_name='映画', on_delete=models.PROTECT)
    watched_date = models.DateField(verbose_name='視聴日')
    movie_score = models.IntegerField(verbose_name='点数')
    movie_review = models.TextField(verbose_name='レビュー', blank=True, null=True)
    movie_image = models.ImageField(verbose_name='画像', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'MovieReviewT'


class MovieWatchLaterT(models.Model):
    """後で見る映画"""

    user = models.ForeignKey(ShumilogUser, verbose_name='ユーザ', on_delete=models.PROTECT)
    movie = models.ForeignKey(MovieM, verbose_name='映画', on_delete=models.PROTECT)
    created_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'MovieWatchLaterT'

