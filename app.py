```python
import streamlit as st
st.image("logo.jpg")
# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================================================
# DỮ LIỆU LÃI SUẤT
# Đơn vị: %/năm
# Đây là dữ liệu mẫu - có thể thay đổi khi ngân hàng cập nhật
# =========================================================

LAI_SUAT_NGAN_HANG = {
    "Vietcombank": {
        1: 1.60,
        3: 1.90,
        6: 2.90,
        12: 4.60,
        24: 4.70
    },

    "BIDV": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.70,
        24: 4.70
    },

    "VietinBank": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.70,
        24: 4.80
    },

    "Agribank": {
        1: 1.60,
        3: 1.90,
        6: 3.00,
        12: 4.70,
        24: 4.70
    },

    "ACB": {
        1: 2.30,
        3: 2.70,
        6: 3.50,
        12: 4.40,
        24: 4.50
    },

    "Sacombank": {
        1: 2.80,
        3: 3.20,
        6: 4.20,
        12: 4.90,
        24: 5.00
    }
}

# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")

st.write(
    "Chọn ngân hàng và kỳ hạn để hệ thống tự động lấy lãi suất "
    "và tính số tiền lãi bạn nhận được."
)

st.divider()

# =========================================================
# CHỌN NGÂN HÀNG
# =========================================================

st.subheader("🏦 Thông tin khoản gửi")

ngan_hang = st.selectbox(
    "Chọn ngân hàng",
    list(LAI_SUAT_NGAN_HANG.keys())
)

# =========================================================
# NHẬP SỐ TIỀN
# =========================================================

so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=100_000.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

# =========================================================
# CHỌN KỲ HẠN
# =========================================================

cac_ky_han = list(LAI_SUAT_NGAN_HANG[ngan_hang].keys())

ky_han = st.selectbox(
    "📅 Kỳ hạn",
    cac_ky_han,
    format_func=lambda x: f"{x} tháng"
)

# =========================================================
# TỰ ĐỘNG LẤY LÃI SUẤT
# =========================================================

lai_suat = LAI_SUAT_NGAN_HANG[ngan_hang][ky_han]

st.info(
    f"📈 Lãi suất hiện được sử dụng: "
    f"**{lai_suat:.2f}%/năm**"
)

# =========================================================
# HÌNH THỨC NHẬN LÃI
# =========================================================

hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================================================
# NÚT TÍNH LÃI
# =========================================================

if st.button(
    "🧮 TÍNH LÃI",
    use_container_width=True
):

    # -----------------------------------------------------
    # KIỂM TRA SỐ TIỀN
    # -----------------------------------------------------

    if so_tien_gui <= 0:

        st.error(
            "❌ Số tiền gửi phải lớn hơn 0."
        )

    else:

        # -------------------------------------------------
        # CHUYỂN LÃI SUẤT % SANG SỐ THẬP PHÂN
        # -------------------------------------------------

        lai_suat_nam = lai_suat / 100

        # -------------------------------------------------
        # TÍNH TỔNG TIỀN LÃI
        #
        # Tiền lãi =
        # Tiền gửi × Lãi suất năm × Kỳ hạn / 12
        # -------------------------------------------------

        tong_tien_lai = (
            so_tien_gui
            * lai_suat_nam
            * ky_han
            / 12
        )

        # -------------------------------------------------
        # TÍNH TIỀN LÃI ĐỊNH KỲ
        # -------------------------------------------------

        if hinh_thuc == "Cuối kỳ":

            tien_lai_dinh_ky = tong_tien_lai
            ten_dinh_ky = "cuối kỳ"

        elif hinh_thuc == "Hàng tháng":

            tien_lai_dinh_ky = (
                tong_tien_lai / ky_han
            )

            ten_dinh_ky = "mỗi tháng"

        else:

            # Hàng quý
            so_quy = ky_han / 3

            tien_lai_dinh_ky = (
                tong_tien_lai / so_quy
            )

            ten_dinh_ky = "mỗi quý"

        # -------------------------------------------------
        # TỔNG TIỀN NHẬN ĐƯỢC
        # -------------------------------------------------

        tong_tien_nhan = (
            so_tien_gui + tong_tien_lai
        )

        # =================================================
        # HIỂN THỊ KẾT QUẢ
        # =================================================

        st.divider()

        st.subheader("📊 KẾT QUẢ")

        # -------------------------------------------------
        # HIỂN THỊ 3 KẾT QUẢ CHÍNH
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💵 Lãi định kỳ",
                dinh_dang_tien(tien_lai_dinh_ky)
            )

        with col2:

            st.metric(
                "💰 Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        with col3:

            st.metric(
                "🏦 Tổng nhận được",
                dinh_dang_tien(tong_tien_nhan)
            )

        # =================================================
        # CHI TIẾT KHOẢN GỬI
        # =================================================

        st.subheader("📋 Chi tiết khoản gửi")

        st.write(
            f"""
            **Ngân hàng:** {ngan_hang}

            **Số tiền gửi:** {dinh_dang_tien(so_tien_gui)}

            **Kỳ hạn:** {ky_han} tháng

            **Lãi suất:** {lai_suat:.2f}%/năm

            **Hình thức nhận lãi:** {hinh_thuc}

            **Tiền lãi {ten_dinh_ky}:**
            {dinh_dang_tien(tien_lai_dinh_ky)}

            **Tổng tiền lãi:**
            {dinh_dang_tien(tong_tien_lai)}

            **Tổng tiền gốc + tiền lãi:**
            {dinh_dang_tien(tong_tien_nhan)}
            """
        )

        # =================================================
        # CÔNG THỨC
        # =================================================

        with st.expander("📚 Xem công thức tính"):

            st.write("### Tổng tiền lãi")

            st.latex(
                r"""
                Tiền\ lãi =
                Tiền\ gửi
                \times
                \frac{Lãi\ suất}{100}
                \times
                \frac{Kỳ\ hạn}{12}
                """
            )

            st.write("### Tổng tiền nhận được")

            st.latex(
                r"""
                Tổng\ tiền\ nhận =
                Tiền\ gốc + Tiền\ lãi
                """
            )

            st.write(
                "Lưu ý: App đang tính theo phương pháp lãi đơn "
                "trên số tiền gốc, chưa tính trường hợp tái tục "
                "hoặc nhập lãi vào vốn."
            )

# =========================================================
# BẢNG LÃI SUẤT
# =========================================================

st.divider()

st.subheader("📈 Bảng lãi suất tham khảo")

st.write(
    "Bảng dưới đây giúp người dùng dễ dàng so sánh "
    "lãi suất giữa các ngân hàng."
)

# Tạo bảng dữ liệu

du_lieu_bang = []

for ten_ngan_hang, cac_muc_lai in LAI_SUAT_NGAN_HANG.items():

    dong = {
        "Ngân hàng": ten_ngan_hang,
        "1 tháng": f"{cac_muc_lai.get(1, '-')}%",
        "3 tháng": f"{cac_muc_lai.get(3, '-')}%",
        "6 tháng": f"{cac_muc_lai.get(6, '-')}%",
        "12 tháng": f"{cac_muc_lai.get(12, '-')}%",
        "24 tháng": f"{cac_muc_lai.get(24, '-')}%"
    }

    du_lieu_bang.append(dong)

st.dataframe(
    du_lieu_bang,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "⚠️ Lãi suất trong bảng là dữ liệu tham khảo. "
    "Lãi suất thực tế có thể thay đổi theo từng thời điểm, "
    "kênh gửi và chính sách của từng ngân hàng."
)
```
