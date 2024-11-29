from ursina import *  # Importer toutes les classes et fonctions du module Ursina
import random  # Importer le module random pour générer des positions aléatoires

class SnakeGame(Entity):  # Définir une classe SnakeGame qui hérite de la classe Entity
    def __init__(self):  # Initialiser la classe
        super().__init__()  # Appeler le constructeur de la classe parente Entity
        self.snake = [Entity(model='cube', color=color.green, position=(0, 0, 0))]  # Créer le serpent comme une liste d'entités, initialement un cube vert
        self.food = Entity(model='sphere', color=color.red, position=self.random_position())  # Créer la nourriture comme une sphère rouge à une position aléatoire
        self.direction = Vec3(1, 0, 0)  # Initialement, le serpent se déplace vers la droite (axe X)
        self.speed = 0.2  # Définir la vitesse du serpent
        self.timer = 0  # Initialiser un timer pour gérer le mouvement du serpent
        self.score = 0  # Initialiser le score à 0
        self.score_text = Text(text=f'Score: {self.score}', position=(0.6, 0.45), scale=2, color=color.white)  # Afficher le score à l'écran

        # Ajout du sol pour donner un repère visuel
        for x in range(-10, 11):  # Boucle pour les positions en X
            for z in range(-10, 11):  # Boucle pour les positions en Z
                Entity(model='quad', scale=(1, 1), position=(x, -0.5, z), rotation=(90, 0, 0), color=color.gray)  # Créer une entité de sol grise

    def random_position(self):  # Définir une méthode pour générer une position aléatoire
        return Vec3(random.randint(-9, 9), 0, random.randint(-9, 9))  # Retourner une position aléatoire sur les axes X et Z

    def input(self, key):  # Définir une méthode pour gérer les entrées clavier
        # Gestion des directions pour clavier AZERTY et flèches directionnelles
        if key == 'w' or key == 'up arrow':  # Si la touche 'w' ou la flèche haut est pressée
            if self.direction != Vec3(0, 0, -1):  # Ne pas faire un demi-tour vers le bas
                self.direction = Vec3(0, 0, 1)  # Déplacer vers le haut (avant sur l'axe Z)
        elif key == 's' or key == 'down arrow':  # Si la touche 's' ou la flèche bas est pressée
            if self.direction != Vec3(0, 0, 1):  # Ne pas faire un demi-tour vers le haut
                self.direction = Vec3(0, 0, -1)  # Déplacer vers le bas
        elif key == 'a' or key == 'left arrow':  # Si la touche 'a' ou la flèche gauche est pressée
            if self.direction != Vec3(1, 0, 0):  # Ne pas faire demi-tour vers la droite
                self.direction = Vec3(-1, 0, 0)  # Déplacer vers la gauche
        elif key == 'd' or key == 'right arrow':  # Si la touche 'd' ou la flèche droite est pressée
            if self.direction != Vec3(-1, 0, 0):  # Ne pas faire demi-tour vers la gauche
                self.direction = Vec3(1, 0, 0)  # Déplacer vers la droite

    def update(self):  # Définir une méthode pour mettre à jour le jeu à chaque frame
        self.timer += time.dt  # Incrémenter le timer avec le temps écoulé depuis la dernière frame
        if self.timer >= self.speed:  # Si le timer atteint la vitesse définie
            self.timer = 0  # Réinitialiser le timer
            new_head_position = self.snake[-1].position + self.direction  # Calculer la nouvelle position de la tête du serpent

            # Gérer le passage à travers les bordures
            if new_head_position.x > 10:  # Si dépasse à droite
                new_head_position.x = -10
            elif new_head_position.x < -10:  # Si dépasse à gauche
                new_head_position.x = 10
            elif new_head_position.z > 10:  # Si dépasse en haut
                new_head_position.z = -10
            elif new_head_position.z < -10:  # Si dépasse en bas
                new_head_position.z = 10

            new_head = Entity(model='cube', color=color.green, position=new_head_position)  # Créer une nouvelle tête de serpent
            self.snake.append(new_head)  # Ajouter la nouvelle tête au serpent

            # Vérifie si le serpent mange la nourriture
            if new_head.position == self.food.position:  # Si la position de la tête du serpent est la même que celle de la nourriture
                self.food.position = self.random_position()  # Repositionner la nourriture à une position aléatoire
                self.score += 1  # Incrémenter le score
                self.score_text.text = f'Score: {self.score}'  # Mettre à jour le texte du score
            else:
                tail = self.snake.pop(0)  # Retirer la queue du serpent
                destroy(tail)  # Détruire l'entité de la queue

            # Vérifie les collisions avec soi-même
            if any(segment.position == new_head.position for segment in self.snake[:-1]):  # Si la tête du serpent entre en collision avec son corps
                print("Game Over!")  # Afficher "Game Over!"
                application.quit()  # Quitter l'application

# Lancer le jeu
app = Ursina()  # Créer une instance de l'application Ursina
window.title = 'Snake 3D'  # Définir le titre de la fenêtre
game = SnakeGame()  # Créer une instance du jeu SnakeGame

# Positionner la caméra pour une vue éloignée
camera.position = (0, 30, -40)  # Définir la position de la caméra
camera.rotation_x = 35  # Définir la rotation de la caméra

app.run()  # Démarrer l'application