$(document).ready(function() {
	$.validate({
		modules: 'file'
	});
	$('#title').restrictLength($('#title-length'));
	$('#description').restrictLength($('#description-length'));
});
