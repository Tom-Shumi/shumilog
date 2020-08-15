$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

function showConfirmWatchLaterModal(id){
    $('#m_id').val(id);
    $('#confirm_msg').text('登録します。よろしいですか？');
    $('#modal_confirm').modal('show');
}

function execute(){
	document.movie_recommend_list_form.method = 'post';
	document.movie_recommend_list_form.action="/movie/recommend_to_watch_later/";
    document.movie_recommend_list_form.submit();
}

function showSearchModal(){
    $('#modal_movie_recommend_search').modal('show');
}

function movie_recommend_search(){
    var from = $('#id_released_date_from').val();
    var to = $('#id_released_date_to').val();
    var errSbt = 0;
    if (from != '' && !isDate(from)) errSbt = 1;
    if (to != '' && !isDate(to)) errSbt = 1;
    if (errSbt == 1) {
        $('#danger_msg').text('公開日はYYYY/MM/DD形式で入力してください。');
        $('#modal_danger_msg').modal('show');
        return false;
    }
	document.movie_recommend_search_form.method = 'get';
	document.movie_recommend_search_form.action="/movie/recommend_search/";
    document.movie_recommend_search_form.submit();
}

function movie_recommend_search_clear(){
    $('#id_movie_title').val('');
    $('#id_released_date_from').val('');
    $('#id_released_date_to').val('');
    $('#id_movie_genre').val('');
}