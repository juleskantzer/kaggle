# kaggle

Tous mes notebooks de compétitions Kaggle : Playground, Getting Started, Featured, Research, etc.

Mon compte Kaggle : https://www.kaggle.com/juleskantzer

## Organisation

```
competitions/
  <type>/            playground, getting-started, featured, research, community…
    <slug-kaggle>/   nom exact de la compétition sur Kaggle
      *.ipynb        le(s) notebook(s)
      README.md      lien, statut, scores CV / LB, notes
```

Le dossier porte le slug Kaggle, donc `kaggle competitions download -c <slug>` marche directement.
Les données et les fichiers de soumission ne sont jamais commités (voir `.gitignore`).

## Workflow sur le VPS

JupyterLab : https://kaggle.juleskantzer.com (voir [`deploy/jupyter/`](deploy/jupyter/)).
Depuis un terminal (VPS ou terminal Jupyter) :

```bash
kg new playground-series-s6e3            # dossier + données + notebook starter + ligne dans l'index
kg submit playground-series-s6e3 submissions/cat_cv0.91234.csv -m "catboost optuna" --cv 0.91234
kg scores playground-series-s6e3         # dernières soumissions
```

- `kg new` devine le type (playground, featured…) ; forcer avec `--type getting-started`.
  Si le téléchargement renvoie 403, accepter d'abord les règles de la compétition sur Kaggle.
- Le notebook starter ([`template/playground_starter.ipynb`](template/playground_starter.ipynb)) :
  EDA rapide, CV KFold CatBoost / XGBoost, Optuna sur sous-échantillon, fit sur tout le train,
  écrit `submissions/<modèle>_cv<score>.csv` et affiche la commande `kg submit` à lancer.
- `kg submit` attend le score public et ajoute une ligne au tableau Scores du README de la compétition.

## Compétitions

| Compétition | Type | Statut | Meilleur score | Lien |
|---|---|---|---|---|
| [Titanic - Machine Learning from Disaster](competitions/getting-started/titanic/) | getting-started | Terminé | — | [Kaggle](https://www.kaggle.com/competitions/titanic) |
| [Binary Classification with a Software Defects Dataset](competitions/playground/playground-series-s3e23/) | playground | En cours | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s3e23) |
| [Regression with an Insurance Dataset](competitions/playground/playground-series-s4e12/) | playground | Terminé | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s4e12) |
| [Binary Prediction with a Rainfall Dataset](competitions/playground/playground-series-s5e3/) | playground | Terminé | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s5e3) |
| [Predict Podcast Listening Time](competitions/playground/playground-series-s5e4/) | playground | Terminé | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s5e4) |
| [Predict Calorie Expenditure](competitions/playground/playground-series-s5e5/) | playground | En cours | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s5e5) |
| [Predicting Optimal Fertilizers](competitions/playground/playground-series-s5e6/) | playground | En cours | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s5e6) |
| [Predicting Road Accident Risk](competitions/playground/playground-series-s5e10/) | playground | En cours | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s5e10) |
| [Predicting Student Test Scores](competitions/playground/playground-series-s6e1/) | playground | Terminé | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s6e1) |
| [Predicting Heart Disease](competitions/playground/playground-series-s6e2/) | playground | En cours | — | [Kaggle](https://www.kaggle.com/competitions/playground-series-s6e2) |
