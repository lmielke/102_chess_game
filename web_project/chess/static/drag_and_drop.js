const figures  = document.querySelectorAll('.figure');
const empties = document.querySelectorAll('.chess_field');
let moveFigureParent = 0;
let moveFigure = 0;
let boardTextHash = {};
let hasMoved = {};
var hashBackup
var protocol = window.location.protocol;
var domain = window.location.hostname;
var pk
if (domain.includes('localhost')){
    var baseUrl = protocol + "//" + domain + ":8000";
}
else {
    var baseUrl = protocol + "//" + domain;
}
var mainMessage = document.getElementById('mainMessage');
var srcFieldId;
var toField;
var whiteRemoveds = document.getElementById('white_removeds');
var blackRemoveds = document.getElementById('black_removeds');
var checkBox1 = document.getElementById('checkBox1');
var backGroundColor = "#95aacc";
var gamePk;
var updateMode = false;
var rochade = false;


//#########################################################################################
// figure drag and drop area
// user can move figures useing drag and drop function, here all drag functions are defined
for ( const figure of figures) {
    figure.addEventListener('dragstart', dragStart);
    figure.addEventListener('dragend', dragEnd);
    }

for ( const chess_field of empties) {
    chess_field.addEventListener('dragover', dragOver);
    chess_field.addEventListener('dragenter', dragEnter);
    chess_field.addEventListener('dragleave', dragLeave);
    chess_field.addEventListener('drop', dragDrop);
    }


function dragStart() {
    this.className += ' hold';
    setTimeout(() => (this.className = 'invisible'), 0);
    moveFigure = this;
    moveFigureParent = this.parentNode.id;
    return moveFigure, moveFigureParent;
}

function dragEnd() {
    this.className = 'figure';
}

function dragOver(event) {
    event.preventDefault();
}

function dragEnter(event) {
    event.preventDefault();
    if (Object.keys(restData.moves).includes(moveFigure.id)){
        if (restData.moves[moveFigure.id].includes(this.id)) {
            this.className += ' allowed';
        } 
        else {
            this.className += ' not_allowed';
        }
    }
    else{
        this.className += ' not_allowed'
    }
}

function dragLeave() {
    this.className = 'chess_field';
}

// target field for user moves, resembles the update function for computer move above
function dragDrop() {
    if (Object.keys(restData.moves).includes(moveFigure.id)){
        if (restData.moves[moveFigure.id].includes(this.id)) {
            this.className = 'chess_field';
            // if target cell is occupied by opponent then beat the oponent
            if (this.firstElementChild !== null) {
                if (this.firstElementChild.id !== moveFigure.id) {
                    // if beateble oppoinent is a king, you have won the game
                    if (this.firstElementChild.id[0]==="K"){
                        this.style.backgroundColor = "red";
                        restData.gameStatus = "won";
                        mainMessage.textContent = 'You have won!';
                        mainMessage.style.backgroundColor = "green";
                    }
                    else{   
                        this.firstElementChild.className = 'removed_img';
                        if (this.firstElementChild.id[1] === '1'){
                            restData.removeds.white.push(this.firstElementChild.id);
                            document.getElementById('white_removeds').append(this.firstElementChild);
                        }
                        else{
                            restData.removeds.black.push(this.firstElementChild.id);
                            document.getElementById('black_removeds').append(this.firstElementChild);
                        }
                    }
                }
            }
            // this does the actual removal/assignment of figure to source/target fields
            if (this.id !== moveFigureParent & restData.gameStatus!=="won"){
                this.append(moveFigure);
                restData.boardText[this.id] = moveFigure.id;
                restData.boardText[moveFigureParent] = '----';
                boardTextHash[moveFigure.id] = this.id;
                if ((moveFigure.id[0]==='K') & (!restData.rochPara[restData.activePlayer]['K'][0][0])) {
                    mkRochade(moveFigure.id, this.id);
                }
            }
        } 
        else {
            this.className = 'chess_field';
        }
    }
    else {
        this.className = 'chess_field';
    }
}

function dragRemove() {
    this.className = 'chess_field';
}

function mkRochade(figure, tgtField){
    restData.rochPara[restData.activePlayer]['K'][0][0] = true;
    if (tgtField==='01' || tgtField==='06' || tgtField==='71' || tgtField==='76'){
        var king = restData.rochPara[restData.activePlayer]['K'];
        if ((tgtField==='06'&restData.activePlayer==='1')||(tgtField==='76'&restData.activePlayer==='2')){
            var direction = 2;
            var strdir = '2';
        }
        else {
            var direction = 1;
            var strdir = '1';
        }
        var rock = restData.rochPara[restData.activePlayer]['R'+strdir];
        var kingFieldIdx = JSON.stringify(king[direction][0]) + JSON.stringify(king[direction][1]);
        var tgtField = document.getElementById(tgtField);
        var rockName = 'R' + restData.activePlayer + '-' + strdir;
        var rockFigure = document.getElementById(rockName);
        var rockFigureParent = rockFigure.parentNode;
        var srcRock = document.getElementById(JSON.stringify(rock[1][0])+JSON.stringify(rock[1][1]));
        var tgtRock = document.getElementById(JSON.stringify(rock[2][0])+JSON.stringify(rock[2][1]));
        tgtRock.append(rockFigure);
        restData.boardText[tgtRock.id] = rockFigure.id;
        restData.boardText[rockFigureParent.id] = '----';
        boardTextHash[rockFigure.id] = tgtRock.id;
        rochade = true;
    }
}
// figure drag and drop area ENDS HERE
//#########################################################################################

// updae moves
// when computer player returns his move ($ajax response), the board is updated accordinly 
function updateBoard(data, hash){
    var isMate = checkMate(hash)
    // run update over entire board (old data) vs rest data from ajax response (updated data)
    for (restFigure of Object.keys(data.boardText)){
        var srcField = document.getElementById(restFigure);
        if (srcField.firstElementChild !== null){
            var imgFigure = srcField.firstElementChild;
            // check for every figure in data.boardText (ajax rest response) if it has been moved
            if (data.boardText[restFigure] !== imgFigure.id & imgFigure.id != undefined){
                // a figure might have been beaten by compouter player, then it does not exist in hash
                if (hash[imgFigure.id] == undefined){
                    if (isMate){
                        imgFigure.parentNode.style.backgroundColor = "red";
                    }
                    else{
                        // beaten figures are added to removed repo to be displayed below board
                        // there are two repos 1: white, 2: black
                        imgFigure.className = 'removed_img';
                        if (imgFigure.id[1] === '1'){
                            document.getElementById('white_removeds').append(imgFigure);
                        }
                        else{
                            document.getElementById('black_removeds').append(imgFigure);
                        }
                    }
                }
                else{
                    // if figure still exists and has been moved, than change its position on baord
                    hasMoved[imgFigure.id] = [srcField.id, hash[imgFigure.id]];
                    if (!isMate){
                        document.getElementById(hash[imgFigure.id]).append(imgFigure);
                    }
                    srcFieldId = document.getElementById(srcField.id);
                    toField = document.getElementById(imgFigure.id);
                    if(restData.gameStatus !== "initial" & (updateMode)){
                        srcFieldId.style.backgroundColor = backGroundColor;
                        toField.style.backgroundColor = backGroundColor;
                    }
                }
            }
            // rest api delivers possible moves to restrict user moves on board, but crrent figure position is not in moves
            // but as long as user has not confirmed move, he must be able to return moved figure to its original position
            if (data.moves[imgFigure.id] !== undefined) {
                data.moves[imgFigure.id].push(document.getElementById(imgFigure.id).parentNode.id);
            }
        }
    }
    // if user chooses to switch game, then above moves should not be set during initialization
    updateMode = true;
}

function checkMate(hash){
    var playerKing = "K"+restData.activePlayer+"-1"
    if (hash[playerKing] !== undefined){
        var isMate = false;
    }
    else{
        var isMate = true;
        backGroundColor = "red";
        restData.gameStatus = "lost";
        mainMessage.textContent = 'You have lost!';
        mainMessage.style.backgroundColor = "red";
    }
    return isMate
}

function updates(){
    var data = restData;
    var hash = boardTextHash;
    mainMessage.textContent = 'Make your Move!';
    updateBoard(data, hash);
}

function setColors(){
    if (srcFieldId){
        toField.style.backgroundColor = "";
        srcFieldId.style.backgroundColor = "";
    }}

function undo(reload){
    window.location.href = reload;
}


function exitGame(){
    var chPid = document.getElementById("chPid")
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://localhost:8000/exit/chPid="+chPid.textContent, false ); // false for synchronous request
    try {
        xmlHttp.send( null );
    }
    catch(err) {

        window.location.href = "https://en.wikipedia.org/wiki/Grandmaster_(chess)";
    }
    return xmlHttp.responseText;
};

function restart(){
    protocol = window.location.protocol;
    domain = window.location.hostname;
    window.location.assign(protocol+"//"+domain+":8000/chess");
}


//*** after initial load, the page is updated using ajax call to django
// ajax calls start here using jqery ***
// GET request to read current game database for specified gameId
var restUrl = baseUrl + "/rest/chess/";
var restData;

// new board is returned via ajax as a dictionary with keys = figure but is needed here
// as object with keys = positionIndex, therefore keys and values are reversed here
function arrayToObj(boardText){
    var idx = 0;
    var restOut = {};
    for (i = 0; i < 8; i++) {
        for (j = 0; j < 8; j++){
            restOut[i.toString()+j.toString()] = boardText[idx];
            idx++;
        }
    }
    boardTextHash = {};
    for (elem of Object.keys(restOut)){
        if (restOut[elem] != '----'){
            boardTextHash[restOut[elem]] = elem
        }
    }
    hashBackup = JSON.parse(JSON.stringify(boardTextHash));
    return restOut
}

function callback(response) {
    restData = response;
    restData.removeds = JSON.parse(restData.removeds.replace(/'/g, '"'))
    restData.rochPara = JSON.parse(restData.rochPara.replace(/'/g, '"'))
    restData.moves = JSON.parse(restData.moves.replace(/'/g, '"'))
    restData.boardText = JSON.parse(restData.boardText.replace(/'/g, '"'));
    restData.boardText = arrayToObj(restData.boardText);
    restBackup = restData
    updates()
}

// anonymous ajax runs when board is created and initialized
if (document.getElementById("pk").innerText !== ''){
    pk = parseInt(document.getElementById("pk").textContent, 10)
    console.log(restUrl + pk);
    $.ajax({
        type: 'GET',
        url: restUrl + pk,
        success: function(data) {
            callback(data)
                                },
        error: function(){alert('error loading board');}
            });
}

checkBox1.addEventListener('change', get_all_games);

// user can switch between existing games at any time, here games are displayed for selection
function get_all_games(){
    $.ajax({
        type: 'GET',
        url: restUrl,
        success: function(data) {
            pk = parseInt(document.getElementById("pk").textContent, 10)
            var gameSelector = document.getElementById("selectGame");
                var game = document.createElement("option");
                game.textContent = "- make a choice -";
                game.value = undefined;
                gameSelector.appendChild(game);
            for (record of data){
                if (record.pk !== 1){
                    var game = document.createElement("option");
                    game.textContent = record.gameName;
                    game.value = record.pk;
                    gameSelector.appendChild(game);
                }
            }
            gameSelector.style.visibility = "visible";
            gameSelector.addEventListener('change', function (event)
                {
                    var protocol = window.location.protocol
                    var domain = window.location.hostname
                    if (window.location.href.indexOf("Game") > -1){
                        window.location.assign(protocol+"//"+domain+":8000/chess/Game="+this.value);
                    }
                    else{
                        window.location.replace(window.location+"Game="+this.value)
                    }
                }
            );
        },
        error: function(){alert('error loading board');
        }
    });
}

// make sure, the user exactly moves 1 figure at a time
function validateMove(){
    var moveCounter = 0;
    for (figure of Object.keys(boardTextHash)){
        if (boardTextHash[figure] === hashBackup[figure]){
            undefined;
        }
        else {moveCounter++};
    }
    if (rochade){
        moveCounter--;
        rochade = false;
    }
    if (moveCounter !== 1){
            let message = moveCounter+' moves detected';
            alert(message);
            return false;
    }
    else{
        return true;
    }
}

//*** getCookie and csrfSafeMehod are standard functions taken form the django website
// 2019-09: https://docs.djangoproject.com/en/2.2/ref/csrf/
function mkPost(){
    if (validateMove()){
        mainMessage.textContent = 'I am thinking!';
        setColors();
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        };
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        // PUT request to the django database and retieve updated data
        $(function(){
            pk = parseInt(document.getElementById("pk").textContent, 10)
            restData.gameStatus = "active";
            restData.moves = JSON.stringify(restData.moves);
            restData.removeds = JSON.stringify(restData.removeds);
            restData.rochPara = JSON.stringify(restData.rochPara);
            restData.boardText = JSON.stringify(restData.boardText);
            $.ajax({
                type: 'PUT',
                url: restUrl + pk + '/',
                data: restData,
                success: function(data) {
                            //restData = data
                            callback(data)
                            //restData.moves = JSON.parse(restData.moves.replace(/'/g, '"'))
                        },
                error: function(){
                            alert('error loading board');
                        }
                });
        });

    }
}