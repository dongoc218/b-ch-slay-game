import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Office Escape - Slay Game 3D", layout="wide")

# Code game HTML/JS đã được tinh chỉnh lại kích thước chuẩn để hiển thị đầy đủ
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Office Escape - Slay Game</title>
    <style>
        body {
            margin: 0;
            background: #0f172a;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 3px solid #6366f1;
            border-radius: 10px;
            background: #1e293b;
        }
        canvas {
            display: block;
        }
        #ui {
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
        }
        .badge {
            background: rgba(15, 23, 42, 0.9);
            padding: 6px 14px;
            border-radius: 15px;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid rgba(255,255,255,0.2);
        }
        #instructions {
            margin-top: 10px;
            font-size: 14px;
            color: #94a3b8;
            text-align: center;
        }
        kbd {
            background: #334155;
            padding: 2px 6px;
            border-radius: 4px;
            color: #fff;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <!-- Đặt kích thước chuẩn vừa khít màn hình Streamlit -->
        <canvas id="gameCanvas" width="760" height="420"></canvas>
        <div id="ui">
            <div class="badge" id="mission">🎯 Nhiệm vụ: Lấy 3 tài liệu & Chạy tới Cửa Xanh!</div>
            <div class="badge" id="status" style="color:#ef4444">🏃 Đang chạy</div>
        </div>
    </div>
    <div id="instructions">
        Dùng phím <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> để đi | Giữ <kbd>Shift</kbd> để ẨN NẤP sau bàn!
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let gameState = 'PLAYING';
        let itemsCollected = 0;
        let totalItems = 3;

        // Nhân viên (Áo xanh, mũ đỏ)
        let player = {
            x: 80,
            y: 210,
            radius: 14,
            speed: 3.2,
            crouchSpeed: 1.4,
            isCrouching: false
        };

        // Bà chủ (Váy hồng)
        let boss = {
            x: 650,
            y: 210,
            radius: 18,
            speed: 1.6,
            state: 'PATROL',
            visionRange: 150,
            target: {x: 550, y: 100}
        };

        // Bàn làm việc (Chỗ nấp)
        let desks = [
            {x: 200, y: 80, w: 100, h: 60},
            {x: 200, y: 280, w: 100, h: 60},
            {x: 440, y: 160, w: 110, h: 100}
        ];

        // Vật phẩm cần nhặt
        let items = [
            {x: 250, y: 50, collected: false, icon: '📁'},
            {x: 495, y: 290, collected: false, icon: '💼'},
            {x: 700, y: 360, collected: false, icon: '👑'}
        ];

        // Cửa thoát
        let exitDoor = {x: 700, y: 20, w: 45, h: 50};

        let keys = {};
        window.addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; });
        window.addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });

        function update() {
            if (gameState !== 'PLAYING') return;

            player.isCrouching = keys['shift'] || false;
            let currentSpeed = player.isCrouching ? player.crouchSpeed : player.speed;

            let dx = 0, dy = 0;
            if (keys['w'] || keys['arrowup']) dy -= currentSpeed;
            if (keys['s'] || keys['arrowdown']) dy += currentSpeed;
            if (keys['a'] || keys['arrowleft']) dx -= currentSpeed;
            if (keys['d'] || keys['arrowright']) dx += currentSpeed;

            player.x += dx;
            if (checkDeskCollision(player)) player.x -= dx;
            player.y += dy;
            if (checkDeskCollision(player)) player.y -= dy;

            player.x = Math.max(20, Math.min(canvas.width - 20, player.x));
            player.y = Math.max(20, Math.min(canvas.height - 20, player.y));

            // Nhặt đồ
            items.forEach(item => {
                if (!item.collected) {
                    let dist = Math.hypot(player.x - item.x, player.y - item.y);
                    if (dist < 25) {
                        item.collected = true;
                        itemsCollected++;
                        document.getElementById('mission').innerText =🎯 Nhiệm vụ: Đã lấy (${itemsCollected}/${totalItems}) tài liệu`;
                    }
                }
            });

            // Thắng game
            if (itemsCollected >= totalItems) {
                let distToExit = Math.hypot(player.x - (exitDoor.x + exitDoor.w/2), player.y - (exitDoor.y + exitDoor.h/2));
                if (distToExit < 35) {
                    gameState = 'WIN';
                }
            }

            // AI Bà chủ
            let distToBoss = Math.hypot(boss.x - player.x, boss.y - player.y);
            
            if (distToBoss < boss.visionRange && !player.isCrouching) {
                boss.state = 'CHASE';
            } else if (distToBoss > boss.visionRange * 1.5) {
                boss.state = 'PATROL';
            }

            if (boss.state === 'CHASE') {
                let angle = Math.atan2(player.y - boss.y, player.x - boss.x);
                boss.x += Math.cos(angle) * boss.speed;
                boss.y += Math.sin(angle) * boss.speed;

                if (distToBoss < player.radius + boss.radius) {
                    gameState = 'GAMEOVER';
                }
            } else {
                let targetDist = Math.hypot(boss.target.x - boss.x, boss.target.y - boss.y);
                if (targetDist < 15) {
                    boss.target = {
                        x: Math.random() * 300 + 400,
                        y: Math.random() * 300 + 50
                    };
                }
                let angle = Math.atan2(boss.target.y - boss.y, boss.target.x - boss.x);
                boss.x += Math.cos(angle) * (boss.speed * 0.6);
                boss.y += Math.sin(angle) * (boss.speed * 0.6);
            }

            let statusEl = document.getElementById('status');
            if (player.isCrouching) {
                statusEl.innerText = "🤫 Đang ẩn nấp";
                statusEl.style.color = "#10b981";
            } else {
                statusEl.innerText = "🏃 Đang chạy";
                statusEl.style.color = "#ef4444";
            }
        }

        function checkDeskCollision(entity) {
            for (let desk of desks) {
                if (entity.x + entity.radius > desk.x &&
                    entity.x - entity.radius < desk.x + desk.w &&
                    entity.y + entity.radius > desk.y &&
                    entity.y - entity.radius < desk.y + desk.h) {
                    return true;
                }
            }
            return false;
        }

        function draw() {
            // Nền phòng
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Lưới sàn
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 1;
            for (let i = 0; i < canvas.width; i += 40) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke();
            }

            // Cửa thoát
            ctx.fillStyle = itemsCollected >= totalItems ? '#10b981' : '#475569';
            ctx.fillRect(exitDoor.x, exitDoor.y, exitDoor.w, exitDoor.h);
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText("EXIT", exitDoor.x + 10, exitDoor.y + 30);

            // Bàn làm việc
            desks.forEach(desk => {
                ctx.fillStyle = '#78350f';
                ctx.fillRect(desk.x, desk.y, desk.w, desk.h);
                ctx.fillStyle = '#92400e';
                ctx.fillRect(desk.x + 5, desk.y + 5, desk.w - 10, desk.h - 10);
            });

            // Vật phẩm
            items.forEach(item => {
                if (!item.collected) {
                    ctx.font = '22px sans-serif';
                    ctx.fillText(item.icon, item.x - 10, item.y + 8);
                }
            });

            // Nhân viên (Player)
            ctx.save();
            let pRadius = player.isCrouching ? player.radius * 0.75 : player.radius;
            ctx.beginPath();
            ctx.arc(player.x, player.y, pRadius, 0, Math.PI * 2);
            ctx.fillStyle = '#3b82f6';
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#ffffff';
            ctx.stroke();
            // Mũ đỏ
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.arc(player.x, player.y - 2, pRadius * 0.6, Math.PI, 0, false);
            ctx.fill();
            ctx.restore();

            // Bà chủ (Boss)
            if (boss.state === 'PATROL') {
                ctx.fillStyle = 'rgba(239, 68, 68, 0.08)';
                ctx.beginPath();
                ctx.arc(boss.x, boss.y, boss.visionRange, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.beginPath();
            ctx.arc(boss.x, boss.y, boss.radius, 0, Math.PI * 2);
            ctx.fillStyle = boss.state === 'CHASE' ? '#991b1b' : '#ec4899';
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#ffffff';
            ctx.stroke();

            // Thắng / Thua
            if (gameState !== 'PLAYING') {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = gameState === 'WIN' ? '#10b981' : '#ef4444';
                ctx.font = 'bold 26px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(gameState === 'WIN' ? '🎉 THẮNG RỒI! TRỐN THÀNH CÔNG!' : '💥 BỊ BÀ CHỦ TÓM GỌN!', canvas.width / 2, canvas.height / 2 - 10);
                ctx.font = '14px sans-serif';
                ctx.fillStyle = '#cbd5e1';
                ctx.fillText("Nhấn F5 để chơi lại", canvas.width / 2, canvas.height / 2 + 25);
                ctx.textAlign = 'left';
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

# Hiển thị game chuẩn với chiều cao vừa khít
components.html(game_html, height=520)











    
