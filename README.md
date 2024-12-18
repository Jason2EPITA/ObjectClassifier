## Jason Perez
## Samy Hadj-said

# Présentation des Projets

Ce dépôt contient deux projets distincts mettant en œuvre des concepts avancés de machine learning et de déploiement de modèles. Voici un aperçu des deux projets :

## 1. Système Embarqué - Modèle de Détection d’Objets

### Description
Le but de ce projet est de faire fonctionner un modèle de détection d’objets (comme YOLO ou Tiny YOLO) sur un dispositif embarqué tel qu’un téléphone portable, un Raspberry Pi ou une autre cible similaire.

### Étapes principales
1. **Modèle** : Entraîner ou utiliser un modèle pré-entraîné pour la détection d’objets.
2. **Dataset** : Utilisation de datasets adaptés, comme :
   - Reconnaissance des déchets plastiques ([Surfrider Dataset](https://github.com/m2dsupsdlclass/project))
   - Détection de plantes malades pour l’agriculture
   - Surveillance d’incidents/incendies
3. **Optimisation** : Implémentation d’optimisations telles que la quantification ou la distillation pour améliorer la performance du modèle sur le dispositif embarqué.
4. **Dispositif cible** : Intégration et test du modèle sur la plateforme embarquée (téléphone, Raspberry Pi, etc.).

### Fichiers principaux
- **notebook/** : Scripts et entraînement du modèle
- **xcode/** : Intégration iOS
- **slides.pdf** : Présentation du projet

---

## 2. MLOps - Mise en Production d'un Modèle de Machine Learning

### Description
Ce projet a pour objectif de mettre en production un modèle de machine learning non trivial à travers une architecture modulaire et dockerisée.

### Étapes principales
1. **Modèle** : Utilisation d’un modèle avancé, par exemple pour la classification d’images ou la détection d’objets.
2. **Déploiement** : Mise en place des services via différentes modalités :
   - Web Service (API Flask)
   - Interface utilisateur (Streamlit)
   - Orchestration avec Docker Compose

### Fichiers principaux
- **app.py** : Service d’API (Flask)
- **streamlit_live.py** : Interface utilisateur (Streamlit)
- **docker-compose.yml** : Orchestration des services
- **best.pt** : Modèle entraîné

---

## Organisation du Répertoire
- **systEmbarque/** : Contient les fichiers liés au projet de système embarqué.
- **MLOPS_lvl0/** : Contient les fichiers liés au projet de mise en production.