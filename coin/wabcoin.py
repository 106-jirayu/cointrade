import streamlit as st
import requests

st.set_page_config(page_title="อัตราแลกเปลี่ยนเงินตราระหว่างประเทศ", page_icon="💱")

st.title("อัตราแลกเปลี่ยนเงินตราระหว่างประเทศ")
st.write("ดึงข้อมูลอัตราแลกเปลี่ยนแบบ Real-time")

# API Key
API_KEY = "9db5ab62431cea2ed028be23"

# สกุลเงิน
CURRENCIES = ["USD", "THB", "EUR", "JPY", "GBP", "AUD", "CAD", "CNY", "SGD"]

# ฟังก์ชันดึงข้อมูลแบบ Caching (จำค่าไว้ 1 ชั่วโมง = 3600 วินาที)
@st.cache_data(ttl=3600)
def fetch_exchange_rate(api_key, from_curr, to_curr):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_curr}/{to_curr}"
    response = requests.get(url, timeout=5) # ตั้ง timeout ไว้เพื่อไม่ให้ค้างนานเกินไป
    return response.json()

# ส่วนของการคำนวณอัตราแลกเปลี่ยน
st.subheader("คำนวณการแปลงเงิน")

col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("จำนวนเงิน:", min_value=0.0, value=1.0, step=1.0)

with col2:
    from_currency = st.selectbox("จากสกุลเงิน:", CURRENCIES, index=0)

with col3:
    to_currency = st.selectbox("ไปยังสกุลเงิน:", CURRENCIES, index=1)

if st.button("คำนวณอัตราแลกเปลี่ยน", type="primary"):
    try:
        # เรียกใช้ฟังก์ชันผ่าน Cache
        data = fetch_exchange_rate(API_KEY, from_currency, to_currency)
        
        if data.get("result") == "success":
            conversion_rate = data["conversion_rate"]
            conversion_result = amount * conversion_rate
            
            # แสดงผลลัพธ์
            st.success(f"### **{amount:,.2f} {from_currency}** = **{conversion_result:,.2f} {to_currency}**")
            st.info(f"💡 อัตราแลกเปลี่ยนปัจจุบัน: 1 {from_currency} = {conversion_rate:,.4f} {to_currency}")
        else:
            error_type = data.get("error-type", "Unknown error")
            st.error(f"ไม่สามารถดึงข้อมูลได้ (ข้อผิดพลาด: {error_type})")
            
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
