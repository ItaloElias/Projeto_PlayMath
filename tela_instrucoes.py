import pygame
import pygame_gui

class TelaInstrucoes:
    def __init__(self, tela_principal):
        self.tela = tela_principal  # Referência à tela principal do pygame
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'theme.json')  # Gerenciador GUI

        self.fundo_instrucoes = pygame.image.load('imagens/fundo_instrucoes.jpg')  # Imagem de fundo
        self.fundo_instrucoes = pygame.transform.scale(self.fundo_instrucoes, self.tela.get_size())  # Redimensiona fundo

        # Botão "Voltar" para retornar ao menu principal
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (150, 40)),
            text="Voltar",
            manager=self.manager
        )
        self.voltar_para_main = False  # Flag para sinalizar retorno ao menu

        # Texto das instruções formatado em HTML para melhor apresentação
        self.instrucoes_html = (
            "1ª Escolha sua operação: +, - ou ×. Aqui a matemática é simples, mas cheia de desafios!<br>"
            "<p>2ª Você tem 30 segundos. Use bem esse tempo e mostre que tá com os cálculos afiados.<br>"
            "<p>3ª Cada resposta certa vale ponto. Cada erro custa uma vida. Você começa com 3, então atenção!<br>"
            "<p>4ª Perdeu todas as vidas? A rodada termina, mas você pode tentar de novo!<br>"
            "<p>5ª Respire fundo, mantenha o foco e resolva com calma. O cronômetro corre, mas você comanda o jogo.<br>"
            "<p>6ª Pronto pra encarar o desafio? Se a resposta for sim, é só apertar 'Jogar'!"
        )

        # Caixa de texto com rolagem automática para exibir as instruções
        self.caixa_instrucoes = pygame_gui.elements.UITextBox(
            html_text=self.instrucoes_html,
            relative_rect=pygame.Rect(((self.tela.get_width() - 670) // 2, 150), (670, 400)),
            manager=self.manager,
            object_id="#textbox_instrucoes"
        )

    def process_event(self, evento):
        self.manager.process_events(evento)  # Envia evento para o gerenciador GUI

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_voltar:  # Detecta clique no botão voltar
                self.voltar_para_main = True  # Sinaliza para retornar ao menu

    def update(self, time_delta):
        self.manager.update(time_delta)  # Atualiza a interface

    def draw(self):
        self.tela.blit(self.fundo_instrucoes, (0, 0))  # Desenha o fundo

        # Desenha título centralizado na tela
        largura_tela = 800
        fonte_titulo = pygame.font.SysFont("Comic Sans MS", 60)
        titulo = fonte_titulo.render("Instruções", True, (255, 255, 255))
        largura_texto = titulo.get_width()

        pos_x = (largura_tela - largura_texto) // 2
        pos_y = 30

        self.tela.blit(titulo, (pos_x, pos_y))  # Renderiza o título

        self.manager.draw_ui(self.tela)  # Desenha todos os elementos GUI
