# JupyterLab Kaggle sur le VPS

JupyterLab (CPU, pas de GPU) servi sur https://kaggle.juleskantzer.com par le Traefik de Dokploy
(HTTPS Let's Encrypt), protégé par mot de passe. Le dépôt est monté dans `/work`, le token Kaggle
`/root/.kaggle` en lecture seule, et `kg` est disponible dans le terminal Jupyter.
Limites : 3 CPU, 10 Go de RAM (pour laisser de la place aux autres apps du VPS).

Image : python 3.12 + jupyterlab, pandas, scikit-learn, catboost, xgboost, lightgbm, optuna,
matplotlib, seaborn, plotly, kaggle.

## Déployer / mettre à jour

```bash
cd deploy/jupyter
cp .env.example .env     # puis remplir (jamais commité)
docker compose up -d --build
```

## Changer le mot de passe

```bash
docker run --rm kaggle-jupyter python -c "from jupyter_server.auth import passwd; print(passwd('NOUVEAU'))"
# coller le hash entre apostrophes dans .env (JUPYTER_PASSWORD_HASH='argon2:…'), puis :
docker compose up -d
```

Le mot de passe actuel est dans `/root/.jupyter-kaggle-password` sur le VPS (chmod 600).
