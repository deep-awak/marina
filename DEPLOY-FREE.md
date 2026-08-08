# Utiliser marina gratuitement via GitHub Actions

Pas de Docker, pas de Render, pas de serveur a payer : GitHub compile
et execute marina a la demande, dans les minutes gratuites de ton
compte GitHub (largement suffisant pour un usage personnel/etudiant).

## 1. Pousser le fichier sur GitHub
```bash
cd marina-main
git add .github/workflows/solve.yml
git commit -m "Add on-demand solve workflow"
git push
```

## 2. Lancer une resolution
1. Va sur ton repo GitHub -> onglet **Actions**.
2. Dans la liste a gauche, clique sur **Solve**.
3. Clique sur **Run workflow** (bouton a droite).
4. Renseigne le champ **formula** avec ta proposition logique, par
   exemple :
   ```
   (a&b | c)->d <-> ~e
   ```
5. Clique **Run workflow**. Une nouvelle execution demarre.

## 3. Voir le resultat
1. Clique sur l'execution qui vient de se lancer (dans la liste des
   runs de "Solve").
2. Une fois terminee (icone verte), le resultat est affiche
   directement dans le **Summary** de l'execution (en haut de la
   page), sous "Resultat" -- pas besoin de fouiller dans les logs.

C'est tout : chaque run est independant, gratuit, et tu peux en
lancer autant que tu veux avec des formules differentes.
