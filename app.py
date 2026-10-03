import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM_NGUYỄN KHÁNH QUỲNH")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# TÍNH LÃI
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")

    else:
        # Lãi suất theo năm chuyển thành dạng thập phân
        lai_suat_nam = lai_suat / 100

        # Tiền lãi toàn bộ kỳ hạn
        tong_tien_lai = (
            so_tien_gui
            * lai_suat_nam
            * ky_han
            / 12
        )

        # =========================
        # TÍNH LÃI ĐỊNH KỲ
        # =========================
        if hinh_thuc == "Cuối kỳ":

            tien_lai_dinh_ky = tong_tien_lai
            so_ky_nhan_lai = 1
            don_vi_ky = "cuối kỳ"

        elif hinh_thuc == "Hàng tháng":

            so_ky_nhan_lai = ky_han
            tien_lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai
            don_vi_ky = "tháng"

        else:  # Hàng quý

            so_ky_nhan_lai = ky_han / 3
            tien_lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai
            don_vi_ky = "quý"

        # Tổng tiền gốc + lãi
        tong_tien_nhan_duoc = so_tien_gui + tong_tien_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================
        st.divider()

        st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi định kỳ",
                dinh_dang_tien(tien_lai_dinh_ky)
            )

        with col2:
            st.metric(
                "💰 Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        st.metric(
            "🏦 Tổng tiền gốc + tiền lãi",
            dinh_dang_tien(tong_tien_nhan_duoc)
        )

        # =========================
        # CHI TIẾT
        # =========================
        st.info(
            f"""
            **Thông tin khoản gửi:**

            - Số tiền gửi: **{dinh_dang_tien(so_tien_gui)}**
            - Kỳ hạn: **{ky_han} tháng**
            - Lãi suất: **{lai_suat:.2f}%/năm**
            - Hình thức nhận lãi: **{hinh_thuc}**
            - Tiền lãi mỗi {don_vi_ky}: **{dinh_dang_tien(tien_lai_dinh_ky)}**
            - Tổng tiền lãi: **{dinh_dang_tien(tong_tien_lai)}**
            - Tổng tiền nhận được: **{dinh_dang_tien(tong_tien_nhan_duoc)}**
            """
        )

        # =========================
        # CÔNG THỨC
        # =========================
        with st.expander("📚 Xem công thức tính"):

            st.write(
                "**Tổng tiền lãi:**"
            )

            st.latex(
                r"\text{Tiền lãi} = "
                r"\text{Tiền gửi} \times "
                r"\frac{\text{Lãi suất năm}}{100} \times "
                r"\frac{\text{Kỳ hạn (tháng)}}{12}"
            )

            st.write(
                "**Tổng tiền nhận được:**"
            )

            st.latex(
                r"\text{Tổng tiền nhận} = "
                r"\text{Tiền gốc} + \text{Tiền lãi}"
            )
