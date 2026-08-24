import json
import os
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Biz Bize Sohbet", page_icon="💬")

st.title("💬 Biz Bize Sohbet")

DB_MESAJ = "mesajlar.json"
DB_GRUP = "gruplar.json"


def veri_yukle(dosya):
  if os.path.exists(dosya):
    try:
      with open(dosya, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []


def veri_kaydet(dosya, veri):
  with open(dosya, "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=4)


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

  # Menü Seçimi
  menu = st.sidebar.selectbox(
      "Menü",
      [
          "Genel Sohbet",
          "Özel Mesaj (DM)",
          "Gruplarım / Grup Kur",
          "Grup Sohbeti",
      ],
  )

  mesajlar = veri_yukle(DB_MESAJ)
  gruplar = veri_yukle(DB_GRUP)

  # 1. GENEL SOHBET
  if menu == "Genel Sohbet":
    st.markdown("### Genel Sohbet (Grup) 🌐")
    aktif_mesajlar = [m for m in mesajlar if m.get("tip", "grup") == "grup"]

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

    with st.form(key="genel_form", clear_on_submit=True):
      yeni_mesaj = st.text_input("Mesajını yaz...")
      gonder = st.form_submit_button("Gönder")
      if gonder and yeni_mesaj.strip():
        zaman_str = datetime.now().strftime("%H:%M")
        mesajlar.append({
            "kullanici": st.session_state.kullanici,
            "mesaj": yeni_mesaj.strip(),
            "tip": "grup",
            "zaman": zaman_str,
        })
        veri_kaydet(DB_MESAJ, mesajlar)
        st.rerun()

  # 2. ÖZEL MESAJ (DM)
  elif menu == "Özel Mesaj (DM)":
    st.markdown("### Özel Mesaj (DM) 🔒")
    hedef_kisi = st.text_input("Mesaj atılacak kişinin adı:")

    if hedef_kisi.strip():
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

      with st.form(key="dm_form", clear_on_submit=True):
        yeni_mesaj = st.text_input("Özel mesajını yaz...")
        gonder = st.form_submit_button("Gönder")
        if gonder and yeni_mesaj.strip():
          zaman_str = datetime.now().strftime("%H:%M")
          mesajlar.append({
              "kullanici": st.session_state.kullanici,
              "alici": hedef_kisi.strip(),
              "mesaj": yeni_mesaj.strip(),
              "tip": "dm",
              "zaman": zaman_str,
          })
          veri_kaydet(DB_MESAJ, mesajlar)
          st.rerun()
    else:
      st.info("Lütfen mesajlaşmak istediğin kişinin adını yukarıya yaz.")

  # 3. GRUPLARIM / GRUP KUR
  elif menu == "Gruplarım / Grup Kur":
    st.markdown("### 👥 Yeni Grup Kur")
    grup_adi = st.text_input("Grup Adı:")
    # Üyeleri virgülle ayırarak yazabilirsiniz (Örn: ahmet, mehmet, ayse)
    uye_input = st.text_input(
        "Grup Üyeleri (Kullanıcı adlarını virgülle ayırın):"
    )

    if st.button("Grup Oluştur"):
      if grup_adi.strip() and uye_input.strip():
        # Grubu kuranı da otomatik üyelere ekleyelim
        uyeler = [u.strip() for u in uye_input.split(",")]
        if st.session_state.kullanici not in uyeler:
          uyeler.append(st.session_state.kullanici)

        # Aynı isimde grup var mı kontrol et
        if any(g["grup_adi"] == grup_adi.strip() for g in gruplar):
          st.warning("Bu isimde bir grup zaten var!")
        else:
          gruplar.append({"grup_adi": grup_adi.strip(), "uyeler": uyeler})
          veri_kaydet(DB_GRUP, gruplar)
          st.success(f"'{grup_adi}' grubu başarıyla oluşturuldu! 🎉")
          st.rerun()
      else:
        st.warning("Lütfen grup adı ve en az bir üye girin.")

    st.markdown("---")
    st.markdown("### 📋 Dahil Olduğun Gruplar")
    kullanici_gruplari = [
        g
        for g in gruplar
        if st.session_state.kullanici in g.get("uyeler", [])
    ]
    if kullanici_gruplari:
      for g in kullanici_gruplari:
        st.write(
            f"🔹 **{g['grup_adi']}** (Üyeler: {', '.join(g['uyeler'])})"
        )
    else:
      st.info("Henüz üyesi olduğun bir grup yok.")

  # 4. GRUP SOHBETİ
  elif menu == "Grup Sohbeti":
    st.markdown("### 💬 Gizli Grup Sohbeti")
    # Sadece kullanıcının üye olduğu grupları listele
    kullanici_gruplari = [
        g
        for g in gruplar
        if st.session_state.kullanici in g.get("uyeler", [])
    ]
    grup_isimleri = [g["grup_adi"] for g in kullanici_gruplari]

    if grup_isimleri:
      secilen_grup = st.selectbox("Sohbet Etmek İstediğin Grubu Seç", grup_isimleri)

      aktif_mesajlar = [
          m
          for m in mesajlar
          if m.get("tip") == "grup_ozel" and m.get("grup") == secilen_grup
      ]

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

      with st.form(key="grup_ozel_form", clear_on_submit=True):
        yeni_mesaj = st.text_input("Gruba mesaj yaz...")
        gonder = st.form_submit_button("Gönder")
        if gonder and yeni_mesaj.strip():
          zaman_str = datetime.now().strftime("%H:%M")
          mesajlar.append({
              "kullanici": st.session_state.kullanici,
              "grup": secilen_grup,
              "mesaj": yeni_mesaj.strip(),
              "tip": "grup_ozel",
              "zaman": zaman_str,
          })
          veri_kaydet(DB_MESAJ, mesajlar)
          st.rerun()
    else:
      st.info(
          "Henüz üyesi olduğun bir grup yok. Sol menüden 'Gruplarım / Grup Kur'"
          " sekmesine giderek grup oluşturabilirsin."
      )
