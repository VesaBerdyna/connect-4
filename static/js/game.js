reloaded = false


function autoUpdate() {
    myVar = setInterval(getNewBoard, 1000);
}


function displayBoard(board) {
    for (var row = 0; row < board.length; row++) {
        for (var col = 0; col < board[0].length; col++) {
            if (board[row][col] == 'RED') {
                document.querySelectorAll('[num="'+col+'"]')[row].style.backgroundColor = 'red'
            } else if (board[row][col] == 'BLUE') {
                document.querySelectorAll('[num="'+col +'"]')[row].style.backgroundColor = 'yellow'
            }
        }
    }
}
function getNewBoard() {
    console.log("new board");
    const Http = new XMLHttpRequest();
    var game_id_input = document.getElementById("game_id")
    var url = "http://127.0.0.1:5000/board?game_id=" + game_id_input.value
    Http.open("GET", url)
    Http.send()
    Http.onload = function () {
        if (Http.readyState == Http.DONE) {
            if (Http.status == 200) {
                data = JSON.parse(Http.response)
                console.log(JSON.parse(data.game_state))
                dataa = JSON.parse(data.game_state)
                displayBoard(dataa.board)

            }
        }
    }
}
getNewBoard()

function move(event) {
    const Http = new XMLHttpRequest();

    var url = "http://127.0.0.1:5000/move"

    Http.open('POST', url)
    Http.setRequestHeader("Content-Type", "application/json");
    let colNum = event.target.getAttribute('num')
    data = JSON.stringify({ 'column': colNum})
    console.log(data)
    Http.responseType = 'text'
    Http.send(data)
}


autoUpdate()
