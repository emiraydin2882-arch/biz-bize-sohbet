import json
import os
from datetime import datetime
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
      st.warning("Lütfen geçerli bir ad gir.")
else:
  st.success(f"Hoş geldin, **{st.session_state.kullanici}**! 🎉")

  # Sohbet Modu Seçimi (Genel veya DM)
  sohbet_tipi = st.selectbox(
      "Sohbet Seç", ["Genel Sohbet (Grup)", "Özel Mesaj (DM)"]
  )

  hedef_kisi = ""
  if sohbet_tipi == "Özel Mesaj (DM)":
    hedef_kisi = st.text_input("Mesaj atılacak kişinin adı:")

  # Mesajları yükle
  mesajlar = mesajlari_yukle()

  # Mesajları filtrele
  if sohbet_tipi == "Genel Sohbet (Grup)":
    st.markdown("### Genel Sohbet (Grup) 🌐")
    aktif_mesajlar = [m for m in mesajlar if m.get("tip", "grup") == "grup"]
  else:
    if hedef_kisi.strip():
      st.markdown(f"### Özel Sohbet: {hedef_kisi} 🔒")
      aktif_mesajlar = [
          m
          for m in mesajlar
          if m.get("tip") == "dm"
          and (
              (
                  m["kullanici"] == st.session_state.kullanici
                  and m.get("alici") == hedef_kisi.strip()
              )
              or (
                  m["kullanici"] == hedef_kisi.strip()
                  and m.get("alici") == st.session_state.kullanici
              )
          )
      ]
    else:
      st.info("Lütfen yukarıya mesaj atmak istediğin kişinin adını yaz.")
      aktif_mesajlar = []

  # Sohbet geçmişini göster (Asil Gece Mavisi Kutucuklar)
  chat_container = st.container()
  with chat_container:
    for m in aktif_mesajlar:
      zaman = m.get("zaman", "")
      if m["kullanici"] == st.session_state.kullanici:
        st.markdown(
            f"<div style='background-color: #1b2a4a; color: #e0fbfc; padding:"
            f" 10px; border-radius: 10px; margin-bottom: 8px;'><b>Sen</b>"
            f" <span style='font-size: 0.8em; color: #8d99ae;'>({zaman})</span><br>"
            f" {m['mesaj']}</div>",
            unsafe_allow_html=True,
        )
      else:
        st.markdown(
            f"<div style='background-color: #111827; color: #edf2f4; padding:"
            f" 10px; border-radius: 10px; margin-bottom: 8px;'><b>{m['kullanici']}</b>"
            f" <span style='font-size: 0.8em; color: #8d99ae;'>({zaman})</span><br>"
            f" {m['mesaj']}</div>",
            unsafe_allow_html=True,
        )

  # Yeni mesaj gönderme formu
  with st.form(key="mesaj_formu", clear_on_submit=True):
    yeni_mesaj = st.text_input("Mesajını yaz...")
    gonder = st.form_submit_button("Gönder")

    if gonder and yeni_mesaj.strip():
      zaman_str = datetime.now().strftime("%H:%M")
      if sohbet_tipi == "Genel Sohbet (Grup)":
        yeni_veri = {
            "kullanici": st.session_state.kullanici,
            "mesaj": yeni_mesaj.strip(),
            "tip": "grup",
            "zaman": zaman_str,
        }
        mesajlar.append(yeni_veri)
        mesajlari_kaydet(mesajlar)
        st.rerun()
      else:
        if hedef_kisi.strip():
          yeni_veri = {
              "kullanici": st.session_state.kullanici,
              "alici": hedef_kisi.strip(),
              "mesaj": yeni_mesaj.strip(),
              "tip": "dm",
              "zaman": zaman_str,
          }
          mesajlar.append(yeni_veri)
          mesajlari_kaydet(mesajlar)
          st.rerun()
        else:
          st.warning("Özel mesaj göndermek için bir alıcı adı yazmalısın!")
