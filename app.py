import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Slay Game - Bà Chủ Nhảy", layout="wide")

# Đoạn mã HTML/JS của game được bọc an toàn trong chuỗi Python
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Slay Game - Bà Chủ Nhảy Né Chướng Ngại Vật</title>
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
            border: 4px solid #ec4899;
            border-radius: 12px;
            background: #1e293b;
        }
        canvas { display: block; background: linear-gradient(to bottom, #1e293b, #0f172a); }
        #ui {
            position: absolute;
            top: 15px; left: 15px; right: 15px;
            display: flex; justify-content: space-between;
            pointer-events: none;
            font-size: 18px; font-weight: bold;
        }
        .badge {
            background: rgba(15, 23, 42, 0.85);
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        #instructions {
            margin-top: 12px;
            font-size: 15px;
            color: #94a3b8;
            text-align: center;
        }
        kbd {
            background: #334155; padding: 3px 8px; border-radius: 4px; color: #fff; font-weight: bold;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="400"></canvas>
        <div id="ui">
            <div class="badge" id="score-text">🏆 Điểm: 0</div>
            <div class="badge" id="high-score-text" style="color: #f59e0b;">⭐ Kỷ lục: 0</div>
        </div>
    </div>
    <div id="instructions">
        Nhấn phím <kbd>Space</kbd> (Dấu cách) hoặc bấm <kbd>Mũi tên lên</kbd> để điều khiển Bà Chủ NHẢY QUA chướng ngại vật!
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let gameState = 'PLAYING';
        let score = 0;
        let highScore = 0;

        let boss = {
            x: 100,
            y: 280,
            radiusX: 25,
            radiusY: 30,
            vy: 0,
            gravity: 0.8,
            jumpForce: -13,
            isGrounded: true
        };

        let obstacles = [];
        let obstacleTimer = 0;
        let gameSpeed = 5;

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' || e.code === 'ArrowUp') {
                e.preventDefault();
                if (boss.isGrounded && gameState === 'PLAYING') {
                    boss.vy = boss.jumpForce;
                    boss.isGrounded = false;
                } else if (gameState === 'GAMEOVER') {
                    resetGame();
                }
            }
        });

        window.addEventListener('click', () => {
            if (boss.isGrounded && gameState === 'PLAYING') {
                boss.vy = boss.jumpForce;
                boss.isGrounded = false;
            } else if (gameState === 'GAMEOVER') {
                resetGame();
            }
        });

        function resetGame() {
            gameState = 'PLAYING';
            score = 0;
            obstacles = [];
            gameSpeed = 5;
            boss.y = 280;
            boss.vy = 0;
            boss.isGrounded = true;
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            boss.vy += boss.gravity;
            boss.y += boss.vy;

            if (boss.y >= 280) {
                boss.y = 280;
                boss.vy = 0;
                boss.isGrounded = true;
            }

            gameSpeed = 5 + Math.floor(score / 10) * 0.5;

            obstacleTimer++;
            if (obstacleTimer > Math.max(50, 100 - score * 2)) {
                obstacles.push({
                    x: canvas.width,
                    y: 285,
                    w: 30,
                    h: 45,
                    type: Math.random() > 0.5 ? 'box' : 'chair'
                });
                obstacleTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;

                let bx = boss.x;
                let by = boss.y - 15;
                let ox = obstacles[i].x + obstacles[i].w / 2;
                let oy = obstacles[i].y + obstacles[i].h / 2;

                let dist = Math.hypot(bx - ox, by - oy);
                if (dist < 32) {
                    gameState = 'GAMEOVER';
                    if (score > highScore) highScore = score;
                }

                if (!obstacles[i].passed && obstacles[i].x < boss.x) {
                    obstacles[i].passed = true;
                    score += 1;
                }

                if (obstacles[i].x < -50) {
                    obstacles.splice(i, 1);
                }
            }

            document.getElementById('score-text').innerText = 🏆 Điểm: ${score};
            document.getElementById('high-score-text').innerText = ⭐ Kỷ lục: ${highScore};
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 315);
            ctx.lineTo(canvas.width, 315);
            ctx.stroke();

            obstacles.forEach(obs => {
                ctx.fillStyle = obs.type === 'box' ? '#b45309' : '#475569';
                ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 1.5;
                ctx.strokeRect(obs.x, obs.y, obs.w, obs.h);
            });

            ctx.save();
            ctx.translate(boss.x, boss.y);

            ctx.fillStyle = '#ec4899';
            ctx.beginPath();
            ctx.ellipse(0, 0, boss.radiusX, boss.radiusY, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.lineWidth = 2.5;
            ctx.strokeStyle = '#fff';
            ctx.stroke();

            ctx.fillStyle = '#451a03';
            ctx.beginPath();
            ctx.arc(0, -25, 16, Math.PI, 0, false);
            ctx.fill();

            ctx.fillStyle = '#f472b6';
            ctx.fillRect(-8, -38, 7, 10);
            ctx.fillRect(2, -38, 7, 10);

            ctx.fillStyle = '#9333ea';
            ctx.fillRect(15, -10, 5, 35);

            ctx.restore();

            if (gameState === 'GAMEOVER') {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#ef4444';
                ctx.font = 'bold 30px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('💥 BÀ CHỦ ĐÃ VẤP NGÃ!', canvas.width / 2, canvas.height / 2 - 20);

                ctx.fillStyle = '#fff';
                ctx.font = '18px sans-serif';
                ctx.fillText(Điểm đạt được: ${score}, canvas.width / 2, canvas.height / 2 + 20);

                ctx.fillStyle = '#10b981';
                ctx.font = '15px sans-serif';
                ctx.fillText('Nhấn phím SPACE hoặc Click để chơi lại', canvas.width / 2, canvas.height / 2 + 55);
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

# Hiển thị game chuẩn xác trên Streamlit
components.html(game_html, height=500)










    
