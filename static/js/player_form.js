const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('mode');

var player1 = document.getElementById('player1');
var player2 = document.getElementById('player2');
var titleOfPlayer1 = document.getElementById('single');
var titleOfPlayer2 = document.getElementById('multi');

if (myParam == 'single') {
  player2.style.display = 'none';
  titleOfPlayer2.style.display = 'none';
} else if (myParam == 'multi') {
  titleOfPlayer1.style.display = 'none';
}
