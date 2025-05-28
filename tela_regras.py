import pygame
import pygame_gui

class TelaRegras:
    def __init__(self, tela_principal):
        self.tela = tela_principal  # Tela principal do pygame
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'theme.json')  # Gerenciador UI com tema

        self.fundo_regras = pygame.image.load('imagens/fundo.jpg')  # Carrega imagem de fundo
        self.fundo_regras = pygame.transform.scale(self.fundo_regras, self.tela.get_size())  # Ajusta tamanho da imagem

        self.fonte_titulo = pygame.font.SysFont(None, 60)  # Fonte grande para título
        self.fonte_texto = pygame.font.SysFont(None, 28)  # Fonte menor para texto das regras

        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (150, 40)),  # Posição e tamanho do botão
            text="Voltar",  # Texto exibido no botão
            manager=self.manager  # Gerenciador do botão
        )

        self.voltar_para_main = False  # Flag para indicar retorno ao menu

        self.texto_regras = [
            "Regras do Jogo:",
            "- Regra 1: Faça isso.",
            "- Regra 2: Não faça aquilo.",
            "- Regra 3: Respeite os outros jogadores.",
            "- Regra 4: Divirta-se!",
        ]

    def process_event(self, evento):
        self.manager.process_events(evento)  # Processa eventos da UI

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:  # Se um botão foi pressionado
            if evento.ui_element == self.botao_voltar:  # Botão "Voltar" pressionado
                self.voltar_para_main = True  # Sinaliza retorno ao menu

    def update(self, time_delta):
        self.manager.update(time_delta)  # Atualiza gerenciador da UI

    def draw(self):
        self.tela.blit(self.fundo_regras, (0, 0))  # Desenha fundo

        titulo = self.fonte_titulo.render("Regras", True, (255, 255, 255))  # Renderiza título
        self.tela.blit(titulo, (350, 30))  # Desenha título na tela

        y_offset = 100  # Posição vertical inicial para texto
        for linha in self.texto_regras:
            texto_renderizado = self.fonte_texto.render(linha, True, (230, 230, 230))  # Renderiza cada linha
            self.tela.blit(texto_renderizado, (40, y_offset))  # Desenha linha na tela
            y_offset += 35  # Avança posição vertical para próxima linha

        self.manager.draw_ui(self.tela)  # Desenha botões e elementos da UI
