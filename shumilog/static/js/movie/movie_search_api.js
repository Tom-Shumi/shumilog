function movieSearch() {
	var movie_title = $('#id_movie_title').val();
	if (movie_title == "") {
	    $('#danger_msg').text('映画タイトルを入力してください。');
        $('#modal_danger_msg').modal('show');
        return false;
	}
    $.ajax({
        url: '/movie/search_movie_api/',
        method: 'POST',
        dataType: 'text',
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            , 'movie_title': movie_title},
    }).done(function(data) {
        movie_json = JSON.parse(data);
        if (movie_json.length == 0) {
            $('#danger_msg').text('存在しない映画タイトルです。');
            $('#modal_danger_msg').modal('show');
            return false;
        }
        $('#movie_search_table tr').remove();
        $('#movie_search_table').append('<tr class="tr_movie_search_table"><th>映画タイトル</th><th>公開日</th><th class="cell_cmd_btn"></th></tr>');
        for (i = 0; i < movie_json.length ; i++){
            $('#movie_search_table').append('<tr><td class="td_movie_title">' + movie_json[i].title + '</td><td>' + movie_json[i].release_date
                + '</td><td class="cell_cmdBtn"><button class="btn btn-primary cmd_btn" '
                + 'onclick="movieSelect(\''
                                        + movie_json[i].id + '\',\''
                                        + movie_json[i].title + '\',\''
                                        + movie_json[i].release_date +'\',\''
                                        + movie_json[i].genre_ids +'\',\''
                                        + movie_json[i].genre_names +'\',\''
                                        + movie_json[i].summary + '\' ); return false;">選択</button></td></tr>');
        }
        $('#modal_movie_search_api').modal('show');
    }).fail(function() {
        $('#danger_msg').text('映画タイトルの検索に失敗しました。');
        $('#modal_danger_msg').modal('show');
    });
}