import requests
import time


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
                time.sleep(2)
                continue

            data = response.json().get('products', [])

            if not data:
                print("   🏁 Plus de produits disponibles dans cette catégorie.")
                break

            all_products.extend(data)
            page += 1
            time.sleep(0.5)  # Politesse : On laisse le serveur respirer

        except Exception as e:
            print(f"   ❌ Erreur réseau : {e}")
            break

    print(f"✅ Collecte terminée : {len(all_products)} produits récupérés.")

    # On coupe si on en a trop récupéré
    return all_products[:target_count]
