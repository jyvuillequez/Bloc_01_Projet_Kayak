# Bloc 01 – Projet Kayak

Analyse de données météo et hôtels pour comprendre les facteurs influençant l’attractivité d’un voyage et améliorer les recommandations de destinations et d’hébergements

Projet réalisé dans le cadre de la certification **RNCP Niveau 6 – Concepteur Développeur en Science des données (Jedha Bootcamp)**.

## 1. Contexte & enjeux
**Problématique métier :** Aider Kayak à mieux recommander des destinations : Combinaison de signaux externes (météo) et signaux d’offre (hébergements : quantité, notes, localisation). L’enjeu est d’identifier les destinations les plus attractives selon des critères objectifs (ex : météo favorable + offre d’hôtels bien notés).

**Décideurs cibles :**
- Produit (amélioration des recommandations)
- Marketing (campagnes sur destinations “tendance”)
- Business / Ops (pilotage de l’offre et partenariats)

## 2. Objectifs du projet 
- Construire un pipeline simple de collecte de données (destinations → météo → hôtels)
- Explorer et comparer les destinations sur des indicateurs clés (météo, densité d’hôtels, notes, localisation)
- Produire un classement / shortlist de destinations + une sélection d’hébergements “recommandés”

## 3. Compétences mobilisées

- Scraping (Selenium)
- APIs (Données gps et météo)
- Nettoyage et structuration des données
- Analyse exploratoire (EDA) + visualisations
- Recommandations orientées Buisiness

## 4. Données

- **Destinations (input)** : liste de villes dans un fichier de config (JSON)
- **Météo** : via API météo (OpenWeatherAPI)
- **Hôtels** : scraping Booking (pages de résultats + pages détail)

## 5. Méthodologie

1. **Paramétrage des villes**
   - Les destinations ne sont pas codées en dur : elles proviennent de `data/config/cities_best.json`.
2. **Collecte**
   - Construction d’URL de recherche dynamique (par ville)
   - Scraping des cartes hôtels (page résultats)
   - Scraping des pages hôtel (détails : description, adresse complète, lat/lng)
3. **Préparation**
   - Normalisation des champs, gestion des valeurs manquantes
   - Consolidation multi-villes dans un seul dataset
4. **Analyse**
   - Comparaisons inter-destinations (ex : volume d’hôtels, distribution des notes)
   - Mise en évidence de critères pour recommandations
5. **Restitution**
   - Synthèse, insights, recommandations

## 6. Résultats & recommandations

- **Résultat clé 1 :** Top destinations par météo favorable + disponibilité hôtels
- **Résultat clé 2 :** Corrélation / tendances entre zones et 
- **Limites :**
  - Scraping sensible aux changements de structure HTML
  - Pagination non prise en compte
  - Données dépendantes de la date de collecte

## 7. Organisation du projet

```text
.
├─ data/
│  ├─ config/
│  │  ├─ cities_best.json     # liste des villes "best"
│  │  ├─ cities.json          # autre liste (initialisation)
│  │  └─ parameters.yml       # paramètres globaux
│  ├─ raw/                    # données brutes
│  └─ outputs/                # exports (csv)
├─ notebooks/                 # notebooks Jupyter
├─ src/                       # scripts Python réutilisables
└─ présentation/              # slides + exports/captures
