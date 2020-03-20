$(document).ready(function() {
	// confirm deletion of book 
	$('.delete-button').unbind('click').click(function(event){
		return confirm('Are you sure you want to remove this book?');
	});
});