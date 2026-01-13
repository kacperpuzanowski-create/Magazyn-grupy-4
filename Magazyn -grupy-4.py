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
import streamlit as st
from supabase import create_client, Client

# Konfiguracja połączenia
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Magazyn Pro", layout="wide")
st.title("📦 System Zarządzania Magazynem")

# --- POBIERANIE DANYCH ---
def get_data():
    produkty = supabase.table("Produkty").select("*, Kategorie(nazwa)").execute()
    kategorie = supabase.table("Kategorie").select("*").execute()
    return produkty.data, kategorie.data

prod_data, kat_data = get_data()

# --- SEKCJA OSTRZEŻEŃ (DASHBOARD) ---
st.header("⚠️ Alerty i Stan")
niski_stan = 5  # Próg ostrzegawczy

# Filtrowanie produktów z niskim stanem
produkty_brakujace = [p for p in prod_data if p['liczba'] <= niski_stan]

if produkty_brakujace:
    for p in produkty_brakujace:
        if p['liczba'] == 0:
            st.error(f"🚨 **BRAK NA STANIE:** {p['nazwa']} (0 szt.)")
        else:
            st.warning(f"📉 **NISKI STAN:** {p['nazwa']} - pozostało tylko {p['liczba']} szt.")
else:
    st.success("✅ Wszystkie stany magazynowe są w normie.")

st.divider()

# --- WIDOK TABELI STANU ---
st.subheader("📊 Aktualny stan magazynu")
if prod_data:
    # Przygotowanie danych do tabeli
    tabela_danych = []
    for p in prod_data:
        tabela_danych.append({
            "Produkt": p['nazwa'],
            "Ilość": p['liczba'],
            "Cena (PLN)": f"{p['cena']:.2f}",
            "Kategoria": p.get('Kategorie', {}).get('nazwa', 'Brak')
        })
    st.table(tabela_danych)

---

# --- DODAWANIE I USUWANIE (W KOLUMNACH) ---
col_prod, col_kat = st.columns(2)

with col_kat:
    st.subheader("📂 Zarządzaj Kategoriami")
    with st.form("dodaj_kategorie", clear_on_submit=True):
        nazwa_kat = st.text_input("Nowa kategoria")
        opis_kat = st.text_area("Opis")
        if st.form_submit_button("Dodaj"):
            if nazwa_kat:
                supabase.table("Kategorie").insert({"nazwa": nazwa_kat, "opis": opis_kat}).execute()
                st.rerun()

    # Usuwanie kategorii
    for kat in kat_data:
        c1, c2 = st.columns([3, 1])
        c1.write(kat['nazwa'])
        if c2.button("Usuń", key=f"del_k_{kat['id']}"):
            supabase.table("Kategorie").delete().eq("id", kat["id"]).execute()
            st.rerun()

with col_prod:
    st.subheader("🍎 Zarządzaj Produktami")
    kategorie_dict = {k['nazwa']: k['id'] for k in kat_data}
    
    with st.form("dodaj_produkt", clear_on_submit=True):
        n_prod = st.text_input("Nazwa produktu")
        n_liczba = st.number_input("Ilość", min_value=0)
        n_cena = st.number_input("Cena", min_value=0.0)
        n_kat = st.selectbox("Kategoria", options=list(kategorie_dict.keys()))
        if st.form_submit_button("Dodaj"):
            if n_prod:
                supabase.table("Produkty").insert({
                    "nazwa": n_prod, "liczba": n_liczba, 
                    "cena": n_cena, "kategoria_id": kategorie_dict[n_kat]
                }).execute()
                st.rerun()

    # Usuwanie produktów
    for p in prod_data:
        c1, c2 = st.columns([3, 1])
        c1.write(f"{p['nazwa']} ({p['liczba']} szt.)")
        if c2.button("Usuń", key=f"del_p_{p['id']}"):
            supabase.table("Produkty").delete().eq("id", p["id"]).execute()
            st.rerun()
