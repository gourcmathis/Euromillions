# Euromillions

## Choix techniques et installation

### Choix techniques

Aucun gros choix technique n'a été réalisé. Nous avons choisis de séparer les différentes routes et le modèle pour une meilleure lisibilité.

### Installation

Créer et se placer dans son environnement virtuel

installer :

pip install "fastapi[all]"

pip install pandas

pip install scikit-learn

se placer dans le main et lancer un serveur local :

uvicorn main:app --reload

Aller sur l'adresse locale indiquée et ajouter /docs
