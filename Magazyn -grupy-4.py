import streamlit as st

# 1. Konfiguracja strony (musi być jako pierwsza komenda Streamlit)
st.set_page_config(page_title="Magazyn Grupy 4", page_icon="📦")

# 2. Nagłówek z Mikołajem w prawym górnym rogu
col1, col2 = st.columns([3, 1])

with col1:
    st.title("📦 Magazyn Grupy 4")

with col2:
    # Używamy stabilnego linku do grafiki Mikołaja
    st.image("https://cdn.pixabay.com/photo/2017/11/20/15/51/santa-claus-2965934_1280.png", width=120)

# 3. Inicjalizacja listy produktów (pamięć podręczna)
if 'produkty' not in st.session_state:
    st.session_state.produkty = []

# 4. Formularz dodawania produktów
st.subheader("Dodaj nowy produkt")
with st.form(key="dodaj_produkt", clear_on_submit=True):
    nowy_produkt = st.text_input("Nazwa produktu:")
    submit_button = st.form_submit_button(label="Dodaj do bazy")

if submit_button and nowy_produkt:
    if nowy_produkt not in st.session_state.produkty:
        st.session_state.produkty.append(nowy_produkt)
        st.success(f"Dodano: {nowy_produkt}")
        st.rerun()
    else:
        st.warning("Ten produkt już jest na liście.")

st.divider()

# 5. Wyświetlanie listy i usuwanie
st.subheader("Aktualny stan magazynu")

if not st.session_state.produkty:
    st.info("Brak produktów w magazynie.")
else:
    for index, produkt in enumerate(st.session_state.produkty):
        c1, c2 = st.columns([4, 1])
        c1.write(f"🔹 **{produkt}**")
        if c2.button("Usuń", key=f"btn_{index}"):
            st.session_state.produkty.pop(index)
            st.rerun()
