import requests
import time
import random


def get_mock_data(count=50):
    """Génère des fausses données crédibles si l'API est en panne."""
    print("⚠️ API INDISPONIBLE : Utilisation de données de secours (Mock Data).")
    mock_products = []
    for i in range(count):
        # Simulation d'un profil nutritionnel de biscuit
        score = random.choice(['A', 'B', 'C', 'D', 'E'])
        sucre = random.uniform(0, 10) if score in ['A', 'B'] else random.uniform(20, 50)
        gras = random.uniform(0, 10) if score in ['A', 'B'] else random.uniform(15, 30)
        mock_products.append({
            'product_name': f'Produit Test {i}',
            'brands': 'Marque Test',
            'nutriscore_grade': score,
            'nutriments': {
                'energy-kcal_100g': random.uniform(300, 550),
                'sugars_100g': sucre,
                'fat_100g': gras,
                'saturated-fat_100g': gras / 2,
                'salt_100g': random.uniform(0.1, 1.5),
                'fiber_100g': random.uniform(0, 5),
                'proteins_100g': random.uniform(2, 8)
            }
        })
    return mock_products


def fetch_products(category, page_size=100):
    """
    Récupère les données avec 3 tentatives (Retries) et un fallback.
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": category,
        "page_size": page_size,
        "json": 1,
        "fields": "product_name,nutriscore_grade,nutriments,brands"
    }

    # On essaie 3 fois avant d'abandonner
    for attempt in range(3):
        try:
            print(f"📡 Tentative {attempt+1}/3 pour : {category}...")
            response = requests.get(url, params=params, timeout=100)
            if response.status_code == 200:
                data = response.json().get('products', [])
                if data: return data # Succès !
            # Si le serveur nous dit d'attendre (429) ou erreur serveur (500+)
            time.sleep(2) # On attend 2 secondes avant de recommencer
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur connexion ({e})...")
            time.sleep(2)

    # Si on arrive ici, c'est que les 3 essais ont échoué.
    # On renvoie les données de secours pour SAUVER LA DÉMO.
    return get_mock_data(page_size)
