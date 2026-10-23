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
