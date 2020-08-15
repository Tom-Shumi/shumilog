function movieSelect(id, title, release_date, genre_ids, genre_names, summary){
    $('#id_movie_id_hidden').val(id);
    $('#id_movie_title_hidden').val(title);
    $('#id_released_date_hidden').val(release_date);
    $('#id_genre_ids_hidden').val(genre_ids);
    $('#id_movie_title').val(title);
    $("#movie_genres").text(genre_names);
    $("#movie_summary").text(summary);
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
    $('#movie_genres').text('');
    $('#movie_summary').text('');
	$("#search_btn").prop('disabled', false);
	$("#id_movie_title").prop('disabled', false);
	$("#id_movie_title").focus();
}

function showModal(){
    i = $('#id_movie_id_hidden').val();
    if (i == "") {
        $('#danger_msg').text('映画タイトルを検索して、選択してください。');
        $('#modal_danger_msg').modal('show');
    } else {
        $('#confirm_msg').text('登録します。よろしいですか？');
        $('#modal_confirm').modal('show');
    }
}

function execute(){
    var s = $('#movie_summary').text()
    $('#id_movie_summary_hidden').val(s);
    $('#invisible_btn').click();
}
