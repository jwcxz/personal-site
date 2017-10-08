// https://paulund.co.uk/smooth-scroll-to-internal-links-with-jquery
// http://www.sycha.com/jquery-smooth-scrolling-internal-anchor-links
$(document).ready(function(){
    $('a[href^="#"]').on('click',function (e) {
        e.preventDefault();

        var scrollTop = 0;
        if ( this.hash != '' ) {
            scrollTop = $(this.hash).offset().top
        } else {
            scrollTop = 0;
        }

        $('html, body').stop().animate({
            'scrollTop': scrollTop
        }, 500, 'swing', function () {
            window.location.hash = target;
        });
    });
});
