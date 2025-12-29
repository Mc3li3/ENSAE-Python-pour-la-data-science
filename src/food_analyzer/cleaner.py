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

    return df
