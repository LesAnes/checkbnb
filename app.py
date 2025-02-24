import streamlit as st
import pandas as pd
from utils import is_id_number_valid

st.set_page_config(page_title="Analyse CSV", page_icon="📊")

def load_excel_or_csv(file):
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file, engine="openpyxl")
    return pd.read_csv(file, index_col=False)

def analyze_data(source_name, source_file, teleservice_df, id_col, postal_code_col):
    if source_file is not None:
        source_df = load_excel_or_csv(source_file)
        source_df[id_col] = source_df[id_col].astype(str)

        merged_df = source_df.merge(
            teleservice_df,
            left_on=id_col,
            right_on="numero_declaration",
            suffixes=(f'_{source_name.lower()}', ''),
            how="left"
        )
        
        empty_id_mask = merged_df["numero_declaration"].isnull()
        empty_id = empty_id_mask.sum()
        empty_id_df = merged_df[empty_id_mask]
        cols = [id_col] + [col for col in merged_df.columns if col != id_col]
        empty_id_df = empty_id_df[cols]
        
        duplicate_id_mask = source_df[id_col].duplicated()
        duplicate_id_source = duplicate_id_mask.sum()
        duplicate_id_df = source_df[duplicate_id_mask]
        cols = [id_col] + [col for col in source_df.columns if col != id_col]
        duplicate_id_df = duplicate_id_df[cols]
        
        invalid_id_mask = merged_df.apply(lambda x: is_id_number_valid(x[id_col], str(x[postal_code_col])), axis=1)
        invalid_id_platform = invalid_id_mask.sum()
        invalid_id_df = merged_df[~invalid_id_mask]
        cols = [id_col] + [col for col in merged_df.columns if col != id_col]
        invalid_id_df = invalid_id_df[cols]

        return merged_df, empty_id, empty_id_df, duplicate_id_source, duplicate_id_df, invalid_id_platform, invalid_id_df
    return None, 0, None, 0, None, 0, None

def display_results(tab, source_name, results):
    with tab:
        if results[0] is not None:
            st.header(f"Analyse {source_name}")
            st.dataframe(results[0].head())
            st.write(f"Nombre de nuitées {source_name} ne correspondant pas à un id du téléservice: {results[1]}")
            with st.expander("Voir les nuitées inconnues"):
                st.dataframe(results[2])
            st.write(f"Nombre d'id de nuitées en double: {results[3]}")
            with st.expander("Voir les id en double"):
                st.dataframe(results[4])
            st.write(f"Nombre d'id de nuitées invalides: {results[5]}")
            with st.expander("Voir les id invalides"):
                st.dataframe(results[6])
        else:
            st.write("Pas de fichier")
        st.divider()

st.title("Analyse des données")

with st.expander("Données"):
    teleservice_file = st.file_uploader("Fichier téléservice", type=["csv", "xlsx"])
    airbnb_file = st.file_uploader("Fichier Airbnb", type=["csv", "xlsx"])
    booking_file = st.file_uploader("Fichier Booking", type=["csv", "xlsx"])

if teleservice_file is not None:
    teleservice_df = load_excel_or_csv(teleservice_file)
    teleservice_df["numero_declaration"] = teleservice_df["numero_declaration"].astype(str)
    
    if st.button("Analyser tous les fichiers"):
        airbnb_results = analyze_data("Airbnb", airbnb_file, teleservice_df, "Numéro de déclaration du meublé", "Code postal")
        booking_results = analyze_data("Booking", booking_file, teleservice_df, "id_num", "ad_cp")

        tabs = st.tabs(["Airbnb", "Booking"])
        
        display_results(tabs[0], "Airbnb", airbnb_results)
        display_results(tabs[1], "Booking", booking_results)
        
        # Graphique comparatif en bar chart
        st.header("Graphique comparatif")
        labels = ["Nuitées inconnues", "Id en double", "Id invalides"]
        airbnb_values = [airbnb_results[1], airbnb_results[3], airbnb_results[5]]
        booking_values = [booking_results[1], booking_results[3], booking_results[5]]
        
        chart_data = pd.DataFrame({"Erreurs": labels, "Airbnb": airbnb_values, "Booking": booking_values})
        st.bar_chart(chart_data.set_index("Erreurs"))
