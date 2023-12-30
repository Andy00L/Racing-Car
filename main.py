import pygame
import time
import math

from outils import taille_image, blit_centre_rotation

HERBE = taille_image(pygame.image.load("img/grass.jpg"), 2.5)
PISTE = taille_image(pygame.image.load("img/track.png"), 0.9)

BORDUR_PISTE = taille_image(pygame.image.load("img/track-border.png"), 0.9)
BORDUR_PISTE_MASK = pygame.mask.from_surface(BORDUR_PISTE)

ARRIVER = pygame.image.load("img/finish.png")
ARRIVER_MASK = pygame.mask.from_surface(ARRIVER)
POSITION_ARRIVER = (130,250)

VOITURE_R = taille_image(pygame.image.load("img/red-car.png"), 0.55)
VOITURE_V = taille_image(pygame.image.load("img/green-car.png"), 0.55)

LARGEUR, HAUTEUR = PISTE.get_width(), PISTE.get_height()

FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))

pygame.display.set_caption(" jeu de course!")

FPS = 60

class AbstractCar:
    def __init__(self, vel_max , vel_rotation):
        self.img = self.IMG
        self.vel_max = vel_max
        self.vel = 0
        self.vel_rotation = vel_rotation
        self.angle = 0
        self.x, self.y = self.position_depart
        self.acceleration = 0.1
        
    def rotation(self, gauche = False, droite = False):
        if gauche:
            self.angle += self.vel_rotation
        elif droite:
            self.angle -= self.vel_rotation
        
    def dessiner(self, fenetre):
        blit_centre_rotation(fenetre, self.img, (self.x, self.y), self.angle)
    
    def avancer(self):
        self.vel = min(self.vel + self.acceleration, self.vel_max)
        self.bouger()
    
    def reculer(self):
        self.vel = max(self.vel - self.acceleration, -self.vel_max/2)
        self.bouger()
        
    def bouger(self):
        radian = math.radians(self.angle)
        vertical = math.cos(radian) * self.vel
        horizontal = math.sin(radian) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
    
    def collision(self, mask, x = 0, y = 0 ):
        mask_voiture = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        point_intersection = mask.overlap(mask_voiture, offset)
        return point_intersection

    def reset(self):
        self.x, self.y = self.position_depart
        self.angle = 0
        self.vel = 0

class VoitureJoueur(AbstractCar):
    IMG = VOITURE_R
    position_depart = (180, 200)

    def reduire_vitesse(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.bouger()
    def rebondir(self):
        self.vel = -self.vel
        self.bouger()
# La fonction 'dessiner' prend deux parametre, 'fenetre' qui est une la taile de la fenettre du jeu
# et ' images' qui est une liste de listes contenant une image et sa position. Elle permet de les dessiner
# le terrain et ces objets.
def dessiner(fenetre, images, voiture_joueur):
    for img, position in images:
        fenetre.blit(img, position)
    voiture_joueur.dessiner(fenetre)
    pygame.display.update()

def bouger_joueur(voiture_joueur):
    keys = pygame.key.get_pressed()
    
    bougeer = False
    if keys[pygame.K_a]:
        voiture_joueur.rotation(gauche = True)
    if keys[pygame.K_d]:
        voiture_joueur.rotation(droite = True)
    if keys[pygame.K_w]:
        bougeer =True
        voiture_joueur.avancer()
    if keys[pygame.K_s]:
        bougeer = True
        voiture_joueur.reculer()
        
    if not bougeer:
        voiture_joueur.reduire_vitesse()   
run = True

# Permet de fixer la vitesse du jeu.
horloge = pygame.time.Clock()
images = [(HERBE, (0,0)), (PISTE, (0,0)), (ARRIVER, POSITION_ARRIVER), (BORDUR_PISTE, (0,0))]
voiture_joueur = VoitureJoueur(4, 4)

while run:
    # empeche le heu de tourner a plus de 60 fps.
    horloge.tick(FPS)
    
    # Permet de dessiner le terrain
    dessiner(FENETRE, images, voiture_joueur)
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            run = False
            break
    bouger_joueur(voiture_joueur)
    
    if voiture_joueur.collision(BORDUR_PISTE_MASK) != None:
        voiture_joueur.rebondir()
    
    arriver_position_collision = voiture_joueur.collision(ARRIVER_MASK, *POSITION_ARRIVER)
    if arriver_position_collision != None:
        if arriver_position_collision[1] == 0:
            voiture_joueur.rebondir()
        else: 
            voiture_joueur.reset()
pygame.quit()