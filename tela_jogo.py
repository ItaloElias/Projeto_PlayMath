import pygame
import pygame_gui

class TelaJogo:
    def __init__(self, tela_principal):
        self.tela = tela_principal
        self.manager = pygame_gui.UIManager(self.tela.get_size())

        self.fundo = pygame.Surface(self.tela.get_size())
        self.fundo.fill((0, 50, 100))  # fundo azul escuro

        self.fonte = pygame.font.SysFont(None, 60)

        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (150, 40)),
            text="Voltar ao Menu",
            manager=self.manager
        )

        self.voltar_para_main = False

    def process_event(self, evento):
        self.manager.process_events(evento)

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.voltar_para_main = True

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self):
        self.tela.blit(self.fundo, (0, 0))
        texto = self.fonte.render("Tela de Jogo", True, (255, 255, 255))
        self.tela.blit(texto, (self.tela.get_width()//2 - texto.get_width()//2, 100))
        self.manager.draw_ui(self.tela)

    def reset_voltar(self):
        self.voltar_para_main = False
