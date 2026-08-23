import json
import os
import streamlit as st

st.set_page_config(page_title="Biz Bize Sohbet", page_icon="💬")

st.title("💬 Biz Bize Sohbet")

DB_FILE = "mesajlar.json"


def mesajlari_yukle():
  if os.path.exists(DB_FILE):
    try:
      with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []


def mesajlari_kaydet(mesajlar):
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(mesajlar, f, ensure_ascii=False, indent=4)


# Kullanıcı adı belirleme
if "kullanici" not in st.session_state:
  st.session_state.kullanici = ""

if not st.session_state.kullanici:
  kullanici_adi = st.text_input("Sohbete katılmak için adını yaz:")
  if st.button("Giriş Yap"):
    if kullanici_adi.strip():
      st.session_state.kullanici = kullanici_adi.strip()
      st.rerun()
else:
  st.write(f"Hoş geldin, **{st.session_state.kullanici}**! 🎉")

  # Mesajları yükle
  mesajlar = mesajlari_yukle()

  # Sohbet geçmişini göster
  st.markdown("### Sohbet Odası")
  chat_container = st.container()

  with chat_container:
    for m in mesajlar:
      st.markdown(f"**{m['kullanici']}**: {m['mesaj']}")

  # Yeni mesaj gönderme formu
  with st.form(key="mesaj_formu", clear_on_submit=True):
    yeni_mesaj = st.text_input("Mesajını yaz...")
    gonder = st.form_submit_button("Gönder")

    if gonder and yeni_mesaj.strip():
      mesajlar.append(
          {"kullanici": st.session_state.kullanici, "mesaj": yeni_mesaj.strip()}
      )
      mesajlari_kaydet(mesajlar)
      st.rerun()