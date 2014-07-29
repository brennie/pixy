$(document).ready(function() {
	$.validate({
		modules: 'security'
	});

	$('#bio').restrictLength($('#bio-length'));
	$('#bio').focus();
	$('#bio').blur();


	$('#email_row').hide();
	$('#current_row').hide();
	$('#password_row').hide();
	$('#confirmation_row').hide();
	
	$('#change_email').change(function() {
		if (this.checked)
			$('#email_row').show(300);
		else
			$('#email_row').hide(300);
	});

	$('#change_password').change(function() {
		if (this.checked)
		{
			$('#current_row').show(300);;
			$('#password_row').show(300);
			$('#confirmation_row').show(300);
		}
		else
		{
			$('#current_row').hide(300);
			$('#password_row').hide(300);
			$('#confirmation_row').hide(300);
		}
	});
});
