// login.js

$(document).ready(function(){

	$('#search-form').on('submit', function(event){
		event.preventDefault();
		// remove all previous errors
		$('#search-form').find('.error-msg').remove();

		var all_filled = true;

		$('#search-form input').each(function(){
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

			if(msg == 'no_book_found'){
				console.log("Book not found!");
				$('#search input').after('<p class="error-msg" style="color:red">Book not found!</p>');
			}
			else{
				console.log("all info ok, redirecting");
				// redirect to home
				window.location.href = '/searchresult';
			}

			return false;
		});
	});
})