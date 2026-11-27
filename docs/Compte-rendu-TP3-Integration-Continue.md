# Compte rendu du TP3 — Intégration continue avec GitHub

**Matière :** Plateforme collaborative et intégration continue (DevOps)<br>
**Établissement :** Institut Supérieur d'Informatique et de Multimédia de Sfax (ISIMS)<br>
**Année universitaire :** 2026–2027<br>
**Enseignante :** Siwar CHAABENE<br>
**Étudiant(e) :** _À compléter_<br>
**Classe / groupe :** _À compléter_<br>
**Date :** 27 novembre 2026

## Objectif

Ce TP met en place une intégration continue pour l'application FastAPI du TP2. Le travail comprend une nouvelle fonctionnalité de soustraction, des tests unitaires, la mesure de la couverture, l'analyse Pylint et leur automatisation avec GitHub Actions. GitHub remplace GitLab pour le dépôt, le pipeline et la demande de fusion (*Pull Request*).

**Dépôt GitHub :** [medjmalami/TP-3-devops](https://github.com/medjmalami/TP-3-devops)

## Environnement et commandes locales

- Python 3.11
- FastAPI et son `TestClient`
- `uv` pour installer les dépendances verrouillées
- `pytest` et `pytest-cov` pour les tests et la couverture
- Pylint pour l'analyse de qualité
- GitHub Actions pour l'exécution automatique

Installation et vérifications utilisées :

```bash
uv sync --locked --dev
uv run pytest -v
uv run pytest -v --cov=main --cov-report=term-missing \
  --cov-report=xml:coverage.xml --cov-report=html:htmlcov
uv run pylint main.py test_main.py
```

## 1. Vérification de l'application existante

Les tests de régression vérifient le point d'entrée, l'addition, le message d'accueil, la multiplication, la division, ainsi que la consultation et la suppression des éléments. Ils vérifient aussi les cas d'erreur de division par zéro et de suppression d'un élément absent.

## 2. Nouvelle fonctionnalité : soustraction

L'endpoint `GET /soustraction` reçoit deux entiers `a` et `b` et renvoie leur différence. Par exemple, la requête `/soustraction?a=5&b=3` répond avec le résultat `2` et le nom du développeur.

Le test dédié utilise `TestClient` de FastAPI et vérifie le code HTTP ainsi que le contenu JSON de la réponse. Le code est dans `main.py` et les tests dans `test_main.py`.

## 3. Tests automatisés et rapport JUnit

Le fichier `.github/workflows/ci.yml` lance `pytest -v`. Le job `run-test` produit un rapport JUnit XML et le publie sous forme d'artefact GitHub nommé `junit-test-report`, téléchargeable depuis la page du run.

## 4–5. Couverture du code

La suite finale contient **7 tests réussis**. La mesure locale et celle du pipeline indiquent **51 instructions, 0 instruction manquée, soit 100 % de couverture de lignes pour `main.py`**. Ce résultat dépasse l'objectif du TP (> 90 %).

Les tests couvrent notamment les branches de succès et d'erreur de l'API, le repli vers `127.0.0.1` si la recherche d'adresse IP échoue, et le rejet d'une division par zéro. Une couverture de 100 % indique que toutes les lignes mesurées ont été exécutées par les tests; elle ne prouve pas à elle seule que tous les comportements possibles sont corrects.

Le job `calculate-coverage` affiche le pourcentage dans le résumé du run GitHub Actions et publie les rapports XML et HTML sous forme d'artefact nommé `coverage-report`.

## 6. Qualité du code avec Pylint

Les problèmes signalés localement ont été corrigés, notamment les docstrings manquantes et un import inutilisé. Pylint obtient **10,00/10** sur `main.py` et `test_main.py`. Le job `pylint` exécute cette même vérification dans GitHub Actions.

## 7. Pull Request et résultat du pipeline

Le travail a été développé sur `feature/soustraction-with-unit-tests`, puis proposé à la fusion vers `main` via la [Pull Request #1](https://github.com/medjmalami/TP-3-devops/pull/1). La Pull Request a été fusionnée le **27 novembre 2026**. Le commit de fusion est `d5fae75`.

Le [pipeline exécuté sur `main`](https://github.com/medjmalami/TP-3-devops/actions/runs/45985388735) a réussi. Les trois jobs sont verts : `pylint`, `run-test` et `calculate-coverage`. Les logs confirment le score Pylint de 10/10, les 7 tests réussis et les 100 % de couverture. Les artefacts `junit-test-report` et `coverage-report` sont disponibles dans le run.

GitHub Actions n'organise pas les jobs en *stages* comme GitLab CI. L'ordre est obtenu avec `needs: pylint` : les jobs de test et de couverture démarrent après le succès du contrôle Pylint. Ils peuvent ensuite s'exécuter en parallèle.

## Captures d'écran à ajouter

Les résultats GitHub ont été vérifiés via les pages et les logs de la Pull Request et du run. Les tentatives de capture d'écran depuis cet environnement ont produit une page incomplète ou un écran noir; aucune de ces images n'est ajoutée au rapport. Ajouter les captures ci-dessous avant de le remettre. Les liens ouvrent directement les pages à montrer.

### Capture 1 — Exécution locale des tests

Faire une capture du terminal après `uv run pytest -v`, où apparaissent les 7 tests réussis.

> **Emplacement :** _Insérer ici la capture du terminal — par exemple `captures/01-tests-locaux.png`._

### Capture 2 — Couverture locale

Faire une capture du terminal après la commande `pytest --cov` montrant `main.py`, `51` instructions et `100%`. Le rapport HTML peut aussi être ouvert avec `uv run coverage html` puis consulté dans `htmlcov/index.html`.

> **Emplacement :** _Insérer ici la capture de la couverture — par exemple `captures/02-couverture-locale.png`._

### Capture 3 — Score Pylint

Faire une capture du terminal après `uv run pylint main.py test_main.py`, avec le score `10.00/10` visible.

> **Emplacement :** _Insérer ici la capture de Pylint — par exemple `captures/03-pylint.png`._

### Capture 4 — Résultat des jobs GitHub Actions

Ouvrir le [run sur `main`](https://github.com/medjmalami/TP-3-devops/actions/runs/45985388735) et capturer le résumé montrant les trois jobs réussis. La page permet aussi de consulter les logs et de télécharger les artefacts.

> **Emplacement :** _Insérer ici la capture du pipeline — par exemple `captures/04-github-actions.png`._

### Capture 5 — Pull Request fusionnée

Ouvrir la [Pull Request #1](https://github.com/medjmalami/TP-3-devops/pull/1) et capturer son état fusionné ainsi que les vérifications réussies.

> **Emplacement :** _Insérer ici la capture de la Pull Request — par exemple `captures/05-pull-request.png`._

## Validation des acquis

1. **Pourquoi écrire des tests unitaires ?** Ils vérifient automatiquement le comportement attendu et aident à repérer rapidement une régression après une modification.
2. **Comment la couverture aide-t-elle ?** Elle montre les parties du code exécutées par les tests et révèle des lignes non vérifiées. Une forte couverture ne remplace toutefois pas des assertions pertinentes.
3. **Faut-il créer un dépôt par développeur ?** Pour un projet d'équipe courant, un dépôt partagé avec des branches de fonctionnalité et des Pull Requests facilite la collaboration. Les forks peuvent convenir aux contributions externes ou lorsque les droits sur le dépôt principal sont limités.
4. **Quand fusionner dans `main` ?** Il est préférable de fusionner régulièrement de petites contributions relues et validées par les tests automatisés. Le travail en cours reste isolé sur une branche jusqu'à ce qu'il soit prêt.

## Conclusion

L'application dispose d'une fonctionnalité de soustraction testée et d'une suite de régression couvrant 100 % des lignes mesurées de `main.py`. GitHub Actions automatise Pylint, les tests unitaires, la génération des rapports et leur publication en artefacts. La Pull Request a été fusionnée et le pipeline sur `main` a réussi.
