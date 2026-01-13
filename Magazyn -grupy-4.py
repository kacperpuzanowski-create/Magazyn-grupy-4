import streamlit as st
from supabase import create_client, Client

# Konfiguracja połączenia z Supabase
# Dane pobierane są z "Secrets" w Streamlit dla bezpieczeństwa
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📦 Zarządzanie Magazynem")

# --- SEKCJA KATEGORIE ---
st.header("📂 Kategorie")

with st.form("dodaj_kategorie"):
    nazwa_kat = st.text_input("Nazwa kategorii")
    opis_kat = st.text_area("Opis")
    submit_kat = st.form_submit_button("Dodaj kategorię")
    
    if submit_kat and nazwa_kat:
        data = {"nazwa": nazwa_kat, "opis": opis_kat}
        supabase.table("Kategorie").insert(data).execute()
        st.success(f"Dodano kategorię: {nazwa_kat}")

# Wyświetlanie i usuwanie kategorii
kat_data = supabase.table("Kategorie").select("*").execute()
if kat_data.data:
    for kat in kat_data.data:
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{kat['nazwa']}** (ID: {kat['id']})")
        if col2.button("Usuń", key=f"del_kat_{kat['id']}"):
            supabase.table("Kategorie").delete().eq("id", kat["id"]).execute()
            st.rerun()

---

# --- SEKCJA PRODUKTY ---
st.header("🍎 Produkty")

# Pobranie kategorii do selectboxa
kategorie_list = {k['nazwa']: k['id'] for k in kat_data.data}

with st.form("dodaj_produkt"):
    nazwa_prod = st.text_input("Nazwa produktu")
    liczba = st.number_input("Liczba", min_value=0, step=1)
    cena = st.number_input("Cena", min_value=0.0, format="%.2f")
    kategoria_nazwa = st.selectbox("Wybierz kategorię", options=list(kategorie_list.keys()))
    submit_prod = st.form_submit_button("Dodaj produkt")

    if submit_prod and nazwa_prod:
        prod_data = {
            "nazwa": nazwa_prod,
            "liczba": liczba,
            "cena": cena,
            "kategoria_id": kategorie_list[kategoria_nazwa]
        }
        supabase.table("Produkty").insert(prod_data).execute()
        st.success(f"Dodano produkt: {nazwa_prod}")

# Wyświetlanie i usuwanie produktów
prod_res = supabase.table("Produkty").select("*, Kategorie(nazwa)").execute()
if prod_res.data:
    for p in prod_res.data:
        col1, col2 = st.columns([4, 1])
        # Kategorie(nazwa) to join dzięki relacji Foreign Key
        kat_label = p.get('Kategorie', {}).get('nazwa', 'Brak')
        col1.write(f"{p['nazwa']} | Ilość: {p['liczba']} | Cena: {p['cena']} PLN | Kat: {kat_label}")
        if col2.button("Usuń", key=f"del_prod_{p['id']}"):
            supabase.table("Produkty").delete().eq("id", p["id"]).execute()
            st.rerun()
