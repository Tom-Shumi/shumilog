function movieSelect(id, title, release_date, genre_ids, genre_names, summary){
    $('#id_movie_id_hidden').val(id);
    $('#id_movie_title_hidden').val(title);
    $('#id_released_date_hidden').val(release_date);
    $('#id_genre_ids_hidden').val(genre_ids);
    $('#id_movie_summary_hidden').val(summary);
    $('#id_movie_title').val(title);
    $("#search_btn").prop('disabled', true);
    $("#id_movie_title").prop('disabled', true);
    $('#modal_movie_search_api').modal('hide');
}

function movieClear() {
    $('#id_movie_title').val('');
    $('#id_movie_id_hidden').val('');
    $('#id_movie_title_hidden').val('');
    $('#id_released_date_hidden').val('');
    $('#id_genre_ids_hidden').val('');
	$("#search_btn").prop('disabled', false);
	$("#id_movie_title").prop('disabled', false);
	$("#id_movie_title").focus();
}

function execute(){
    $('#invisible_btn').click();
}

function showModal(){
    i = $('#id_movie_id_hidden').val();
    if (i == "") {
        $('#danger_msg').text('映画タイトルを検索して、視聴した映画を選択してください。');
        $('#modal_danger_msg').modal('show');
    } else {
        $('#confirm_msg').text('登録します。よろしいですか？');
        $('#modal_confirm').modal('show');
    }
}
