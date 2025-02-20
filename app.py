import streamlit as st
import pandas as pd
from utils import is_id_number_valid

st.set_page_config(page_title="Analyse CSV", page_icon="📊")

def load_excel_or_csv(file):
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file, engine="openpyxl")
    return pd.read_csv(file, index_col=False)

def analyze_data(source_name, source_file, teleservice_df, id_col, name_col, postal_code_col):
    if source_file is not None:
        st.header(f"Analyse {source_name}")
        source_df = load_excel_or_csv(source_file)
        source_df[id_col] = source_df[id_col].astype(str)

        if st.button(f"Analyser {source_name}"):
            merged_df = source_df.merge(
                teleservice_df,
                left_on=id_col,
                right_on="numero_declaration",
                suffixes=(f'_{source_name.lower()}', ''),
                how="left"
            )
            st.dataframe(merged_df.head())

            empty_id_mask = merged_df["numero_declaration"].isnull()
            empty_id = empty_id_mask.sum()
            st.write(f"Nombre de nuitées {source_name} ne correspondant pas à un id connu: {empty_id}")
            with st.expander("Voir les nuitées sans id"):
                empty_rows = merged_df[empty_id_mask][[id_col, name_col]]
                st.dataframe(empty_rows)
            
            duplicate_id_mask = source_df[id_col].duplicated()
            duplicate_id_source = duplicate_id_mask.sum()
            st.write(f"Nombre d'id de nuitées en double: {duplicate_id_source}")
            with st.expander("Voir les id en double"):
                duplicate_rows = source_df[duplicate_id_mask][[id_col, name_col]]
                st.dataframe(duplicate_rows)

            invalid_id_mask = merged_df.apply(lambda x: is_id_number_valid(x[id_col], str(x[postal_code_col])), axis=1)
            invalid_id_platform = invalid_id_mask.sum()
            st.write(f"Nombre d'id de nuitées invalides: {invalid_id_platform}")
            with st.expander("Voir les id invalides"):
                invalid_rows = merged_df[~invalid_id_mask][[id_col, name_col]]
                st.dataframe(invalid_rows)

st.title("Analyse des données")

with st.expander("Données"):
    teleservice_file = st.file_uploader("Fichier téléservice", type=["csv", "xlsx"])
    airbnb_file = st.file_uploader("Fichier Airbnb", type=["csv", "xlsx"])
    booking_file = st.file_uploader("Fichier Booking", type=["csv", "xlsx"])

if teleservice_file is not None:
    teleservice_df = load_excel_or_csv(teleservice_file)
    teleservice_df["numero_declaration"] = teleservice_df["numero_declaration"].astype(str)

    tabs = st.tabs(["Airbnb", "Booking"])

    with tabs[0]:
        analyze_data("Airbnb", airbnb_file, teleservice_df, "Numéro de déclaration du meublé", "Nom du loueur", "Code postal")
    
    with tabs[1]:
        analyze_data("Booking", booking_file, teleservice_df, "id_num", "nom_loueur", "ad_cp")
