let court;
let ball;
let paddle;
let x;
let y;
let dx;
let dy;
let strikes;
let maxScore = 0;
let stopId;
let speed = 3;
let OFFSET;
let flag;

const BALLDIAMETER = 20;
const PADDLEHIGHT = 102;
const COURTHIGHT = 500;
const COURTWIDTH = 800;


function initialize() {
    paddle = document.getElementById("paddle");
    court = document.getElementById("court");
    ball  = document.getElementById("ball");
    OFFSET = court.offsetTop
    resetGame()
}

function startGame() {
    if (stopId){
        cancelAnimationFrame(stopId)
    }
    
    window.requestAnimationFrame(moveBall)
}

function resetGame() {
    x  = 0;
    y  = Math.floor(Math.random() * 482 ) - 82;
    dy = 0
    dx = 1;
    while (Math.abs(dy) < 0.1){
        dy = (Math.random() * 2 ) - 1;
    }
    strikes = 0;
    speed = 3;
    document.getElementById("slow").checked = true;
    document.getElementById("strikes").innerHTML = strikes
    if (stopId){
        cancelAnimationFrame(stopId)
    }
    ball.style.left = x + 'px';
    ball.style.top  = y + 'px';
}

function setSpeed(par) {
    speed = (par + 1)*4
    console.log(speed)
}

function movePaddle(event) {
    if(event.clientY < OFFSET + PADDLEHIGHT/2) {
        paddleY = 0
    }
    else if (event.clientY > OFFSET + COURTHIGHT - PADDLEHIGHT/2) {
        paddleY = 400
    }
    else {
        paddleY = event.clientY - OFFSET - PADDLEHIGHT/2
    }
    paddle.style.top = paddleY + 'px'
}

function moveBall() {

    if (x < 0){
        dx = -dx
    }
    if (y < -82 || y > 400){
        dy = -dy
    }
    if (x>750){
        console.log(paddleY,y, paddleY - PADDLEHIGHT - BALLDIAMETER/2, paddleY + BALLDIAMETER/2)
        if (y >= paddleY - PADDLEHIGHT - BALLDIAMETER/2 && y <= paddleY + BALLDIAMETER/2 ){
            dx = -dx
            strikes += 1
            document.getElementById("strikes").innerHTML = strikes
        }
        else{
            flag = true
            if (strikes > maxScore){
                maxScore = strikes
                document.getElementById("score").innerHTML = strikes
                document.getElementById("messages").innerHTML = "Congrats!! you achieved a new Max score."
            }
            else{
                document.getElementById("messages").innerHTML = "Out!! better luck next time."
            }
            resetGame();
        }
    }

    x += dx*speed
    y += dy*speed
    
    if (flag){
        flag = false
    }
    else{
        
//        document.getElementById("messages").innerHTML = "Defend the right side wall from the ball."
        ball.style.left = x + 'px';
        ball.style.top  = y + 'px';
        stopId = window.requestAnimationFrame(moveBall)
    }
}