
Python

import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Magazyn Mikołaja", page_icon="🎅")

# --- NAGŁÓWEK Z MIKOŁAJEM ---
# Tworzymy dwie kolumny: lewa na tytuł, prawa na obrazek
col1, col2 = st.columns([3, 1])

with col1:
    st.title("📦 Prosta Aplikacja Magazynowa")

with col2:
    # Link do obrazka Mikołaja (możesz wymienić na własny URL lub plik)
    url_mikolaja = "https://cdn.pixabay.com/photo/2017/11/20/15/51/santa-claus-2965934_1280.png"
    st.image(url_mikolaja, width=150)

# --- LOGIKA MAGAZYNU ---
if 'produkty' not in st.session_state:
    st.session_state.produkty = []

# SEKCJA: DODAWANIE
st.subheader("Dodaj nowy produkt")
nowy_produkt = st.text_input("Nazwa produktu:", placeholder="Np. Prezent dla Grzegorza")

if st.button("Dodaj do magazynu"):
    if nowy_produkt:
        if nowy_produkt not in st.session_state.produkty:
            st.session_state.produkty.append(nowy_produkt)
            st.success(f"Dodano: {nowy_produkt}")
            st.rerun()
        else:
            st.warning("Ten produkt już jest na liście.")
    else:
        st.error("Pole nazwy nie może być puste!")

st.divider()

# SEKCJA: LISTA I USUWANIE
st.subheader("Aktualny stan magazynu")

if not st.session_state.produkty:
    st.info("Magazyn jest pusty.")
else:
    for index, produkt in enumerate(st.session_state.produkty):
        c1, c2 = st.columns([4, 1])
        c1.write(f"🔹 {produkt}")
        if c2.button("Usuń", key=f"del_{index}"):
            st.session_state.produkty.pop(index)
            st.rerun()
