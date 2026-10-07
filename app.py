import random
import streamlit as st

st.set_page_config(
    page_title="Dino vs Cactus - Arrow & J Keys", page_icon="🦖", layout="centered"
)

# Style Đồ họa Pixel với Bầu trời xanh ngắt
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    .stApp {
        background-color: #00bbf9; /* Bầu trời màu xanh ngắt */
        color: #ffffff;
        font-family: 'Press Start 2P', monospace;
    }
    h1 {
        font-family: 'Press Start 2P', monospace !important;
        color: #ffffff !important;
        text-shadow: 3px 3px 0px #0077b6;
        font-size: 1.5rem !important;
        text-align: center;
        line-height: 1.6;
    }
    .stButton>button {
        background-color: #0077b6;
        color: #ffffff;
        border: 2px solid #ffffff;
        padding: 15px;
        font-family: 'Press Start 2P', monospace;
        font-size: 1rem;
        transition: 0.2s;
        border-radius: 6px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #023e8a;
        color: #00f5d4;
    }
    .game-screen {
        background-color: #70e000; /* Mặt đất xanh tươi */
        border: 4px solid #38b000;
        border-radius: 10px;
        padding: 20px;
        text-align: left;
        margin-bottom: 20px;
        min-height: 180px;
        box-shadow: 0px 8px 0px #0077b6;
    }
    .sky-bg {
        background-color: #00bbf9;
        border-radius: 6px;
        padding: 10px;
        border: 2px dashed #ffffff;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("☀️ DINO VS CACTUS")
st.caption("CONTROLS: UP ARROW (JUMP) | J (CROUCH) | RIGHT ARROW (RUN)")

# Khởi tạo Session State
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "dino_state" not in st.session_state:
    st.session_state.dino_state = "stand"  # "stand", "crouch", "jump"
if "obstacle_dist" not in st.session_state:
    st.session_state.obstacle_dist = 5
if "obstacle_type" not in st.session_state:
    st.session_state.obstacle_type = "🌵"
if "game_over" not in st.session_state:
    st.session_state.game_over = False


def next_turn(action):
    # Cộng điểm
    st.session_state.score += 10
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

    # Chướng ngại vật tiến sang bên trái về phía khủng long
    st.session_state.obstacle_dist -= 1

    # Kiểm tra va chạm (dist = 0)
    if st.session_state.obstacle_dist == 0:
        obs = st.session_state.obstacle_type
        # Nếu là Xương rồng hoặc Hoa độc mà không Nhảy -> GAME OVER
        if obs in ["🌵", "🌺"] and action != "jump":
            st.session_state.game_over = True
        # Nếu là Chim bay mà không Nghiêng người/Cúi (J) -> GAME OVER
        elif obs == "🦇" and action != "crouch":
            st.session_state.game_over = True

    # Tạo chướng ngại vật mới khi đã vượt qua
    if st.session_state.obstacle_dist < 0:
        st.session_state.obstacle_dist = random.randint(4, 6)
        st.session_state.obstacle_type = random.choice(
            ["🌵", "🌵", "🌺", "🌺", "🦇", "🦇"]
        )


# MÀN HÌNH GAME OVER
if st.session_state.game_over:
    st.markdown(
        """
        <div class="game-screen" style="text-align: center; background-color: #ff4d6d;">
            <h2 style="color: #ffffff; font-family: 'Press Start 2P';">💥 GAME OVER 💥</h2>
            <p style="font-size: 2.5rem;">😵 🦖 💀</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.error(
        f"FINAL SCORE: {st.session_state.score} | HIGH SCORE: {st.session_state.high_score}"
    )

    if st.button("🔄 RESTART GAME"):
        st.session_state.score = 0
        st.session_state.obstacle_dist = 5
        st.session_state.game_over = False
        st.session_state.dino_state = "stand"
        st.rerun()

else:
    # HIỂN THỊ ĐIỂM
    st.write(
        f"🏆 **HIGH SCORE:** {st.session_state.high_score:05d}  |  🎮 **SCORE:** {st.session_state.score:05d}"
    )

    # ĐỊNH NGHĨA KHỦNG LONG BÊN TRÁI MÀN HÌNH
    if st.session_state.dino_state == "jump":
        dino_top = "🦘"
        dino_bottom = "&nbsp;"
    elif st.session_state.dino_state == "crouch":
        dino_top = "&nbsp;"
        dino_bottom = "🦕"  # Nghiêng người cúi thấp chân dài
    else:
        dino_top = "&nbsp;"
        dino_bottom = "🦖"

    # HÀNG TRÊN (BẦU TRỜI / CHIM) VÀ HÀNG DƯỚI (MẶT ĐẤT / XƯƠNG RỒNG & HOA ĐỘC)
    top_track = ["&nbsp;"] * 7
    bottom_track = ["_"] * 7

    if 0 <= st.session_state.obstacle_dist < 7:
        if st.session_state.obstacle_type == "🦇":
            top_track[st.session_state.obstacle_dist] = "🦇"
        else:
            bottom_track[st.session_state.obstacle_dist] = (
                st.session_state.obstacle_type
            )

    top_str = " ".join(top_track)
    bottom_str = " ".join(bottom_track)

    # KHUNG BẦU TRỜI XANH NGẮT
    display_html = f"""
    <div class="game-screen">
        <div class="sky-bg">
            <p style="font-size: 1.8rem; margin: 0; padding: 5px 0;">{dino_top} &nbsp;&nbsp;&nbsp; {top_str}</p>
            <p style="font-size: 1.8rem; margin: 0; padding: 5px 0; border-bottom: 4px solid #ffffff;">{dino_bottom} {bottom_str}</p>
        </div>
    </div>
    """

    st.markdown(display_html, unsafe_allow_html=True)

    # GỢI Ý ĐIỀU KHIỂN
    obs = st.session_state.obstacle_type
    if obs == "🌵":
        st.warning("⚠️ CACTUS AHEAD! Press [ ↑ ] to JUMP! 🌵")
    elif obs == "🌺":
        st.error("🚨 POISON FLOWER AHEAD! Press [ ↑ ] to JUMP! 🌺")
    elif obs == "🦇":
        st.info("🦇 BIRD FLYING HIGH! Press [ J ] to LEAN & CROUCH! 🦕")

    # BÀN PHÍM ĐIỀU KHIỂN
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("↑ (JUMP)"):
            st.session_state.dino_state = "jump"
            next_turn("jump")
            st.rerun()

    with col2:
        if st.button("J (LEAN / CROUCH)"):
            st.session_state.dino_state = "crouch"
            next_turn("crouch")
            st.rerun()

    with col3:
        if st.button("→ (RUN)"):
            st.session_state.dino_state = "stand"
            next_turn("run")
            st.rerun()
