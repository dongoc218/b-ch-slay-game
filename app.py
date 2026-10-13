import streamlit as st
import random

st.set_page_config(page_title="Lén lấy đồ công ty Slay", page_icon="💼")

st.title("💼 Nhiệm vụ: Lén lấy đồ công ty rồi trốn thoát!")
st.write("Đi xung quanh phòng, lấy đủ 3 món đồ và tránh bà chủ tóc xoăn cuốn lô hồng!")

# Khởi tạo trạng thái game trong session_state
if "pos" not in st.session_state:
    st.session_state.pos = [0, 0]
if "score" not in st.session_state:
    st.session_state.score = 0
if "collected_items" not in st.session_state:
    st.session_state.collected_items = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Vị trí của Bà chủ tóc xoăn cuốn lô hồng
boss = [3, 3]

# Danh sách các món đồ cần lấy (dùng tên biến tránh xung đột với method items())
game_items = {
    (1, 1): "💻 Laptop công ty",
    (3, 2): "📱 Điện thoại sếp",
    (5, 2): "☕ Cốc cà phê"
}

# Điều khiển di chuyển
st.markdown("### 🕹️ Điều khiển nhân vật")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Trái"):
        st.session_state.pos[1] = max(0, st.session_state.pos[1] - 1)
with col2:
    if st.button("⬆️ Lên"):
        st.session_state.pos[0] = max(0, st.session_state.pos[0] - 1)
    if st.button("⬇️ Xuống"):
        st.session_state.pos[0] = min(5, st.session_state.pos[0] + 1)
with col3:
    if st.button("➡️ Phải"):
        st.session_state.pos[1] = min(5, st.session_state.pos[1] + 1)

pos = tuple(st.session_state.pos)

# Kiểm tra trạng thái va chạm và thu thập
if st.session_state.game_over:
    st.error("💥 Game Over! Bạn đã bị bắt bởi bà chủ tóc xoăn cuốn lô hồng!")
    if st.button("🔄 Chơi lại"):
        st.session_state.pos = [0, 0]
        st.session_state.score = 0
        st.session_state.collected_items = []
        st.session_state.game_over = False
        st.rerun()
else:
    # Kiểm tra nếu gặp boss
    if pos == tuple(boss):
        st.session_state.game_over = True
        st.rerun()
    
    # Kiểm tra nếu nhặt được đồ (dùng biến game_items thay vì items để tránh lỗi method)
    elif pos in game_items and game_items[pos] not in st.session_state.collected_items:
        item_name = game_items[pos]
        st.session_state.collected_items.append(item_name)
        st.session_state.score += 10
        st.success(f"✨ Bạn đã lén lấy thành công: {item_name}!")

    # Hiển thị thông tin trạng thái
    st.info(f"📍 Vị trí hiện tại của bạn: {pos}")
    st.write(f"🏆 Điểm số: {st.session_state.score}")
    st.write(f"🎒 Đồ đã lấy: {st.session_state.collected_items}")

    if len(st.session_state.collected_items) >= 3:
        st.balloons()
        st.success("🎉 Chúc mừng! Bạn đã lấy đủ đồ và trốn thoát thành công khỏi văn phòng!")
