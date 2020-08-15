$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

function movieDetail(id) {
	$('#r_id').val(id);
	document.movie_review_list_form.method = 'post';
	document.movie_review_list_form.action="/movie/review_detail/";
    document.movie_review_list_form.submit();
}

function execute(){
	document.movie_review_list_form.method = 'post';
	document.movie_review_list_form.action="/movie/review_delete/";
    document.movie_review_list_form.submit();
}

function showConfirmDeleteModal(id){
    $('#r_id').val(id);
    $('#confirm_msg').text('削除します。よろしいですか？');
    $('#modal_confirm').modal('show');
}

function showSearchModal(){
    $('#modal_movie_list_search').modal('show');
}

function movie_review_search(){
    var from = $('#id_watched_date_from').val();
    var to = $('#id_watched_date_to').val();
    var errSbt = 0;
    if (from != '' && !isDate(from)) errSbt = 1;
    if (to != '' && !isDate(to)) errSbt = 1;
    if (errSbt == 1) {
        $('#danger_msg').text('視聴日はYYYY/MM/DD形式で入力してください。');
        $('#modal_danger_msg').modal('show');
        return false;
    }
	document.movie_review_search_form.method = 'get';
	document.movie_review_search_form.action="/movie/review_search/";
    document.movie_review_search_form.submit();
}

function movie_review_search_clear(){
    $('#id_watched_date_from').val('');
    $('#id_watched_date_to').val('');
    $('#id_movie_title').val('');
    $('#id_movie_score_from').val('');
    $('#id_movie_score_to').val('');
}