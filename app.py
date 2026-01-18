import streamlit as st
import requests
import hashlib
import pandas as pd

st.set_page_config(page_title="Live Verifier Pro", layout="wide")

st.title("🔍 Live Bitcoin Block Verifier")

# Data တွေကို ပျောက်မသွားအောင် သိမ်းထားမယ်
if 'block_data' not in st.session_state:
    st.session_state.block_data = None

if st.button("နောက်ဆုံးထွက်ထားတဲ့ Block ကို ဆွဲထုတ်မည်"):
    latest_hash = requests.get("https://blockchain.info/latestblock").json()['hash']
    st.session_state.block_data = requests.get(f"https://blockchain.info/rawblock/{latest_hash}").json()

if st.session_state.block_data:
    data = st.session_state.block_data
    
    st.success(f"Block Index #{data['block_index']} ကို ရရှိပါပြီ")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Version", data['ver'])
    col2.metric("Nonce", data['nonce'])
    col3.metric("TX Count", len(data['tx']))

    st.text_input("Current Block Hash", data['hash'])
    
    st.divider()
    
    # Details ကြည့်ဖို့ အပိုင်း
    show_details = st.checkbox("Technical Details (JSON) ကိုကြည့်မည်")
    if show_details:
        st.subheader("⚙️ Raw Data Summary")
        # အရေးကြီးတဲ့ အချက်တွေကို ဇယားနဲ့ ပြမယ်
        summary = {
            "Merkle Root": [data['mrkl_root']],
            "Bits (Difficulty)": [data['bits']],
            "Weight": [data['weight']],
            "Size": [data['size']]
        }
        st.table(pd.DataFrame(summary))
        
        with st.expander("Transaction IDs အားလုံးကို ကြည့်ရန်"):
            for tx in data['tx'][:10]: # ပထမ ၁၀ ခုပဲ ပြမယ် (အရမ်းများမှာစိုးလို့)
                st.write(f"🔗 {tx['hash']}")
            st.write(f"... and {len(data['tx'])-10} more transactions.")
            
        st.json(data) # Full JSON data
