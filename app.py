import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chém Trái Cây",
    page_icon="🍉",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #17213b, #351d40);
    color: white;
}
h1 {
    color: #ffd34e !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🍉 CHÉM TRÁI CÂY 🍊")
st.markdown(
    "<p style='text-align:center;color:white'>"
    "Vuốt qua trái cây để chém! Né bom nhé 💣"
    "</p>",
    unsafe_allow_html=True
)

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport"
 content="width=device-width, initial-scale=1, maximum-scale=1">
<style>
* { box-sizing:border-box; }
body {
    margin:0;
    font-family:Arial,sans-serif;
    background:#17213b;
    color:white;
    overflow:hidden;
}
#panel {
    display:flex;
    justify-content:space-around;
    align-items:center;
    gap:6px;
    padding:10px 4px;
    font-size:17px;
    font-weight:bold;
}
#score { color:#ffdb4d; }
#time { color:#9cf5ff; }
#lives { color:#ff7777; }
canvas {
    width:100%;
    height:auto;
    display:block;
    border:3px solid #ffda70;
    border-radius:16px;
    background:linear-gradient(#182b51,#713c50 65%,#34213a);
    touch-action:none;
}
#help {
    text-align:center;
    color:#ffe9ad;
    font-size:14px;
    padding:10px 2px;
}
button {
    width:100%;
    padding:13px;
    border:0;
    border-radius:14px;
    background:linear-gradient(90deg,#ffb52e,#ffdf58);
    color:#46213b;
    font-size:18px;
    font-weight:bold;
}
</style>
</head>
<body>
<div id="panel">
  <div>🍉 Điểm: <span id="score">0</span></div>
  <div>⏱️ <span id="time">45</span>s</div>
  <div>❤️ <span id="lives">3</span></div>
</div>

<canvas id="game" width="700" height="470"></canvas>

<div id="help">
  👆 Vuốt qua trái cây để chém · Tránh 💣 · Có 45 giây!
</div>
<button id="restart">🔄 CHƠI LẠI</button>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const timeEl = document.getElementById("time");
const livesEl = document.getElementById("lives");

const fruits = ["🍉","🍊","🍎","🍓","🍍","🍋","🥝","🍑"];
let objects = [];
let particles = [];
let trails = [];
let score = 0;
let lives = 3;
let remaining = 45;
let running = true;
let last = performance.now();
let spawnTimer = 0;
let lastSecond = performance.now();
let dragging = false;
let pointer = {x:0,y:0};
let previous = {x:0,y:0};

function reset() {
    score = 0;
    lives = 3;
    remaining = 45;
    running = true;
    objects = [];
    particles = [];
    trails = [];
    spawnTimer = 0;
    last = performance.now();
    lastSecond = last;
    scoreEl.textContent = score;
    livesEl.textContent = lives;
    timeEl.textContent = remaining;
    requestAnimationFrame(frame);
}

function position(event) {
    const r = canvas.getBoundingClientRect();
    return {
        x: (event.clientX-r.left)*canvas.width/r.width,
        y: (event.clientY-r.top)*canvas.height/r.height
    };
}

canvas.addEventListener("pointerdown", e => {
    e.preventDefault();
    dragging = true;
    pointer = position(e);
    previous = {...pointer};
    trails.push({...pointer, life:9});
    canvas.setPointerCapture(e.pointerId);
});

canvas.addEventListener("pointermove", e => {
    if (!dragging || !running) return;
    e.preventDefault();
    const p = position(e);
    trails.push({...p, life:10});

    for (const o of objects) {
        if (o.cut) continue;
        const d = Math.hypot(o.x-p.x, o.y-p.y);
        const segment = Math.hypot(
            o.x-(p.x+previous.x)/2,
            o.y-(p.y+previous.y)/2
        );
        if (d < o.r+13 || segment < o.r+10) {
            o.cut = true;
            if (o.bomb) {
                lives--;
                livesEl.textContent = lives;
                burst(o.x,o.y,"💥");
                if (lives <= 0) endGame("Hết mạng rồi!");
            } else {
                score += 10;
                scoreEl.textContent = score;
                burst(o.x,o.y,o.emoji);
            }
            break;
        }
    }
    previous = {...p};
    pointer = {...p};
});

function stopPointer() { dragging = false; }
canvas.addEventListener("pointerup", stopPointer);
canvas.addEventListener("pointercancel", stopPointer);

function burst(x,y,emoji) {
    particles.push({x,y,emoji,life:24});
}

function spawn() {
    const count = Math.random() < 0.3 ? 3 : 2;
    for (let i=0; i<count; i++) {
        const bomb = Math.random() < 0.12;
        objects.push({
            x: 65+Math.random()*570,
            y: 485,
            vx: (Math.random()-0.5)*4.5,
            vy: -9-Math.random()*4,
            r: 27,
            emoji: bomb ? "💣" :
                fruits[Math.floor(Math.random()*fruits.length)],
            bomb,
            cut:false
        });
    }
}

function endGame(message) {
    running = false;
    dragging = false;
    ctx.fillStyle = "rgba(12,15,38,0.83)";
    ctx.fillRect(0,0,700,470);
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffdb4d";
    ctx.font = "bold 40px Arial";
    ctx.fillText("TRÒ CHƠI KẾT THÚC",350,190);
    ctx.fillStyle = "white";
    ctx.font = "bold 27px Arial";
    ctx.fillText(message,350,245);
    ctx.font = "24px Arial";
    ctx.fillText("Điểm của bạn: "+score,350,295);
    ctx.font = "20px Arial";
    ctx.fillText("Bấm CHƠI LẠI bên dưới nhé!",350,345);
}

function drawBackground() {
    ctx.clearRect(0,0,700,470);
    ctx.fillStyle = "#ffd98a";
    ctx.beginPath();
    ctx.arc(590,65,33,0,Math.PI*2);
    ctx.fill();

    for(let i=0;i<8;i++) {
        ctx.fillStyle = i%2 ? "#264d4b" : "#203c46";
        ctx.beginPath();
        ctx.arc(i*100+15,440,85,Math.PI,Math.PI*2);
        ctx.fill();
    }

    ctx.fillStyle = "#ffe8ac";
    ctx.font = "18px Arial";
    ctx.textAlign = "center";
    ctx.fillText("CHÉM TRÁI CÂY",350,35);
}

function frame(now) {
    if (!running) return;

    const dt = Math.min((now-last)/16.67,2);
    last = now;

    if (now-lastSecond >= 1000) {
        remaining--;
        timeEl.textContent = remaining;
        lastSecond = now;
        if (remaining <= 0) {
            endGame("Hết giờ!");
            return;
        }
    }

    spawnTimer += dt;
    if (spawnTimer > 28) {
        spawn();
        spawnTimer = 0;
    }

    drawBackground();

    for (const o of objects) {
        o.x += o.vx*dt;
        o.y += o.vy*dt;
        o.vy += 0.19*dt;

        if (!o.cut) {
            ctx.font = "43px Arial";
            ctx.textAlign = "center";
            ctx.fillText(o.emoji,o.x,o.y);
        }
    }

    objects = objects.filter(o => o.y < 530 && !o.cut);

    for (const p of particles) {
        ctx.globalAlpha = Math.max(0,p.life/24);
        ctx.font = "30px Arial";
        ctx.textAlign = "center";
        ctx.fillText(p.emoji,p.x,p.y);
        p.y -= 1.4*dt;
        p.life -= dt;
    }
    particles = particles.filter(p => p.life > 0);
    ctx.globalAlpha = 1;

    for (const t of trails) {
        t.life -= dt;
        ctx.globalAlpha = Math.max(0,t.life/10);
        ctx.fillStyle = "#bdfcff";
        ctx.beginPath();
        ctx.arc(t.x,t.y,5,0,Math.PI*2);
        ctx.fill();
    }
    trails = trails.filter(t => t.life > 0);
    ctx.globalAlpha = 1;

    if (dragging && trails.length > 1) {
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 5;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(previous.x,previous.y);
        ctx.lineTo(pointer.x,pointer.y);
        ctx.stroke();
    }

    requestAnimationFrame(frame);
}

document.getElementById("restart").addEventListener("click",reset);
reset();
</script>
</body>
</html>
"""

components.html(game, height=650, scrolling=False)


   











    
