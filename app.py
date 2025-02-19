import streamlit as st
import pandas as pd
from utils import est_numero_declaration_veridique

st.title("Analyse des données")

with st.expander("Données"):
    teleservice_file = st.file_uploader("Fichier CSV téléservice", type="csv")
    airbnb_file = st.file_uploader("Fichier CSV Airbnb", type="csv")
    booking_file = st.file_uploader("Fichier CSV Booking", type="csv")

if teleservice_file is not None and airbnb_file is not None:
    teleservice_df = pd.read_csv(teleservice_file, index_col=False)
    teleservice_df["numero_declaration"] = teleservice_df["numero_declaration"].astype(str)
    
    airbnb_df = pd.read_csv(airbnb_file, index_col=False)
    airbnb_df["Numéro de déclaration du meublé"] = airbnb_df["Numéro de déclaration du meublé"].astype(str)
    
    
    if st.button("Analyser"):
        # Merge the two DataFrames
        airbnb_merged = airbnb_df.merge(teleservice_df, left_on="Numéro de déclaration du meublé",right_on="numero_declaration", suffixes=('_airbnb', ''), how="left")
        st.dataframe(airbnb_merged.head())
        
        # count the number of empty values in id_internal
        empty_id_mask = airbnb_merged["numero_declaration"].isnull()
        empty_id = empty_id_mask.sum()
        st.write(f"Nombre de nuitées ne correspondant pas à un id connu: {empty_id}")
        with st.expander("Voir les nuitées sans id"):
            empty_id = airbnb_merged[empty_id_mask]["Numéro de déclaration du meublé"]
            st.write(empty_id)
        
        # count duplicates in id_platform
        duplicates_id_mask = airbnb_df["Numéro de déclaration du meublé"].duplicated()
        duplicates_id_airbnb = duplicates_id_mask.sum()
        st.write(f"Nombre d'id de nuitées en double: {duplicates_id_airbnb}")
        with st.expander("Voir les id en double"):
            duplicates = airbnb_df[duplicates_id_mask]["Numéro de déclaration du meublé"]
            st.write(duplicates)
        
        # count number of invalid id_platform
        invalid_id_mask = airbnb_merged.apply(lambda x: est_numero_declaration_veridique(x["Numéro de déclaration du meublé"], str(x["Code postal"])), axis=1)
        invalid_id_platform = invalid_id_mask.sum()
        st.write(f"Nombre d'id de nuitées invalides: {invalid_id_platform}")
        with st.expander("Voir les id invalides"):
            invalid_id = airbnb_merged[~invalid_id_mask]["Numéro de déclaration du meublé"]
            st.write(invalid_id)
        