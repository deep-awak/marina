# Déployer marina avec Docker, GitHub et Render

## Ce qui a été ajouté
- `Dockerfile` — build multi-étapes : compile marina avec OCaml/opam, puis
  copie le binaire dans une image Debian minimale (aucune dépendance
  runtime à OCaml, car le `Makefile` compile déjà en mode `-custom`).
- `docker-entrypoint.sh` — exécute `./marina "$PROP"`, où `PROP` est la
  formule à résoudre.
- `.dockerignore` — exclut le `.git`, la doc, les artefacts de build.
- `render.yaml` — Blueprint Render qui déploie l'image comme **Cron Job**,
  déclenchable à la demande.

## 1. Tester en local (optionnel mais recommandé)
```bash
docker build -t marina .
docker run --rm -e PROP='(a&b | c)->d <-> ~e' marina
# ou directement :
docker run --rm marina '(a&b | c)->d <-> ~e'
```

## 2. Pousser sur GitHub
```bash
cd marina-main
git init                     # si ce n'est pas déjà un repo git
git add Dockerfile docker-entrypoint.sh .dockerignore render.yaml DEPLOY.md
git commit -m "Add Docker + Render deployment"
git branch -M main
git remote add origin git@github.com:<ton-user>/marina.git
git push -u origin main
```
(Remplace `<ton-user>` par ton compte GitHub ; crée le repo vide sur
GitHub avant si besoin, sans README/licence pour éviter les conflits.)

## 3. Déployer sur Render en tant que Cron Job
Deux façons de faire, choisis l'une des deux :

### Option A — via le Blueprint (`render.yaml`), automatique
1. Sur [render.com](https://dashboard.render.com), clique **New +** →
   **Blueprint**.
2. Connecte ton compte GitHub et sélectionne le repo `marina`.
3. Render détecte `render.yaml` et propose de créer le service
   `marina-solver` (type Cron Job, runtime Docker). Valide.
4. Une fois créé, va dans les **Environment Variables** du service et
   ajuste `PROP` avec la formule que tu veux tester (elle est marquée
   `sync: false`, donc Render te demande de la définir toi-même).

### Option B — création manuelle dans le dashboard
1. **New +** → **Cron Job**.
2. Connecte le repo GitHub `marina`.
3. Runtime : **Docker** (Render détecte le `Dockerfile` à la racine).
4. Schedule : mets par exemple `0 0 1 1 *` (1x/an) — ça ne sert qu'à
   satisfaire le champ obligatoire, tu ne l'utiliseras pas vraiment.
5. Ajoute la variable d'environnement `PROP` avec ta formule.
6. Crée le service.

## 4. Lancer une exécution à la demande
Un Cron Job Render ne se lance pas tout seul en dehors de son
planning — mais tu peux le déclencher manuellement à tout moment :
va sur la page du service → bouton **Trigger Run**. Les logs de
sortie (le résultat de `marina`) s'affichent dans l'onglet **Logs**.

## Pour changer de formule à chaque run
Comme `PROP` est une variable d'environnement statique, il faut la
modifier dans le dashboard Render avant chaque `Trigger Run` si tu
veux tester une formule différente. Si tu veux plutôt passer la
formule dynamiquement à chaque appel (par ex. via une requête HTTP),
il faudrait plutôt déployer marina comme **Web Service** avec un
petit wrapper HTTP — dis-le-moi si tu préfères cette approche, je
peux l'ajouter.
