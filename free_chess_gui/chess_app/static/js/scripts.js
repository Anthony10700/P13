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
var color_night_views_1 = "#0D1115"
var color_night_views_2 = "#161B25"
var color_night_views_3 = "#344052"
var color_day_views = "#f2f2f2"
var font_color_day_views = "#000000"
var user_color = "white"
var last_move = ""
var game_id_current = 0
var chess_game_history_saved = []
var pgn_of_chess_game_complete = ""
var last_move_chess_game_history_saved = ""
NB_OF_ENGINE = 3

if (localStorage.getItem("nigh_views_mode_activate") == null || localStorage.getItem("nigh_views_mode_activate") == "true") {

    if ($('#img-night-mode').attr('src') == DJANGO_STATIC_URL + 'night-mode.svg') {
        $('#img-night-mode').attr('src', DJANGO_STATIC_URL + 'day-mode.png');

        $('.bg-night').css({
            "background-color": color_night_views_1,
            "color": color_day_views,
            "scrollbar-color": color_night_views_1
        });
        $('.shadow_perso').css({ "box-shadow": "2px 2px 12px #344052" });
        $('.bg-night_2').css({
            "background-color": color_night_views_2,
            "color": color_day_views
        });
        $('#img_acc_dropdown').css({ "background-color": "rgba(255, 255, 255,0.9)" });



        var styles = "<style type='text/css'>.style-1::-webkit-scrollbar{background-color: #0D1115}.style-1::-webkit-scrollbar-track{background-color: #161B25}</style>";

        $(styles).appendTo('head');


        localStorage.setItem("nigh_views_mode_activate", "true");

    }

}

if (GAME_VIEWER == true) {
    if (data_for_chart_lc0 != "None") {
        var len = data_for_chart_lc0.length;
        var label = [...Array(len).keys()];

    } else {
        var label = [];
        var data_for_chart_lc0 = [];
        var data_for_chart_komodo = [];
        var data_for_chart_stockfish = [];
    }

    var config = {}

    window.chartColors = {
        red: 'rgba(255, 99, 132, 0.5)',
        orange: 'rgba(255, 159, 64, 0.5)',
        yellow: 'rgba(255, 205, 86, 1)',
        green: 'rgba(75, 192, 192, 0.5)',
        blue: 'rgba(54, 162, 235, 0.8)',
        purple: 'rgba(153, 102, 255, 0.5)',
        grey: 'rgba(201, 203, 207, 0.5)'
    };


    var ctx = $('#myChart')[0].getContext('2d');

    var chart = chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: label,
            datasets: [{
                    label: 'lc0 analyse',
                    backgroundColor: window.chartColors.red,
                    borderColor: window.chartColors.red,
                    data: data_for_chart_lc0,
                    fill: true
                },
                {
                    label: 'stockfish analyse',
                    backgroundColor: window.chartColors.blue,
                    borderColor: window.chartColors.blue,
                    data: data_for_chart_komodo,
                    fill: true
                },
                {
                    label: 'komodo12 analyse',
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
                    data: data_for_chart_stockfish,
                    fill: true
                }
            ]
        },

        // Configuration options go here
        options: {
            responsive: true,
            scales: {
                yAxes: [{

                    gridLines: {
                        display: true,
                        zeroLineColor: '#2a73e0',
                        color: 'rgba(255, 255, 255, 0.3)',
                        lineWidth: 1
                    }
                }],
                xAxes: [{

                    gridLines: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.1)',
                        lineWidth: 1
                    }
                }]
            }
        }
    });

    ctx.style = window.chartColors.yellow

}





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
            $('.bg-night_2').css({
                "background-color": color_night_views_2,
                "color": color_day_views
            });
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
            $('.bg-night_2').css({
                "background-color": "#fff",
                "color": font_color_day_views
            });
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

    $('.dropdown-toggle').dropdown()

    if ($(window).width() <= 1450 && $("#menu-toggle-right").text() == ">") {
        $("#menu-toggle-right").trigger('click');
    }
    if ($(window).width() > 1450 && $("#menu-toggle-right").text() == "<") {
        $("#menu-toggle-right").trigger('click');
    }


    if (MODULE != "") {
        if (MODULE == "lc0" || MODULE == "stockfish" || MODULE == "komodo") {
            compurteur_vs_human = true
        }

        config = {
            orientation: user_color,
            draggable: false,
            position: 'start',
            pieceTheme: DJANGO_STATIC_URL + '{piece}.png',

        }
        board = Chessboard('myBoard', config)
        board.start()
        $(window).resize(function() {
            board.resize()
        })
        if (user_color == "white") {

            $("#white_info").append("<p> You are white</p>");
            $("#black_info").append("<p> The computer is black</p>");
        } else {

            $("#white_info").append("<p> You are black</p>");
            $("#black_info").append("<p> The computer is white</p>");
        }

    } else if (TITTLE == "History of your games") {
        $("#menu-toggle-right").trigger('click');

        var list_of_board = []

        $.each($(".board_smaller"), function(index, value) {
            config = {
                orientation: user_color,
                draggable: false,
                position: $("#" + value.id + "").attr("fen"),
                pieceTheme: DJANGO_STATIC_URL + '{piece}.png',

            }
            list_of_board.push(Chessboard(value.id, config))

        });

        $(window).resize(
            function() {
                $.each(list_of_board, function(index, value) {
                    value.resize()

                });
            })

    } else if (GAME_VIEWER == true) {


        $("#div_col_middle").removeClass("col-10").addClass("col-6");
        $("#div_col_right").removeClass("col-1").addClass("col-5");
        $("#menu-toggle-right").trigger('click');

        game.load_pgn($("#pgn").html())
        pgn_of_chess_game_complete = $("#pgn").html()
        chess_game_history_saved = game.history();

        config = {
            draggable: false,
            moveSpeed: 100,
            snapbackSpeed: 500,
            snapSpeed: 100,
            orientation: user_color,
            position: game.fen(),
            pieceTheme: DJANGO_STATIC_URL + '{piece}.png',

        }
        board = Chessboard('myBoard', config);

        $(window).resize(function() {
            board.resize();
            chart.resize();

        });



    } else if (MODULE == "" && TITTLE != "Account") {
        config = {
            orientation: user_color,
            draggable: false,
            position: 'start',
            pieceTheme: DJANGO_STATIC_URL + '{piece}.png',

        }
        board = Chessboard('myBoard', config);
        board.start()
    }


});



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
    if (compurteur_vs_human == true && user_color == "white" && game.turn() == 'b') {
        send_fen(game.fen())
    }
    if (compurteur_vs_human == true && user_color == "black" && game.turn() == 'w') {
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

    pgn_of_chess_game_complete = game.pgn()

    var list_of_moves = game.history()


    last_move = list_of_moves[list_of_moves.length - 1]
    chess_game_history_saved = game.history();
}




function onChange(oldPos, newPos) {

    updateStatus()
}


$("#switch_color").click(function(e) {
    $("#white_info").empty();
    $("#black_info").empty();
    if (user_color == "black") {
        user_color = "white"
        $("#white_info").append("<p> You are white</p>");
        $("#black_info").append("<p> The computer is black</p>");
    } else {
        user_color = "black"
        $("#white_info").append("<p> You are black</p>");
        $("#black_info").append("<p> The computer is white</p>");
    }
    board.flip();
    send_fen(game.fen())


});

$("#flip").click(function(e) {
    board.flip();
});


$("#btn-analyse").click(function(e) {
    game_save_for_analyse = new Chess()
    game_save_for_analyse.load_pgn(pgn_of_chess_game_complete)
    get_nb_of_move = game_save_for_analyse.fen().split(" ")
    get_nb_of_move = get_nb_of_move[get_nb_of_move.length - 1]
    get_nb_of_move = parseInt(get_nb_of_move) * NB_OF_ENGINE

    $("#message_analyse").text("Please wait about " + parseInt($("#time_input").val()) * get_nb_of_move + " sec on average for the time you indicated")
    if (GAME_ID == "") {
        data_to_send = {
            "id": GAME_ID,
            "time": $("#time_input").val(),
            "pgn": pgn_of_chess_game_complete
        }
    } else {
        data_to_send = {
            "id": GAME_ID,
            "time": $("#time_input").val()
        }
    }



    $.ajax({
        type: "GET",
        url: "/chess_app/get_list_of_evalutation/",
        dataType: "json",
        data: data_to_send,

        success: function(response) {
            if ("error" in response) {
                alert(response.error)
            } else {
                var len = Object.keys(response.stockfish).length
                chart.data.labels = [...Array(len).keys()]
                chart.data.datasets = [{
                        label: 'lc0 analyse',
                        backgroundColor: window.chartColors.red,
                        borderColor: window.chartColors.red,
                        data: response.lc0,
                        fill: true
                    },
                    {
                        label: 'stockfish analyse',
                        backgroundColor: window.chartColors.blue,
                        borderColor: window.chartColors.blue,
                        data: response.stockfish,
                        fill: true
                    },
                    {
                        label: 'komodo12 analyse',
                        backgroundColor: window.chartColors.green,
                        borderColor: window.chartColors.green,
                        data: response.komodo12,
                        fill: true
                    }
                ]
                chart.update();
                $("#message_analyse").text("Indicate the time between 1 to 10 sec per movement")

            }

        },
        error: function(error) {
            console.log(error)

        }
    });
});





$("#new_game").click(function(e) {
    game = new Chess()
    config = {
        orientation: user_color,
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
    board = Chessboard('myBoard', config)
    board.start()
    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())

    $.ajax({
        url: "new_game",
        dataType: "json",
        data: {
            "module": MODULE,
            "user_color": user_color
        },

        success: function(response) {
            // console.log(response.new_fen)


            if (parseInt(response.game_id) > 0) {
                game_id_current = response.game_id
                $("#div_chat").append("<p> I'm ready !!</p>");
            }
        },
        error: function(error) {
            alert("error")
        }
    });

    if (user_color == "black") {
        send_fen(game.fen())
    }

});


function send_fen(fen) {
    var list_of_moves = game.history()


    last_move = list_of_moves[list_of_moves.length - 1]

    $.ajax({
        url: "get_fen",
        dataType: "json",
        data: {
            "fen": fen,
            "module": MODULE,
            "last_move": last_move,
            "user_color": user_color,
            "game_id_current": game_id_current
        },

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

        if (TITTLE == "History of your games") {
            $("#wrapper-right").animate({ "opacity": "show", left: 0 }, 1);
        } else {
            $("#wrapper-right").animate({ "opacity": "show", left: 0 }, 1000);
        }

        $('#wrapper-right').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
            $(window).trigger('resize');
        });


    } else if ($("#menu-toggle-right").text() == ">") {

        $("#menu-toggle-right").text("<");

        if (TITTLE == "History of your games") {
            $("#wrapper-right").hide();
        } else {
            $("#wrapper-right").animate({ "opacity": "hide", left: $("#wrapper-right").width() }, 1000);
        }



        $('#wrapper-right').promise().done(function() {
            $(window).trigger('resize');
            $(window).trigger('resize');
            $(window).trigger('resize');
        });
    }



});


$("#fa-arrow-left").click(function() {
    game.undo()
    board.position(game.fen())
    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())
});

$("#fa-arrow-right").click(function() {
    move_to_play = chess_game_history_saved[game.history().length]

    game.move(move_to_play)
    board.position(game.fen())
    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())
});

$("#analyse_opt").click(function() {

    if (game_id_current != 0) {

        window.location.href = "/chess_app/show_the_game.html/?id=" + game_id_current
    }


});

$("#btn_load_pgn").click(function() {
    game.load_pgn($("#text_load_pgn").val())
    board.position(game.fen())
    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())
    pgn_of_chess_game_complete = $("#pgn").html()
    chess_game_history_saved = game.history();

});


$("#do_any_moves_btn").click(function() {
    game = new Chess()
    config = {
        orientation: user_color,
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
    board = Chessboard('myBoard', config)
    board.start()
    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())

});

$("#refresh").click(function() {


    window.location.href = "/chess_app/show_the_game.html/"



});