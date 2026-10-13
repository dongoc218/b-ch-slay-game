import streamlit as st
import random

st.set_page_config(
    page_title="Bà Chủ Slay",
    page_icon="💗",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff0f6, #fce7f3, #fff7ed);
}
h1, h2, h3, p {
    color: #831843;
}
.gameboard {
    background: #d8b99a;
    border: 5px solid #8b5e3c;
    border-radius: 18px;
    padding: 12px;
    display: grid;
    grid-template-columns: repeat(8, minmax(35px, 1fr));
    gap: 5px;
}
.tile {
    aspect-ratio: 1;
    background: #f8e1c5;
    border: 2px solid #b98b65;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(20px, 3vw, 36px);
}
</style>
""", unsafe_allow_html=True)

st.title("💗 BÀ CHỦ SLAY 💗")
st.subheader("💼 Nhiệm vụ: Lén lấy đồ công ty rồi trốn thoát!")
st.write("Đi quanh văn phòng, lấy đủ 3 món đồ và tránh bà chủ tóc xoăn cuốn lô hồng!")

if "player" not in st.session_state:
    st.session_state.player = [0, 2]
    st.session_state.boss = [7, 2]
    st.session_state.items = {
        (2, 1): "💻",
        (4, 3): "📁",
        (6, 1): "💎"
    }
    st.session_state.collected = []
    st.session_state.hidden = False
    st.session_state.caught = False
    st.session_state.won = False
    st.session_state.message = "🤫 Suỵt! Bà chủ đang ở trong văn phòng!"

def reset_game():
    for key in [
        "player", "boss", "items", "collected",
        "hidden", "caught", "won", "message"
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.player = [0, 2]
    st.session_state.boss = [7, 2]
    st.session_state.items = {
        (2, 1): "💻",
        (4, 3): "📁",
        (6, 1): "💎"
    }
    st.session_state.collected = []
    st.session_state.hidden = False
    st.session_state.caught = False
    st.session_state.won = False
    st.session_state.message = "🤫 Bắt đầu nhiệm vụ!"

def move_player(dx, dy):
    if st.session_state.caught or st.session_state.won:
        return

    p = st.session_state.player
    nx = max(0, min(7, p[0] + dx))
    ny = max(0, min(4, p[1] + dy))
    st.session_state.player = [nx, ny]
    st.session_state.hidden = False

    pos = (nx, ny)
    if pos in st.session_state.items:
        item = st.session_state.items.pop(pos)
        st.session_state.collected.append(item)
        st.session_state.message = f"✨ Bạn đã lấy được {item}!"
    else:
        st.session_state.message = "👀 Đi nhẹ thôi, đừng để bà chủ thấy!"

    if len(st.session_state.collected) == 3 and nx == 7 and ny == 4:
        st.session_state.won = True
        st.session_state.message = "🏆 THẮNG RỒI! Bạn đã lấy đủ đồ và trốn thoát!"

    # Bà chủ di chuyển về phía người chơi
    b = st.session_state.boss
    if random.random() < 0.8:
        if abs(nx - b[0]) > abs(ny - b[1]):
            b[0] += 1 if nx > b[0] else -1 if nx < b[0] else 0
        else:
            b[1] += 1 if ny > b[1] else -1 if ny < b[1] else 0
    st.session_state.boss = [
        max(0, min(7, b[0])),
        max(0, min(4, b[1]))
    ]

    if st.session_state.player == st.session_state.boss:
        st.session_state.caught = True
        st.session_state.message = "😱 BÀ CHỦ SLAY BẮT ĐƯỢC BẠN! Hãy chơi lại!"

def hide_player():
    if st.session_state.caught or st.session_state.won:
        return
    st.session_state.hidden = True
    st.session_state.message = "🫣 Bạn đang núp sau bàn! Bà chủ chưa phát hiện bạn."

st.markdown("### 🏢 Văn phòng công ty")

player = tuple(st.session_state.player)
boss = tuple(st.session_state.boss)
items = st.session_state.items

cells = []
for y in range(5):
    for x in range(8):
        pos = (x, y)
        if pos == player:
            emoji = "🥷"
            if st.session_state.hidden:
                emoji = "🫣"
        elif pos == boss:
            emoji = "👩🏻‍🦱"
        elif pos in items:
            emoji = items[pos]
        elif (x, y) in [(1, 1), (3, 2), (5, 2), (2, 4)]:
            emoji = "🗄️"
        elif (x, y) in [(1, 3), (5, 4)]:
            emoji = "🪴"
        else:
            emoji = "🟫"
        cells.append(f'<div class="tile">{emoji}</div>')

st.markdown(
    '<div class="gameboard">' + "".join(cells) + '</div>',
    unsafe_allow_html=True
)

st.caption("🥷 Bạn  |  👩🏻‍🦱 Bà chủ váy hồng  |  💻📁💎 Đồ cần lấy  |  🗄️ Tủ để núp")

st.markdown("### 🎯 Nhiệm vụ")
st.write(f"Đồ đã lấy: *{len(st.session_state.collected)}/3*")
st.write("Đồ trong ba lô: " + (" ".join(st.session_state.collected) or "Chưa có món nào"))
st.write("📍 Lối thoát nằm ở ô cuối cùng bên phải, hàng dưới cùng.")

st.info(st.session_state.message)

c1, c2, c3 = st.columns(3)
with c2:
    if st.button("⬆️ Đi lên", use_container_width=True):
        move_player(0, -1)
        st.rerun()

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("⬅️ Sang trái", use_container_width=True):
        move_player(-1, 0)
        st.rerun()
with c2:
    if st.button("⬇️ Đi xuống", use_container_width=True):
        move_player(0, 1)
        st.rerun()
with c3:
    if st.button("➡️ Sang phải", use_container_width=True):
        move_player(1, 0)
        st.rerun()

h1, h2 = st.columns(2)
with h1:
    if st.button("🫣 NÚP", use_container_width=True):
        hide_player()
        st.rerun()
with h2:
    if st.button("🔄 Chơi lại", use_container_width=True):
        reset_game()
        st.rerun()

if st.session_state.caught:
    st.error("Bị bắt mất rồi! Nhấn Chơi lại để thử lần nữa.")
elif st.session_state.won:
    st.balloons()
    st.success("BẠN ĐÃ THẮNG! Bà chủ Slay không bắt được bạn!")

