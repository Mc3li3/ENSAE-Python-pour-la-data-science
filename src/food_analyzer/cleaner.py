import pandas as pd
import numpy as np


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
            'Energie': n.get('energy-kcal_100g', np.nan),
            'Sucre': n.get('sugars_100g', np.nan),
            'Gras': n.get('fat_100g', np.nan),
            'Saturés': n.get('saturated-fat_100g', np.nan),
            'Sel': n.get('salt_100g', np.nan),
            'Fibres': n.get('fiber_100g', 0),    # On assume 0 si vide
            'Protéines': n.get('proteins_100g', np.nan)
        })

    df = pd.DataFrame(data)

    # Filtres stricts pour le ML
    cols_to_check = ['Nutriscore', 'Energie', 'Sucre', 'Saturés', 'Sel', 'Protéines']
    df = df.dropna(subset=cols_to_check)
    df = df[df['Nutriscore'].isin(['A', 'B', 'C', 'D', 'E'])]
    df = df.sort_values('Nutriscore')

    return df
