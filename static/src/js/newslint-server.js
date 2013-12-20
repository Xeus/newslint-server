/**
 * extra js
 */
$(function() {
    $('.button-lint').on('click', function(e) {
        e.preventDefault();
        window.location.href = '/lint/';
    });
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
});
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-46575602-1', 'newslint.com');
ga('send', 'pageview');
