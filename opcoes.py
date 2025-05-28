import pygame
import pygame_gui

class TelaOpcoes:
    def __init__(self, tela_principal):
        self.tela = tela_principal  # Tela principal onde será desenhada a tela de opções
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'theme.json')  # Gerenciador da interface para a tela de 800x600

        # Carrega e redimensiona a imagem de fundo para as opções
        self.fundo_opcoes = pygame.image.load('imagens/fundo.jpg')
        self.fundo_opcoes = pygame.transform.scale(self.fundo_opcoes, (800, 600))

        # Fonte para o título da tela de opções
        self.fonte = pygame.font.SysFont(None, 60)

        # Botão "Voltar" centralizado na parte inferior da tela
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 500), (200, 50)),
            text="Voltar",
            manager=self.manager
        )

        self.voltar_para_main = False  # Flag para indicar quando o usuário quer voltar à tela principal

    def process_event(self, evento):
        # Processa eventos da interface gráfica
        self.manager.process_events(evento)

        # Se o botão "Voltar" for pressionado, ativa a flag para retornar à tela principal
        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True

    def update(self, time_delta):
        # Atualiza o gerenciador da interface, necessário para animações e estado dos botões
        self.manager.update(time_delta)

    def draw(self):
        # Desenha o fundo da tela de opções
        self.tela.blit(self.fundo_opcoes, (0, 0))

        # Renderiza e desenha o título "Tela de Opções" no centro superior
        texto = self.fonte.render("Tela de Opções", True, (255, 255, 255))
        self.tela.blit(texto, (250, 270))

        # Desenha os elementos da interface, como botões
        self.manager.draw_ui(self.tela)
