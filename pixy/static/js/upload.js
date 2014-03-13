window.addEventListener('load', function(e) {
	$.validate({
		modules: 'file'
	});
	$('#title').restrictLength($('#title-length'));
	$('#description').restrictLength($('#description-length'));
});