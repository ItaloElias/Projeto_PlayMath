import pygame
import pygame_gui

class TelaInstrucoes:
    def __init__(self, tela_principal):
        self.tela = tela_principal  # Tela principal do pygame
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'theme.json')

        self.fundo_instrucoes = pygame.image.load('imagens/fundo_instrucoes.jpg')
        self.fundo_instrucoes = pygame.transform.scale(self.fundo_instrucoes, self.tela.get_size())

        # Botão para voltar
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (150, 40)),
            text="Voltar",
            manager=self.manager
        )
        self.voltar_para_main = False

        # Construa o texto em HTML com quebras de linha para facilitar a formatação
        self.instrucoes_html = (
            "- Regra 1: Escolha sua arma: +, - ou ×. Nada de dividir, aqui é pancadaria direta!<br>"
            "<p>- Regra 2: Você tem 30 segundos. Meio minutinho pra mostrar que sabe fazer conta.<br>"
            "<p>- Regra 3: Cada acerto vale ponto. Cada erro tira uma vida. Começou com 3, então não vacila.<br>"
            "<p>- Regra 4: Zerar as vidas? Game over. A matemática não perdoa.<br>"
            "<p>- Regra 5: Respira, foca, responde. O relógio não para, mas seu cérebro pode brilhar.<br>"
            "<p>- Regra 6: Se não for pra fazer conta com emoção, nem aperta 'Jogar'."
        )

        # Crie uma UITextBox que automaticamente habilita a rolagem se o texto for maior que a área definida.
        self.caixa_instrucoes = pygame_gui.elements.UITextBox(
            html_text=self.instrucoes_html,
            relative_rect=pygame.Rect(((self.tela.get_width() - 670) // 2, 150), (670, 400)),
            manager=self.manager,
            object_id="#textbox_instrucoes"
        )

    def process_event(self, evento):
        self.manager.process_events(evento)

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self):
        self.tela.blit(self.fundo_instrucoes, (0, 0))
        
        # Se preferir desenhar um título separado
        largura_tela = 800
        fonte_titulo = pygame.font.SysFont("Comic Sans MS", 60)
        titulo = fonte_titulo.render("Instruções", True, (255, 255, 255))
        largura_texto = titulo.get_width()

        pos_x = (largura_tela - largura_texto) // 2
        pos_y = 30

        self.tela.blit(titulo, (pos_x, pos_y))
        
        self.manager.draw_ui(self.tela)
