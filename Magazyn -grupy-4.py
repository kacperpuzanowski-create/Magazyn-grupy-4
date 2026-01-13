
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
