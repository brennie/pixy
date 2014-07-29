$(document).ready(function() {
	$.formUtils.addValidator({
		name : 'strongPassword',
		validatorFunction : function(value, $el, config, language, $form) {
			return value.length >= 8 && value.match(/[^a-zA-Z0-9]/);
		},
		errorMessage : 'The password must be at least 8 characters long and contain a non-alphanumeric character'
	});
});

