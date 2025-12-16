import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Prosty Magazyn", page_icon="📦")

st.title("📦 Prosta Aplikacja Magazynowa")

# Inicjalizacja listy produktów w sesji (jeśli jeszcze nie istnieje)
if 'produkty' not in st.session_state:
    st.session_state.produkty = []

# --- SEKCJA: DODAWANIE ---
st.subheader("Dodaj nowy produkt")
nowy_produkt = st.text_input("Nazwa produktu:", placeholder="Np. Śrubki M8")

if st.button("Dodaj do magazynu"):
    if nowy_produkt:
        if nowy_produkt not in st.session_state.produkty:
            st.session_state.produkty.append(nowy_produkt)
            st.success(f"Dodano: {nowy_produkt}")
        else:
            st.warning("Ten produkt już jest na liście.")
    else:
        st.error("Pole nazwy nie może być puste!")

st.divider()

# --- SEKCJA: LISTA I USUWANIE ---
st.subheader("Aktualny stan magazynu")

if not st.session_state.produkty:
    st.info("Magazyn jest pusty.")
else:
    # Wyświetlanie listy z przyciskiem usuwania obok każdego przedmiotu
    for index, produkt in enumerate(st.session_state.produkty):
        cols = st.columns([3, 1])
        cols[0].write(f"🔹 {produkt}")
        
        # Unikalny klucz dla każdego przycisku usuwania
        if cols[1].button("Usuń", key=f"del_{index}"):
            st.session_state.produkty.pop(index)
            st.rerun() # Odświeżenie aplikacji po usunięciu
