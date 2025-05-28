import pygame
import pygame_gui

class TelaRegras:
    def __init__(self, tela_principal):
        self.tela = tela_principal  # Tela principal onde será desenhado
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'theme.json') # Gerenciador da interface

        # Surface para o fundo da tela de regras, preenchida com cinza escuro
        self.fundo_regras = pygame.Surface(self.tela.get_size())
        self.fundo_regras.fill((30, 30, 30))

        # Fontes para título e texto das regras
        self.fonte_titulo = pygame.font.SysFont(None, 60)
        self.fonte_texto = pygame.font.SysFont(None, 28)

        # Botão "Voltar" para retornar à tela principal
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (150, 40)),
            text="Voltar",
            manager=self.manager
        )

        self.voltar_para_main = False  # Flag para indicar quando voltar para a tela principal

        # Lista de strings com as regras do jogo que serão exibidas na tela
        self.texto_regras = [
            "Regras do Jogo:",
            "- Regra 1: Faça isso.",
            "- Regra 2: Não faça aquilo.",
            "- Regra 3: Respeite os outros jogadores.",
            "- Regra 4: Divirta-se!",
            # Você pode adicionar mais regras aqui
        ]

    def process_event(self, evento):
        self.manager.process_events(evento)  # Envia evento para o gerenciador da UI

        # Se o botão "Voltar" for pressionado, ativa a flag para voltar para a tela principal
        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True

    def update(self, time_delta):
        self.manager.update(time_delta)  # Atualiza a interface (animações, etc)

    def draw(self):
        self.tela.blit(self.fundo_regras, (0, 0))  # Desenha o fundo cinza

        # Renderiza e desenha o título "Regras"
        titulo = self.fonte_titulo.render("Regras", True, (255, 255, 255))
        self.tela.blit(titulo, (350, 30))

        # Desenha as regras uma a uma, com espaçamento vertical
        y_offset = 100
        for linha in self.texto_regras:
            texto_renderizado = self.fonte_texto.render(linha, True, (230, 230, 230))
            self.tela.blit(texto_renderizado, (40, y_offset))
            y_offset += 35  # Espaço entre as linhas

        # Desenha os elementos da interface (botões, etc)
        self.manager.draw_ui(self.tela)
