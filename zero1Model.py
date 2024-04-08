
from flask_sqlalchemy import SQLAlchemy
import random


# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()

# Table intermédiaire pour la relation many-to-many entre Utilisateur et Programme
avis = db.Table('avis',
     db.Column('utilisateur_id', db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True),
     db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'), primary_key=True),
     db.Column('note', db.Integer),
     db.Column('commentaire', db.Text)
)

# Table intermédiaire pour la relation many-to-many entre Programme et Exercice
programme_exercice = db.Table('programme_exercice',
    db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'), primary_key=True),
    db.Column('exercice_id', db.Integer, db.ForeignKey('exercice.id'), primary_key=True)
)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    type_utilisateur = db.Column(db.String(20), nullable=False)
    programmes = db.relationship('Programme', secondary=avis, backref=db.backref('utilisateurs', lazy='dynamic'))

class Programme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    coach = db.relationship('Utilisateur', backref=db.backref('programmes_coach', lazy=True))
    exercices = db.relationship('Exercice', secondary=programme_exercice, backref=db.backref('programmes', lazy='dynamic'))

class Exercice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    video = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)

# Ajout d'exemples d'enregistrements dans la base de données
def create_example_records():
    # Création d'exemples d'utilisateurs
    utilisateur1 = Utilisateur(nom='John', prenom='Doe', email='john@example.com', mot_de_passe='password1', type_utilisateur='admin')
    utilisateur2 = Utilisateur(nom='Jane', prenom='Doe', email='jane@example.com', mot_de_passe='password2', type_utilisateur='utilisateur')
    db.session.add(utilisateur1)
    db.session.add(utilisateur2)

    # Création d'exemples de programmes
    programme1 = Programme(nom='Programme 1', type='Type 1', coach_id=1)
    programme2 = Programme(nom='Programme 2', type='Type 2', coach_id=2)
    db.session.add(programme1)
    db.session.add(programme2)

    # Création d'exemples d'exercices
    exercice1 = Exercice(nom='Exercice 1', video='lien_vers_la_video1', description='Description de l\'exercice 1')
    exercice2 = Exercice(nom='Exercice 2', video='lien_vers_la_video2', description='Description de l\'exercice 2')
    db.session.add(exercice1)
    db.session.add(exercice2)

    # Ajout des enregistrements dans la base de données
    db.session.commit()

    from models import db, Utilisateur, Programme, Exercice, Avis, programme_exercice

# Fonction pour ajouter des exemples d'avis dans la base de données
def add_example_avis():
    # Ajouter des avis pour les programmes existants
    programmes = Programme.query.all()
    utilisateurs = Utilisateur.query.all()

    for programme in programmes:
        for utilisateur in utilisateurs:
            note = random.randint(1, 5)  # Note aléatoire entre 1 et 5
            commentaire = f"Un super programme ! Je recommande vivement. Note : {note}"
            aviss = avis(utilisateur_id=utilisateur.id, programme_id=programme.id, note=note, commentaire=commentaire)
            db.session.add(aviss)

    db.session.commit()

# Fonction pour associer des exercices à des programmes existants
def add_example_programme_exercice():
    # Ajouter des exercices à des programmes existants
    programmes = Programme.query.all()
    exercices = Exercice.query.all()

    for programme in programmes:
        # Sélectionner un nombre aléatoire d'exercices à associer au programme
        nb_exercices = random.randint(1, len(exercices))
        selected_exercices = random.sample(exercices, nb_exercices)

        # Associer les exercices au programme
        for exercice in selected_exercices:
            programme.exercices.append(exercice)

    db.session.commit()

# Appel des fonctions pour ajouter des exemples d'avis et d'associations programme-exercice
#add_example_avis()
#add_example_programme_exercice()
