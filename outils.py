import pygame

# La fonction 'taille_image' prend deux paramettre, 'img' une image et 'facteur' un chiffre qui
# represente la veleur d'agrandissement. Elle permet d'augmenter ou reduire la taille d'une image 
# en fonction du facteur d'agrandissement.
def taille_image(img, facteur):
    taille = round(img.get_width() * facteur), round(img.get_height() * facteur)
    return pygame.transform.scale(img, taille)

# La fonction ' blit_centre_rotation ' prend comme parametre:
# - fenetre:
# - image:
# - top_gauche:
# - angle:
# Elle retourne une image retouner en fonction d'un certain angle.
def blit_centre_rotation(fenetre, image, top_gauche, angle):
    image_tourner = pygame.transform.rotate(image, angle)
    
    nouv_rectange = image_tourner.get_rect(center = image.get_rect(topleft = top_gauche).center)
    fenetre.blit(image_tourner, nouv_rectange.topleft)
    
def blit_text_center(fenetre, font , text):
    render = font.render(text, 1, (200, 200, 200))
    fenetre.blit(render, (fenetre.get_width() / 2 - render.get_width() / 2,
                          fenetre.get_height() / 2 - render.get_height() / 2))
    

