import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ค้นหา จาก PPIM",
    layout="wide"
)

st.title("🔍 ค้นหาข้อมูล จาก PPIM")
st.write("ค้นหาจากชื่อผู้ใช้ไฟฟ้า (รวมข้อมูลจากทุกชีท)")

@st.cache_data
def load_data():
    xls = pd.ExcelFile("data.xlsx")
    all_sheets = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        all_sheets.append(df)

    return pd.concat(all_sheets, ignore_index=True)

try:
    df = load_data()

    search = st.text_input("พิมพ์ชื่อผู้ใช้ไฟฟ้าที่ต้องการค้นหา")

    if search:
        result = df[
            df["ชื่อผู้ใช้ไฟฟ้า"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

        st.write(f"พบข้อมูล {len(result)} รายการ")

        st.dataframe(
            result[[
                "ชื่อผู้ใช้ไฟฟ้า",
                "เลขที่คำขอ",
                "หมายเลข CA",
                "กำลังการผลิต (kW)",
                "สถานะคำขอ",
                "พื้นที่ กฟฟ."
            ]],
            use_container_width=True
        )
    else:
        st.info("กรุณาพิมพ์ชื่อผู้ใช้ไฟฟ้าเพื่อค้นหา")

except Exception as e:
    st.error("❌ ไม่สามารถอ่านข้อมูลจากไฟล์ Excel ได้")
    st.exception(e)

