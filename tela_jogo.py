import pygame  # biblioteca principal para jogos
import random  # para gerar números aleatórios
import pygame_gui  # biblioteca para interface gráfica com botões e afins

class TelaJogo:
    def __init__(self, tela_principal):
        self.tela = tela_principal  # tela principal do pygame onde tudo será desenhado
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'theme.json')  # gerenciador de UI com tema

        self.fundo = pygame.image.load('imagens/fundo.jpg')  # carrega imagem de fundo
        self.fundo = pygame.transform.scale(self.fundo, self.tela.get_size())  # ajusta tamanho do fundo à tela

        self.fonte = pygame.font.SysFont("comicsansms", 48)  # fonte normal para textos
        self.fonte_grande = pygame.font.SysFont("comicsansms", 60)  # fonte maior para títulos

        self.coracao_vermelho = pygame.image.load('imagens/coracao_vermelho.png')  # imagem coração cheio (vida)
        self.coracao_vermelho = pygame.transform.scale(self.coracao_vermelho, (30, 30))  # redimensiona coração

        self.coracao_branco = pygame.image.load('imagens/coracao_branco.png')  # imagem coração vazio
        self.coracao_branco = pygame.transform.scale(self.coracao_branco, (30, 30))  # redimensiona coração vazio

        # botão para voltar ao menu principal
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 540), (150, 40)),
            text="Voltar ao Menu",
            manager=self.manager
        )

        # botão para recomeçar o jogo (escondido inicialmente)
        self.botao_recomecar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 450), (200, 50)),
            text="Recomeçar",
            manager=self.manager
        )
        # botão para voltar ao menu no fim do jogo (escondido inicialmente)
        self.botao_voltar_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((520, 450), (200, 50)),
            text="Voltar ao Menu",
            manager=self.manager
        )

        self.botao_recomecar.hide()  # esconde botão recomeçar
        self.botao_voltar_menu.hide()  # esconde botão voltar ao menu no fim

        # Botões para escolher operação (mesmo estilo dos outros)
        self.botoes_operacoes = []
        op_x = 250  # posição horizontal inicial para botões de operação
        op_y = 250  # posição vertical fixa para os botões
        largura_botao = 100
        altura_botao = 50
        espacamento = 150
        for i, op in enumerate(['+', '-', '*']):
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((op_x + i * espacamento, op_y), (largura_botao, altura_botao)),
                text=op,
                manager=self.manager
            )
            self.botoes_operacoes.append(botao)

        self.voltar_para_main = False  # flag para controlar retorno ao menu principal

        self.pontos = 0  # inicializa pontos do jogador
        self.vidas = 3  # número inicial de vidas
        self.tempo_total = 30  # tempo total do jogo em segundos
        self.inicio = pygame.time.get_ticks()  # marca o tempo inicial do jogo

        self.pergunta = ""  # string da pergunta atual
        self.resposta_certa = 0  # resposta correta da pergunta atual
        self.alternativas = []  # opções de resposta (botões)
        self.botoes = []  # lista de botões para alternativas

        self.jogo_ativo = False  # só ativa quando operação escolhida
        self.operacao_escolhida = None  # operação matemática escolhida pelo jogador

    def gerar_pergunta(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operacao = self.operacao_escolhida

        if operacao == "+":
            resultado = a + b
        elif operacao == "-":
            resultado = a - b
        else:  # "*"
            resultado = a * b

        self.pergunta = f"{a} {operacao} {b}"

        opcoes = [resultado, resultado + random.randint(1, 5), resultado - random.randint(1, 5)]
        random.shuffle(opcoes)

        self.resposta_certa = resultado
        self.alternativas = opcoes

    def criar_botoes(self):
        espaco_y = 300
        self.botoes.clear()
        for i in range(3):
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((300, espaco_y + i * 70), (200, 50)),
                text=str(self.alternativas[i]),
                manager=self.manager
            )
            self.botoes.append(botao)

    def mostrar_botoes_jogo(self):
        for botao in self.botoes:
            botao.show()
        self.botao_voltar.show()
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()

    def mostrar_botoes_fim(self):
        for botao in self.botoes:
            botao.hide()
        self.botao_voltar.hide()

        largura_tela = self.tela.get_width()
        largura_botao = 200
        espaco_entre = 40

        total_largura = largura_botao * 2 + espaco_entre
        x_inicio = (largura_tela - total_largura) // 2

        self.botao_recomecar.set_position((x_inicio, 450))
        self.botao_voltar_menu.set_position((x_inicio + largura_botao + espaco_entre, 450))

        self.botao_recomecar.show()
        self.botao_voltar_menu.show()

    def process_event(self, evento):
        self.manager.process_events(evento)

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            # Se operação ainda não escolhida, verifica botões de operação
            if self.operacao_escolhida is None:
                for botao in self.botoes_operacoes:
                    if evento.ui_element == botao:
                        self.operacao_escolhida = botao.text
                        self.gerar_pergunta()
                        self.criar_botoes()
                        self.jogo_ativo = True
                        # Esconde os botões de operação para não poluir a tela
                        for b in self.botoes_operacoes:
                            b.hide()
                        return

            if not self.jogo_ativo:
                if evento.ui_element == self.botao_recomecar:
                    self.reset_jogo()
                elif evento.ui_element == self.botao_voltar_menu:
                    self.voltar_para_main = True
                return

            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True

            for botao in self.botoes:
                if evento.ui_element == botao:
                    if int(botao.text) == self.resposta_certa:
                        self.pontos += 1
                    else:
                        self.vidas -= 1
                        if self.vidas <= 0:
                            self.jogo_ativo = False
                            self.pontos = 0
                            self.mostrar_botoes_fim()
                            return

                    if self.jogo_ativo:
                        self.gerar_pergunta()
                        for i in range(3):
                            self.botoes[i].set_text(str(self.alternativas[i]))

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.voltar_para_main = True

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self):
        self.tela.blit(self.fundo, (0, 0))

        # Se operação ainda não foi escolhida, mostra tela de escolha
        if self.operacao_escolhida is None:
            texto = self.fonte_grande.render("Escolha a Operação", True, (255, 255, 255))
            self.tela.blit(texto, (self.tela.get_width() // 2 - texto.get_width() // 2, 150))
            for botao in self.botoes_operacoes:
                botao.show()
            self.manager.draw_ui(self.tela)
            return
        else:
            for botao in self.botoes_operacoes:
                botao.hide()

        tempo_passado = (pygame.time.get_ticks() - self.inicio) / 1000
        tempo_restante = max(0, int(self.tempo_total - tempo_passado))

        texto = self.fonte_grande.render("Desafio de Matemática", True, (255, 255, 255))
        self.tela.blit(texto, (self.tela.get_width() // 2 - texto.get_width() // 2, 150))

        if tempo_restante <= 0 or not self.jogo_ativo:
            self.jogo_ativo = False
            self.mostrar_botoes_fim()

            texto_fim = self.fonte.render("Fim de jogo!", True, (255, 255, 255))
            pos_x = self.tela.get_width() // 2 - texto_fim.get_width() // 2
            pos_y = 350
            self.tela.blit(texto_fim, (pos_x, pos_y))

            pontos_str = f"Sua pontuação: {self.pontos}"
            texto_pontos_fim = self.fonte.render(pontos_str, True, (255, 255, 255))
            pos_x_pontos = self.tela.get_width() // 2 - texto_pontos_fim.get_width() // 2
            self.tela.blit(texto_pontos_fim, (pos_x_pontos, 260))

        else:
            self.jogo_ativo = True
            self.mostrar_botoes_jogo()

            texto_pergunta = self.fonte.render(f"Quanto é: {self.pergunta} ?", True, (255, 255, 255))
            self.tela.blit(texto_pergunta, (self.tela.get_width() // 2 - texto_pergunta.get_width() // 2, 215))
                    # Desenha vidas
        for i in range(3):
            if i < self.vidas:
                self.tela.blit(self.coracao_vermelho, (20 + i * 40, 20))
            else:
                self.tela.blit(self.coracao_branco, (20 + i * 40, 20))

        # Desenha pontuação
        if self.jogo_ativo:
            texto_pontos = self.fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
            self.tela.blit(texto_pontos, (self.tela.get_width() - 230, 20))

        # Desenha cronômetro
        if self.jogo_ativo:
            texto_tempo = self.fonte.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))
            self.tela.blit(texto_tempo, (self.tela.get_width() // 2 - texto_tempo.get_width() // 2, 70))

        self.manager.draw_ui(self.tela)

    def reset_jogo(self):
        self.pontos = 0
        self.vidas = 3
        self.inicio = pygame.time.get_ticks()
        self.operacao_escolhida = None
        self.jogo_ativo = False
        for botao in self.botoes:
            botao.hide()
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()
        for botao in self.botoes_operacoes:
            botao.show()

