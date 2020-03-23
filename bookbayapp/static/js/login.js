// login.js

$(document).ready(function(){

	$('#login-form').on('submit', function(event){
		event.preventDefault();
		console.log('Login form submitted.');

		// remove all previous errors
		$('#login-form').find('.error-msg').remove();

		// check -
		// all fields non-empty
		var all_filled = true;

		$('#login-form input').each(function(){
			if(! $(this).val()){

				$(this).parent().addClass('has-error');
				$(this).after('<p class="error-msg">Please fill in this field</p>');
				all_filled = false;
			}
		});

		if (!all_filled)
			return false;
	    var $form = $(this);

	    // post to register_validate view - check if username and email taken
		$.post($(location).attr("href"), $form.serializeArray(),
										function(msg){
			console.log(msg);

			if(msg == "password_mismatch"){
				console.log("password_mismatch");
				$('#password input').after('<p class="error-msg" style="color:red">Incorrect Password!</p>');
			}
			else if(msg == "user_id_not_found"){
				console.log("User Id not found!");
				$('#username input').after('<p class="error-msg" style="color:red">Invalid User Id!</p>');
			}
			else if(msg == "no_error"){
				console.log("all info ok, redirecting");
				// redirect to home
				window.location.href = '/';
			}

			return false;
		});
	});
})