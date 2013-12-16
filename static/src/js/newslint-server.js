/**
 * extra js
 */

$('.more-link').on('click', function(e) {
	e.preventDefault();

	if ($('.hidden-fields').css('display') === 'none') {
		$('.hidden-fields').css('display', 'table');
		$('.more-link').html('hide extra fields');
	}
	else {
		$('.hidden-fields').css('display', 'none');
		$('.more-link').html('show more fields');
	}
});
 