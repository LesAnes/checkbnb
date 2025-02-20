      
def is_id_number_valid(id_number, postal_code):
    """
    Vérifie si un numéro de déclaration de meublé de tourisme est vraisemblable
    pour un code postal donné à Paris.

    Args:
        id_number (str): Le numéro de déclaration à 13 chiffres.
        postal_code (str): Le code postal de Paris (format "750XX").

    Returns:
        bool: True si le numéro de déclaration est vraisemblable pour le code postal, False sinon.
    """
    if not isinstance(id_number, str) or not id_number.isdigit() or len(id_number) != 13:
        return False  # Format du numéro de déclaration incorrect

    if not isinstance(postal_code, str) or not postal_code.startswith("75") or len(postal_code) != 5 or not postal_code[2:].isdigit():
        return False  # Format du code postal incorrect ou n'est pas un code postal parisien

    code_insee_ville = id_number[:2]
    arrondissement_declaration_str = id_number[2:5]
    arrondissement_cp_str = postal_code[2:]

    if code_insee_ville != "75":
        return False # Doit commencer par le code INSEE de Paris

    if not arrondissement_declaration_str.isdigit() or not arrondissement_cp_str.isdigit():
        return False # Les parties arrondissement doivent être numériques

    arrondissement_declaration = int(arrondissement_declaration_str)
    arrondissement_cp = int(arrondissement_cp_str)

    if arrondissement_cp < 1 or arrondissement_cp > 20:
        return False # Code postal d'arrondissement parisien invalide

    arrondissement_cp_based_declaration = 100 + arrondissement_cp # Approximation simple
    return arrondissement_declaration == arrondissement_cp_based_declaration