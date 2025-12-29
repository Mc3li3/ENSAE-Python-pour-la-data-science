import requests
import time
import os
import pandas as pd
from .cleaner import clean_data


def fetch_products(category, target_count=500):
    """
    Récupère 'target_count' produits en demandant page par page
    pour ne pas surcharger l'API (Pagination).
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    all_products = []
    page = 1
    page_size = 50  # On demande par petits paquets pour être sûr d'avoir une réponse

    print(f"📡 Démarrage de la collecte pour atteindre {target_count} produits...")

    while len(all_products) < target_count:
        params = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": page_size,
            "page": page,
            "json": 1,
            "fields": "product_name,brands,nutriscore_grade,nutriments,nova_group"
        }

        try:
            print(f"   ... Récupération page {page} ({len(all_products)}/{target_count})")
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print("   ⚠️ Erreur serveur temporaire, on réessaie...")
                time.sleep(1)
                continue

            data = response.json().get('products', [])

            if not data:
                print("   🏁 Plus de produits disponibles dans cette catégorie.")
                break

            all_products.extend(data)
            page += 1
            time.sleep(0.05)  # Politesse : On laisse le serveur respirer

        except Exception as e:
            print(f"   ❌ Erreur réseau : {e}")
            break

    print(f"✅ Collecte terminée : {len(all_products)} produits récupérés.")

    # On coupe si on en a trop récupéré
    return all_products[:target_count]


def downloader(saved_dataset):
    categories_map = {
        "Légumes": "canned-vegetables",
        "Légumineuses": "legumes",
        "Céréales": "breakfast_cereals",
        "Pizzas": "pizzas",
        "Fromages": "cheeses",
        "Chocolats": "chocolates",
        "Jus de Fruits": "fruit-juices",
        "Biscuits": "biscuits"
    }

    print("🌍 Lancement de la collecte")
    all_data = []

    # GitHub Actions définit automatiquement la variable d'environnement 'CI'
    IS_CI = os.environ.get('CI') == 'true'

    base_dir = os.path.dirname(os.path.abspath(__file__))

    csv_path = os.path.join(base_dir, '..', '..', 'data', 'food.csv')

    csv_path = os.path.abspath(csv_path)

    if IS_CI or saved_dataset:
        print("🤖 Utilisation du dataset ")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Fichier manquant : {csv_path}")
        df_final = pd.read_csv(csv_path)
        if IS_CI:
            df_final = df_final.sample(n=100, random_state=42)
    else:
        print("💻 Mode Local : Chargement complet du Dataset.")
        TARGET_PER_CAT = 500

        for label, api_tag in categories_map.items():
            print(f"\n📦 [{label}] Récupération en cours...")
            products = fetch_products(api_tag, target_count=TARGET_PER_CAT)

            # On ajoute le label propre pour l'analyse plus tard
            for p in products:
                p['Category_Label'] = label

            all_data.extend(products)
            print(f"   ✅ {len(products)} récupérés.")

        df_raw = pd.json_normalize(all_data)

        # 2. Configuration pour voir TOUTES les colonnes (sinon Pandas en cache au milieu)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 100)

        print(f"📊 Nombre total de colonnes brutes : {len(df_raw.columns)}")
        print("-" * 50)

        # 3. Afficher la liste complète des colonnes
        # On les trie par ordre alphabétique pour s'y retrouver
        sorted_cols = sorted(df_raw.columns.tolist())
        print(sorted_cols)

        # Nettoyage global
        df_final = clean_data(all_data)
        df_final.to_csv(csv_path, index=False)

    print("-" * 50)
    print(f"🚀 DATASET FINAL : {len(df_final)} produits.")
    print("-" * 50)

    # Affichage de la diversité
    print("Répartition par Catégorie :")
    print(df_final['Category_Label'].value_counts())
    print("\nRépartition par Nutriscore :")
    print(df_final['Nutriscore'].value_counts().sort_index())

    return df_final
