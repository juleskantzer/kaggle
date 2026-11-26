"""kg : raccourcis Kaggle pour ce dépôt.

  kg new <slug> [--type playground]   crée competitions/<type>/<slug>/, télécharge les données,
                                      copie le notebook starter, ajoute la ligne au README index
  kg submit <slug> <fichier.csv> -m "message" [--cv 0.123]
                                      soumet, attend le score public, le logge dans le README
  kg scores <slug>                    affiche les dernières soumissions
"""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMP = REPO / "competitions"
TEMPLATE = REPO / "template" / "playground_starter.ipynb"
TYPES = ["playground", "getting-started", "featured", "research", "community"]


def api():
    from kaggle.api.kaggle_api_extended import KaggleApi
    a = KaggleApi()
    a.authenticate()
    return a


def find_comp(a, slug):
    res = a.competitions_list(search=slug)
    res = getattr(res, "competitions", res) or []
    for c in res:
        if c and c.ref.rstrip("/").split("/")[-1] == slug:
            return c
    return None


def guess_type(slug, category):
    if slug.startswith("playground-series"):
        return "playground"
    cat = (category or "").lower().replace(" ", "-")
    return cat if cat in TYPES else "featured"


def comp_dir(slug):
    hits = list(COMP.glob(f"*/{slug}"))
    if not hits:
        sys.exit(f"Dossier introuvable pour {slug} (lance d'abord : kg new {slug})")
    return hits[0]


def short_name(slug):
    m = re.match(r"playground-series-(s\d+e\d+)", slug)
    return m.group(1) if m else slug.replace("-", "_")


def cmd_new(args):
    a = api()
    c = find_comp(a, args.slug)
    if c is None:
        sys.exit(f"Compétition {args.slug} introuvable sur Kaggle")
    title = c.title
    ctype = args.type or guess_type(args.slug, c.category)
    d = COMP / ctype / args.slug
    data = d / "data"
    data.mkdir(parents=True, exist_ok=True)
    print(f"→ {d.relative_to(REPO)}  ({title}, métrique : {c.evaluation_metric})")

    if not any(data.glob("*.csv")):
        print("→ téléchargement des données…")
        try:
            a.competition_download_files(args.slug, path=str(data), quiet=False)
        except Exception as e:  # 403 = règles pas encore acceptées
            print(f"⚠️  téléchargement impossible : {e}\n"
                  f"   Accepte les règles : https://www.kaggle.com/competitions/{args.slug}/rules "
                  f"puis relance kg new {args.slug}")
        for z in data.glob("*.zip"):
            with zipfile.ZipFile(z) as zf:
                zf.extractall(data)
            z.unlink()
    for f in sorted(data.iterdir()):
        print(f"   data/{f.name}")

    nb = d / f"{short_name(args.slug)}_{re.sub(r'[^A-Za-z0-9]+', '_', title).strip('_')}.ipynb"
    if not list(d.glob("*.ipynb")):
        nbj = json.loads(TEMPLATE.read_text())
        src = nbj["cells"][0]["source"]
        nbj["cells"][0]["source"] = [s.replace("{{TITLE}}", title).replace("{{SLUG}}", args.slug)
                                     .replace("{{METRIC}}", c.evaluation_metric or "?") for s in src]
        nb.write_text(json.dumps(nbj, indent=1, ensure_ascii=False) + "\n")
        print(f"→ notebook {nb.name}")

    readme = d / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {title}\n\n"
            f"- Compétition : [{args.slug}](https://www.kaggle.com/competitions/{args.slug})\n"
            f"- Type : {ctype}\n- Statut : En cours\n"
            f"- Métrique : {c.evaluation_metric}\n"
            f"- Notebook : [`{nb.name}`]({nb.name})\n\n"
            "## Scores\n\n| Date | Version | CV | Public LB | Private LB | Notes |\n"
            "|---|---|---|---|---|---|\n\n## Notes\n"
        )
    index = REPO / "README.md"
    txt = index.read_text()
    if f"({d.relative_to(REPO)}/)" not in txt:
        row = (f"| [{title}]({d.relative_to(REPO)}/) | {ctype} | En cours | — | "
               f"[Kaggle](https://www.kaggle.com/competitions/{args.slug}) |")
        index.write_text(txt.rstrip("\n") + "\n" + row + "\n")
        print("→ ligne ajoutée au README index")


def submissions(a, slug):
    return [s for s in (a.competition_submissions(slug) or []) if s]


def cmd_submit(args):
    a = api()
    d = comp_dir(args.slug)
    f = Path(args.file)
    if not f.exists():
        f = d / args.file
    print(f"→ soumission de {f} …")
    a.competition_submit(str(f), args.message, args.slug)
    sub = None
    for _ in range(60):  # ~10 min max
        time.sleep(10)
        subs = submissions(a, args.slug)
        sub = next((s for s in subs if s.description == args.message), subs[0] if subs else None)
        status = str(getattr(sub, "status", "")).lower()
        if sub and ("complete" in status or "error" in status):
            break
        print("   en attente du score…")
    if sub is None:
        sys.exit("Aucune soumission trouvée")
    if "error" in str(sub.status).lower():
        sys.exit(f"Erreur Kaggle : {sub.error_description}")
    pub, priv = sub.public_score or "", sub.private_score or ""
    print(f"✅ public {pub}  private {priv or '—'}")
    readme = d / "README.md"
    txt = readme.read_text()
    row = (f"| {dt.date.today()} | {args.message} | {args.cv or ''} | {pub} | {priv} | {f.name} |")
    lines = txt.splitlines()
    # insère après la dernière ligne du tableau Scores (en retirant la ligne vide d'exemple)
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().lower() == "## scores")
    except StopIteration:
        lines += ["", "## Scores", "", "| Date | Version | CV | Public LB | Private LB | Notes |",
                  "|---|---|---|---|---|---|"]
        start = len(lines) - 4
    i = start + 1
    while i < len(lines) and not lines[i].startswith("|"):
        i += 1
    end = i
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    table = [l for l in lines[i:end] if l.replace("|", "").strip()]
    lines[i:end] = table + [row]
    readme.write_text("\n".join(lines) + "\n")
    print(f"→ score loggé dans {readme.relative_to(REPO)}")


def cmd_scores(args):
    for s in submissions(api(), args.slug)[:10]:
        print(f"{str(s.date)[:16]}  {s.public_score or '-':>10}  {s.private_score or '-':>10}  {s.description}")


def main():
    p = argparse.ArgumentParser(prog="kg", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    n = sp.add_parser("new", help="nouvelle compétition")
    n.add_argument("slug")
    n.add_argument("--type", choices=TYPES)
    n.set_defaults(fn=cmd_new)
    s = sp.add_parser("submit", help="soumettre et logger le score")
    s.add_argument("slug")
    s.add_argument("file")
    s.add_argument("-m", "--message", required=True)
    s.add_argument("--cv", help="score CV à logger avec la soumission")
    s.set_defaults(fn=cmd_submit)
    sc = sp.add_parser("scores", help="dernières soumissions")
    sc.add_argument("slug")
    sc.set_defaults(fn=cmd_scores)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
