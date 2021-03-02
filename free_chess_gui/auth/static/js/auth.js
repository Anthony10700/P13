var color_night_views = "#DCDCDC"
var color_day_views = "#f8f9fa"
var color_night_views_1 = "#0D1115"
var color_night_views_2 = "#161B25"
var color_night_views_3 = "#344052"
var color_day_views = "#f8f9fa"
var font_color_day_views = "#000000"

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

    if (localStorage.getItem("nigh_views_mode_activate") == "true") {

        if ($('#img-night-mode').attr('src') == DJANGO_STATIC_URL + 'night-mode.svg') {
            $('#img-night-mode').click();
        }
    }
})

$('#img-night-mode').on({
    'click': function() {
        if ($('#img-night-mode').attr('src') == DJANGO_STATIC_URL + 'night-mode.svg') {
            $('#img-night-mode').attr('src', DJANGO_STATIC_URL + 'day-mode.svg');

            $('.bg-night').css({
                "background-color": color_night_views_1,
                "color": color_day_views,
                "scrollbar-color": color_night_views_1
            });
            $('.shadow_perso').css({ "box-shadow": "2px 2px 12px #344052" });
            $('.bg-night_2').css({ "background-color": color_night_views_2 });
            $('#img_acc_dropdown').css({ "background-color": "rgba(255, 255, 255,0.9)" });



            var styles = "<style type='text/css'>.style-1::-webkit-scrollbar{background-color: #0D1115}.style-1::-webkit-scrollbar-track{background-color: #161B25}</style>";

            $(styles).appendTo('head');
            localStorage.setItem("nigh_views_mode_activate", "true");


        } else {
            $('#img-night-mode').attr('src', DJANGO_STATIC_URL + 'night-mode.svg');

            $('.shadow_perso').css({ "box-shadow": "2px 2px 12px #aaa" });
            $('.bg-night').css({
                "background-color": color_day_views,
                "color": font_color_day_views
            });
            $('.bg-night_2').css({ "background-color": color_day_views });
            $('#img_acc_dropdown').css({ "background-color": "rgba(248, 249, 250,1)" });

            var styles = "<style type='text/css'>.style-1::-webkit-scrollbar{background-color: #f8f9fa}.style-1::-webkit-scrollbar-track{background-color: #f8f9fa}</style>";

            $(styles).appendTo('head');
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