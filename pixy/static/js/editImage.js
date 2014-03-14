var transform = 'none';
var preview = null;

window.addEventListener('load', function(e) {
	$.validate({});
	$('#title').restrictLength($('#title-length'));
	$('#description').restrictLength($('#description-length'));

	$('#title').focus();
	$('#title').blur();
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
			requestPreview({transform: 'blur', radius: $('#blur-radius').value, id: imageID });
		}
		else if (transform == 'brightdark')
		{
			$('#brightdark-row').show(300);
			requestPreview({transform: 'brightdark', factor: $('#brightdark-factor').value, id: imageID });
		}
		else if (transform == 'sharpen')
		{
			$('#sharpen-row').show(300);
			requestPreview({transform: 'sharpen', factor: $('#sharpen-factor').value, id: imageID });
		}
		else
		{
			$('#preview-row').show(300);
			requestPreview({transform: transform, id: imageID});
			$('#preview').attr('src', spinnerURL);
		}
	});

	$('#blur-radius').change(function() {
		$('#blur-radius-value').text(this.value);
		requestPreview({transform: 'blur', radius: this.value, id: imageID });
	});

	$('#brightdark-factor').change(function() {
		$('#brightdark-factor-value').text(this.value);
		requestPreview({transform: 'sharpen', factor: this.value, id: imageID });
	});

	$('#sharpen-factor').change(function() {
		$('#sharpen-factor-value').text(this.value);
		requestPreview({transform: 'sharpen', factor: this.value, id: imageID });
	});

});

function updatePreview(response)
{
	console.log(response);
}

function requestPreview(args)
{
	$.getJSON(transformURL, args).done(updatePreview);
}