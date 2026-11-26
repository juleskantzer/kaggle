FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends git tini libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    jupyterlab==4.4.* jupytext \
    numpy pandas pyarrow scikit-learn scipy \
    catboost xgboost lightgbm optuna \
    matplotlib seaborn plotly \
    kaggle six

# kg (scaffold / submit) disponible dans le terminal Jupyter
RUN ln -s /work/tools/kg /usr/local/bin/kg

WORKDIR /work
EXPOSE 8888
ENTRYPOINT ["tini", "--"]
# JUPYTER_PASSWORD_HASH : hash argon2 généré par jupyter_server.auth.passwd (jamais commité)
CMD ["sh", "-c", "exec jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \
     --ServerApp.root_dir=/work \
     --PasswordIdentityProvider.hashed_password=\"$JUPYTER_PASSWORD_HASH\" \
     --IdentityProvider.token='' \
     --ServerApp.trust_xheaders=True"]
