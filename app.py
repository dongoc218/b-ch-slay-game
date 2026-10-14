import random
import streamlit as st

st.set_page_config(
    page_title="Bạn Mập Vượt Chướng Ngại",
    page_icon="🏃",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(#dff5ff, #ffffff 65%, #d9f7c8);
}
h1 {
    text-align: center;
    color: #087e8b;
}
div.stButton > button {
    width: 100%;
    min-height: 55px;
    border-radius: 14px;
    font-size: 18px;
    font-weight: bold;
}
.game {
    background: linear-gradient(#bdeaff 0%, #eafaff 65%,
                #a7df83 65%, #6eb34e 100%);
    border: 3px solid white;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
}
.character {
    font-size: 75px;
}
.road {
    background: #c5a17b;
    border-radius: 12px;
    padding: 15px;
    font-size: 40px;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)


def new_game():
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.obstacle = random.choice(
        ["🪨", "📦", "🪵", "🪨"]
    )
    st.session_state.message = "Sẵn sàng! Hãy nhảy qua chướng ngại vật!"
    st.session_state.over = False
    st.session_state.won = False


if "score" not in st.session_state:
    new_game()


def next_obstacle():
    st.session_state.obstacle = random.choice(
        ["🪨", "📦", "🪵", "🌵"]
    )


def jump():
    if st.session_state.over or st.session_state.won:
        return

    st.session_state.score += 1
    st.session_state.message = "Nhảy thành công! +1 điểm 🎉"
    next_obstacle()

    if st.session_state.score >= 10:
        st.session_state.won = True
        st.session_state.message = "Bạn Mập đã về đích! Bạn thắng rồi!"


def run():
    if st.session_state.over or st.session_state.won:
        return

    if random.random() < 0.65:
        st.session_state.lives -= 1
        st.session_state.message = (
            "Ôi! Bạn Mập va vào chướng ngại vật, mất 1 mạng!"
        )

        if st.session_state.lives <= 0:
            st.session_state.over = True
            st.session_state.message = (
                "Hết mạng rồi! Hãy chơi lại nhé."
            )
        else:
            next_obstacle()
    else:
        st.session_state.score += 1
        st.session_state.message = "Chạy qua an toàn! +1 điểm 🎉"
        next_obstacle()

        if st.session_state.score >= 10:
            st.session_state.won = True
            st.session_state.message = (
                "Bạn Mập đã về đích! Bạn thắng rồi!"
            )


st.title("🏃 BẠN MẬP VƯỢT CHƯỚNG NGẠI")
st.markdown(
    "<p style='text-align:center'>"
    "Nhảy thật khéo, tránh chướng ngại vật và về đích!"
    "</p>",
    unsafe_allow_html=True
)

a, b = st.columns(2)
a.metric("⭐ Điểm", st.session_state.score, "Mục tiêu: 10")
b.metric("❤️ Số mạng", st.session_state.lives)

st.markdown(
    f"""
    <div class="game">
        <div style="font-size:30px">☁️　🌤️　☁️</div>
        <div class="character">🧑🏻‍🦱</div>
        <div><b>BẠN MẬP</b></div>
        <div class="road">
            🏃　　{st.session_state.obstacle}　　🏁
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(st.session_state.message)

if st.session_state.over:
    st.error("😵 Bạn Mập hết mạng rồi!")
elif st.session_state.won:
    st.balloons()
    st.success("🏆 CHIẾN THẮNG! Bạn Mập đã về đích!")

left, right = st.columns(2)

with left:
    if st.button(
        "🦘 NHẢY QUA!",
        disabled=st.session_state.over or st.session_state.won
    ):
        jump()
        st.rerun()

with right:
    if st.button(
        "🏃 CHẠY TIẾP",
        disabled=st.session_state.over or st.session_state.won
    ):
        run()
        st.rerun()

if st.button("🔄 CHƠI LẠI"):
    new_game()
    st.rerun()

st.caption(
    "Cách chơi: Bấm NHẢY QUA để vượt chướng ngại vật. "
    "Đạt 10 điểm để chiến thắng. Bạn có 3 mạng."
)










    
