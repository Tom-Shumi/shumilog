from django.urls import reverse_lazy
from movie.views import *

from ..models import *
from common.tests.test_common import LoggedInTestCase


class TestMovieReviewView(LoggedInTestCase):

    def test_create_movie_review_success(self):
        params = {
            'movie_id_hidden': '1',
            'movie_title_hidden': 'テスト',
            'released_date_hidden': '2000-01-01',
            'movie_summary_hidden': 'あらすじ',
            'genre_ids_hidden': '99',
            'watched_year': '2020',
            'watched_month': '01',
            'watched_day': '01',
            'movie_review_score': '5',
            'movie_review': 'レビュー',
            'movie_image': '',
        }

        response = self.client.post(reverse_lazy('movie:review_create'), params)
        self.assertRedirects(response, reverse_lazy('movie:review_list'))
        self.assertEqual(MovieReviewT.objects.filter(movie_review='レビュー').count(), 1)

    def test_movie_review_update_success(self):
        movie = MovieM.objects.create(movie_id='1', movie_title='テスト', released_date='2000-01-01', movie_summary='あらすじ')
        movie_genre_m = MovieGenreM.objects.get(movie_genre_id='12')
        movie.movie_genres.add(movie_genre_m)
        movie_review = MovieReviewT.objects.create(id=1, user=self.test_user, movie=movie, watched_date='2020-01-01',
                                                   movie_score='5',
                                                   movie_review='レビュー')
        params = {
            'id': '1',
            'watched_year': '2020',
            'watched_month': '01',
            'watched_day': '01',
            'movie_review_score': '5',
            'movie_review': 'レビュー編集',
            'movie_image': '',
        }

        response = self.client.post(reverse_lazy('movie:review_update', kwargs={'id': 1}), params)
        self.assertRedirects(response, reverse_lazy('movie:review_detail', kwargs={'id': 1}))
        self.assertEqual(MovieReviewT.objects.filter(movie_review='レビュー編集').count(), 1)

    def test_movie_review_delete_success(self):
        movie = MovieM.objects.create(movie_id='1', movie_title='テスト', released_date='2000-01-01', movie_summary='あらすじ')
        movie_genre_m = MovieGenreM.objects.get(movie_genre_id='12')
        movie.movie_genres.add(movie_genre_m)
        movie_review = MovieReviewT.objects.create(id=1, user=self.test_user, movie=movie, watched_date='2020-01-01',
                                                   movie_score='5',
                                                   movie_review='レビュー')
        params = {
            'r_id': '1',
        }

        self.assertEqual(MovieReviewT.objects.filter(movie_review='レビュー').count(), 1)

        response = self.client.post(reverse_lazy('movie:review_delete'), params)
        self.assertRedirects(response, reverse_lazy('movie:review_list'))
        self.assertEqual(MovieReviewT.objects.filter(movie_review='レビュー').count(), 0)
