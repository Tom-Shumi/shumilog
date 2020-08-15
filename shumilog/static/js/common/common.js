function inputToday() {
	var now = new Date();
	$('#id_watched_year').val(now.getFullYear());
	$('#id_watched_month').val(now.getMonth() + 1);
	$('#id_watched_day').val(now.getDate());
}

function isDate(str) {
  var arr = str.split('/');
  if (arr.length !== 3) return false;
  const date = new Date(arr[0], arr[1] - 1, arr[2]);
  if (arr[0] !== String(date.getFullYear()) || arr[1] !== ('0' + (date.getMonth() + 1)).slice(-2) || arr[2] !== ('0' + date.getDate()).slice(-2)) {
    return false;
  } else {
    return true;
  }
};