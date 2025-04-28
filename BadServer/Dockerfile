# Utiliser une image officielle PHP légère avec serveur web intégré
FROM php:8.2-cli

# Définir le dossier de travail
WORKDIR /var/www/html

# Copier tous les fichiers du projet dans le conteneur
COPY . .

# Exposer le port 80
EXPOSE 80

# Lancer le serveur PHP interne à l'IP 0.0.0.0 sur le port 80
CMD ["php", "-S", "0.0.0.0:80"]