import logging
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from tmdbv3api import TMDb
from tmdbv3api import Movie
import json
from datetime import datetime
from django.db.models import Q, Avg

logger = logging.getLogger(__name__)


class MovieReviewListView(LoginRequiredMixin, generic.ListView):
    model = MovieReviewT
    template_name = 'movie_review_list.html'
    context_object_name = 'movie_review_list'
    paginate_by = 3

    def get_queryset(self):
        movie_reviews = MovieReviewT.objects.filter(
            make_condition_user(self)
            & make_condition_watched_date_from(self)
            & make_condition_watched_date_to(self)
            & make_condition_movie_title_review(self)
            & make_condition_movie_score_from(self)
            & make_condition_movie_score_to(self)).order_by('-watched_date', 'movie')
        return movie_reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MovieReviewSearchForm(initial={'watched_date_from': self.request.GET.get("watched_date_from"),
                                                         'watched_date_to': self.request.GET.get("watched_date_to"),
                                                         'movie_title': self.request.GET.get("movie_title"),
                                                         'movie_score_from': self.request.GET.get("movie_score_from"),
                                                         'movie_score_to': self.request.GET.get("movie_score_to")})
        return context


class MovieReviewDetailView(LoginRequiredMixin, generic.DetailView):
    model = MovieReviewT
    template_name = 'movie_review_detail.html'
    pk_url_kwarg = 'id'


class MovieReviewCreateView(LoginRequiredMixin, generic.FormView):
    model = MovieReviewT
    template_name = 'movie_review_create.html'
    form_class = MovieReviewCreateForm
    success_url = reverse_lazy('movie:review_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wl_id = self.request.GET.get("wl_id")
        # 後で見る映画一覧から遷移時のみmovie_idに値が入る。
        if wl_id is not None:
            movie_watch_later = MovieWatchLaterT.objects.get(id=wl_id)
            context["wl_id"] = wl_id
            context["movie_id_wl"] = movie_watch_later.movie.movie_id
            context["movie_title_wl"] = movie_watch_later.movie.movie_title
            context["cancel_url"] = reverse_lazy('movie:watch_later_list')
            context["wl_flg"] = 1
        else:
            context["cancel_url"] = reverse_lazy('movie:review_list')
            context["wl_flg"] = 0
        return context

    def form_valid(self, form):
        save_movie_review(self, form)
        # 後で見る映画一覧から遷移時は、元の後で見る映画を削除する。
        if self.request.POST.get("wl_flg") == "1":
            MovieWatchLaterT.objects.filter(id=self.request.POST.get("wl_id")).delete()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class MovieReviewUpdateView(LoginRequiredMixin, generic.FormView):
    model = MovieReviewT
    template_name = 'movie_review_update.html'
    form_class = MovieReviewCreateForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('movie:review_detail', kwargs={'id': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        movie_review = MovieReviewT.objects.get(id=self.kwargs['id'])
        context = super().get_context_data(**kwargs)
        context['form'] = MovieReviewCreateForm(initial={'movie_review': movie_review.movie_review,
                                                         'watched_year': movie_review.watched_date.year,
                                                         'watched_month': movie_review.watched_date.month,
                                                         'watched_day': movie_review.watched_date.day,
                                                         'movie_image': movie_review.movie_image})
        context['id'] = movie_review.id
        context['movie'] = movie_review.movie
        context['movie_score'] = movie_review.movie_score
        return context

    def form_valid(self, form):
        update_movie_review(self, form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


def review_delete(request):
    review_id = request.POST.get("r_id")
    MovieReviewT.objects.filter(id=review_id).delete()

    return redirect(reverse_lazy('movie:review_list'))


def search_movie_api(request):
    movie_title = request.POST.get("movie_title")

    tmdb = TMDb()
    tmdb.api_key = 'd624f6311529ea50a6238e7d7296610a'
    tmdb.language = 'ja-JA'

    movie = Movie()
    search = movie.search(movie_title)

    movie_genres = MovieGenreM.objects

    movie_list = []
    for res in search:
        genre_names = None
        for genre_id in res.genre_ids:
            movie_genre = movie_genres.get(movie_genre_id=genre_id)
            if genre_names:
                genre_names = genre_names + ',' + movie_genre.movie_genre_name
            else:
                genre_names = movie_genre.movie_genre_name

        d = {'id': res.id, 'title': res.title, 'release_date': res.release_date, 'genre_ids': res.genre_ids,
             'genre_names': genre_names, 'summary': res.overview.replace('"', '').replace("'", "")}
        movie_list.append(d)

    movie_list.sort(key=lambda x: x['release_date'])
    movie_list_json = json.dumps(movie_list)

    return HttpResponse(movie_list_json)


def save_movie_review(self, form):
    movie_review = MovieReviewT()
    movie_review.user = self.request.user
    movie_review.movie = create_movie_m(form)
    movie_review.watched_date = \
        datetime(form.cleaned_data['watched_year'],
                 form.cleaned_data['watched_month'],
                 form.cleaned_data['watched_day'], 00, 00)
    movie_review.movie_score = form.cleaned_data['movie_review_score']
    movie_review.movie_review = form.cleaned_data['movie_review']
    movie_review.movie_image = form.cleaned_data['movie_image']
    movie_review.save()


def create_movie_m(form):
    movie = MovieM()
    form_movie_id = form.cleaned_data['movie_id_hidden']
    movie.movie_id = form_movie_id
    movie.movie_title = form.cleaned_data['movie_title_hidden']
    movie.released_date = form.cleaned_data['released_date_hidden']
    movie.movie_summary = form.cleaned_data['movie_summary_hidden']

    count = MovieM.objects.filter(movie_id=form_movie_id).count()
    if count == 0:
        movie.save()
        set_movie_genre(form, movie)
    return movie


def set_movie_genre(form, movie):
    genre_ids = form.cleaned_data['genre_ids_hidden'].split(',')
    for genre_id in genre_ids:
        movie_genre_m = MovieGenreM.objects.get(movie_genre_id=genre_id)
        movie.movie_genres.add(movie_genre_m)


def update_movie_review(self, form):
    movie_review = MovieReviewT.objects.get(id=self.kwargs['id'])
    movie_review.watched_date = \
        datetime(form.cleaned_data['watched_year'],
                 form.cleaned_data['watched_month'],
                 form.cleaned_data['watched_day'], 00, 00)
    movie_review.movie_score = form.cleaned_data['movie_review_score']
    movie_review.movie_review = form.cleaned_data['movie_review']
    if form.cleaned_data['movie_image']:
        movie_review.movie_image = form.cleaned_data['movie_image']
    else:
        movie_review.movie_image = ''

    movie_review.save()


def make_condition_user(self):
    condition = Q(user=self.request.user)
    return condition


def make_condition_watched_date_from(self):
    watched_date_from_str = self.request.GET.get("watched_date_from")
    if watched_date_from_str is None or watched_date_from_str == '':
        watched_date_from = None
    else:
        watched_date_from = datetime.strptime(watched_date_from_str, '%Y/%m/%d')
    condition = Q()
    if watched_date_from:
        condition = Q(watched_date__gte=watched_date_from)
    return condition


def make_condition_watched_date_to(self):
    watched_date_to_str = self.request.GET.get("watched_date_to")
    if watched_date_to_str is None or watched_date_to_str == '':
        watched_date_to = None
    else:
        watched_date_to = datetime.strptime(watched_date_to_str, '%Y/%m/%d')
    condition = Q()
    if watched_date_to:
        condition = Q(watched_date__lte=watched_date_to)
    return condition


def make_condition_movie_title_review(self):
    movie_title = self.request.GET.get("movie_title")
    condition = Q()
    if movie_title:
        condition = Q(movie__movie_title__contains=movie_title)
    return condition


def make_condition_movie_score_from(self):
    movie_score_from = self.request.GET.get("movie_score_from")
    condition = Q()
    if movie_score_from:
        condition = Q(movie_score__gte=movie_score_from)
    return condition


def make_condition_movie_score_to(self):
    movie_score_to = self.request.GET.get("movie_score_to")
    condition = Q()
    if movie_score_to:
        condition = Q(movie_score__lte=movie_score_to)
    return condition


class MovieWatchLaterListView(LoginRequiredMixin, generic.ListView):
    model = MovieWatchLaterT
    template_name = 'movie_watch_later_list.html'
    context_object_name = 'movie_watch_later_list'
    paginate_by = 3

    def get_queryset(self):
        movie_watch_laters = MovieWatchLaterT.objects.filter(user=self.request.user).order_by('-created_date', 'movie')
        return movie_watch_laters


class MovieWatchLaterCreateView(LoginRequiredMixin, generic.FormView):
    model = MovieWatchLaterT
    template_name = 'movie_watch_later_create.html'
    form_class = MovieWatchLaterForm
    success_url = reverse_lazy('movie:watch_later_list')

    def form_valid(self, form):
        save_movie_watch_later(self, form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


def save_movie_watch_later(self, form):
    movie_watch_later = MovieWatchLaterT()
    movie_watch_later.user = self.request.user
    movie_watch_later.movie = create_movie_m(form)
    movie_watch_later.save()


def watch_later_delete(request):
    watch_later_id = request.POST.get("wl_id")
    MovieWatchLaterT.objects.filter(id=watch_later_id).delete()

    return redirect(reverse_lazy('movie:watch_later_list'))


class MovieRecommendListView(LoginRequiredMixin, generic.ListView):
    model = MovieM
    template_name = 'movie_recommend_list.html'
    context_object_name = 'movie_recommend_list'
    paginate_by = 3

    def get_queryset(self):
        movies = MovieM.objects.annotate(movie_score_avg=Avg('moviereviewt__movie_score')) \
            .filter(movie_score_avg__gte=4) \
            .exclude(moviereviewt__user=self.request.user) \
            .exclude(moviewatchlatert__user=self.request.user) \
            .filter(make_condition_movie_title_recommend(self)
                    & make_condition_released_date_from(self)
                    & make_condition_released_date_to(self)
                    & make_condition_movie_genre(self)).order_by('-movie_score_avg')
        return movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MovieRecommendSearchForm(
            initial={'released_date_from': self.request.GET.get("released_date_from"),
                     'released_date_to': self.request.GET.get("released_date_to"),
                     'movie_title': self.request.GET.get("movie_title"),
                     'movie_genre': self.request.GET.get("movie_genre")})
        return context


def recommend_to_watch_later(request):
    movie_id = request.POST.get("m_id")
    movie_watch_later = MovieWatchLaterT()
    movie_watch_later.user = request.user
    movie_watch_later.movie = MovieM(movie_id=movie_id)
    movie_watch_later.save()
    return redirect(reverse_lazy('movie:recommend_list'))


def make_condition_movie_title_recommend(self):
    movie_title = self.request.GET.get("movie_title")
    condition = Q()
    if movie_title:
        condition = Q(movie_title__contains=movie_title)
    return condition


def make_condition_released_date_from(self):
    released_date_from_str = self.request.GET.get("released_date_from")
    if released_date_from_str is None or released_date_from_str == '':
        released_date_from = None
    else:
        released_date_from = datetime.strptime(released_date_from_str, '%Y/%m/%d')
    condition = Q()
    if released_date_from:
        condition = Q(released_date__gte=released_date_from)
    return condition


def make_condition_released_date_to(self):
    released_date_to_str = self.request.GET.get("released_date_to")
    if released_date_to_str is None or released_date_to_str == '':
        released_date_to = None
    else:
        released_date_to = datetime.strptime(released_date_to_str, '%Y/%m/%d')
    condition = Q()
    if released_date_to:
        condition = Q(released_date__lte=released_date_to)
    return condition


def make_condition_movie_genre(self):
    movie_genre = self.request.GET.get("movie_genre")
    condition = Q()
    if movie_genre:
        condition = Q(movie_genres__movie_genre_id=movie_genre)
    return condition
