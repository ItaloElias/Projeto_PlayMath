import pygame
import random
import pygame_gui

class TelaJogo:
    def __init__(self, tela_principal):
        self.tela = tela_principal
        self.manager = pygame_gui.UIManager(self.tela.get_size())

        self.fundo = pygame.image.load('fundo.jpg')
        self.fundo = pygame.transform.scale(self.fundo, self.tela.get_size())

        self.fonte = pygame.font.Font(None, 48)
        self.fonte_grande = pygame.font.SysFont(None, 60)

        # Botão voltar do jogo ativo
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 540), (150, 40)),
            text="Voltar ao Menu",
            manager=self.manager
        )

        # Botões para fim de jogo
        self.botao_recomecar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 450), (200, 50)),
            text="Recomeçar",
            manager=self.manager
        )
        self.botao_voltar_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((520, 450), (200, 50)),
            text="Voltar ao Menu",
            manager=self.manager
        )

        # Inicialmente escondemos esses botões de fim de jogo
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()

        self.voltar_para_main = False

        self.pontos = 0
        self.tempo_total = 60
        self.inicio = pygame.time.get_ticks()

        self.pergunta = ""
        self.resposta_certa = 0
        self.alternativas = []
        self.botoes = []

        self.gerar_pergunta()
        self.criar_botoes()

        self.jogo_ativo = True  # Controle se o jogo está rodando ou acabou

    def gerar_pergunta(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operacao = random.choice(["+", "-", "*"])

        if operacao == "+":
            resultado = a + b
        elif operacao == "-":
            resultado = a - b
        else:
            resultado = a * b

        self.pergunta = f"{a} {operacao} {b}"
        opcoes = [resultado, resultado + random.randint(1, 5), resultado - random.randint(1, 5)]
        random.shuffle(opcoes)

        self.resposta_certa = resultado
        self.alternativas = opcoes

    def criar_botoes(self):
        espaco_y = 200
        self.botoes.clear()
        for i in range(3):
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((300, espaco_y + i * 70), (200, 50)),
                text=str(self.alternativas[i]),
                manager=self.manager
            )
            self.botoes.append(botao)

    def process_event(self, evento):
        self.manager.process_events(evento)

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            # Botões do fim de jogo
            if not self.jogo_ativo:
                if evento.ui_element == self.botao_recomecar:
                    self.reset_jogo()
                elif evento.ui_element == self.botao_voltar_menu:
                    self.voltar_para_main = True
                return

            # Jogo ativo
            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True

            for botao in self.botoes:
                if evento.ui_element == botao:
                    if int(botao.text) == self.resposta_certa:
                        self.pontos += 1
                    self.gerar_pergunta()
                    for i in range(3):
                        self.botoes[i].set_text(str(self.alternativas[i]))

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.voltar_para_main = True

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self):
        tempo_passado = (pygame.time.get_ticks() - self.inicio) / 1000
        tempo_restante = max(0, int(self.tempo_total - tempo_passado))

        self.tela.blit(self.fundo, (0, 0))

        # Título
        texto = self.fonte_grande.render("Desafio de Matemática", True, (255, 255, 255))
        self.tela.blit(texto, (self.tela.get_width() // 2 - texto.get_width() // 2, 40))

        if tempo_restante <= 0:
            self.jogo_ativo = False

            # Esconder botões normais
            for botao in self.botoes:
                botao.hide()
            self.botao_voltar.hide()

            # Mostrar botões fim de jogo e centralizar horizontalmente
            largura_tela = self.tela.get_width()
            largura_botao = 200
            espaco_entre = 40

            total_largura = largura_botao * 2 + espaco_entre
            x_inicio = (largura_tela - total_largura) // 2

            self.botao_recomecar.set_position((x_inicio, 450))
            self.botao_voltar_menu.set_position((x_inicio + largura_botao + espaco_entre, 450))

            self.botao_recomecar.show()
            self.botao_voltar_menu.show()


            # Função para desenhar texto com contorno
            def draw_text_with_outline(surface, text, font, pos, text_color, outline_color):
                base = font.render(text, True, text_color)
                outline = font.render(text, True, outline_color)
                x, y = pos
                # Desenha contorno ao redor do texto (8 direções)
                for dx, dy in [(-2,0),(2,0),(0,-2),(0,2), (-2,-2), (2,-2), (-2,2), (2,2)]:
                    surface.blit(outline, (x + dx, y + dy))
                surface.blit(base, pos)

            # Texto com contorno branco e texto preto
            draw_text_with_outline(
                self.tela,
                "Fim de jogo!",
                self.fonte,
                (largura_tela//2 - self.fonte.size("Fim de jogo!")[0]//2, 200),
                (0, 0, 0),
                (255, 255, 255)
            )

            pontos_str = f"Sua pontuação: {self.pontos}"
            draw_text_with_outline(
                self.tela,
                pontos_str,
                self.fonte,
                (largura_tela//2 - self.fonte.size(pontos_str)[0]//2, 260),
                (0, 0, 0),
                (255, 255, 255)
            )

        else:
            self.jogo_ativo = True

            for botao in self.botoes:
                botao.show()
            self.botao_voltar.show()

            self.botao_recomecar.hide()
            self.botao_voltar_menu.hide()

            texto_pergunta = self.fonte.render(f"Quanto é: {self.pergunta}?", True, (255, 255, 255))
            self.tela.blit(texto_pergunta, (250, 120))

            texto_tempo = self.fonte.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))
            texto_pontos = self.fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
            self.tela.blit(texto_tempo, (10, 10))
            self.tela.blit(texto_pontos, (10, 60))

        self.manager.draw_ui(self.tela)

    def reset_jogo(self):
        self.pontos = 0
        self.inicio = pygame.time.get_ticks()
        self.gerar_pergunta()
        for i in range(3):
            self.botoes[i].set_text(str(self.alternativas[i]))

        for botao in self.botoes:
            botao.show()
        self.botao_voltar.show()
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()

        self.jogo_ativo = True
        self.voltar_para_main = False

    def reset_voltar(self):
        self.voltar_para_main = False
