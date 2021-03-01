var board = null
var game = new Chess()
var white_Square_Grey = '#a9a9a9'
var black_Square_Grey = '#696969'
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')
var compurteur_vs_computer = false
var compurteur_vs_human = false
var human_take_white = true
var color_night_views_1 = "#0D1117"
var color_night_views_2 = "#161B22"
var color_night_views_3 = "#344052"
var color_day_views = "#f8f9fa"
var font_color_day_views = "#000000"






$('#img-night-mode').on({
    'click': function() {
        if ($('#img-night-mode').attr('src') == DJANGO_STATIC_URL + 'night-mode.svg') {
            $('#img-night-mode').attr('src', DJANGO_STATIC_URL + 'day-mode.png');

            $('.bg-night').css({
                "background-color": color_night_views_1,
                "color": color_day_views,
                "scrollbar-color": color_night_views_1
            });
            $('.shadow_perso').css({ "box-shadow": "2px 2px 12px #344052" });
            $('.bg-night_2').css({ "background-color": color_night_views_2 });
            $('#img_acc_dropdown').css({ "background-color": "rgba(255, 255, 255,0.9)" });
            $('.style-1::-webkit-scrollbar-track').css({ "background-color": color_night_views_1 });



            var styles = "<style type='text/css'>.style-1::-webkit-scrollbar{background-color: #0D1117}.style-1::-webkit-scrollbar-track{background-color: #161B22}</style>";

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

            localStorage.setItem("nigh_views_mode_activate", "false");
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


$(document).ready(function() {
    if (MODULE == "lc0" || MODULE == "stockfish" || MODULE == "komodo") {
        compurteur_vs_human = true
    }
    $('.dropdown-toggle').dropdown()
    board = Chessboard('myBoard', config)
    board.start

    if ($(window).width() <= 1450 && $("#menu-toggle-right").text() == ">") {
        $("#menu-toggle-right").trigger('click');
    }
    if ($(window).width() > 1450 && $("#menu-toggle-right").text() == "<") {
        $("#menu-toggle-right").trigger('click');
    }
    $(window).resize(board.resize)

    if (localStorage.getItem("nigh_views_mode_activate") == "true") {

        if ($('#img-night-mode').attr('src') == DJANGO_STATIC_URL + 'night-mode.svg') {
            $('#img-night-mode').click();
        }
    }
})



function removeGreySquares() {
    $('#myBoard .square-55d63').css('background', '')
}

function greySquare(square) {
    var $square = $('#myBoard .square-' + square)

    var background = white_Square_Grey
    if ($square.hasClass('black-3c85d')) {
        background = black_Square_Grey
    }

    $square.css('background', background)
}

function onDragStart(source, piece) {
    if (game.game_over()) return false
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false
    }
}

function onDrop(source, target) {
    removeGreySquares()

    var move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    })

    if (move === null) return 'snapback'
    if (compurteur_vs_human == true && human_take_white == true && game.turn() == 'b') {
        send_fen(game.fen())
    }
    if (compurteur_vs_computer == true) {
        send_fen(game.fen())
    }
}

function onMouseoverSquare(square, piece) {
    var moves = game.moves({
        square: square,
        verbose: true
    })

    if (moves.length === 0) return
    greySquare(square)

    for (var i = 0; i < moves.length; i++) {
        greySquare(moves[i].to)
    }
}

function onMouseoutSquare(square, piece) {
    removeGreySquares()
}

function onSnapEnd() {
    board.position(game.fen())
}

function updateStatus() {
    var status = ''

    var moveColor = 'White'
    if (game.turn() === 'b') {
        moveColor = 'Black'
    }

    if (game.in_checkmate()) {
        status = 'Game over, ' + moveColor + ' is in checkmate.'
    } else if (game.in_draw()) {
        status = 'Game over, drawn position'
    } else {
        status = moveColor + ' to move'
        if (game.in_check()) {
            status += ', ' + moveColor + ' is in check'
        }
        if (compurteur_vs_computer) {
            send_fen(game.fen())
        }

    }

    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())
}

var config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd,
    pieceTheme: DJANGO_STATIC_URL + '{piece}.png',
    onChange: onChange
}



function onChange(oldPos, newPos) {

    updateStatus()
}





function send_fen(fen) {
    $.ajax({
        url: "get_fen",
        dataType: "json",
        data: { "fen": fen, "module": MODULE },

        success: function(response) {
            // console.log(response.new_fen)
            // console.log(game.moves())
            game.move(response.new_fen, { sloppy: true })
            board.position(game.fen())
        },
        error: function(error) {
            console.log(console.log(error))
        }
    });
}



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