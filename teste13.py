import math
from time import sleep
import pygame
import pygame.freetype
import win32api
import webbrowser

pygame.mixer.init()
pew = pygame.mixer.Sound('pew.mp3')
pew.set_volume(0.1)
hit = pygame.mixer.Sound('hit.mp3')
hit.set_volume(0.1)


pygame.init()

branco = (255,255,255)

tela = pygame.display.set_mode((500,500))
pygame.display.set_caption('./Jogo Ballerini')

imagem = pygame.image.load("./player.png")
imagem = pygame.transform.scale(imagem, (100,100))
enemyf = pygame.image.load("megamente.png")
enemyf = pygame.transform.scale(enemyf, (150,150))
x = 250
y = 250
speed = 20

class Enemy:
    def __init__(self,x,y,foto,vida):
        self.vida = vida
        self.x = x
        self.y = y
        self.foto = foto
        self.changex = 2

    def moves(self):
        self.x += self.changex

        if self.x <= 0:
            self.changex = 2
        elif self.x >= 500-150:
            self.changex = -2

    def draw(self):
        a = tela.blit(self.foto, (self.x,self.y))
        return a

class Player:
    def __init__(self,x,y,foto):
        self.x = x
        self.y = y
        self.foto = foto

    def desenhar(self):
        tela.blit(self.foto, (self.x, self.y))

class bulet:
    def __init__(self, x,y, sp):
        self.x = x
        self.y = y
        self.sp = sp
        self.reset = y

    def mover(self):
        pew.play()
        if self.y > 0:
            self.y -= self.sp
        else:
            self.y = self.reset
            

    def draw(self):
        bala = pygame.draw.rect(tela, (255,0,0),rect=[self.x, self.y, 10,10])
        return bala

bala = bulet(x,y, 1)
enemy = Enemy(250,20,enemyf, 100000)
enemylife = enemy.vida

fonte = pygame.freetype.Font('./comic.ttf', 30)


rodando = True

while rodando:

    if enemylife <= 0:
        webbrowser.open('https://www.youtube.com/c/rafaellaballerini/featured')
        win32api.MessageBox(0,'Você ganhou!','Winning Screen!',16)
        
        rodando=False


    tela.fill(branco)
    plr = Player(x,y,imagem)

    def atirar():
        bala.draw()
        bala.mover()
        bala.x = plr.x

    def enemy_func():
        enemy.draw()
        enemy.moves()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x-1>=0:
                x -= speed
            if event.key == pygame.K_RIGHT and x+1<500-100:
                x += speed

    plr.desenhar()
    enemy_func()

    fonte.render_to(tela, (0,0), f"Enemy's Life: {math.trunc(enemylife)}", (0,0,0))

    atirar()

    bulcol = bala.draw()
    enemycol = enemy.draw()

    if bulcol.colliderect(bulcol):
        enemylife -= 20
        hit.play()

    
    pygame.display.update()
