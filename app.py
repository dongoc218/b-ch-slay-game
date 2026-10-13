import streamlit as st

st.set_page_config(page_title="Lén lấy đồ công ty", page_icon="💼")

st.title("💼 Nhiệm vụ: Lén lấy đồ công ty rồi trốn thoát!")
st.write("Đi xung quanh phòng (🚶‍♂️), nhặt đủ 3 món đồ (💻, 📱, ☕) và tránh xa Bà chủ (👩‍🦱)!")

# 1. Khởi tạo trạng thái game
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [0, 0]
if "collected" not in st.session_state:
    st.session_state.collected = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Vị trí cố định của Bà chủ và Đồ đạc
BOSS_POS = (3, 3)
ITEMS = {
    (1, 1): "💻 Laptop",
    (3, 1): "📱 Điện thoại",
    (5, 2): "☕ Cốc cà phê"
}

# 2. Xử lý di chuyển
col_left, col_mid, col_right = st.columns(3)
with col_left:
    if st.button("⬅️ Trái"):
        st.session_state.player_pos[1] = max(0, st.session_state.player_pos[1] - 1)
with col_mid:
    if st.button("⬆️ Lên"):
        st.session_state.player_pos[0] = max(0, st.session_state.player_pos[0] - 1)
    if st.button("⬇️ Xuống"):
        st.session_state.player_pos[0] = min(5, st.session_state.player_pos[0] + 1)
with col_right:
    if st.button("➡️ Phải"):
        st.session_state.player_pos[1] = min(5, st.session_state.player_pos[1] + 1)

px, py = st.session_state.player_pos

# Kiểm tra nhặt đồ hoặc gặp boss
if (px, py) == BOSS_POS:
    st.session_state.game_over = True
elif (px, py) in ITEMS and ITEMS[(px, py)] not in st.session_state.collected:
    st.session_state.collected.append(ITEMS[(px, py)])

# 3. VẼ BẢN ĐỒ CĂN PHÒNG HIỂN THỊ HÌNH ẢNH NHÂN VẬT & BÀ CHỦ
st.markdown("### 🏢 Căn phòng công ty")

if st.session_state.game_over:
    st.error("💥 BẠN ĐÃ BỊ BÀ CHỦ TÓC XOĂN BẮT ĐƯỢC ROÀI!")
    if st.button("🔄 Chơi lại"):
        st.session_state.player_pos = [0, 0]
        st.session_state.collected = []
        st.session_state.game_over = False
        st.rerun()
else:
    # Tạo bản đồ 6x6 dạng ô cờ
    grid_html = "<style>.cell { width: 50px; height: 50px; text-align: center; font-size: 28px; border: 1px solid #ccc; display: inline-block; line-height: 50px; background-color: #f9f9f9; }</style>"
    
    for r in range(6):
        row_str = ""
        for c in range(6):
            if [r, c] == st.session_state.player_pos:
                icon = "🚶‍♂️" # Nhân vật của bạn
            elif (r, c) == BOSS_POS:
                icon = "👩‍🦱" # Bà chủ tóc xoăn
            elif (r, c) in ITEMS and ITEMS[(r, c)] not in st.session_state.collected:
                if ITEMS[(r, c)] == "💻 Laptop": icon = "💻"
                elif ITEMS[(r, c)] == "📱 Điện thoại": icon = "📱"
                else: icon = "☕"
            else:
                icon = "⬜" # Ô trống căn phòng
            
            row_str += f"<div class='cell'>{icon}</div>"
        grid_html += f"<div>{row_str}</div>"
    
    st.markdown(grid_html, unsafe_allow_html=True)

    # Hiển thị tiến trình
    st.write(f"🎒 Đồ đã lấy: {len(st.session_state.collected)}/3 món -> {st.session_state.collected}")

    if len(st.session_state.collected) == 3:
        st.balloons()
        st.success("🎉 BẠN ĐÃ LẤY ĐỦ ĐỒ VÀ TRỐN THOÁT THÀNH CÔNG!")


