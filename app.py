
        
 
import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Office Stealth 2.5D", layout="wide")

# Nhúng toàn bộ game HTML/Canvas/JS vào Streamlit
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; background: #111; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }
        #game-container { position: relative; margin-top: 10px; border: 3px solid #444; border-radius: 8px; }
        canvas { display: block; background: #222533; }
        #ui { position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; pointer-events: none; }
        .badge { background: rgba(0,0,0,0.7); padding: 6px 12px; border-radius: 12px; font-size: 14px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="480"></canvas>
        <div id="ui">
            <div class="badge" id="mission">Nhiệm vụ: Tìm 3 vật phẩm & thoát hiểm!</div>
            <div class="badge" id="status" style="color:#e74c3c">🏃 Đang chạy</div>
        </div>
    </div>
    <p style="font-size:13px; color:#aaa;">Phím W A S D / Mũi tên để di chuyển | Giữ Shift để nấp sau bàn</p>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let gameState = 'PLAYING', itemsCollected = 0, totalItems = 3;

        let player = { x: 80, y: 240, r: 12, speed: 3, crouchSpeed: 1.4, isCrouching: false };
        let boss = { x: 700, y: 240, r: 16, speed: 1.7, state: 'PATROL', vision: 150, target: {x: 600, y: 100} };
        let desks = [{x: 200, y: 100, w: 90, h: 60}, {x: 200, y: 300, w: 90, h: 60}, {x: 450, y: 180, w: 90, h: 100}];
        let items = [{x: 245, y: 70, c: false}, {x: 495, y: 320, c: false}, {x: 720, y: 400, c: false}];
        let exit = {x: 750, y: 30, w: 35, h: 50};

        let keys = {};
        window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
        window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

        function update() {
            if (gameState !== 'PLAYING') return;
            player.isCrouching = keys['shift'] || false;
            let spd = player.isCrouching ? player.crouchSpeed : player.speed;

            let dx = 0, dy = 0;
            if (keys['w'] || keys['arrowup']) dy -= spd;
            if (keys['s'] || keys['arrowdown']) dy += spd;
            if (keys['a'] || keys['arrowleft']) dx -= spd;
            if (keys['d'] || keys['arrowright']) dx += spd;

            player.x += dx; if (checkDesk(player)) player.x -= dx;
            player.y += dy; if (checkDesk(player)) player.y -= dy;

            player.x = Math.max(15, Math.min(canvas.width - 15, player.x));
            player.y = Math.max(15, Math.min(canvas.height - 15, player.y));

            items.forEach(it => {
                if (!it.c && Math.hypot(player.x - it.x, player.y - it.y) < 25) {
                    it.c = true; itemsCollected++;
                    document.getElementById('mission').innerText = Nhiệm vụ: Lấy vật phẩm (${itemsCollected}/${totalItems});
                }
            });

            if (itemsCollected >= totalItems && Math.hypot(player.x - (exit.x + 15), player.y - (exit.y + 25)) < 30) {
                gameState = 'WIN';
            }

            let dist = Math.hypot(boss.x - player.x, boss.y - player.y);
            if (dist < boss.vision && !player.isCrouching) boss.state = 'CHASE';
            else if (dist > boss.vision * 1.4) boss.state = 'PATROL';

            if (boss.state === 'CHASE') {
                let angle = Math.atan2(player.y - boss.y, player.x - boss.x);
                boss.x += Math.cos(angle) * boss.speed;
                boss.y += Math.sin(angle) * boss.speed;
                if (dist < player.r + boss.r) gameState = 'GAMEOVER';
            } else {
                let tDist = Math.hypot(boss.target.x - boss.x, boss.target.y - boss.y);
                if (tDist < 10) boss.target = { x: Math.random() * 400 + 350, y: Math.random() * 350 + 50 };
                let angle = Math.atan2(boss.target.y - boss.y, boss.target.x - boss.x);
                boss.x += Math.cos(angle) * (boss.speed * 0.6);
                boss.y += Math.sin(angle) * (boss.speed * 0.6);
            }

            let st = document.getElementById('status');
            if (player.isCrouching) { st.innerText = '🤫 Đang ẩn nấp'; st.style.color = '#2ecc71'; }
            else { st.innerText = '🏃 Đang chạy'; st.style.color = '#e74c3c'; }
        }

        function checkDesk(p) {
            return desks.some(d => p.x + p.r > d.x && p.x - p.r < d.x + d.w && p.y + p.r > d.y && p.y - p.r < d.y + d.h);
        }

        function draw() {
            ctx.fillStyle = '#222533'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Cửa thoát
            ctx.fillStyle = itemsCollected >= totalItems ? '#2ecc71' : '#555';
            ctx.fillRect(exit.x, exit.y, exit.w, exit.h);

            // Bàn làm việc
            desks.forEach(d => {
                ctx.fillStyle = '#5c4033'; ctx.fillRect(d.x, d.y, d.w, d.h);
                ctx.fillStyle = '#333'; ctx.fillRect(d.x + 25, d.y + 15, 30, 20);
            });

            // Vật phẩm
            items.forEach(it => { if(!it.c) { ctx.fillStyle = '#f1c40f'; ctx.beginPath(); ctx.arc(it.x, it.y, 8, 0, Math.PI*2); ctx.fill(); }});

            // Player
            ctx.fillStyle = '#3498db'; ctx.beginPath(); ctx.arc(player.x, player.y, player.isCrouching ? 8 : 12, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#e74c3c'; ctx.beginPath(); ctx.arc(player.x, player.y - 3, 5, Math.PI, 0); ctx.fill();

            // Boss
            if (boss.state === 'PATROL') {
                ctx.fillStyle = 'rgba(231, 76, 60, 0.1)';
                ctx.beginPath(); ctx.arc(boss.x, boss.y, boss.vision, 0, Math.PI*2); ctx.fill();
            }
            ctx.fillStyle = boss.state === 'CHASE' ? '#e74c3c' : '#ff69b4';
            ctx.beginPath(); ctx.arc(boss.x, boss.y, boss.r, 0, Math.PI*2); ctx.fill();

            if (gameState !== 'PLAYING') {
                ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0,0,canvas.width,canvas.height);
                ctx.fillStyle = gameState === 'WIN' ? '#2ecc71' : '#e74c3c';
                ctx.font = 'bold 28px sans-serif'; ctx.textAlign = 'center';
                ctx.fillText(gameState === 'WIN' ? '🎉 THẮNG CỦA GAME!' : '💥 BỊ BÀ CHỦ BẮT!', canvas.width/2, canvas.height/2);
            }
        }

        function loop() { update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
</body>
</html>
"""

# Hiển thị game trên giao diện Streamlit
components.html(game_html, height=580)

