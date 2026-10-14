<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Office Escape - Slay Game 3D</title>
    <style>
        body {
            margin: 0;
            background: #0b0f19;
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
            box-shadow: 0 15px 35px rgba(0,0,0,0.8);
            border: 4px solid #6366f1;
            border-radius: 12px;
            background: #1e2235;
        }
        canvas {
            display: block;
        }
        #ui {
            position: absolute;
            top: 15px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
        }
        .badge {
            background: rgba(15, 23, 42, 0.85);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        #instructions {
            margin-top: 12px;
            font-size: 15px;
            color: #94a3b8;
            text-align: center;
        }
        kbd {
            background: #334155;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid #475569;
            color: #fff;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="900" height="540"></canvas>
        <div id="ui">
            <div class="badge" id="mission">🎯 Nhiệm vụ: Thu thập 3 tài liệu & Chạy đến Cửa Xanh!</div>
            <div class="badge" id="status" style="color:#ef4444">🏃 Đang chạy</div>
        </div>
    </div>
    <div id="instructions">
        Dùng phím <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> hoặc <kbd>Mũi tên</kbd> để di chuyển | Giữ phím <kbd>Shift</kbd> để NẤP sau bàn làm việc!
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let gameState = 'PLAYING'; // PLAYING, WIN, GAMEOVER
        let itemsCollected = 0;
        let totalItems = 3;

        // Nhân vật chính (Áo xanh, mũ đỏ)
        let player = {
            x: 100,
            y: 270,
            radius: 15,
            speed: 3.5,
            crouchSpeed: 1.5,
            isCrouching: false
        };

        // Bà chủ văn phòng (Váy hồng cầm gậy)
        let boss = {
            x: 780,
            y: 270,
            radius: 20,
            speed: 1.8,
            state: 'PATROL', // PATROL, CHASE
            visionRange: 180,
            target: {x: 700, y: 120}
        };

        // Các bàn làm việc trong phòng (Vật cản và chỗ nấp)
        let desks = [
            {x: 240, y: 100, w: 120, h: 75},
            {x: 240, y: 360, w: 120, h: 75},
            {x: 520, y: 200, w: 130, h: 140}
        ];

        // Vật phẩm cần tìm
        let items = [
            {x: 300, y: 60, collected: false, icon: '📁'},
            {x: 585, y: 370, collected: false, icon: '💼'},
            {x: 820, y: 460, collected: false, icon: '👑'}
        ];

        // Cửa thoát hiểm
        let exitDoor = {x: 830, y: 30, w: 50, h: 65};

        // Xử lý bàn phím
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

            // Va chạm bàn
            player.x += dx;
            if (checkDeskCollision(player)) player.x -= dx;
            player.y += dy;
            if (checkDeskCollision(player)) player.y -= dy;

            // Giới hạn khung hình
            player.x = Math.max(25, Math.min(canvas.width - 25, player.x));
            player.y = Math.max(25, Math.min(canvas.height - 25, player.y));

            // Nhặt vật phẩm
            items.forEach(item => {
                if (!item.collected) {
                    let dist = Math.hypot(player.x - item.x, player.y - item.y);
                    if (dist < 30) {
                        item.collected = true;
                        itemsCollected++;
                        document.getElementById('mission').innerText =🎯 Nhiệm vụ: Đã lấy (${itemsCollected}/${totalItems}) tài liệu`;
                    }
                }
            });

            // Kiểm tra chiến thắng
            if (itemsCollected >= totalItems) {
                let distToExit = Math.hypot(player.x - (exitDoor.x + exitDoor.w/2), player.y - (exitDoor.y + exitDoor.h/2));
                if (distToExit < 40) {
                    gameState = 'WIN';
                }
            }

            // AI Bà chủ (Boss)
            let distToBoss = Math.hypot(boss.x - player.x, boss.y - player.y);
            
            if (distToBoss < boss.visionRange && !player.isCrouching) {
                boss.state = 'CHASE';
            } else if (distToBoss > boss.visionRange * 1.6) {
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
                        x: Math.random() * 400 + 450,
                        y: Math.random() * 400 + 70
                    };
                }
                let angle = Math.atan2(boss.target.y - boss.y, boss.target.x - boss.x);
                boss.x += Math.cos(angle) * (boss.speed * 0.65);
                boss.y += Math.sin(angle) * (boss.speed * 0.65);
            }

            // Cập nhật giao diện trạng thái
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
            // Vẽ nền phòng làm việc
            ctx.fillStyle = '#1e2235';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Vẽ lưới sàn văn phòng
            ctx.strokeStyle = '#282d4a';
            ctx.lineWidth = 1;
            for (let i = 0; i < canvas.width; i += 50) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke();
            }

            // Cửa thoát hiểm (EXIT)
            ctx.fillStyle = itemsCollected >= totalItems ? '#10b981' : '#475569';
            ctx.fillRect(exitDoor.x, exitDoor.y, exitDoor.w, exitDoor.h);
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 14px sans-serif';
            ctx.fillText("EXIT", exitDoor.x + 10, exitDoor.y + 38);

            // Vẽ bàn làm việc
            desks.forEach(desk => {
                ctx.fillStyle = '#78350f';
                ctx.fillRect(desk.x, desk.y, desk.w, desk.h);
                ctx.fillStyle = '#92400e';
                ctx.fillRect(desk.x + 6, desk.y + 6, desk.w - 12, desk.h - 12);
                // Màn hình máy tính trên bàn
                ctx.fillStyle = '#334155';
                ctx.fillRect(desk.x + desk.w/2 - 20, desk.y + 15, 40, 25);
            });

            // Vẽ vật phẩm
            items.forEach(item => {
                if (!item.collected) {
                    ctx.font = '26px sans-serif';
                    ctx.fillText(item.icon, item.x - 12, item.y + 10);
                }
            });

            // Vẽ nhân viên (Player - Áo xanh dương, mũ đỏ)
            ctx.save();
            let pRadius = player.isCrouching ? player.radius * 0.75 : player.radius;
            ctx.beginPath();
            ctx.arc(player.x, player.y, pRadius, 0, Math.PI * 2);
            ctx.fillStyle = '#3b82f6';
            ctx.fill();
            ctx.lineWidth = 2.5;
            ctx.strokeStyle = '#ffffff';
            ctx.stroke();
            // Mũ đỏ
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.arc(player.x, player.y - 3, pRadius * 0.65, Math.PI, 0, false);
            ctx.fill();
            ctx.restore();

            // Vẽ Bà chủ (Boss - Váy hồng)
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
            ctx.lineWidth = 2.5;
            ctx.strokeStyle = '#ffffff';
            ctx.stroke();

            // Màn hình Thắng / Thua
            if (gameState !== 'PLAYING') {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = gameState === 'WIN' ? '#10b981' : '#ef4444';
                ctx.font = 'bold 32px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(gameState === 'WIN' ? '🎉 THẮNG RỒI! BẠN ĐÃ TRỐN THÀNH CÔNG!' : '💥 BỊ BÀ CHỦ TÓM GỌN RỒI!', canvas.width / 2, canvas.height / 2 - 15);
                ctx.font = '16px sans-serif';
                ctx.fillStyle = '#cbd5e1';
                ctx.fillText("Nhấn F5 để chơi lại ván mới", canvas.width / 2, canvas.height / 2 + 30);
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








    
