var color_night_views = "#DCDCDC"
var color_day_views = "#f8f9fa"

$(document).ready(function() {
    $("#div_of_sign_in").hide();

    $("#div_of_account").hide();
    $('.dropdown-toggle').dropdown()


    $("#menu-toggle").trigger('click');
    $("#menu-toggle-right").trigger('click');

    $('#wrapper-right').promise().done(function() {
        $("#div_of_sign_in").animate({ "opacity": "show" }, 1000);
        $("#div_of_account").animate({ "opacity": "show" }, 1000);
    });


})

$('#img-night-mode').on({
    'click': function() {
        if ($('#img-night-mode').attr('src') == DJANGO_STATIC_URL + 'night-mode.svg') {
            $('#img-night-mode').attr('src', DJANGO_STATIC_URL + 'day-mode.svg');
            $('body').css("background-color", color_night_views);
            $('#footer_base').css("background-color", color_night_views);
            $('#wrapper').css("background-color", color_night_views);
            $('.list-group-item').css("background-color", color_night_views);

        } else {
            $('#img-night-mode').attr('src', DJANGO_STATIC_URL + 'night-mode.svg');
            $('body').css("background-color", color_day_views);
            $('#footer_base').css("background-color", color_day_views);
            $('#wrapper').css("background-color", color_day_views);
            $('.list-group-item').css("background-color", color_day_views);
        }
    }
});

$('#img-night-mode').on({
    'mouseover': function() {
        $('#img-night-mode').css("width", "23px");

    }
});
$('#img-night-mode').on({
    'mouseout': function() {
        $('#img-night-mode').css("width", "20px");

    }
});


$("#menu-toggle").click(function(e) {


    if ($("#menu-toggle").text() == "<") {
        $("#menu-toggle").text(">");
        $("#sidebar-wrapper").animate({ "opacity": "hide", right: $("#sidebar-wrapper").width() }, 1000);

        $('#sidebar-wrapper').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
            $(window).trigger('resize');
        });

    } else if ($("#menu-toggle").text() == ">") {

        $("#menu-toggle").text("<");

        $("#sidebar-wrapper").animate({ "opacity": "show", right: 0 }, 1000);

        $('#sidebar-wrapper').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
            $(window).trigger('resize');
        });
    }

});


$("#menu-toggle-right").click(function(e) {
    if ($("#menu-toggle-right").text() == "<") {
        $("#menu-toggle-right").text(">");
        $("#wrapper-right").animate({ "opacity": "show", left: 0 }, 1000);
        $('#wrapper-right').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
            $(window).trigger('resize');
        });


    } else if ($("#menu-toggle-right").text() == ">") {
        $("#menu-toggle-right").text("<");
        $("#wrapper-right").animate({ "opacity": "hide", left: $("#wrapper-right").width() }, 1000);
        $('#wrapper-right').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
            $(window).trigger('resize');
        });
    }

});