import pandas as pd


def remove_aberrant_values(df):
    """
    Filtre les valeurs physico-chimiques impossibles et normalise les pourcentages.
    """
    initial_shape = df.shape

    # Définition des colonnes cibles
    nutrients_cols = ['Sucre', 'Gras', 'Saturés', 'Sel', 'Fibres', 'Protéines']
    energy_col = 'Energie'
    fruit_col = 'Fruits et Légumes'
    
    # 1. Suppression des valeurs négatives (toutes colonnes numériques)
    cols_to_check = nutrients_cols + [energy_col, fruit_col]
    existing_cols = [c for c in cols_to_check if c in df.columns]
    
    for col in existing_cols:
        df = df[df[col] >= 0]

    # 2. Seuil physique : Max 101g pour 100g (tolérance 1% pour arrondis)
    for col in nutrients_cols:
        if col in df.columns:
            df = df[df[col] <= 101.0]

    # 3. Seuil énergétique : Max 1000 kcal/100g (huile pure = 900kcal)
    if energy_col in df.columns:
        df = df[df[energy_col] <= 1000.0]

    # 4. Cohérence lipidique : Saturés <= Gras total
    if 'Gras' in df.columns and 'Saturés' in df.columns:
        df = df[df['Saturés'] <= df['Gras']]

    # 5. Normalisation (Clamping) des fruits & légumes [0, 100]
    # Gère les cas de concentration (ex: sauce tomate) sans supprimer la ligne
    if fruit_col in df.columns:
        df[fruit_col] = df[fruit_col].clip(lower=0, upper=100)

    dropped_count = initial_shape[0] - df.shape[0]
    if dropped_count > 0:
        print(f"[Data Cleaning] Removed {dropped_count} aberrant records.")

    return df


def clean_data(products_list):
    """
    Nettoie les données et prépare les colonnes pour l'analyse.
    """
    if not products_list:
        return pd.DataFrame()

    data = []
    for item in products_list:
        n = item.get('nutriments', {})
        data.append({
            'Nom': item.get('product_name', 'Inconnu'),
            'Marque': item.get('brands', 'Inconnu'),
            'Nutriscore': str(item.get('nutriscore_grade', 'nan')).upper(),
            'Category_Label': item.get('Category_Label', 'Autre'),
            'Energie': n.get('energy-kcal_100g', 0),
            'Sucre': n.get('sugars_100g', 0),
            'Gras': n.get('fat_100g', 0),
            'Saturés': n.get('saturated-fat_100g', 0),
            'Sel': n.get('salt_100g', 0),
            'Fibres': n.get('fiber_100g', 0),
            'Protéines': n.get('proteins_100g', 0),
            'Fruits et Légumes': n.get('fruits-vegetables-nuts-estimate-from-ingredients_100g', 0)
        })

    df = pd.DataFrame(data)

    # Filtres stricts pour le ML
    cols_to_check = ['Nutriscore', 'Energie', 'Sucre', 'Saturés', 'Sel', 'Protéines']
    df = df.dropna(subset=cols_to_check)
    df = df[df['Nutriscore'].isin(['A', 'B', 'C', 'D', 'E'])]
    df = df.sort_values('Nutriscore')

    df = remove_aberrant_values(df)

    return df
