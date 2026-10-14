import streamlit as st
import random

st.set_page_config(
    page_title="Tom Gold Run",
    page_icon="🐱",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #b8efff, #fff1cf);
}
h1 {
    color: #ff713b !important;
    text-align: center;
}
h2, h3, p, label {
    color: #24345b;
}
div.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 14px;
    font-size: 17px;
    font-weight: bold;
    border: 2px solid #ffc94f;
    background: #fff3b0;
    color: #29345c;
}
</style>
""", unsafe_allow_html=True)


def create_obstacles():
    lanes = ["", "", ""]
    gold_lane = random.randint(0, 2)
    lanes[gold_lane] = "🪙"

    if random.random() < 0.65:
        obstacle_lane = random.randint(0, 2)
        while obstacle_lane == gold_lane:
            obstacle_lane = random.randint(0, 2)

        lanes[obstacle_lane] = random.choice(["🚆", "🪨"])

    return lanes


def new_game():
    st.session_state.lane = 1
    st.session_state.coins = 0
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.obstacles = create_obstacles()
    st.session_state.playing = True
    st.session_state.message = "Tom đã sẵn sàng! Hãy đi tìm vàng!"












    
