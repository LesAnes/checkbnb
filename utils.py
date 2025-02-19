      
def est_numero_declaration_veridique(numero_declaration, code_postal):
    """
    Vérifie si un numéro de déclaration de meublé de tourisme est vraisemblable
    pour un code postal donné à Paris.

    Args:
        numero_declaration (str): Le numéro de déclaration à 13 chiffres.
        code_postal (str): Le code postal de Paris (format "750XX").

    Returns:
        bool: True si le numéro de déclaration est vraisemblable pour le code postal, False sinon.
    """
    if not isinstance(numero_declaration, str) or not numero_declaration.isdigit() or len(numero_declaration) != 13:
        return False  # Format du numéro de déclaration incorrect

    if not isinstance(code_postal, str) or not code_postal.startswith("75") or len(code_postal) != 5 or not code_postal[2:].isdigit():
        return False  # Format du code postal incorrect ou n'est pas un code postal parisien

    code_insee_ville = numero_declaration[:2]
    arrondissement_declaration_str = numero_declaration[2:5]
    arrondissement_cp_str = code_postal[2:]

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