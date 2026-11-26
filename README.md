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

Nouvelle compétition : créer `competitions/<type>/<slug>/`, y mettre le notebook et un README
(copier celui d'une autre compétition), puis ajouter une ligne au tableau ci-dessous.

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
