import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Office Stealth 2.5D", layout="wide")

# Nhúng game HTML/Canvas/JS vào Streamlit với màu sắc rõ nét hơn
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; background: #0f111a; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #game-container { position: relative; border: 4px solid #4f46e5; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        canvas { display: block; background: #1e2235; }
        #ui { position: absolute; top: 12px; left: 12px; right: 12px; display: flex; justify-content: space-between; pointer-events: none; }
        .badge { background: rgba(0,0,0,0.8); padding: 8px 16px; border-radius: 20px; font-size: 15px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2); }
        #instructions { margin-top: 10px; font-size: 14px; color: #94a3b8; }
        kbd { background: #334155; padding: 2px 6px; border-radius: 4px; border: 1px solid #475569; color: #fff; }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="480"></canvas>
        <div id="ui">
            <div class="badge" id="mission">🎯 Nhiệm vụ: Tìm 3 vật phẩm & thoát hiểm!</div>
            <div class="badge" id="status" style="color:#ef4444">🏃 Đang chạy</div>
        </div>
    </div>
    <div id="instructions">
        Dùng phím <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> hoặc <kbd>Mũi tên</kbd> để đi | Giữ <kbd>Shift</kbd> để ẨN NẤP
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let gameState = 'PLAYING', itemsCollected = 0, totalItems = 3;

        // Nhân viên (Player) màu xanh sáng, mũ đỏ nổi bật
        let player = { x: 80, y: 240, r: 14, speed: 3.2, crouchSpeed: 1.4, isCrouching: false };
        // Bà chủ (Boss) váy hồng nổi bật
        let boss = { x: 700, y: 240, r: 18, speed: 1.6, state: 'PATROL', vision: 160, target: {x: 600, y: 100} };
        
        // Bàn làm việc
        let desks = [
            {x: 200, y: 100, w: 100, h: 65}, 
            {x: 200, y: 310, w: 100, h: 65}, 
            {x: 460, y: 180, w: 110, h: 100}
        ];
        // Vật phẩm cần tìm
        let items = [
            {x: 250, y: 60, c: false, icon: '📁'},
            {x: 515, y: 320, c: false, icon: '💼'},
            {x: 730, y: 400, c: false, icon: '👑'}
        ];
        // Cửa thoát
        let exit = {x: 740, y: 30, w: 45, h: 55};

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

            player.x = Math.max(20, Math.min(canvas.width - 20, player.x));
            player.y = Math.max(20, Math.min(canvas.height - 20, player.y));

            // Nhặt đồ
            items.forEach(it => {
                if (!it.c && Math.hypot(player.x - it.x, player.y - it.y) < 25) {
                    it.c = true; itemsCollected++;
                    document.getElementById('mission').innerText =🎯 Nhiệm vụ: Lấy vật phẩm (${itemsCollected}/${totalItems})`;
                }
            });

            // Thắng game
            if (itemsCollected >= totalItems && Math.hypot(player.x - (exit.x + 22), player.y - (exit.y + 27)) < 35) {
                gameState = 'WIN';
            }

            // AI Bà chủ
            let dist = Math.hypot(boss.x - player.x, boss.y - player.y);
            if (dist < boss.vision && !player.isCrouching) {
                boss.state = 'CHASE';
            } else if (dist > boss.vision * 1.5) {
                boss.state = 'PATROL';
            }

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
            if (player.isCrouching) { st.innerText = '🤫 Đang ẩn nấp'; st.style.color = '#10b981'; }
            else { st.innerText = '🏃 Đang chạy'; st.style.color = '#ef4444'; }
        }

        function checkDesk(p) {
            return desks.some(d => p.x + p.r > d.x && p.x - p.r < d.x + d.w && p.y + p.r > d.y && p.y - p.r < d.y + d.h);
        }

        function draw() {
            // Nền sàn văn phòng
            ctx.fillStyle = '#1e2235'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Kẻ lưới sàn cho dễ nhìn không gian
            ctx.strokeStyle = '#282d45';
            ctx.lineWidth = 1;
            for (let i = 0; i < canvas.width; i += 40) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke();
            }

            // Cửa thoát hiểm
            ctx.fillStyle = itemsCollected >= totalItems ? '#10b981' : '#475569';
            ctx.fillRect(exit.x, exit.y, exit.w, exit.h);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px sans-serif';
            ctx.fillText("EXIT", exit.x + 8, exit.y + 33);

            // Bàn làm việc
            desks.forEach(d => {
                ctx.fillStyle = '#78350f'; ctx.fillRect(d.x, d.y, d.w, d.h); // thân bàn
                ctx.fillStyle = '#92400e'; ctx.fillRect(d.x + 4, d.y + 4, d.w - 8, d.h - 8); // mặt bàn
                ctx.fillStyle = '#334155'; ctx.fillRect(d.x + 35, d.y + 15, 40, 25); // máy tính
            });

            // Vật phẩm
            items.forEach(it => {
                if (!it.c) {
                    ctx.font = '22px sans-serif';
                    ctx.fillText(it.icon, it.x - 11, it.y + 8);
                }
            });

            // NHÂN VIÊN (Player - Áo xanh, mũ đỏ)
            ctx.save();
            ctx.beginPath();
            let currentR = player.isCrouching ? player.r * 0.75 : player.r;
            ctx.arc(player.x, player.y, currentR, 0, Math.PI * 2);
            ctx.fillStyle = '#3b82f6'; // Áo xanh dương
            ctx.fill();
            ctx.lineWidth = 2; ctx.strokeStyle = '#fff'; ctx.stroke();
            // Mũ đỏ
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.arc(player.x, player.y - 3, currentR * 0.6, Math.PI, 0, false);
            ctx.fill();
            ctx.restore();

            // BÀ CHỦ (Boss - Váy hồng)
            if (boss.state === 'PATROL') {
                ctx.fillStyle = 'rgba(239, 68, 68, 0.08)';
                ctx.beginPath(); ctx.arc(boss.x, boss.y, boss.vision, 0, Math.PI * 2); ctx.fill();
            }
            ctx.beginPath();
            ctx.arc(boss.x, boss.y, boss.r, 0, Math.PI * 2);
            ctx.fillStyle = boss.state === 'CHASE' ? '#991b1b' : '#ec4899'; // Váy hồng / đỏ khi đuổi
            ctx.fill();
            ctx.lineWidth = 2; ctx.strokeStyle = '#fff'; ctx.stroke();

            // Màn hình thắng/thua
            if (gameState !== 'PLAYING') {
                ctx.fillStyle = 'rgba(0,0,0,0.88)'; ctx.fillRect(0,0,canvas.width,canvas.height);
                ctx.fillStyle = gameState === 'WIN' ? '#10b981' : '#ef4444';
                ctx.font = 'bold 28px sans-serif'; ctx.textAlign = 'center';
                ctx.fillText(gameState === 'WIN' ? '🎉 CHIẾN THẮNG TRỐN THÀNH CÔNG!' : '💥 BỊ BÀ CHỦ TÓM GỌN!', canvas.width/2, canvas.height/2 - 10);
                ctx.font = '15px sans-serif'; ctx.fillStyle = '#cbd5e1';
                ctx.fillText("Nhấn F5 để chơi lại ván mới", canvas.width/2, canvas.height/2 + 30);
                ctx.textAlign = 'left';
            }
        }

        function loop() { update(); draw(); requestAnimationFrame(loop); }
        loop();
    </script>
</body>
</html>
"""

components.html(game_html, height=580)






    
