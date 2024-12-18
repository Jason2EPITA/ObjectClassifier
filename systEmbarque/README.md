## Jason Perez
## Samy Hadj-said

# Détection et Classification de Matériaux Recyclables avec YOLOv5 et Core ML

Ce projet vise à développer un modèle de détection d’objets pour classifier différents matériaux recyclables (plastique, carton, verre, etc.) à partir d’images de déchets. Le modèle, entraîné avec YOLOv5, est converti au format Core ML pour être intégré dans une application iOS, optimisant ainsi la détection en temps réel sur appareil mobile.

## 📋 Contexte et Objectifs

### Problématique
- Comment convertir un modèle YOLOv5 (.pt) en Core ML tout en conservant une performance optimale pour la détection en temps réel ?

### Objectifs
1. Entraîner un modèle YOLOv5 pour classifier des matériaux recyclables.
2. Convertir le modèle entraîné en format Core ML (.mlmodel).
3. Intégrer le modèle Core ML dans une application iOS via Xcode.
4. Réduire la latence d’inférence et améliorer la robustesse du modèle.

## 📚 Dataset

Le dataset utilisé provient de **Roboflow**, intitulé “Plastic-Project-1”. Il contient des images annotées pour les catégories suivantes :

- Carton
- Verre
- Métal
- Autres
- Papier
- Plastique
- Polystyrène (Styrofoam)

### Format
- **Images** : JPEG/PNG
- **Annotations** : Format YOLO

## 🚀 Étapes d’Implémentation

1. **Préparation des données** :
   - Charger et préparer le dataset annoté.

2. **Entraînement** :
   - Entraîner un modèle YOLOv5 (v6.2 recommandé) avec les données préparées.

3. **Conversion en Core ML** :
   - Convertir le modèle YOLOv5 (.pt) en Core ML (.mlmodel) à l’aide de l’outil `yolov5_convert_weight_to_coreml`.

4. **Déploiement** :
   - Intégrer le modèle Core ML dans une application iOS avec Xcode.

## ⚙️ Pré-requis

### Environnement
- **Python** ≥ 3.8.0
- **YOLOv5** (v6.2 recommandé)
- **Core ML Tools** (v6.0 recommandé)

### Installation

1. **Cloner le dépôt YOLOv5 et installer les dépendances** :
   ```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
git checkout v6.2                    # (recommandé) switcher à la version 6.2
pip install -r requirements.txt      # installer les dépendances
   ```

2. **Cloner le dépôt de conversion et installer les outils requis** :
   ```bash
git clone https://github.com/ClintRen/yolov5_convert_weight_to_coreml.git
cd yolov5_convert_weight_to_coreml
pip install coremltools==6.0         # installer Core ML Tools
pip install numpy==1.23.1            # IMPORTANT : éviter les erreurs de compatibilité
   ```

## 🧪 Tests et Résultats

- **Modèle converti avec succès** : Le fichier `.mlmodel` a été intégré à une application iOS.
- **Limites** :
  - L’éclairage et la qualité des images peuvent affecter les résultats de détection.
  - Le modèle est limité à 7 catégories.

### Améliorations futures
1. **Augmenter le nombre de classes** : Ajouter des catégories pour couvrir un champ d’application plus large.
2. **Optimisation mobile** : Réduire la latence d’inférence à l’aide de techniques comme la quantification ou le pruning.
3. **Diversité des données** : Enrichir le dataset avec des images variées pour améliorer la robustesse.

## 📂 Liens Utiles

- [Dépôt YOLOv5](https://github.com/ultralytics/yolov5)
- [Conversion YOLOv5 → Core ML](https://github.com/ClintRen/yolov5_convert_weight_to_coreml)
