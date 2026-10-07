import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dino Pixel Arcade 8-Bit", page_icon="🦖", layout="centered"
)

st.title("🦖 DINO 8-BIT PIXEL RETRO")

# Game Canvas HTML5 / JS - Đồ họa Pixel 8-Bit
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        body {
            margin: 0;
            background-color: #00bbf9;
            font-family: 'Press Start 2P', cursive;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
            user-select: none;
        }
        canvas {
            background-color: #4eb5e5;
            border: 4px solid #ffffff;
            border-radius: 8px;
            box-shadow: 0px 6px 0px #0077b6;
            image-rendering: pixelated; /* Khử nhòe để nét chuẩn Pixel 8-bit */
            image-rendering: crisp-edges;
        }
        .info {
            margin-top: 12px;
            font-size: 10px;
            text-shadow: 2px 2px 0px #000;
            letter-spacing: 1px;
            text-align: center;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="200"></canvas>
    <div class="info">
        🎮 CONTROLS:<br>
        [ ↑ / W ] JUMP | [ J / ↓ ] CROUCH & LEAN | [ SPACE ] RESTART
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        ctx.imageSmoothingEnabled = false; // Bật render pixel sắc nét

        let score = 0;
        let highScore = 0;
        let gameOver = false;
        let gameSpeed = 5;
        let frameCount = 0;

        // --- VẼ ĐỒ HỌA PIXEL ART BẰNG CANVAS (8-BIT SPRITES) ---
        
        // 1. Pixel Dino (Đứng / Chạy)
        function drawPixelDinoRun(x, y, frame) {
            ctx.fillStyle = "#535353";
            // Đầu & Thân
            ctx.fillRect(x + 12, y, 16, 12);
            ctx.fillRect(x + 20, y + 4, 12, 4);
            ctx.fillRect(x + 8, y + 12, 16, 16);
            ctx.fillRect(x, y + 16, 8, 8); // Đuôi
            // Mắt Pixel
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(x + 16, y + 4, 4, 4);

            // Chân (Chạy đổi chân)
            ctx.fillStyle = "#535353";
            if (frame % 10 < 5) {
                ctx.fillRect(x + 8, y + 28, 4, 8);
                ctx.fillRect(x + 18, y + 28, 4, 4);
            } else {
                ctx.fillRect(x + 8, y + 28, 4, 4);
                ctx.fillRect(x + 18, y + 28, 4, 8);
            }
        }

        // 2. Pixel Dino Cúi Thấp / Nghiêng Người / Chân Dài (Cúi Núp Chim)
        function drawPixelDinoCrouch(x, y, frame) {
            ctx.fillStyle = "#535353";
            // Thân dài nghiêng ngang
            ctx.fillRect(x, y + 16, 28, 10);
            ctx.fillRect(x + 24, y + 12, 12, 10); // Đầu hạ thấp
            ctx.fillRect(x - 6, y + 14, 8, 6);   // Đuôi duỗi
            // Mắt
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(x + 30, y + 14, 3, 3);

            // Chân duỗi dài bò trườn
            ctx.fillStyle = "#535353";
            if (frame % 8 < 4) {
                ctx.fillRect(x + 2, y + 26, 8, 4);
                ctx.fillRect(x + 18, y + 26, 10, 4);
            } else {
                ctx.fillRect(x + 4, y + 26, 10, 4);
                ctx.fillRect(x + 20, y + 26, 6, 4);
            }
        }

        // 3. Pixel Dino Nhảy
        function drawPixelDinoJump(x, y) {
            ctx.fillStyle = "#535353";
            ctx.fillRect(x + 12, y, 16, 12);
            ctx.fillRect(x + 20, y + 4, 12, 4);
            ctx.fillRect(x + 8, y + 12, 16, 16);
            ctx.fillRect(x, y + 16, 8, 8);
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(x + 16, y + 4, 4, 4);

            // Chân co lên
            ctx.fillStyle = "#535353";
            ctx.fillRect(x + 8, y + 28, 6, 4);
            ctx.fillRect(x + 16, y + 28, 6, 4);
        }

        // 4. Pixel Cactus (Xương Rồng)
        function drawPixelCactus(x, y) {
            ctx.fillStyle = "#2d6a4f";
            ctx.fillRect(x + 8, y, 8, 32);
            ctx.fillRect(x, y + 8, 8, 12);
            ctx.fillRect(x, y + 8, 16, 4);
            ctx.fillRect(x + 16, y + 12, 8, 12);
            ctx.fillRect(x + 8, y + 12, 16, 4);
        }

        // 5. Pixel Poison Flower (Hoa Độc 8-bit)
        function drawPixelFlower(x, y) {
            // Thân gai
            ctx.fillStyle = "#1b4332";
            ctx.fillRect(x + 10, y + 14, 4, 18);
            ctx.fillRect(x + 6, y + 18, 4, 4);
            // Cánh hoa tím/đỏ độc
            ctx.fillStyle = "#d90429";
            ctx.fillRect(x + 4, y + 2, 16, 14);
            ctx.fillStyle = "#7209b7";
            ctx.fillRect(x, y + 6, 24, 6);
            // Nhụy hoa
            ctx.fillStyle = "#ffb703";
            ctx.fillRect(x + 8, y + 6, 8, 6);
        }

        // 6. Pixel Bird (Chim Pterodactyl Bay)
        function drawPixelBird(x, y, frame) {
            ctx.fillStyle = "#222222";
            ctx.fillRect(x + 8, y + 6, 16, 8); // Thân
            ctx.fillRect(x, y + 8, 8, 4);   // Mỏ

            // Cánh đập lên xuống
            if (frame % 12 < 6) {
                ctx.fillRect(x + 10, y - 6, 6, 12); // Cánh giơ lên
            } else {
                ctx.fillRect(x + 10, y + 12, 6, 12); // Cánh xòe xuống
            }
        }

        // --- KHỞI TẠO ĐỐI TƯỢNG ---
        const dino = {
            x: 50,
            y: 120,
            width: 28,
            height: 36,
            dy: 0,
            gravity: 0.7,
            jumpForce: -12,
            isJumping: false,
            isCrouching: false,
            update() {
                this.y += this.dy;
                if (this.y + this.dy < 120) {
                    this.dy += this.gravity;
                } else {
                    this.dy = 0;
                    this.isJumping = false;
                    this.y = 120;
                }

                // Vẽ Dino
                if (this.isJumping) {
                    drawPixelDinoJump(this.x, this.y);
                } else if (this.isCrouching) {
                    drawPixelDinoCrouch(this.x, this.y + 6, frameCount);
                } else {
                    drawPixelDinoRun(this.x, this.y, frameCount);
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
            }
        };

        let obstacles = [];
        function spawnObstacle() {
            if (gameOver) return;
            const rand = Math.random();
            if (rand < 0.4) {
                obstacles.push({ x: canvas.width, y: 124, width: 24, height: 32, type: "cactus" });
            } else if (rand < 0.7) {
                obstacles.push({ x: canvas.width, y: 124, width: 24, height: 32, type: "flower" });
            } else {
                obstacles.push({ x: canvas.width, y: 80, width: 24, height: 20, type: "bird" });
            }
            
            let nextTime = Math.random() * 1200 + 900;
            setTimeout(spawnObstacle, nextTime);
        }

        // BÀN PHÍM
        window.addEventListener("keydown", (e) => {
            if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") dino.jump();
            if (e.key === "j" || e.key === "J" || e.key === "ArrowDown" || e.key === "s") dino.crouch(true);
            if (e.key === " " && gameOver) restartGame();
        });

        window.addEventListener("keyup", (e) => {
            if (e.key === "j" || e.key === "J" || e.key === "ArrowDown" || e.key === "s") dino.crouch(false);
        });

        function restartGame() {
            score = 0;
            obstacles = [];
            gameOver = false;
            dino.y = 120;
            dino.dy = 0;
            dino.isJumping = false;
            dino.isCrouching = false;
            loop();
        }

        // GAME LOOP
        function loop() {
            if (gameOver) return;
            frameCount++;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Bầu trời & Mây Pixel
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(100 - (frameCount % 600), 30, 32, 10);
            ctx.fillRect(350 - (frameCount % 600), 45, 40, 12);

            // Mặt đất Pixel
            ctx.fillStyle = "#55a
