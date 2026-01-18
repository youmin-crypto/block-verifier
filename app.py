import streamlit as st
import requests
import hashlib

st.set_page_config(page_title="Live Block Verifier", layout="wide")

st.title("🔍 Live Bitcoin Block Verifier")
st.write("Bitcoin Network ပေါ်က အမှန်တကယ်ရှိနေတဲ့ Block တွေကို နည်းပညာကျကျ စစ်ဆေးကြည့်ရအောင်။")

# Blockchain API (Blockchain.info) ကနေ နောက်ဆုံး Block ကို ယူမယ်
def get_latest_block():
    res = requests.get("https://blockchain.info/latestblock")
    return res.json()

def get_block_details(block_hash):
    res = requests.get(f"https://blockchain.info/rawblock/{block_hash}")
    return res.json()

if st.button("နောက်ဆုံးထွက်ထားတဲ့ Block ကို ဆွဲထုတ်မည်"):
    latest = get_latest_block()
    data = get_block_details(latest['hash'])
    
    st.subheader(f"📦 Block Index: {data['block_index']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Block Version", data['ver'])
        st.text_input("Block Hash (Current)", data['hash'], disabled=True)
        st.text_input("Previous Block Hash", data['prev_block'], disabled=True)
    
    with col2:
        st.metric("Timestamp", data['time'])
        st.metric("Nonce", data['nonce'])
        st.metric("Transaction အရေအတွက်", len(data['tx']))

    # Verification Logic
    st.divider()
    st.subheader("🛠️ Block Verification (လက်တွေ့စစ်ဆေးခြင်း)")
    st.write("Block Header ထဲက အချက်အလက်တွေကို ပေါင်းပြီး Hash ပြန်တွက်ရင် အပေါ်က Hash နဲ့ တူရပါမယ်။")
    
    # ရိုးရှင်းအောင် Header အချက်အလက်အချို့ကို ပြထားခြင်း
    header_data = str(data['ver']) + data['prev_block'] + data['mrkl_root'] + str(data['time']) + str(data['bits']) + str(data['nonce'])
    calculated_hash = hashlib.sha256(hashlib.sha256(header_data.encode()).digest()).hexdigest()[::-1] # Double SHA256 (Simplified for demo)

    st.code(f"Calculated Hash: {calculated_hash}")
    
    if st.checkbox("Technical Details ကိုကြည့်မည်"):
        st.json(data)
