import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dino vs Cactus - Realtime Arcade",
    page_icon="🦖",
    layout="centered",
)

st.title("☀️ DINO VS CACTUS (REALTIME ARCADE)")

# Nhúng Game HTML5 Canvas chạy siêu mượt bằng bàn phím
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background-color: #00bbf9;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
        }
        canvas {
            background-color: #00bbf9;
            border: 4px solid #ffffff;
            border-radius: 10px;
            box-shadow: 0px 6px 0px #0077b6;
        }
        .info {
            margin-top: 10px;
            font-weight: bold;
            font-size: 14px;
            text-shadow: 1px 1px 2px #000;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="200"></canvas>
    <div class="info">
        🎮 CONTROLS: [ ArrowUp / W ] JUMP | [ J / ArrowDown ] CROUCH / LEAN | [ Space ] RESTART
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let highScore = 0;
        let gameOver = false;
        let gameSpeed = 4;

        // Khủng long
        const dino = {
            x: 50,
            y: 130,
            width: 35,
            height: 40,
            dy: 0,
            gravity: 0.6,
            jumpForce: -11,
            isJumping: false,
            isCrouching: false,
            draw() {
                ctx.font = this.isCrouching ? "28px serif" : "34px serif";
                if (this.isJumping) {
                    ctx.fillText("🦘", this.x, this.y);
                } else if (this.isCrouching) {
                    ctx.fillText("🦕", this.x, this.y + 10); // Nghiêng người cúi thấp
                } else {
                    ctx.fillText("🦖", this.x, this.y);
                }
            },
            jump() {
                if (!this.isJumping && !this.isCrouching) {
                    this.dy = this.jumpForce;
                    this.isJumping = true;
                }
            },
            crouch(state) {
                if (!this.isJumping) {
                    this.isCrouching = state;
                }
            },
            update() {
                this.y += this.dy;
                if (this.y + this.dy < 130) {
                    this.dy += this.gravity;
                } else {
                    this.dy = 0;
                    this.isJumping = false;
                    this.y = 130;
                }
                this.draw();
            }
        };

        // Danh sách chướng ngại vật
        let obstacles = [];
        const types = [
            { icon: "🌵", type: "low", width: 25, height: 30, y: 130 },
            { icon: "🌺", type: "low", width: 25, height: 30, y: 130 },
            { icon: "🦇", type: "high", width: 30, height: 25, y: 85 } // Chim bay tầm cao
        ];

        function spawnObstacle() {
            if (gameOver) return;
            const chosen = types[Math.floor(Math.random() * types.length)];
            obstacles.push({
                x: canvas.width,
                y: chosen.y,
                width: chosen.width,
                height: chosen.height,
                icon: chosen.icon,
                type: chosen.type
            });
            
            let nextTime = Math.random() * 1500 + 1000;
            setTimeout(spawnObstacle, nextTime);
        }

        // Bắt sự kiện bàn phím
        window.addEventListener("keydown", (e) => {
            if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
                dino.jump();
            }
            if (e.key === "j" || e.key === "J" || e.key === "ArrowDown" || e.key === "s") {
                dino.crouch(true);
            }
            if (e.key === " " && gameOver) {
                restartGame();
            }
        });

        window.addEventListener("keyup", (e) => {
            if (e.key === "j" || e.key === "J" || e.key === "ArrowDown" || e.key === "s") {
                dino.crouch(false);
            }
        });

        function restartGame() {
            score = 0;
            obstacles = [];
            gameOver = false;
            dino.y = 130;
            dino.dy = 0;
            dino.isJumping = false;
            dino.isCrouching = false;
            loop();
        }

        function loop() {
            if (gameOver) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Mặt đất
            ctx.fillStyle = "#70e000";
            ctx.fillRect(0, 155, canvas.width, 45);
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 155);
            ctx.lineTo(canvas.width, 155);
            ctx.stroke();

            // Cập nhật Khủng long
            dino.update();

            // Cập nhật Chướng ngại vật
            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                obs.x -= gameSpeed;

                ctx.font = "28px serif";
                ctx.fillText(obs.icon, obs.x, obs.y);

                // Va chạm
                let dinoHitY = dino.isCrouching ? dino.y + 15 : dino.y;
                let dinoHitHeight = dino.isCrouching ? 20 : dino.height;

                if (
                    dino.x < obs.x + obs.width &&
                    dino.x + dino.width > obs.x &&
                    dinoHitY < obs.y + obs.height &&
                    dinoHitY + dinoHitHeight > obs.y - 15
                ) {
                    gameOver = true;
                }
            }

            // Xóa chướng ngại vật ra khỏi màn hình
            obstacles = obstacles.filter(obs => obs.x > -50);

            // Điểm số
            score++;
            if (score > highScore) highScore = score;

            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 14px monospace";
            ctx.fillText(`HI: ${Math.floor(highScore)}  SCORE: ${Math.floor(score)}`, 420, 25);

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff4d6d";
                ctx.font = "bold 24px monospace";
                ctx.fillText("GAME OVER!", 230, 90);
                ctx.fillStyle = "#ffffff";
                ctx.font = "14px monospace";
                ctx.fillText("Press SPACE to Restart", 210, 120);
            } else {
                requestAnimationFrame(loop);
            }
        }

        spawnObstacle();
        loop();
    </script>
</body>
</html>
"""

# Render ứng dụng
components.html(game_html, height=280)
