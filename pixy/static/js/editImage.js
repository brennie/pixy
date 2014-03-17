var transform = 'none';
var preview = null;

window.addEventListener('load', function(e) {
	$.validate({});
	$('#title').restrictLength($('#title-length'));
	$('#description').restrictLength($('#description-length'));

	$('#title').focus();
	$('#description').focus();
	$('#description').blur();

	$('#blur-row').hide();
	$('#brightdark-row').hide();
	$('#sharpen-row').hide();
	$('#preview-row').hide();

	$('input[name=transform]').change(function() {
		if (transform == 'blur')
			$('#blur-row').hide(300)
		
		else if (transform == 'brightdark')
			$('#brightdark-row').hide(300);
		
		else if (transform == 'sharpen')
			$('#sharpen-row').hide(300);

		else if (transform == 'none')
		{
			$('#preview-row').show(300);
			$('#preview').attr('src', spinnerURL);
		}

		transform = this.value;

		if (transform == 'none')
			$('#preview-row').hide(300);

		else if (transform == 'blur')
		{
			$('#blur-row').show(300);
			requestPreview({transform: 'blur', radius: $('#blur-radius').prop('value'), id: imageID });
		}
		else if (transform == 'brightdark')
		{
			$('#brightdark-row').show(300);
			requestPreview({transform: 'brightdark', factor: $('#brightdark-factor').prop('value'), id: imageID });
		}
		else if (transform == 'sharpen')
		{
			$('#sharpen-row').show(300);
			requestPreview({transform: 'sharpen', factor: $('#sharpen-factor').prop('value'), id: imageID });
		}
		else
		{
			$('#preview-row').show(300);
			requestPreview({transform: transform, id: imageID});
			$('#preview').attr('src', spinnerURL);
		}
	});

	$('#blur-radius').change(function() {
		$('#blur-radius-value').text($('#blur-radius').prop('value'));
		requestPreview({transform: 'blur', radius: $('#blur-radius').prop('value'), id: imageID });
	});

	$('#brightdark-factor').change(function() {
		console.log(this);
		$('#brightdark-factor-value').text($('#brightdark-factor').prop('value'));
		requestPreview({transform: 'brightdark', factor: $('#brightdark-factor').prop('value'), id: imageID });
	});

	$('#sharpen-factor').change(function() {
		$('#sharpen-factor-value').text($('#sharpen-factor').prop('value'));
		requestPreview({transform: 'sharpen', factor: $('#sharpen-factor').prop('value'), id: imageID });
	});

});

function updatePreview(response) {
	if ('error' in response)
		addAlert(response['error'], 'danger');
	else
		$('#preview').attr('src', response['url']);
}

function requestPreview(args) {
	$.getJSON(transformURL, args).done(updatePreview);
}

function addAlert(message, category)
{
	$('#main-container').prepend(
		$('<div class="alert alert-' + category + ' alert-dimissable center-block">' +
			'<button class="close" aria-hidden="true" data-dismiss="alert" type="button">&times;</button>' +
				'<p>' + message + '</p>' +
			'</div>'));
}