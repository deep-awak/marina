# Deployer marina en Web Service gratuit sur Render

## Ce que ca ajoute
- `server.py` -- petit serveur HTTP (uniquement la bibliotheque
  standard Python, aucune dependance a installer) qui expose :
  - `GET /` -- une page avec un formulaire pour entrer une formule
  - `GET /solve?formula=...` -- endpoint texte brut, pratique avec
    `curl`
  - `GET /healthz` -- utilise par Render pour verifier que le
    service est vivant
- `Dockerfile` -- compile toujours marina avec OCaml/opam, puis
  l'image finale est basee sur `python:3.12-slim` avec le binaire
  et `server.py` copies dedans.
- `render.yaml` -- declare le service comme **Web Service**, plan
  **free**.

## 1. Tester en local (optionnel)
```bash
docker build -t marina-web .
docker run --rm -p 8000:8000 -e PORT=8000 marina-web
# puis ouvre http://localhost:8000
```

## 2. Pousser sur GitHub
```bash
cd marina-main
git add Dockerfile server.py render.yaml DEPLOY-RENDER-FREE.md
git commit -m "Deploy marina as a free Render web service"
git push
```

## 3. Deployer sur Render (gratuit)
### Option A -- via Blueprint
1. [dashboard.render.com](https://dashboard.render.com) -> **New +**
   -> **Blueprint**.
2. Selectionne le repo `marina`.
3. Render detecte `render.yaml` et propose de creer le service
   `marina-solver` (type **Web Service**, runtime Docker, plan
   **Free**). Valide.

### Option B -- manuelle
1. **New +** -> **Web Service**.
2. Connecte le repo `marina`.
3. Runtime : **Docker** (le `Dockerfile` est detecte automatiquement).
4. Plan : **Free**.
5. Cree le service.

## 4. Tester le deploiement
Une fois le build termine, Render donne une URL du type :
```
https://marina-solver.onrender.com
```
- Ouvre-la dans un navigateur : tu verras le formulaire.
- Ou en ligne de commande :
  ```bash
  curl "https://marina-solver.onrender.com/solve?formula=(a%26b%20%7C%20c)-%3Ed%20%3C-%3E%20~e"
  ```
  (les caracteres speciaux doivent etre URL-encodes ; le formulaire
  web s'en charge tout seul, pas besoin d'encoder a la main si tu
  passes par le navigateur.)

## A savoir sur le plan gratuit Render
- Le service **s'endort apres ~15 minutes d'inactivite**. La
  premiere requete apres une periode d'inactivite peut prendre
  30-60 secondes le temps qu'il redemarre (cold start) -- c'est
  normal, pas un bug.
- 750h d'execution gratuite par mois, largement suffisant pour un
  usage perso/demo.
- Pas de carte bancaire requise pour ce plan.
