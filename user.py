from flask import jsonify, request
from flask_restful import Resource
from models import db, Utilisateur

class UtilisateurResource(Resource):
    # Méthode pour récupérer tous les utilisateurs
    def get(self):
        utilisateurs = Utilisateur.query.all()
        result = [{'id': utilisateur.id,
                   'nom': utilisateur.nom,
                   'prenom': utilisateur.prenom,
                   'email': utilisateur.email,
                   'mot_de_passe': utilisateur.mot_de_passe,
                   'type_utilisateur': utilisateur.type_utilisateur} for utilisateur in utilisateurs]
        return jsonify(result)

    # Méthode pour créer un nouvel utilisateur
    def post(self):
        data = request.json
        nouvel_utilisateur = Utilisateur(nom=data['nom'], prenom=data['prenom'], email=data['email'], mot_de_passe=data['mot_de_passe'], type_utilisateur=data['type_utilisateur'])
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        return jsonify({'message': 'Utilisateur créé avec succès'}), 201

    # Méthode pour récupérer un utilisateur par son ID
    def get(self, utilisateur_id):
        utilisateur = Utilisateur.query.get(utilisateur_id)
        if not utilisateur:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        return jsonify({'id': utilisateur.id,
                        'nom': utilisateur.nom,
                        'prenom': utilisateur.prenom,
                        'email': utilisateur.email,
                        'mot_de_passe': utilisateur.mot_de_passe,
                        'type_utilisateur': utilisateur.type_utilisateur})

    # Méthode pour mettre à jour un utilisateur existant
    def put(self, utilisateur_id):
        data = request.json
        utilisateur = Utilisateur.query.get(utilisateur_id)
        if not utilisateur:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        utilisateur.nom = data['nom']
        utilisateur.prenom = data['prenom']
        utilisateur.email = data['email']
        utilisateur.mot_de_passe = data['mot_de_passe']
        utilisateur.type_utilisateur = data['type_utilisateur']
        db.session.commit()
        return jsonify({'message': 'Utilisateur mis à jour avec succès'})

    # Méthode pour supprimer un utilisateur existant
    def delete(self, utilisateur_id):
        utilisateur = Utilisateur.query.get(utilisateur_id)
        if not utilisateur:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        db.session.delete(utilisateur)
        db.session.commit()
        return jsonify({'message': 'Utilisateur supprimé avec succès'})
