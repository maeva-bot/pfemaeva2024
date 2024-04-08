
from flask_sqlalchemy import SQLAlchemy

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()

# Table intermédiaire pour la relation many-to-many entre Utilisateur et Programme
avis = db.Table('avis',
    db.Column('utilisateur_id', db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True),
    db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'), primary_key=True),
    db.Column('note', db.Integer),
    db.Column('commentaire', db.Text),
    extend_existing=True
)

# Table intermédiaire pour la relation many-to-many entre Programme et Exercice
programme_exercice = db.Table('programme_exercice',
    db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'), primary_key=True),
    db.Column('exercice_id', db.Integer, db.ForeignKey('exercice.id'), primary_key=True),
    extend_existing=True
)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)                               
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    type_utilisateur = db.Column(db.String(20), nullable=False)
    programmes = db.relationship('Programme', secondary=avis, backref=db.backref('utilisateurs', lazy='dynamic', cascade='all, delete'))

class Programme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id', ondelete='CASCADE'), nullable=False)
    coach = db.relationship('Utilisateur', backref=db.backref('programmes_coach', lazy=True))
    exercices = db.relationship('Exercice', secondary=programme_exercice, backref=db.backref('programmes', lazy='dynamic', cascade='all, delete'))

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
    coach1 = Utilisateur(nom='ZAMBO', prenom='Doe', email='coach@example.com', mot_de_passe='password3', type_utilisateur='coach')
    utilisateur3 = Utilisateur(nom='Bob', prenom='Smith', email='bob@example.com', mot_de_passe='password4', type_utilisateur='utilisateur')
    utilisateur4 = Utilisateur(nom='Bobb', prenom='SmithA', email='bob2@example.com', mot_de_passe='password5', type_utilisateur='utilisateur')
    coach2 = Utilisateur(nom='ZAMBOa', prenom='Doea', email='coach@example.coma', mot_de_passe='password3a', type_utilisateur='coach')
    # Création d'exemples de programmes
    programme1 = Programme(nom='Programme 1', type='Type 1', coach=coach1)
    programme2 = Programme(nom='Programme 2', type='Type 2', coach=coach1)

    # Création d'exemples d'exercices
    exercice1 = Exercice(nom='Exercice 1', video='lien_vers_la_video1', description='Description de l\'exercice 1')
    exercice2 = Exercice(nom='Exercice 2', video='lien_vers_la_video2', description='Description de l\'exercice 2')

    # Association des exercices aux programmes
    programme1.exercices.extend([exercice1, exercice2])
    programme2.exercices.append(exercice1)  # Exemple de relation many-to-many

    # Ajout des enregistrements dans la session
    db.session.add_all([utilisateur1, utilisateur2, coach1, programme1, programme2, exercice1, exercice2,utilisateur3,utilisateur4,coach2])

    # Association de l'utilisateur deux aux deux programmes
    utilisateur2.programmes.extend([programme1, programme2])
    utilisateur4.programmes.extend([programme1])

    # Commit des changements
    db.session.commit()


#class Avis(db.Model):
    #__tablename__ = 'avis'

 #   utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True)
  #  programme_id = db.Column(db.Integer, db.ForeignKey('programme.id'), primary_key=True)
   # note = db.Column(db.Integer)
    #commentaire = db.Column(db.Text)

    #utilisateur = db.relationship('Utilisateur', backref=db.backref('avis_utilisateur', cascade='all, delete-orphan'))
    #programme = db.relationship('Programme', backref=db.backref('avis_programme', cascade='all, delete-orphan'))

