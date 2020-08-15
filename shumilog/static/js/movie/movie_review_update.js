$(function() {
  $('#movie_image-clear_id').change(function() {
    if($(this).prop("checked")){
        $("#id_movie_image").prop("disabled", true);
    } else {
        $("#id_movie_image").prop("disabled", false);
    }
  });
});

function execute(){
    $('#invisible_btn').click();
}

function showModal(){
    $('#confirm_msg').text('登録します。よろしいですか？');
    $('#modal_confirm').modal('show');
}