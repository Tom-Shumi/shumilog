$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

function showConfirmDeleteModal(id){
    $('#wl_id').val(id);
    $('#confirm_msg').text('削除します。よろしいですか？');
    $('#modal_confirm').modal('show');
}

function execute(){
	document.movie_watch_later_list_form.method = 'post';
	document.movie_watch_later_list_form.action="/movie/watch_later_delete/";
    document.movie_watch_later_list_form.submit();
}

function displayMovieCreateView(id){
    $('#wl_id').val(id);
	document.movie_watch_later_list_form.method = 'get';
	document.movie_watch_later_list_form.action="/movie/review_create/";
    document.movie_watch_later_list_form.submit();
}