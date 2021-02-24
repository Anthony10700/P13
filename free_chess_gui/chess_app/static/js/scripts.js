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
var color_night_views = "#DCDCDC"
var color_day_views = "#f8f9fa"


$(document).ready(function() {
    if (MODULE == "lc0" || MODULE == "stockfish" || MODULE == "komodo") {
        compurteur_vs_human = true
    }
    $('.dropdown-toggle').dropdown()
    board = Chessboard('myBoard', config)
    board.start

    $(window).resize(board.resize)



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
        });

    } else if ($("#menu-toggle").text() == ">") {

        $("#menu-toggle").text("<");

        $("#sidebar-wrapper").animate({ "opacity": "show", right: 0 }, 1000);

        $('#sidebar-wrapper').promise().done(function() {
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
        });


    } else if ($("#menu-toggle-right").text() == ">") {

        $("#menu-toggle-right").text("<");


        $("#wrapper-right").animate({ "opacity": "hide", left: $("#wrapper-right").width() }, 1000);
        $('#wrapper-right').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
        });
    }



});