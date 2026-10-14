html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stealth Office Escape</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;600;800&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            overflow: hidden;
            touch-action: none;
        }
        .pixel-font {
            font-family: 'Press Start 2P', monospace;
        }
        canvas {
            display: block;
            image-rendering: pixelated;
        }
    </style>
</head>
<body class="w-screen h-screen flex flex-col justify-between items-center select-none bg-slate-950">

    <header class="w-full max-w-5xl flex justify-between items-center px-4 py-3 bg-slate-900/80 border-b border-slate-800 backdrop-blur-md z-10 shadow-lg">
        <div class="flex items-center space-x-3">
            <div class="w-3 h-3 rounded-full bg-red-500 animate-ping"></div>

    '<h1 class="pixel-font text-xs sm:text-sm text-amber-400 tracking-wider">OFFICE STEALTH 2.5D</h1>',
    unsafe_allow_html=True
        </div>
        <div class="flex items-center space-x-6 text-xs sm:text-sm font-semibold">
            <div class="flex items-center space-x-2 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="text-slate-400">Items:</span>
                <span id="scoreVal" class="text-emerald-400 pixel-font">0/3</span>
            </div>
            <div class="flex items-center space-x-2 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <span class="text-slate-400">Alert:</span>
                <span id="alertVal" class="text-blue-400 pixel-font">STABLE</span>
            </div>
        </div>
    </header>

    <main class="relative flex-1 w-full max-w-5xl flex items-center justify-center p-2">
        <div class="relative rounded-2xl overflow-hidden shadow-2xl border-4 border-slate-800 bg-slate-900 w-full h-full max-h-[750px] flex items-center justify-center">
            <canvas id="gameCanvas" class="w-full h-full object-cover"></canvas>

            <div id="overlay" class="absolute inset-0 bg-slate-950/90 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center z-20">
                <div class="max-w-md w-full bg-slate-900 border border-slate-700 p-8 rounded-3xl shadow-2xl space-y-6">
                    <div class="w-16 h-16 bg-blue-600/20 text-blue-400 rounded-2xl flex items-center justify-center mx-auto border border-blue-500/30 text-2xl font-bold">
                      ''  🕵''
                    </div>
                    <div>
                        <h2 id="overlayTitle" class="pixel-font text-lg sm:text-xl text-white mb-2">STEALTH SURVIVAL</h2>
                        <p id="overlayDesc" class="text-xs sm:text-sm text-slate-400 leading-relaxed">
                            Collect 3 office items (Laptop, Briefcase, Golden Trophy) and sneak to the Exit Door! Avoid the Boss Lady in pink with rollers!
                        </p>
                    </div>
                    <div class="bg-slate-800/60 p-4 rounded-xl text-left text-xs space-y-2 text-slate-300 border border-slate-700/50">
                        <p>💻 <b>Controls:</b> Arrow Keys / WASD or Virtual D-Pad</p>
                        <p>🔴 <b>Stealth:</b> Hide behind desks & plants to lose aggro</p>
                    </div>
                    <button id="startBtn" class="w-full py-4 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 pixel-font text-xs sm:text-sm rounded-xl font-extrabold shadow-lg shadow-amber-500/20 transition-all transform active:scale-95">
                        START MISSION
                    </button>
                </div>
            </div>
        </div>
    </main>

    <footer class="w-full max-w-5xl flex justify-between items-center px-4 py-3 bg-slate-900/80 border-t border-slate-800 backdrop-blur-md z-10">
        <div class="text-[10px] sm:text-xs text-slate-500 hidden sm:block">
            Use WASD / Arrow Keys or On-Screen D-Pad
        </div>
        <div class="flex items-center space-x-2 sm:hidden mx-auto">
            <div class="grid grid-cols-3 gap-1 w-32 h-24">
                <div></div>
                <button id="btnUp" class="bg-slate-800 active:bg-slate-700 border border-slate-700 rounded-lg flex items-center justify-center text-white text-xs">▲</button>
                <div></div>
                <button id="btnLeft" class="bg-slate-800 active:bg-slate-700 border border-slate-700 rounded-lg flex items-center justify-center text-white text-xs">◀</button>
                <button id="btnDown" class="bg-slate-800 active:bg-slate-700 border border-slate-700 rounded-lg flex items-center justify-center text-white text-xs">▼</button>
                <button id="btnRight" class="bg-slate-800 active:bg-slate-700 border border-slate-700 rounded-lg flex items-center justify-center text-white text-xs">▶</button>
            </div>
        </div>
        <div class="text-[10px] sm:text-xs text-slate-400 flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Audio Enabled</span>
        </div>
    </footer>

    <script>
        // --- SOUND ENGINE (Web Audio API) ---
        class SoundEngine {
            constructor() {
                this.ctx = null;
            }
            init() {
                if (!this.ctx) {
                    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
                }
                if (this.ctx.state === 'suspended') {
                    this.ctx.resume();
                }
            }
            playBeep(freq, duration, type = 'sine', gainVal = 0.1) {
                this.init();
                if (!this.ctx) return;
                try {
                    const osc = this.ctx.createOscillator();
                    const gain = this.ctx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
                    gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
                    osc.connect(gain);
                    gain.connect(this.ctx.destination);
                    osc.start();
                    osc.stop(this.ctx.currentTime + duration);
                } catch(e) {}
            }
            playCollect() {
                this.playBeep(523.25, 0.1, 'triangle', 0.15);
                setTimeout(() => this.playBeep(659.25, 0.15, 'triangle', 0.15), 100);
            }
            playAlert() {
                this.playBeep(220, 0.2, 'sawtooth', 0.2);
                setTimeout(() => this.playBeep(180, 0.3, 'sawtooth', 0.2), 150);
            }
            playWin() {
                [440, 554.37, 659.25, 880].forEach((f, i) => {
                    setTimeout(() => this.playBeep(f, 0.2, 'sine', 0.15), i * 120);
                });
            }
            playLose() {
                [300, 250, 200, 150].forEach((f, i) => {
                    setTimeout(() => this.playBeep(f, 0.25, 'sawtooth', 0.2), i * 150);
                });
            }
        }

        const soundFX = new SoundEngine();

        // --- GAME MAP & CONFIG ---
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const MAP_WIDTH = 1200;
        const MAP_HEIGHT = 800;

        canvas.width = MAP_WIDTH;
        canvas.height = MAP_HEIGHT;

        let gameState = 'START'; // START, PLAYING, GAMEOVER, WIN
        let score = 0;
        let alertLevel = 'STABLE'; // STABLE, CAUTION, CHASE
        let alertTimer = 0;

        // Player (Blue Hoodie & Red Hat)
        const player = {
            x: 100,
            y: 100,
            radius: 18,
            speed: 3.5,
            vx: 0,
            vy: 0,
            hidden: false
        };

        // Boss Lady (Pink dress, rollers, stick)
        const boss = {
            x: 1000,
            y: 700,
            radius: 20,
            speed: 2.2,
            patrolTarget: { x: 1000, y: 700 },
            patrolTimer: 0,
            visionRange: 220,
            visionAngle: Math.PI / 2
        };

        // Obstacles / Desks / Cabinets (Collisions & Hiding spots)
        const obstacles = [
            // Desks block movement & provide cover
            { x: 250, y: 150, w: 220, h: 90, type: 'desk' },
            { x: 700, y: 150, w: 220, h: 90, type: 'desk' },
            { x: 250, y: 400, w: 220, h: 90, type: 'desk' },
            { x: 700, y: 400, w: 220, h: 90, type: 'desk' },
            // File cabinets (tall cover)
            { x: 100, y: 150, w: 70, h: 180, type: 'cabinet' },
            { x: 1030, y: 400, w: 70, h: 180, type: 'cabinet' },
            // Plant dividers
            { x: 520, y: 280, w: 160, h: 60, type: 'plant' }
        ];

        // Collectibles (Laptop, Briefcase, Golden Trophy)
        let collectibles = [
            { x: 350, y: 190, r: 14, type: 'laptop', collected: false, name: 'Work Laptop' },
            { x: 800, y: 440, r: 14, type: 'briefcase', collected: false, name: 'Secret Briefcase' },
            { x: 1060, y: 180, r: 16, type: 'trophy', collected: false, name: 'Golden Trophy' }
        ];

        // Exit Door
        const exitDoor = { x: 580, y: 20, w: 80, h: 40, open: false };

        // Particles
        let particles = [];

        // Input Handling
        const keys = { w: false, a: false, s: false, d: false, ArrowUp: false, ArrowLeft: false, ArrowDown: false, ArrowRight: false };

        window.addEventListener('keydown', (e) => {
            if (keys.hasOwnProperty(e.key) || keys.hasOwnProperty(e.code)) {
                keys[e.key] = true;
                keys[e.code] = true;
            }
        });
        window.addEventListener('keyup', (e) => {
            if (keys.hasOwnProperty(e.key) || keys.hasOwnProperty(e.code)) {
                keys[e.key] = false;
                keys[e.code] = false;
            }
        });

        // Touch buttons
        const bindTouch = (id, keyName) => {
            const el = document.getElementById(id);
            if (!el) return;
            el.addEventListener('touchstart', (e) => { e.preventDefault(); keys[keyName] = true; });
            el.addEventListener('touchend', (e) => { e.preventDefault(); keys[keyName] = false; });
        };
        bindTouch('btnUp', 'ArrowUp');
        bindTouch('btnDown', 'ArrowDown');
        bindTouch('btnLeft', 'ArrowLeft');
        bindTouch('btnRight', 'ArrowRight');

        // --- COLLISION UTILS ---
        function checkRectCollision(nx, ny, r, rect) {
            let closestX = Math.max(rect.x, Math.min(nx, rect.x + rect.w));
            let closestY = Math.max(rect.y, Math.min(ny, rect.y + rect.h));
            let distX = nx - closestX;
            let distY = ny - closestY;
            return (distX * distX + distY * distY) < (r * r);
        }

        function resolveCollisions(entity) {
            for (let obs of obstacles) {
                // If entity is behind desk/plant, check if hiding is active
                if (checkRectCollision(entity.x, entity.y, entity.radius, obs)) {
                    // Push out or check cover
                    let cx = obs.x + obs.w / 2;
                    let cy = obs.y + obs.h / 2;
                    // Simple pushback resolution
                    let dx = entity.x - cx;
                    let dy = entity.y - cy;
                    let angle = Math.atan2(dy, dx);
                    entity.x += Math.cos(angle) * 1.5;
                    entity.y += Math.sin(angle) * 1.5;
                }
            }

            // Map boundaries
            entity.x = Math.max(entity.radius + 20, Math.min(MAP_WIDTH - entity.radius - 20, entity.x));
            entity.y = Math.max(entity.radius + 20, Math.min(MAP_HEIGHT - entity.radius - 20, entity.y));
        }

        // --- UPDATE GAME LOGIC ---
        function updateGame() {
            if (gameState !== 'PLAYING') return;

            // Player Movement
            let dx = 0, dy = 0;
            if (keys['w'] || keys['W'] || keys['ArrowUp']) dy -= 1;
            if (keys['s'] || keys['S'] || keys['ArrowDown']) dy += 1;
            if (keys['a'] || keys['A'] || keys['ArrowLeft']) dx -= 1;
            if (keys['d'] || keys['D'] || keys['ArrowRight']) dx += 1;

            if (dx !== 0 && dy !== 0) {
                dx *= 0.7071;
                dy *= 0.7071;
            }

            player.vx = dx * player.speed;
            player.vy = dy * player.speed;
            player.x += player.vx;
            player.y += player.vy;

            resolveCollisions(player);

            // Check Hiding Behind Obstacles (Desks or Plants)
            player.hidden = false;
            for (let obs of obstacles) {
                if (obs.type === 'desk' || obs.type === 'plant') {
                    // If player is directly "above" or behind desk relative to boss or inside bounds
                    if (player.x > obs.x && player.x < obs.x + obs.w && player.y > obs.y - 15 && player.y < obs.y + obs.h + 10) {
                        player.hidden = true;
                        break;
                    }
                }
            }

            // Collectibles Check
            collectibles.forEach(item => {
                if (!item.collected) {
                    let dist = Math.hypot(player.x - item.x, player.y - item.y);
                    if (dist < player.radius + item.r) {
                        item.collected = true;
                        score++;
                        soundFX.playCollect();
                        document.getElementById('scoreVal').innerText = ${score}/3;
                        if (score >= 3) {
                            exitDoor.open = true;
                        }
                    }
                }
            });

            // Exit Check
            if (exitDoor.open) {
                if (player.x > exitDoor.x && player.x < exitDoor.x + exitDoor.w && player.y < exitDoor.y + exitDoor.h + 10) {
                    gameState = 'WIN';
                    soundFX.playWin();
                    showOverlay('MISSION ACCOMPLISHED!', 'You successfully stole the office assets and escaped undetected!', 'PLAY AGAIN');
                }
            }

            // Boss AI & Pathfinding
            let distToPlayer = Math.hypot(boss.x - player.x, boss.y - player.y);
            let canSeePlayer = false;

            if (distToPlayer < boss.visionRange && !player.hidden) {
                // Line of sight check
                canSeePlayer = true;
            }

            if (canSeePlayer) {
                alertLevel = 'CHASE';
                alertTimer = 120; // stay alert for a bit
                let angleToPlayer = Math.atan2(player.y - boss.y, player.x - boss.x);
                boss.x += Math.cos(angleToPlayer) * boss.speed * 1.3;
                boss.y += Math.sin(angleToPlayer) * boss.speed * 1.3;

                if (Math.random() < 0.05) soundFX.playAlert();
            } else {
                if (alertTimer > 0) {
                    alertTimer--;
                    alertLevel = 'CAUTION';
                    // Search towards last player position
                    let angle = Math.atan2(player.y - boss.y, player.x - boss.x);
                    boss.x += Math.cos(angle) * (boss.speed * 0.8);
                    boss.y += Math.sin(angle) * (boss.speed * 0.8);
                } else {
                    alertLevel = 'STABLE';
                    // Patrol around office
                    boss.patrolTimer--;
                    if (boss.patrolTimer <= 0) {
                        boss.patrolTarget = {
                            x: 200 + Math.random() * 800,
                            y: 150 + Math.random() * 500
                        };
                        boss.patrolTimer = 180 + Math.random() * 200;
                    }
                    let pAngle = Math.atan2(boss.patrolTarget.y - boss.y, boss.patrolTarget.x - boss.x);
                    boss.x += Math.cos(pAngle) * boss.speed * 0.6;
                    boss.y += Math.sin(pAngle) * boss.speed * 0.6;
                }
            }

            document.getElementById('alertVal').innerText = alertLevel;
            document.getElementById('alertVal').className = pixel-font ${alertLevel === 'CHASE' ? 'text-red-500 animate-pulse' : alertLevel === 'CAUTION' ? 'text-amber-400' : 'text-emerald-400'};

            // Catch Player check
            if (distToPlayer < player.radius + boss.radius - 5) {
                gameState = 'GAMEOVER';
                soundFX.playLose();
                showOverlay('CAUGHT BY THE BOSS!', 'The Boss Lady caught you slacking and hit you with her wooden stick!', 'TRY AGAIN');
            }

            // Particle updates
            particles.forEach((p, index) => {
                p.x += p.vx;
                p.y += p.vy;
                p.life--;
                if (p.life <= 0) particles.splice(index, 1);
            });
        }

        // --- RENDER GAME GRAPHICS (2.5D Retro-Modern Isometric style) ---
        function drawGame() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Office Floor Tile Pattern
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, 0, MAP_WIDTH, MAP_HEIGHT);

            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 1;
            const tileSize = 50;
            for (let x = 0; x < MAP_WIDTH; x += tileSize) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, MAP_HEIGHT);
                ctx.stroke();
            }
            for (let y = 0; y < MAP_HEIGHT; y += tileSize) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(MAP_WIDTH, y);
                ctx.stroke();
            }

            // 2. Office Exit Door
            ctx.fillStyle = exitDoor.open ? '#10b981' : '#64748b';
            ctx.fillRect(exitDoor.x, exitDoor.y, exitDoor.w, exitDoor.h);
            ctx.fillStyle = '#ffffff';
            ctx.font = '10px "Press Start 2P"';
            ctx.textAlign = 'center';
            ctx.fillText(exitDoor.open ? 'EXIT (OPEN)' : 'EXIT (LOCKED)', exitDoor.x + exitDoor.w/2, exitDoor.y - 8);

            // 3. Collectibles
            collectibles.forEach(item => {
                if (!item.collected) {
                    ctx.save();
                    ctx.shadowColor = '#fbbf24';
                    ctx.shadowBlur = 10;
                    ctx.fillStyle = item.type === 'laptop' ? '#38bdf8' : item.type === 'briefcase' ? '#fb923c' : '#facc15';
                    ctx.beginPath();
                    ctx.arc(item.x, item.y, item.r, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    ctx.restore();

                    // Icon/Emoji inside
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    let icon = item.type === 'laptop' ? '💻' : item.type === 'briefcase' ? '💼' : '🏆';
                    ctx.fillText(icon, item.x, item.y);
                }
            });

            // 4. Obstacles (Desks, Cabinets, Plants with 2.5D depth shadow)
            obstacles.forEach(obs => {
                // Drop shadow
                ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
                ctx.fillRect(obs.x + 8, obs.y + 8, obs.w, obs.h);

                if (obs.type === 'desk') {
                    ctx.fillStyle = '#475569';
                    ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
                    ctx.fillStyle = '#64748b';
                    ctx.fillRect(obs.x + 6, obs.y + 6, obs.w - 12, obs.h - 12);
                    // Desk items mockup
                    ctx.fillStyle = '#cbd5e1';
                    ctx.fillRect(obs.x + 20, obs.y + 20, 25, 18); // monitor
                } else if (obs.type === 'cabinet') {
                    ctx.fillStyle = '#334155';
                    ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
                    ctx.fillStyle = '#475569';
                    ctx.strokeRect(obs.x + 5, obs.y + 5, obs.w - 10, obs.h - 10);
                } else if (obs.type === 'plant') {
                    ctx.fillStyle = '#0f766e';
                    ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
                    ctx.fillStyle = '#14b8a6';
                    ctx.beginPath();
                    ctx.arc(obs.x + obs.w/2, obs.y + obs.h/2, 25, 0, Math.PI * 2);
                    ctx.fill();
                }
            });

            // 5. Player (Blue Hoodie & Red Hat)
            ctx.save();
            if (player.hidden) ctx.globalAlpha = 0.5;

            // Player shadow
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.beginPath();
            ctx.arc(player.x, player.y + 12, player.radius * 0.8, 0, Math.PI * 2);
            ctx.fill();

            // Hoodie Body (Blue)
            ctx.fillStyle = '#2563eb';
            ctx.beginPath();
            ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#1d4ed8';
            ctx.lineWidth = 3;
            ctx.stroke();

            // Red Hat
            ctx.fillStyle = '#dc2626';
            ctx.beginPath();
            ctx.arc(player.x, player.y - 4, player.radius * 0.65, Math.PI, 0, false);
            ctx.fill();

            ctx.restore();

            // 6. Boss Lady (Pink Dress, Hair Rollers, Stick)
            ctx.save();
            // Boss Vision Cone
            if (alertLevel === 'CHASE') {
                ctx.fillStyle = 'rgba(239, 68, 68, 0.2)';
            } else if (alertLevel === 'CAUTION') {
                ctx.fillStyle = 'rgba(245, 158, 11, 0.15)';
            } else {
                ctx.fillStyle = 'rgba(59, 130, 246, 0.1)';
            }
            ctx.beginPath();
            let bAngle = Math.atan2(player.y - boss.y, player.x - boss.x);
            ctx.arc(boss.x, boss.y, boss.visionRange, bAngle - 0.6, bAngle + 0.6);
            ctx.lineTo(boss.x, boss.y);
            ctx.fill();

            // Boss Body (Pink Dress)
            ctx.fillStyle = '#ec4899';
            ctx.beginPath();
            ctx.arc(boss.x, boss.y, boss.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#be185d';
            ctx.lineWidth = 3;
            ctx.stroke();

            // Hair Rollers / Angry Face
            ctx.fillStyle = '#fbcfe8';
            ctx.beginPath();
            ctx.arc(boss.x - 8, boss.y - 8, 6, 0, Math.PI * 2);
            ctx.arc(boss.x + 8, boss.y - 8, 6, 0, Math.PI * 2);
            ctx.fill();

            // Wooden Stick
            ctx.strokeStyle = '#92400e';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(boss.x + 15, boss.y);
            ctx.lineTo(boss.x + 35, boss.y - 15);
            ctx.stroke();

            ctx.restore();
        }

        // --- GAME LOOP ---
        function loop() {
            updateGame();
            drawGame();
            requestAnimationFrame(loop);
        }

        // --- OVERLAY CONTROLS ---
        function showOverlay(title, desc, btnText) {
            document.getElementById('overlayTitle').innerText = title;
            document.getElementById('overlayDesc').innerText = desc;
            document.getElementById('startBtn').innerText = btnText;
            document.getElementById('overlay').classList.remove('hidden');
        }

        function resetGame() {
            score = 0;
            document.getElementById('scoreVal').innerText = '0/3';
            player.x = 100;
            player.y = 100;
            boss.x = 1000;
            boss.y = 700;
            exitDoor.open = false;
            collectibles.forEach(item => item.collected = false);
            gameState = 'PLAYING';
            document.getElementById('overlay').classList.add('hidden');
        }

        document.getElementById('startBtn').addEventListener('click', () => {
            resetGame();
        });

        // Initialize display loop
        requestAnimationFrame(loop);
    </script>
</body>


