@st.cache_data
def load_data():
    xls = pd.ExcelFile("data.xlsx")
    all_data = []

    # ชื่อคอลัมน์มาตรฐาน
    col_map = {
        "ชื่อผู้ใช้ไฟฟ้า": "ชื่อผู้ใช้ไฟฟ้า",
        "ชื่อผู้ใช้ไฟฟ้า ": "ชื่อผู้ใช้ไฟฟ้า",
        "ชื่อ": "ชื่อผู้ใช้ไฟฟ้า",

        "เลขที่คำขอ": "เลขที่คำขอ",

        "หมายเลข CA": "หมายเลข CA",
        "CA": "หมายเลข CA",

        "กำลังการผลิต": "กำลังการผลิต",
        "กำลังการผลิต (kW)": "กำลังการผลิต",

        "สถานะคำขอ": "สถานะคำขอ",
        "สถานะ": "สถานะคำขอ",

        "พื้นที่ กฟฟ.": "พื้นที่ กฟฟ.",
        "พื้นที่": "พื้นที่ กฟฟ."
    }

    required_cols = list(set(col_map.values()))

    for sheet in xls.sheet_names:
        raw = pd.read_excel(xls, sheet_name=sheet, header=None)

        # หาแถวที่มีคำว่า "ชื่อผู้ใช้ไฟฟ้า" → ถือว่าเป็น header
        header_row = None
        for i in range(5):  # ตรวจแค่ 5 แถวแรก
            if raw.iloc[i].astype(str).str.contains("ชื่อ").any():
                header_row = i
                break

        if header_row is None:
            continue

        df = pd.read_excel(
            xls,
            sheet_name=sheet,
            header=header_row
        )

        # ล้างชื่อคอลัมน์
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace("\n", "", regex=False)
        )

        # map ชื่อคอลัมน์
        df = df.rename(columns=col_map)

        # เช็กว่ามีคอลัมน์ที่ต้องใช้ไหม
        if not all(col in df.columns for col in required_cols):
            continue

        df = df[required_cols]
        df["ชีท"] = sheet  # ไว้ดูว่ามาจากชีทไหน
        all_data.append(df)

    if not all_data:
        return pd.DataFrame(columns=required_cols)

    return pd.concat(all_data, ignore_index=True)
