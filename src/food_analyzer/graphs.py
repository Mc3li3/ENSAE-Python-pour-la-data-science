import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ipywidgets import interact, widgets


color_map = {'A': '#038141', 'B': '#85BB2F', 'C': '#FECB02', 'D': '#EE8100', 'E': '#E63E11'}
order_config = {"Nutriscore": ["A", "B", "C", "D", "E"]}
nutriments_clés = ['Energie', 'Sucre', 'Gras', 'Saturés', 'Sel', 'Fibres', 'Protéines', 'Fruits et Légumes']


def distribution_nutriments_nutriscore(df_final):
    def interactive_distribution(nutriment_choisi):
        fig = px.box(
            df_final, 
            x="Nutriscore", 
            y=nutriment_choisi,
            color="Nutriscore",
            color_discrete_map=color_map,
            category_orders=order_config,
            title=f"Distribution détaillée : {nutriment_choisi}",
            height=500
        )
        fig.update_layout(showlegend=False)
        return fig

    print("🔍 Analyse détaillée par nutriment :")
    interact(interactive_distribution, nutriment_choisi=nutriments_clés);


def impact_matrix_sugar(df_final):
    fig = px.scatter(
        df_final,
        x="Sucre",
        y="Fruits et Légumes",
        color="Nutriscore",
        size="Energie",                 # La taille des bulles = Calories
        hover_name="Nom",               # <--- Affiche le nom au survol !
        hover_data=["Marque", "Category_Label"],
        color_discrete_map=color_map,
        category_orders=order_config,
        size_max=40,                    # Taille max des bulles
        title="Matrice d'impact : Le sucre condamne-t-il toujours ?",
        labels={"Sucre": "Sucre (g/100g)", "Fruits et Légumes": "Fruits & Légumes (%)"}
    )

    # On ajoute une ligne limite pour montrer les produits très sucrés
    fig.add_vline(x=20, line_dash="dash", line_color="gray", annotation_text="Zone très sucrée")

    return fig


def corr_matrix(df_final):
    # Sélection des colonnes numériques uniquement
    corr_matrix = df_final[nutriments_clés].corr().round(2)

    fig = px.imshow(
        corr_matrix,
        text_auto=True,              # Affiche les chiffres dans les cases
        aspect="auto",
        color_continuous_scale="RdBu_r",  # Rouge = Corrélation Positive, Bleu = Négative
        zmin=-1, zmax=1,
        title="Matrice de Corrélation des Nutriments"
    )
    return fig


def distribution_nutriscore_par_famille_d_aliments(df_final):
    fig = px.histogram(
        df_final,
        y="Category_Label",          # Catégories sur l'axe vertical
        color="Nutriscore",          # Couleurs selon la note
        color_discrete_map=color_map,
        category_orders={"Nutriscore": order_config["Nutriscore"]},  # Force l'ordre A->E dans la légende
        title="Distribution du Nutriscore par Famille d'aliments",
        text_auto=True,              # Affiche le nombre exact DANS la barre (Bonus !)
        height=600                   # Hauteur ajustée pour bien voir les catégories
    )

    # 3. Mise en forme Pro
    fig.update_layout(
        xaxis_title="Nombre de produits",
        yaxis_title="",              # On enlève le titre inutile "Category_Label"
        legend_title="Score",
        # Astuce : On trie les catégories par nombre total de produits (plus joli)
        yaxis={'categoryorder': 'total ascending'},
        barmode='stack'              # 'stack' empile les barres (plus lisible que côte à côte)
    )

    return fig


def nutriscore_par_marques(df_final):
    # On ne garde que les grosses marques (> 5 produits)
    top_marques = df_final['Marque'].value_counts()
    marques_a_garder = top_marques[top_marques > 5].index.tolist()
    df_marques = df_final[df_final['Marque'].isin(marques_a_garder)]

    # Graphique Barrres Empilées 100%
    fig = px.histogram(
        df_marques,
        x="Marque",
        color="Nutriscore",
        pattern_shape="Nutriscore",  # Ajoute des motifs pour l'accessibilité
        barnorm="percent",          # Normalise à 100% pour comparer équitablement
        color_discrete_map=color_map,
        category_orders=order_config,
        title="Podium des Marques : Répartition des Scores (en %)",
        text_auto='.0f'             # Affiche le pourcentage
    ).update_xaxes(categoryorder="total ascending")  # Trie par volume

    return fig


def sucre_gras(df_final):
    choix_categories = ['Toutes'] + sorted(df_final['Category_Label'].unique().tolist())

    def visualiser_plotly(categorie):
        # --- FILTRAGE DES DONNÉES ---
        if categorie == 'Toutes':
            df_plot = df_final
            titre_suffixe = "Global"
        else:
            df_plot = df_final[df_final['Category_Label'] == categorie]
            titre_suffixe = categorie

        if df_plot.empty:
            print("Aucune donnée.")
            return

        # --- CRÉATION DE LA STRUCTURE (2 Graphiques côte à côte) ---
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.4, 0.6],  # Le scatter plot à droite est un peu plus large
            subplot_titles=(f"Distribution Sucre ({titre_suffixe})", f"Gras vs Sucre ({titre_suffixe})"),
            horizontal_spacing=0.1
        )

        # --- REMPLISSAGE DES GRAPHIQUES ---
        # On boucle sur A, B, C, D, E pour garantir les bonnes couleurs et l'ordre
        for score in order_config["Nutriscore"]:
            d_score = df_plot[df_plot['Nutriscore'] == score]
            if d_score.empty:
                continue
            # 1. GAUCHE : Boxplot du Sucre
            fig.add_trace(
                go.Box(
                    y=d_score['Sucre'],
                    name=score,
                    marker_color=color_map[score],
                    boxpoints=False,  # On cache les points pour la clarté
                    showlegend=False  # On ne veut pas de double légende
                ),
                row=1, col=1
            )

            # 2. DROITE : Scatterplot (Gras vs Sucre)
            fig.add_trace(
                go.Scatter(
                    x=d_score['Sucre'],
                    y=d_score['Gras'],
                    mode='markers',
                    name=score,  # Apparaît dans la légende
                    text=d_score['Nom'],  # <--- C'EST ICI QUE TU GAGNES DES POINTS (Nom au survol)
                    customdata=d_score['Marque'],
                    marker=dict(
                        color=color_map[score],
                        size=d_score['Energie'],  # La taille dépend des calories
                        sizemode='area',
                        sizeref=2.*max(df_plot['Energie'])/(40.**2),  # Calibrage de la taille
                        sizemin=4,
                        line=dict(width=1, color='DarkSlateGrey')
                    ),
                    # Ce qui s'affiche dans la bulle au survol
                    hovertemplate="<b>%{text}</b><br>Marque: %{customdata}<br>Sucre: %{x}g<br>Gras: %{y}g<br>Calories: %{marker.size:.0f} kcal<extra></extra>"
                ),
                row=1, col=2
            )

        # --- MISE EN FORME ---
        fig.update_layout(
            height=600,
            width=1100,
            template="plotly_white",
            title_text=f"Analyse Sectorielle Interactive : {titre_suffixe}",
            legend_title="Nutriscore",
            showlegend=True
        )

        # Titres des axes
        fig.update_yaxes(title_text="Sucre (g/100g)", row=1, col=1)
        fig.update_xaxes(title_text="Sucre (g/100g)", row=1, col=2)
        fig.update_yaxes(title_text="Gras (g/100g)", row=1, col=2)

        fig.show()

    # --- LANCEMENT DU MENU DÉROULANT ---
    print("👇 Change de catégorie pour mettre à jour instantanément :")
    interact(visualiser_plotly, categorie=widgets.Dropdown(options=choix_categories, description='Filtre :'))
