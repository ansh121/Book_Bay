// register.js

$(document).ready(function(){
	// both passwords must be the same, visually
	$('#password input, #confirm_password input').keyup(function(){
		if($('#password').find('input').val() != $('#confirm_password').find('input').val()){
			$('#password, #confirm_password').removeClass('has-success');
			$('#password, #confirm_password').addClass('has-error');
		}
		else{
			$('#password, #confirm_password').removeClass('has-error');
			$('#password, #confirm_password').addClass('has-success');
		}
	});



	$('#register-form').on('submit', function(event){
		event.preventDefault();
		console.log('Register form submitted.');

		// remove all previous errors
		$('#register-form').find('.error-msg').remove();

		// check -
		// all fields non-empty
		var all_filled = true;

		$('#register-form input').each(function(){
			if(! $(this).val()){

				$(this).parent().addClass('has-error');
				$(this).after('<p class="error-msg">Please fill in this field</p>');
				all_filled = false;
			}
		});

		var pw_match = true;

		// password check
		if($('#password').find('input').val() != $('#confirm_password').find('input').val()){

			$('#confirm_password input').after('<p class="error-msg" style="color:red">Passwords do not match.</p>');
			pw_match = false;

		}

		if (!all_filled || !pw_match)
			return false;
	    var $form = $(this);

	    // post to register_validate view - check if username and email taken
		$.post($(location).attr("href"), $form.serializeArray(), 
										function(msg){
			console.log(msg);

			if(msg == "name_taken"){
				console.log("name is taken");
				$('#username input').after('<p class="error-msg">This username is taken</p>');
			}
			else if(msg == "email_taken"){
				console.log("email is taken");
				$('#email input').after('<p class="error-msg">This email is already registered</p>');
			}
			else if(msg == "no_error"){
				console.log("all info ok, redirecting");
				// redirect to home
				window.location.href = '/login.html';
			}

			return false;
		});
	});
})