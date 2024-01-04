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

PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]

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
    
class voitureOrdi(AbstractCar):
    IMG = VOITURE_V
    position_depart = (150,200)
    
    def __init__(self, vel_max, vel_rotation, path=[]):
        super().__init__(vel_max, vel_rotation)
        self.path = path
        self.position_present = 0
        self.vel = vel_max
        
    def dessiner_point(self, fenetre):
        for point in self.path:
            pygame.draw.circle(fenetre, (255, 0 , 0), point, 5)
        
    def dessiner(self, fenetre):
        super().dessiner(fenetre)
    #    self.dessiner_point(fenetre)
        
    def calculer_angle(self):
        target_x , target_y = self.path[self.position_present]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        
        if y_diff == 0:
            angle_radiant_voulu = math.pi / 2
        else:
            angle_radiant_voulu = math.atan(x_diff / y_diff)
            
        if target_y > self.y:
            angle_radiant_voulu += math.pi
        
        difference_angle = self.angle - math.degrees(angle_radiant_voulu)
        if difference_angle >= 180:
            difference_angle -= 360
        
        if difference_angle > 0:
            self.angle -= min(self.vel_rotation, abs(difference_angle))
        else:
            self.angle += min(self.vel_rotation, abs(difference_angle))
    
    def update_path_point(self):
        target = self.path[self.position_present]
        rect = pygame.Rect(self.x, self.y , self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.position_present += 1
        
    def bouger(self):
        if self.position_present >= len(self.path):
            return
        
        self.calculer_angle()
        self.update_path_point()
        super().bouger()
        
# La fonction 'dessiner' prend deux parametre, 'fenetre' qui est une la taile de la fenettre du jeu
# et ' images' qui est une liste de listes contenant une image et sa position. Elle permet de les dessiner
# le terrain et ces objets.
def dessiner(fenetre, images, voiture_joueur, voiture_ordi):
    for img, position in images:
        fenetre.blit(img, position)
    voiture_joueur.dessiner(fenetre)
    voiture_ordi.dessiner(fenetre)
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
        
def gerer_colision(voiture_joueur, voiture_ordi):
    if voiture_joueur.collision(BORDUR_PISTE_MASK) != None:
        voiture_joueur.rebondir()
    
    
    ordi_arriver_position_collision = voiture_ordi.collision(ARRIVER_MASK, *POSITION_ARRIVER)
    if ordi_arriver_position_collision != None:
        voiture_joueur.reset()
        voiture_ordi.reset()
        print(" Computer gagner!")
    
    
    joueur_arriver_position_collision = voiture_joueur.collision(ARRIVER_MASK, *POSITION_ARRIVER)
    if joueur_arriver_position_collision != None:
        if joueur_arriver_position_collision[1] == 0:
            voiture_joueur.rebondir()
        else: 
            voiture_joueur.reset()
            voiture_ordi.reset()

run = True
# Permet de fixer la vitesse du jeu.
horloge = pygame.time.Clock()
images = [(HERBE, (0,0)), (PISTE, (0,0)), (ARRIVER, POSITION_ARRIVER), (BORDUR_PISTE, (0,0))]
voiture_joueur = VoitureJoueur(4, 4)
voiture_ordi = voitureOrdi(4, 4, PATH)

while run:
    # empeche le heu de tourner a plus de 60 fps.
    horloge.tick(FPS)
    
    # Permet de dessiner le terrain
    dessiner(FENETRE, images, voiture_joueur, voiture_ordi)
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            run = False
            break
        
        
    bouger_joueur(voiture_joueur)
    voiture_ordi.bouger()
    
    gerer_colision(voiture_joueur , voiture_ordi)
    
            
print(voiture_ordi.path)
pygame.quit()
