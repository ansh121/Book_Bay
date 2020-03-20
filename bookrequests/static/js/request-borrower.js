$(document).ready(function() {
	$('.return-button').unbind('click').click(function(event){
		return confirm('Are you sure you want to return this book?');
	});
});