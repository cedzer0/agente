# Agenté

Je fabrique des agents IA, je les regarde se casser la figure, et je note ce que j'apprends.

## Ce que c'est

Agenté est un blog où je consolide ce que je découvre en jouant avec les agents IA : les features d'Hermes, les outils, les montages multi-agents. Chaque article part d'une question simple (« qu'est-ce qu'un agent ? ») et finit avec du code qui tourne, pas avec une opinion. Tout ce qui est publié a été relu et validé avant de sortir.

## Comment c'est construit

MkDocs Material (thème slate sombre, accents indigo/ambre), déployé sur GitHub Pages à chaque push sur `main`.

## Le format des articles

Chaque article suit le même fil : concept → use case → architecture → code → résultats.

## Ajouter un article

1. Crée un fichier `docs/articles/NNN-titre-de-l-article.md` (NNN = numéro suivant).
2. Écris-le en suivant le format : concept, use case, architecture, code, résultats.
3. Ajoute le lien dans le tableau `## Articles` de `docs/index.md`.
4. Pousse sur `main` : GitHub Actions build le site et le déploie sur la branche `gh-pages`.

## Le site

[https://cedzer0.github.io/agente/](https://cedzer0.github.io/agente/)
