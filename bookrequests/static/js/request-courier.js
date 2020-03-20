$(document).ready(function() {
	$('.done-button').unbind('click').click(function(event){
		return confirm('Please confirm that you have picked up / dropped off this book');
	});
});