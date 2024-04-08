
from flask import Flask, render_template, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from models import create_example_records,avis,programme_exercice
from sqlalchemy import delete

# Importer les classes de models.py
from models import db, Utilisateur, Programme, Exercice

app = Flask(__name__)

# Configuration de l'application à partir de config.py
app.config.from_object('config.Config')

# Initialisation de l'extension SQLAlchemy
db.init_app(app)

# Définition de la route pour afficher les informations de tous les utilisateurs
@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    result = []
    for utilisateur in utilisateurs:
        utilisateur_dict = {
            'id': utilisateur.id,
            'nom': utilisateur.nom,
            'prenom': utilisateur.prenom,
            'email': utilisateur.email,
            'mot_de_passe': utilisateur.mot_de_passe,
            'type_utilisateur': utilisateur.type_utilisateur,
            'programmes': [programme.nom for programme in utilisateur.programmes]
        }
        result.append(utilisateur_dict)
    return jsonify(result)

#Créer un nouvel utilisateur 
@app.route('/utilisateur', methods=['POST'])
def ajouter_utilisateur():
    print("hello wordl")
    # Extraire les données de la requête JSON
    #print(data = request.json)
    data = request.json
    print("hello wordl")
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    type_utilisateur = data.get('type_utilisateur')
    print("hello wordl")
    # Vérifier si tous les champs requis sont présents
    if not nom or not prenom or not email or not mot_de_passe or not type_utilisateur:
        return jsonify({'message': 'Tous les champs sont requis.'}), 400

    # Vérifier si l'email est unique
    print("hello wordl")
    if Utilisateur.query.filter_by(email=email).first():
        return jsonify({'message': 'Cet email est déjà utilisé.'}), 400

    # Créer un nouvel utilisateur
    nouvel_utilisateur = Utilisateur(nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe, type_utilisateur=type_utilisateur)
    print(nouvel_utilisateur)
    # Ajouter l'utilisateur à la base de données
    db.session.add(nouvel_utilisateur)
    db.session.commit()

    # Répondre avec un message de succès
    return jsonify({'message': 'Utilisateur ajouté avec succès.', 'id_utilisateur': nouvel_utilisateur.id}), 201

#Récupérer un utilisateur par son ID :
@app.route('/utilisateur/<int:user_id>', methods=['GET'])
def get_utilisateur(user_id):
    utilisateur = Utilisateur.query.get(user_id)
    if utilisateur:
        utilisateur_dict = {
            'id': utilisateur.id,
            'nom': utilisateur.nom,
            'prenom': utilisateur.prenom,
            'email': utilisateur.email,
            'mot_de_passe': utilisateur.mot_de_passe,
            'type_utilisateur': utilisateur.type_utilisateur,
            'programmes': [programme.nom for programme in utilisateur.programmes]
        }
        return jsonify(utilisateur_dict), 200
    else:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404
    
 #Mettre à jour un utilisateur existant
     
@app.route('/utilisateur/<int:user_id>', methods=['PUT'])
def update_utilisateur(user_id):
    utilisateur = Utilisateur.query.get(user_id)
    if not utilisateur:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    mot_de_passe = request.form.get('mot_de_passe')
    type_utilisateur = request.form.get('type_utilisateur')

    utilisateur.nom = nom
    utilisateur.prenom = prenom
    utilisateur.email = email
    utilisateur.mot_de_passe = mot_de_passe
    utilisateur.type_utilisateur = type_utilisateur

    db.session.commit()

    return jsonify({'message': 'Utilisateur mis à jour avec succès'}), 200

from flask import jsonify
from models import db, Utilisateur


# Supprimer un utilisateur
@app.route('/utilisateur/<int:user_id>', methods=['DELETE'])
def delete_utilisateur(user_id):
    # Récupérer l'utilisateur à supprimer
    utilisateur = Utilisateur.query.get(user_id)

    # Vérifier si l'utilisateur existe
    if not utilisateur:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

    try:
        if utilisateur.type_utilisateur == 'coach':
            # Récupérer tous les programmes associés au coach
            programmes = Programme.query.filter_by(coach_id=user_id).all()
            
            # Supprimer les enregistrements liés dans la table d'association 'avis' pour chaque programme
            for programme in programmes:
                db.session.execute(delete(avis).where(avis.c.programme_id == programme.id))
            
            # Supprimer les enregistrements dans la table d'association 'programme_exercice' pour chaque programme
            for programme in programmes:
                db.session.execute(delete(programme_exercice).where(programme_exercice.c.programme_id == programme.id))
            
            # Supprimer les programmes associés au coach
            Programme.query.filter_by(coach_id=user_id).delete()
            
        # Supprimer l'utilisateur de la base de données
        db.session.delete(utilisateur)
        db.session.commit()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        # En cas d'erreur lors de la suppression, annuler les modifications
        db.session.rollback()
        return jsonify({'message': 'Erreur lors de la suppression de l\'utilisateur', 'error': str(e)}), 500
    
@app.route('/programme', methods=['POST'])
def create_programme():
    data = request.json

    print("hello world")
    nom = data.get('nom')
    type = data.get('type')
    coach_id = data.get('coach_id')

    if not nom or not type or not coach_id:
        return jsonify({'message': 'Tous les champs sont requis.'}), 400

    programme = Programme(nom=nom, type=type, coach_id=coach_id)
    db.session.add(programme)
    db.session.commit()

    return jsonify({'message': 'Programme créé avec succès.', 'programme_id': programme.id}), 201

# Read
@app.route('/programmes', methods=['GET'])
def get_programmes():
    programmes = Programme.query.all()
    result = [{'id': programme.id,
               'nom': programme.nom,
               'type': programme.type,
               'coach_id': programme.coach_id,
               #'membres': [membre.id for membre in programme.membres],
               'exercices': [exercice.id for exercice in programme.exercices]} for programme in programmes]
    return jsonify(result)

# Update
@app.route('/programme/<int:programme_id>', methods=['PUT'])
def update_programme(programme_id):
    programme = Programme.query.get_or_404(programme_id)
    data = request.json
    if 'nom' in data:
        programme.nom = data['nom']
    if 'type' in data:
        programme.type = data['type']
    if 'coach_id' in data:
        programme.coach_id = data['coach_id']
    db.session.commit()
    return jsonify({'message': 'Programme mis à jour avec succès.'})

# Delete
@app.route('/programme/<int:programme_id>', methods=['DELETE'])
def delete_programme(programme_id):
    programme = Programme.query.get_or_404(programme_id)
    db.session.delete(programme)
    db.session.commit()
    return jsonify({'message': 'Programme supprimé avec succès.'})

# Route pour récupérer tous les exercices
@app.route('/exercices', methods=['GET'])
def get_exercices():
    exercices = Exercice.query.all()
    result = [{'id': exercice.id,
               'nom': exercice.nom,
               'video': exercice.video,
               'description': exercice.description} for exercice in exercices]
    return jsonify(result)

# Route pour créer un nouvel exercice
@app.route('/exercice', methods=['POST'])
def create_exercice():
    # Récupérer les données JSON de la requête
    data = request.json

    # Vérifier si toutes les clés nécessaires sont présentes dans les données JSON
    if 'nom' not in data or 'video' not in data or 'description' not in data:
        return jsonify({'message': 'Tous les champs (nom, video, description) sont requis.'}), 400

    # Extraire les valeurs des clés nom, video et description
    nom = data['nom']
    video = data['video']
    description = data['description']

    # Créer un nouvel exercice avec les données fournies
    nouvel_exercice = Exercice(nom=nom, video=video, description=description)

    # Ajouter l'exercice à la base de données
    db.session.add(nouvel_exercice)

    try:
        # Committer les changements à la base de données
        db.session.commit()
        # Retourner une réponse JSON avec un code 201 pour indiquer que l'exercice a été créé avec succès
        return jsonify({'message': 'Exercice créé avec succès'}), 201
    except Exception as e:
        # En cas d'erreur, annuler les modifications et retourner un message d'erreur avec un code 500
        db.session.rollback()
        return jsonify({'message': 'Erreur lors de la création de l\'exercice', 'error': str(e)}), 500

# Route pour récupérer un exercice par son ID
@app.route('/exercice/<int:exercice_id>', methods=['GET'])
def get_exercice(exercice_id):
    exercice = Exercice.query.get(exercice_id)
    if exercice:
        exercice_dict = {
            'id': exercice.id,
            'nom': exercice.nom,
            'video': exercice.video,
            'description': exercice.description
        }
        return jsonify(exercice_dict), 200
    else:
        return jsonify({'message': 'Exercice non trouvé'}), 404

# Route pour mettre à jour un exercice existant
@app.route('/exercice/<int:exercice_id>', methods=['PUT'])
def update_exercice(exercice_id):
    exercice = Exercice.query.get(exercice_id)
    if not exercice:
        return jsonify({'message': 'Exercice non trouvé'}), 404

    nom = request.form.get('nom')
    video = request.form.get('video')
    description = request.form.get('description')

    exercice.nom = nom
    exercice.video = video
    exercice.description = description

    db.session.commit()

    return jsonify({'message': 'Exercice mis à jour avec succès'}), 200

# Route pour supprimer un exercice
@app.route('/exercice/<int:exercice_id>', methods=['DELETE'])
def delete_exercice(exercice_id):
    exercice = Exercice.query.get(exercice_id)
    if not exercice:
        return jsonify({'message': 'Exercice non trouvé'}), 404

    db.session.delete(exercice)
    db.session.commit()

    return jsonify({'message': 'Exercice supprimé avec succès'}), 200

# Route pour créer un nouvel avis
@app.route('/avis', methods=['POST'])
def create_avis():
    # Récupérer les données JSON de la requête
    data = request.json
    
    # Extraire les informations de la requête
    programme_id = data.get('programme_id')
    utilisateur_id = data.get('utilisateur_id')
    note = data.get('note')
    commentaire = data.get('commentaire')

    # Créer un nouvel objet Avis avec les données extraites
    nouvel_avis = avis(programme_id=programme_id, utilisateur_id=utilisateur_id, note=note, commentaire=commentaire)
    
    # Ajouter le nouvel avis à la session de la base de données
    db.session.add(nouvel_avis)
    
    # Commit les changements à la base de données
    db.session.commit()
    
    # Retourner une réponse JSON indiquant que l'avis a été créé avec succès
    return jsonify({'message': 'Avis créé avec succès'}), 201
     # Créer les enregistrements d'exemple dans la base de données
    
def create_app():
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_example_records()
   
# Appel de la fonction create_app() pour initialiser la base de données avec des données d'exemple
create_app()

# Définition de la route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html', message='Hello, World!')

if __name__ == '__main__':
    app.run(debug=True)