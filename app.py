import streamlit as st
import time

st.set_page_config(page_title="Mini WhatsApp", page_icon="💬")
st.title("💬 Kendi Mini WhatsApp'ımız")

# Mesajları saklamak için basit bir liste (Şimdilik bellekte tutuyoruz)
# Not: Tamamen kalıcı olması için ileride buraya bir veritabanı ekleyebiliriz.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kullanıcı adı belirleme (Her gelen kendi adını yazabilsin)
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    st.subheader("Sohbete katılmak için adını gir:")
    name_input = st.text_input("Adın:")
    if st.button("Giriş Yap"):
        if name_input.strip():
            st.session_state.username = name_input.strip()
            st.rerun()
        else:
            st.warning("Lütfen geçerli bir ad gir.")
else:
    st.success(f"Hoş geldin, **{st.session_state.username}**!")
    
    # Sohbet geçmişini ekrana yazdır
    for msg in st.session_state.messages:
        with st.chat_message(msg["user"]):
            st.write(f"**{msg['user']}**: {msg['text']}")

    # Yeni mesaj gönderme kutusu
    if user_msg := st.chat_input("Bir şeyler yaz..."):
        # Mesajı listeye ekle
        st.session_state.messages.append({
            "user": st.session_state.username,
            "text": user_msg
        })
        st.rerun()