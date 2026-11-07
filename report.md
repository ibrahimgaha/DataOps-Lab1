# Rapport TP2 — Versionner le code avec Git et les données avec DVC

## 1. Objectif du TP

L'objectif de ce TP est d'apprendre à versionner séparément le code et les données d'un pipeline de traitement de données.

- **Git** permet de suivre les modifications du code, de créer des branches et de fusionner les changements.
- **DVC (Data Version Control)** permet de versionner les données volumineuses sans stocker directement leur contenu dans Git.
- **Un remote DVC** permet de stocker les données pour qu'un autre membre de l'équipe puisse les récupérer.
- **La reproductibilité** consiste à pouvoir retrouver les versions exactes du code et des données utilisées pour produire un résultat.

## 2. Outils et environnement utilisés

| Outil | Rôle |
|---|---|
| Python | Exécution du pipeline de traitement des données |
| pandas | Manipulation et transformation des données |
| pytest | Exécution des tests automatisés |
| Git | Versionnement du code et gestion des branches |
| DVC | Versionnement et récupération des données |
| CMD (Windows) | Exécution des commandes |
| Environnement virtuel Python | Isolation des dépendances du projet |

## 3. Réponses aux questions

### Étape 1 — Gestion du code avec Git

**Q1. Pendant que vous travailliez sur la branche, `main` contenait-elle la règle 6 ? À quelle commande est-elle apparue sur `main` ? Pourquoi est-ce utile si le rapport tourne chaque nuit depuis `main` ?**

Non. Pendant le développement sur `feature/country-rule`, la règle 6 était présente dans cette branche, mais pas encore dans `main`. Elle a été intégrée à `main` avec la commande `git merge --no-ff feature/country-rule -m "Merge the country rule"`.

Cette méthode permet de développer et de tester une modification séparément avant de l'intégrer au code principal. Elle réduit le risque de perturber un pipeline exécuté régulièrement.

**Q2. Dans une vraie équipe, que permet une pull request GitHub qu'un `git merge` local n'apporte pas ?**

Une pull request permet de proposer une modification aux autres membres de l'équipe avant son intégration. Elle facilite la revue du code, les commentaires, la discussion, la vérification automatique des tests et l'approbation par un responsable. Un `git merge` local réalise la fusion, mais ne fournit pas à lui seul ce processus collaboratif.

### Étape 2 — Versionnement des données avec DVC

**Q3. Que représente la ligne `md5` de `data/raw.dvc` ? Que se passe-t-il si un seul caractère d'un CSV change ?**

La ligne `md5` contient une empreinte qui identifie le contenu suivi par DVC. Elle permet de détecter une modification des données. Si un caractère d'un CSV change, le contenu n'a plus la même empreinte et DVC détecte que les données ont été modifiées.

**Empreinte de mon projet :** à compléter en recopiant la valeur exacte de la ligne `md5` dans `data/raw.dvc`.

**Q4. Les CSV restent sur le disque, mais Git ne les suit plus. Quel fichier les fait ignorer par Git ?**

Le fichier `data/.gitignore` contient la règle `/raw`, qui indique à Git d'ignorer le dossier `data/raw`. Les données restent présentes localement et sont gérées par DVC, tandis que Git suit notamment le fichier pointeur `data/raw.dvc`.

### Étape 3 — Remote DVC

**Q5. Les fichiers dans `dvc-storage` ne s'appellent pas `orders_day1.csv`. Comment sont-ils nommés et pourquoi est-ce utile ?**

DVC stocke les objets dans une structure organisée à partir de leur empreinte, notamment sous `files/md5/`. Les données sont ainsi identifiées par leur contenu plutôt que par leur nom d'origine. Cette organisation facilite la détection des modifications, la réutilisation des objets identiques et le stockage de plusieurs versions.

Le remote de ce TP est un dossier local nommé `dvc-storage`, situé à côté du projet.

### Étape 4 — Création d'une nouvelle version des données

**Q6. Pourquoi les deux lignes modifiées dans `data/raw.dvc` suffisent-elles à Git alors que les données ont changé ? Pourquoi faut-il quand même faire un commit ?**

Git n'a pas besoin de stocker à nouveau le contenu complet des CSV. Le fichier `data/raw.dvc` contient un pointeur et une empreinte permettant à DVC d'identifier la version des données. Quand l'empreinte change, Git peut enregistrer cette modification du pointeur.

Le commit permet de conserver un historique de cette version et de la relier aux autres modifications du projet. Les objets de données doivent également être envoyés vers le remote avec `dvc push`.

**Q7. Entre `data-v1` et `data-v2`, le code a-t-il changé ? Quels sont les deux totaux ?**

La modification de `data-v2` correspond à l'ajout de cinq commandes en retard. Cette étape ne nécessite pas de modification du code : elle crée une nouvelle version des données.

Les totaux attendus dans l'énoncé sont :

- `data-v1` : **7 655,90**
- `data-v2` : **8 835,40**

Ces montants sont les résultats attendus par le TP. Dans mon environnement, une exécution du pipeline s'est arrêtée au contrôle de qualité, car le taux de rejet dépassait la limite configurée de 10 %. Les deux totaux doivent donc être considérés comme les valeurs attendues et non comme des résultats d'exécution confirmés dans mon environnement.

### Étape 5 — Retour à une ancienne version

**Q8. Que changent `git checkout data-v1 -- data/raw.dvc` et `dvc checkout` ?**

La commande `git checkout data-v1 -- data/raw.dvc` restaure le fichier pointeur DVC correspondant au tag `data-v1`.

Ensuite, `dvc checkout` utilise ce pointeur pour restaurer localement la version des données correspondante, à partir du cache DVC disponible.

Git restaure donc la référence de version, tandis que DVC restaure les fichiers de données associés.

**Q9. Que se passe-t-il si on oublie `dvc checkout` ? Pourquoi est-ce dangereux pour un rapport ?**

Si on restaure uniquement le pointeur Git sans exécuter `dvc checkout`, les fichiers de données locaux peuvent toujours correspondre à la version précédente ou à une autre version. Le code et les données peuvent donc ne pas être synchronisés.

Cela peut produire un rapport incorrect ou empêcher son exécution. Il faut restaurer à la fois la bonne référence Git et les données correspondantes avec DVC.

### Étape 6 — Reproductibilité pour un collègue

**Q10. Qu'est-ce que `git clone` donne au collègue, et qu'est-ce que `dvc pull` lui donne ?**

`git clone` récupère le dépôt Git : le code source, l'historique des commits, les branches et les fichiers pointeurs DVC versionnés dans Git.

`dvc pull` récupère depuis le remote DVC les objets de données nécessaires et restaure les fichiers de données dans le projet du collègue.

Les deux commandes sont complémentaires : Git fournit le code et les références, tandis que DVC fournit les données correspondantes.

**Q11. Que se passerait-il si `dvc push` était oublié à l'étape 4 ?**

Le dépôt Git pourrait contenir le pointeur de `data-v2`, mais le remote DVC pourrait ne pas contenir les nouveaux objets correspondant à cette version. Le collègue risquerait alors de ne pas pouvoir récupérer les données avec `dvc pull`.

Il ne pourrait donc pas reproduire correctement le résultat de `data-v2`. Le total attendu de 8 835,40 ne serait pas garanti ; la récupération pourrait échouer parce que les données nécessaires sont absentes du remote.

### Q12. Quelles difficultés de la séance 1 ce TP permet-il de réduire, et à quelles étapes ?

Ce TP contribue à réduire les quatre difficultés suivantes :

- **Livraison lente :** les branches Git et les fusions structurées facilitent le développement des changements ; le remote DVC facilite le partage des données.
- **Erreurs silencieuses :** les règles de validation du pipeline et les tests pytest aident à détecter les données invalides et les régressions.
- **« Ça marche sur ma machine » :** les versions Git et DVC permettent à un collègue de récupérer le même code et les données correspondantes grâce à `git clone` et `dvc pull`.
- **Étapes manuelles :** les commandes reproductibles de Git et DVC facilitent le suivi des versions et la restauration des données. L'automatisation complète du pipeline pourra être renforcée avec les étapes DVC et la CI/CD.

## 4. Historique Git du projet

La commande utilisée est :

`git log --oneline --graph --decorate`

Sortie obtenue :

```text
*   3b85821 (HEAD -> main) Merge the country rule
|\
| * ce77269 (feature/country-rule) Reject orders from countries the shop does not sell to
|/
* 1247ad3 (tag: data-v2) Data v2: late orders for 2026-10-05
* 0019df1 Add the DVC remote
* 2500b76 (tag: data-v1) Track raw data with DVC
* 97e3a65 Add DVC to requirements
* f766a16 (origin/main) workfow
* 6acaba4 first commit
```

Cet historique montre le développement de la règle métier dans une branche dédiée, la fusion dans `main`, la configuration du remote DVC et les deux versions de données identifiées par `data-v1` et `data-v2`.

## 5. Remarque sur les vérifications

Le projet utilise Git pour versionner le code et les pointeurs DVC, et un remote local pour stocker les objets de données. La création des tags `data-v1` et `data-v2`, ainsi que la fusion de la branche `feature/country-rule`, sont visibles dans l'historique Git.

Deux différences avec les vérifications de l'énoncé doivent être signalées :

1. Le dossier `data/raw` de mon projet contient un seul CSV, alors que le document du TP en prévoit trois.
2. Une exécution du pipeline s'est arrêtée lors du contrôle du taux de rejet, car 5 lignes sur 30 étaient rejetées, soit environ 16,7 %, au-dessus de la limite de 10 %. Après l'ajout de cinq lignes valides, le contrôle peut encore échouer si les cinq rejets initiaux sont toujours présents.

Ces points doivent être corrigés ou vérifiés avant de déclarer que tous les résultats numériques attendus ont été reproduits.

## 6. Conclusion

Ce TP m'a permis de pratiquer les principales bases du DataOps : le versionnement du code avec Git, le travail sur une branche, la fusion des modifications, le versionnement des données avec DVC, le stockage dans un remote et la restauration de versions précédentes.

L'utilisation conjointe de Git et DVC facilite le partage du projet et améliore la traçabilité des résultats. Pour garantir une reproductibilité complète, il reste important de vérifier le passage des tests, la cohérence des données et le bon fonctionnement du pipeline.


## TP3

### Lancer le projet sous PowerShell

Exécuter ces commandes depuis la racine de `dataops-lab1` avec Python 3.11 et le CSV du jour 1 dans `data/raw`.

```powershell
py -3.11 -m venv .venv-tp3
.\.venv-tp3\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-tp3\Scripts\python.exe load_raw.py data/raw/orders_day1.csv
.\.venv-tp3\Scripts\dbt.exe build --profiles-dir .
.\.venv-tp3\Scripts\python.exe query.py "select sum(revenue) as total from revenue_by_country"
```

Si `.venv-tp3` contient déjà les dépendances, commencer au chargement. Utiliser `dbt build` pour exécuter les modèles et leurs tests dans l'ordre du lignage.

### Du CSV au rapport

Dans le TP1, Python lit le CSV, le transforme puis écrit le rapport. Dans le TP3, Python lit le CSV et le charge dans DuckDB. Les transformations SQL s'exécutent ensuite dans DuckDB sous le contrôle de dbt. DuckDB conserve les données dans le fichier local `warehouse.duckdb`.

1. `raw.orders` contient les champs bruts et trois colonnes de provenance.
2. `stg_orders` donne un type aux champs et normalise les noms de pays.
3. `int_orders_checked` applique les six règles dans l'ordre. La première règle qui échoue donne le motif.
4. `orders_clean` et `orders_rejected` séparent les commandes valides des rejets. `revenue_by_country` additionne `quantity * unit_price` par pays à partir des commandes valides.

### Réponses Q1 à Q15

**Q1. Pourquoi charger les champs en texte ?** Une quantité `deux` reste visible dans le brut. Le staging peut la convertir en `NULL` et le modèle de contrôle peut classer la ligne comme `invalid_quantity`. Le type deviné à l'import pourrait varier d'un fichier à l'autre.

**Q2. Pourquoi le calcul naïf donne-t-il le même résultat en SQL et en Python ?** Les deux calculs comptent des lignes qui auraient dû être exclues. La fiabilité dépend des règles métier et des tests qui vérifient leur application.

**Q3. À quoi sert le brut si une règle change ?** On peut corriger le SQL et rejouer dbt sur le lot brut courant, puis comparer les décisions de nettoyage. Pour un lot plus ancien, on recharge son CSV versionné avec DVC.

**Q4. Que changer dans le profil pour un autre entrepôt ?** Il faut choisir l'adaptateur du nouvel entrepôt et renseigner ses paramètres de connexion, comme le compte, la base et le schéma. Un secret vient d'une variable d'environnement ou d'un gestionnaire de secrets. dbt peut le lire avec `env_var()`.

**Q5. Pourquoi conserver la commande 1013 au staging ?** Elle doit entrer dans le calcul du taux de rejet et apparaître en quarantaine avec le motif `invalid_date`.

**Q6. Comment fonctionne la vue de staging ?** DuckDB exécute la requête de la vue quand on la lit. Les conversions sont légères et la vue évite de stocker une copie intermédiaire du lot.

**Q7. Que devient `ref('stg_orders')` ?** dbt le remplace par le nom qualifié de la vue, `"warehouse"."main"."stg_orders"`, dans le SQL compilé.

**Q8. Comment le SQL garde-t-il le premier doublon ?** `partition by order_id` crée un groupe par identifiant. Dans chaque groupe, le tri sur `_row_number` reprend l'ordre du CSV. La ligne de rang 1 reste la première commande et les suivantes sont signalées comme doublons.

**Q9. Où ajouter un chiffre d'affaires par produit ?** Créer `models/marts/revenue_by_product.sql`, partir de `ref('orders_clean')` et regrouper les lignes par `product`. Ce changement se fait en SQL.

**Q10. Que se passe-t-il si on retire la règle des doublons ?** Pour refaire l'expérience de l'étape 5, on lance `dbt build --exclude test_type:unit --profiles-dir .`. Le test `unique_orders_clean_order_id` échoue. dbt saute `revenue_by_country` et son test `unique_revenue_by_country_country`, ce qui conserve le rapport précédent. Avec la suite complète, le test unitaire du doublon détecte aussi la régression, avant la création de `int_orders_checked`.

**Q11. Quels contrôles reprennent ceux du pipeline Python ?**

| Contrôle Python | Équivalent dans TP3 |
| --- | --- |
| `check_schema` | Le staging nomme explicitement les champs attendus. DuckDB signale les colonnes manquantes et le test du lot bloque aussi les fichiers sans données. |
| Six règles de `clean_orders` | Le `case` de `int_orders_checked.sql` renseigne le premier motif de rejet. |
| `check_reject_rate` | `assert_reject_rate_below_20_percent` arrête le lot si plus de 20 % des lignes sont rejetées. |
| `rejected_orders.csv` | Table `orders_rejected`. |
| `PIPELINE STOPPED` | `dbt build` échoue et saute les modèles qui dépendent du contrôle en échec. |

**Q12. D'où viennent les données des tests unitaires ?** Elles sont écrites dans `given` dans le YAML. dbt remplace les lignes d'entrée par ces petits exemples, puis compare la sortie à `expect`. Les cas restent reproductibles en CI même si le fichier du fournisseur change. Dans ce projet, `dbt build` crée d'abord la vue de staging dont dbt lit les types pour préparer les exemples.

**Q13. Quels modèles sont touchés si `country` arrive vide ?** `stg_orders`, `int_orders_checked`, `orders_clean`, `orders_rejected` et `revenue_by_country`. Avec le graphe, on suit ces dépendances en quelques secondes. Avec 200 scripts, il faudrait rechercher puis remonter les références à la main.

**Q14. Que se passe-t-il sur les jours 2 et 3 ?** Les fichiers originaux des jours 2 et 3 manquent dans le dépôt et le stockage DVC local. Les vérifications utilisent deux copies temporaires du jour 1. La première exprime chaque prix en centimes. La seconde renomme `unit_price` en `price`. Les CSV suivis par DVC restent ceux du TP2.

| Vérification | Pipeline Python du TP2 | Pipeline dbt du TP3 |
| --- | --- | --- |
| Jour 2 | `check_reject_rate` dépasse la limite Python de 10 %. | Le test `assert_reject_rate_below_20_percent` échoue. |
| Jour 3 | `Missing columns: ['unit_price']`. | DuckDB signale que `src` ne possède pas la colonne `unit_price` dans `stg_orders`. |
| Rapport précédent conservé | Oui, les deux contrôles interviennent avant l'écriture du CSV. | Oui, `revenue_by_country` est sauté et garde le total de `8835.40`. |
| Code de sortie des deux échecs | `1` | `1` |

**Q15. Comment garder les rejets d'un lot bloqué ?** Écrire les rejets dans une table d'audit séparée, identifiée par le fichier et la date de chargement, avant le contrôle du taux. Le contrôle continue de bloquer la publication du chiffre d'affaires.

### Vérifications

Le jour 1 contient 35 lignes, dont 30 valides et 5 rejetées. Le total naïf est `13950.60`. Avec les six règles, le rapport donne le même résultat que la transformation Python.

| Pays | Chiffre d'affaires |
| --- | ---: |
| France | 1646.50 |
| Germany | 542.50 |
| Italy | 2980.40 |
| Morocco | 2113.50 |
| Tunisia | 1552.50 |
| **Total** | **8835.40** |

La commande TP2 complète s'arrête sur le jour 1 car 5 rejets sur 35 représentent 14,29 %, au-dessus de sa limite de 10 %. La comparaison porte donc sur le résultat des fonctions Python de nettoyage et d'agrégation. Le seuil du TP3 est de 20 %.

Résultat de `dbt build` sur le jour 1 avec dbt Core 1.12.6.

```text
Done. PASS=14 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=14
```

Ces commandes ouvrent la documentation du lignage.

```powershell
.\.venv-tp3\Scripts\dbt.exe docs generate --profiles-dir .
.\.venv-tp3\Scripts\dbt.exe docs serve --port 8081 --profiles-dir .
```

Ouvrir [la documentation locale](http://localhost:8081), puis choisir `revenue_by_country` et la sélection `+revenue_by_country`. Le chemin principal est `raw.orders → stg_orders → int_orders_checked → orders_clean → revenue_by_country`. La quarantaine part de `int_orders_checked`.


## TP4

### Où passent les contrôles

L'ancien workflow GitHub était en échec. Son YAML avait des étapes mal indentées et il cherchait un CSV suivi par DVC. Une machine neuve de GitHub récupère le dépôt Git sans les fichiers bruts du stockage DVC local. Le nouveau workflow utilise donc un échantillon fixe de 35 commandes dans `tests/fixtures/orders_sample.csv`.

1. Le contrat ODCS dans `contracts/orders.yaml` décrit les colonnes et les champs obligatoires. Le contrat peut accepter des prix en centimes, car ces prix restent des nombres.
2. Pandera vérifie le fichier avant toute connexion à DuckDB. Il refuse le lot si une colonne manque, si une colonne inattendue apparaît ou si moins de 80 % des prix se situent entre 0,01 et 1000. Le client peut rester vide pour que dbt classe la ligne en quarantaine.
3. dbt applique les six règles métier à chaque commande et teste les modèles. Une seule quantité négative peut aller en quarantaine sans bloquer tout le fichier.
4. `report_md.py` imprime le tableau de chiffre d'affaires. Avec un total attendu en argument, il retourne le code 1 si le total réel diffère.

### Vérifier sur Windows

Depuis la racine du projet, avec l'environnement Python 3.11 `.venv-tp4` installé.

```powershell
.\.venv-tp4\Scripts\ruff.exe check .
.\.venv-tp4\Scripts\python.exe -m pytest
.\.venv-tp4\Scripts\datacontract.exe lint contracts/orders.yaml
.\.venv-tp4\Scripts\datacontract.exe test --server ci contracts/orders.yaml
.\.venv-tp4\Scripts\python.exe load_raw.py tests/fixtures/orders_sample.csv
.\.venv-tp4\Scripts\dbt.exe build --profiles-dir .
.\.venv-tp4\Scripts\python.exe report_md.py 8835.40
```

Pour créer cet environnement sur une autre machine, exécuter `py -3.11 -m venv .venv-tp4`, puis `.\.venv-tp4\Scripts\python.exe -m pip install -r requirements.txt`. TP4 utilise DuckDB 1.x, compatible avec l'outil de contrat. Si l'entrepôt a été créé par DuckDB 2.x, le reconstruire à partir du CSV. Le total de référence est `8835.40`. Passer `9999` à `report_md.py` déclenche le message `REGRESSION` et le code de sortie 1.

Les CSV originaux des jours 2 et 3 manquent. Pour reproduire les deux cas, j'ai utilisé des copies temporaires du jour 1 avec les prix en centimes et avec la colonne `unit_price` renommée `price`.

| Entrée | Contrat | Pandera |
| --- | --- | --- |
| Échantillon du jour 1 | Accepté | Accepté |
| Prix en centimes | Acceptés comme nombres | Lot refusé à cause de l'échelle des prix |
| Colonne `price` | `unit_price` manquante | `price` en trop et `unit_price` manquante |

### Vérifications sur GitHub

La CI exécute `lint`, puis `python-tests`, puis `data-quality`. Un échec empêche les jobs dépendants de démarrer. Le dernier job ajoute le tableau de revenus au résumé et conserve `run_results.json` dans l'artefact `dbt-results`.

Le workflow Nightly tourne chaque jour à 05 h 00 UTC et peut être lancé à la main. Il reconstruit le projet avec l'échantillon et conserve la documentation dbt dans l'artefact `dbt-docs`.


## TP4 bis

### Vérifier le projet sous PowerShell

Exécuter depuis la racine de `dataops-lab1`. L'environnement `.venv-tp4` fournit dbt et le contrat ODCS. L'environnement `.venv-soda` garde les dépendances de Soda séparées.

```powershell
. .\.venv-tp4\Scripts\Activate.ps1
python -m pip install pre-commit sqlfluff
pre-commit install
pre-commit run --all-files
sqlfluff lint models data_tests
python load_raw.py tests/fixtures/orders_sample.csv
dbt build --profiles-dir .
dbt source freshness --profiles-dir .
python report_md.py 8835.40
.\.venv-soda\Scripts\soda.exe scan -d shop -c soda/configuration.yml soda/checks.yml
```

Pour créer l'environnement Soda, exécuter `py -3.11 -m venv .venv-soda`, puis `.\.venv-soda\Scripts\python.exe -m pip install soda-core-duckdb`.

### Les cinq défis

1. **pre-commit** vérifie les fichiers avant le commit. Un import inutilisé déclenche `F401` et un fichier ajouté de 600 000 octets dépasse le seuil de 500 Ko. L'échantillon CSV est exclu des deux hooks qui modifient les fins de ligne pour conserver la copie exacte du jour 1.
2. **SQLFluff** relit le SQL DuckDB après avoir interprété les références Jinja. La règle `AM04` est désactivée pour conserver les projections `SELECT *` de ces modèles internes. La règle `ST06` est désactivée pour conserver l'ordre des colonnes transmis par le staging. Le build garde 14 succès et le total de `8835.40`.
3. **dbt** exige les colonnes `country` et `revenue` à la sortie. Le contrôle de fraîcheur utilise `_loaded_at` et avertit après 12 heures, puis échoue après 24 heures. Pour simuler une source trop vieille, le test local a décalé l'horodatage dans un entrepôt de test. L'expérience sans `Germany` avertit sans bloquer le rapport. Avec `--store-failures`, la table d'audit montre `Germany` et le nombre de lignes concernées.
4. **GitHub Actions** publie le total sur la pull request et annule l'exécution précédente quand une nouvelle la remplace. Le filtre Markdown regarde l'ensemble du diff d'une pull request. Un commit Markdown ajouté à une pull request qui contient du code peut donc relancer la CI. Une pull request dont le diff est entièrement Markdown est ignorée.
5. **Soda** lit l'entrepôt sans le modifier. Ses sept contrôles vérifient le rapport et les commandes valides. Le test volontaire avec six pays échoue parce que le rapport en contient cinq. Le fichier est lisible avec DuckDB 1.5.6 dans le projet et DuckDB 1.0.0 dans l'environnement Soda.

### Comparaison des outils

| Outil | Quand il tourne | Ce qu'il regarde | Ce que j'en retiens |
| --- | --- | --- | --- |
| pre-commit | Avant chaque commit local | Les fichiers du commit | Je vois les erreurs simples avant de pousser. |
| Ruff et SQLFluff | En local et en CI | Le Python et le SQL | Les mêmes règles de style s'appliquent à toute l'équipe. |
| Contrat ODCS | Avant le chargement | La forme du fichier fournisseur | Un renommage de colonne devient un échec explicite. |
| Pandera | Au chargement | Le fichier entier | Je peux refuser un lot dont les prix ont changé d'unité. |
| Tests et contrats dbt | Pendant `dbt build` | Les tables construites | Je vérifie les règles métier et la structure du résultat. |
| Fraîcheur dbt | Avec `dbt source freshness` | L'âge du dernier chargement | Une table correcte peut contenir des données trop anciennes. |
| Soda | À la demande | Les tables accessibles dans l'entrepôt | Je peux vérifier une table créée par un autre outil. |
| GitHub Actions | Sur les PR et les exécutions planifiées | Les commandes de chaque workflow | Tout le monde voit le résultat des mêmes vérifications. |

**R8. Mes trois choix pour le projet de semestre.** Je garde **Pandera** pour refuser un mauvais lot à l'entrée, **dbt** pour construire et vérifier les résultats métier, et **GitHub Actions** pour lancer automatiquement les contrôles de l'équipe.

Essai du filtre Markdown de GitHub Actions.
