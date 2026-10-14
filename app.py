mport random
import streamlit as st

st.set_page_config(
    page_title="Bà Chủ Slay",
    page_icon="🎀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- GIAO DIỆN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #fff0f7 0%, #f7eaff 48%, #eaf4ff 100%);
}
.block-container {max-width: 850px; padding-top: 1.2rem; padding-bottom: 2rem;}
h1 {text-align:center; color:#a21caf; font-weight:900;}
.subtitle {text-align:center; color:#7b3c70; margin-top:-10px;}
div.stButton > button {
    border-radius: 13px; border: 1px solid #e6a8d2;
    background: #fffafd; color: #79265f; font-weight: 750;
    min-height: 2.8rem; width: 100%;
}
div.stButton > button:hover {border-color:#c026d3; color:#a21caf;}
.tile {
    height: 49px; display:flex; align-items:center; justify-content:center;
    border-radius: 10px; margin: 2px; font-size: 25px;
    background: rgba(255,255,255,.88); border: 1px solid #eed3e6;
    box-shadow: 0 2px 5px rgba(112,44,93,.08);
}
.floor {background:rgba(255,255,255,.78);}
.wall {background:#d8c4b1; border-color:#b99f88;}
.item {background:#fff4c7;}
.exit {background:#d9fbe6; border-color:#64c58b;}
.hider {background:#dbeafe; border-color:#93c5fd;}
.small-note {font-size: .9rem; color:#795b76;}
</style>
""", unsafe_allow_html=True)

ROWS, COLS = 8, 9
START_PLAYER = (7, 0)
START_BOSS = (0,8)
EXIT = (0, 0)
WALLS = {
    (1, 1), (1, 2), (1, 6), (1, 7),
    (2, 2), (2, 6), (3, 4), (3, 5),
    (4, 1), (4, 7), (5, 3), (5, 4),
    (6, 6), (6, 7)
}
ITEM_POSITIONS = [(1, 4), (4, 5), (6, 2)]
HIDE_SPOTS = [(2, 4), (5, 7)]  # lockers/desk hiding places

def reset_game():
    st.session_state.player = START_PLAYER
    st.session_state.boss = START_BOSS
    st.session_state.collected = set()
    st.session_state.hidden = False
    st.session_state.won = False
    st.session_state.lost = False
    st.session_state.turn = 0
    st.session_state.message = "Lấy đủ 3 món đồ công ty rồi đến cửa thoát màu xanh. Đừng để bà chủ phát hiện!"
    st.session_state.caught_scene = False

if "player" not in st.session_state:
    reset_game()

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def walkable(pos):
    r, c = pos
    return 0 <= r < ROWS and 0 <= c < COLS and pos not in WALLS

def neighbors(pos):
    r, c = pos
    candidates = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
    return [p for p in candidates if walkable(p)]

def move_boss():
    boss = st.session_state.boss
    player = st.session_state.player
    options = neighbors(boss)
    if not options:
        return
    # If the boss has spotted the player, chase; otherwise patrol.
    if not st.session_state.hidden and distance(boss, player) <= 5:
        options.sort(key=lambda p: distance(p, player))
        best_distance = distance(options[0], player)
        best = [p for p in options if distance(p, player) == best_distance]
        st.session_state.boss = random.choice(best)
    else:
        st.session_state.boss = random.choice(options)

def take_turn(new_pos=None, action="move"):
    if st.session_state.won or st.session_state.lost:
        return

    st.session_state.turn += 1

    if action == "hide":
        if st.session_state.player in HIDE_SPOTS:
            st.session_state.hidden = not st.session_state.hidden
            st.session_state.message = (
                "Bạn núp sau tủ hồ sơ! Chờ bà chủ đi xa rồi hãy chạy."
                if st.session_state.hidden
                else "Bạn đã rời chỗ trốn. Đi nhanh nhé!"
            )
        else:
            st.session_state.message = "Hãy đi đến ô 🗄️ hoặc 🪴 màu xanh để trốn."
    elif action == "move" and new_pos is not None:
        if not walkable(new_pos):
            st.session_state.message = "Bị chặn đường rồi! Thử đi hướng khác."
            st.session_state.turn -= 1
            return
        st.session_state.player = new_pos
        st.session_state.hidden = False

        if new_pos in ITEM_POSITIONS:
            item_index = ITEM_POSITIONS.index(new_pos)
            if item_index not in st.session_state.collected:
                st.session_state.collected.add(item_index)
                st.session_state.message = "Lấy được đồ rồi! Mau tìm món tiếp theo."
            else:
                st.session_state.message = "Chỗ này đã trống. Cẩn thận bà chủ!"

        if new_pos == EXIT:
            if len(st.session_state.collected) == len(ITEM_POSITIONS):
                st.session_state.won = True
                st.session_state.message = "Bạn đã lấy đủ đồ và trốn thoát thành công!"
            else:
                st.session_state.message = "Cửa thoát ở đây, nhưng bạn vẫn cần lấy đủ 3 món đồ!"

    if not st.session_state.won:
        move_boss()
        # Being on the same tile or directly adjacent means the boss catches the player.
        if not st.session_state.hidden and distance(st.session_state.player, st.session_state.boss) <= 1:
            st.session_state.lost = True
            st.session_state.caught_scene = True
            st.session_state.message = "Bà chủ đã tóm được bạn! Hết lượt rồi — thử lại và trốn kỹ hơn nhé."

def render_board():
    collected = st.session_state.collected
    for r in range(ROWS):
        cols = st.columns(COLS, gap="small")
        for c in range(COLS):
            pos = (r, c)
            symbol = " "
            css = "floor"
            if pos == st.session_state.player:
                symbol = "🙈" if st.session_state.hidden else "🧙"
            elif pos == st.session_state.boss:
                symbol = "👩🏻‍💼"
            elif pos == EXIT:
                symbol, css = "🚪", "exit"
            elif pos in WALLS:
                symbol, css = "🪴", "wall"
            elif pos in HIDE_SPOTS:
                symbol, css = "🗄️", "hider"
            elif pos in ITEM_POSITIONS:
                idx = ITEM_POSITIONS.index(pos)
                if idx in collected:
                    symbol = "✨"
                else:
                    symbol, css = ["💼", "📦", "📁"][idx], "item"
            else:
                symbol = "·"
            cols[c].markdown(
                f'<div class="tile {css}">{symbol}</div>',
                unsafe_allow_html=True,
            )

st.title("🎀 BÀ CHỦ SLAY 🎀")
st.markdown('<p class="subtitle">Lén lấy đồ công ty • Né bà chủ • Trốn thoát!</p>', unsafe_allow_html=True)

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Đồ đã lấy", f"{len(st.session_state.collected)}/3")
metric2.metric("Lượt đi", st.session_state.turn)
metric3.metric("Trạng thái", "Đang trốn 🙈" if st.session_state.hidden else ("Bị bắt 😵" if st.session_state.lost else ("Thắng 🏆" if st.session_state.won else "Cẩn thận 👀")))

st.markdown(*Nhiệm vụ:** Tìm 💼, 📦 và 📁 rồi chạy đến 🚪. Bà chủ 👩🏻‍💼 sẽ đuổi theo khi bạn ở gần.")
st.caption("🧙 Bạn  •  👩🏻‍💼 Bà chủ  •  🪴 Chướng ngại vật  •  🗄️ Chỗ trốn  •  🚪 Cửa thoát")
st.markdown("### 🏢 Văn phòng")
render_board()

st.info(st.session_state.message)

if st.session_state.lost:
    st.markdown("""
    <div style="text-align:center; padding:16px; border-radius:14px; background:#ffe4ec; border:1px solid #f9a8c5;">
      <div style="font-size:48px;">😵‍💫 ✨</div>
      <b>Ối! Bà chủ xách bạn lên trong cảnh hoạt hình rồi kết thúc lượt chơi!</b><br>
      <span>Không có cảnh bạo lực chi tiết — bấm “Chơi lại” để thử trốn thoát nhé.</span>
    </div>
    """, unsafe_allow_html=True)
elif st.session_state.won:
    st.balloons()
    st.success("🏆 THẮNG RỒI! Bạn lấy đủ đồ và trốn thoát khỏi văn phòng!")

st.markdown("### 🎮 Điều khiển")
left, up, right = st.columns(3)
with left:
    if st.button("⬅️ Trái", disabled=st.session_state.won or st.session_state.lost):
        r, c = st.session_state.player
        take_turn((r, c-1))
        st.rerun()
with up:
    if st.button("⬆️ Lên", disabled=st.session_state.won or st.session_state.lost):
        r, c = st.session_state.player
        take_turn((r-1, c))
        st.rerun()
with right:
    if st.button("➡️ Phải", disabled=st.session_state.won or st.session_state.lost):
        r, c = st.session_state.player
        take_turn((r, c+1))
        st.rerun()

down, hide, restart = st.columns(3)
with down:
    if st.button("⬇️ Xuống", disabled=st.session_state.won or st.session_state.lost):
        r, c = st.session_state.player
        take_turn((r+1, c))
        st.rerun()
with hide:
    if st.button("🙈 Trốn / Ra", disabled=st.session_state.won or st.session_state.lost):
        take_turn(action="hide")
        st.rerun()
with restart:
    if st.button("🔄 Chơi lại"):
        reset_game()
        st.rerun()

st.markdown("---")
st.markdown('<p class="small-note">Bản thử nghiệm 2D trên Streamlit. Muốn đồ họa 3D thật sự như game mẫu, cần làm thêm bằng một game engine như Godot hoặc Unity.</p>', unsafe_allow_html=True)

