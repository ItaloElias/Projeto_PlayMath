import pygame  # engine gráfica principal
import random  # geração de números aleatórios para perguntas
import pygame_gui  # gerenciador de UI para botões e interface gráfica
import datetime # para registro da data e hora no histórico

class TelaJogo:
    def __init__(self, tela_principal):
        self.tela = tela_principal
        self.manager = pygame_gui.UIManager(self.tela.get_size(), 'fonts_temas/theme.json')

        # Configura fundo e fontes
        self.fundo = pygame.image.load('imagens/fundo.jpg')
        self.fundo = pygame.transform.scale(self.fundo, self.tela.get_size())
        self.fonte = pygame.font.SysFont("comicsansms", 48)
        self.fonte_grande = pygame.font.SysFont("comicsansms", 60)

        # Imagens para representar vidas (corações)
        self.coracao_vermelho = pygame.image.load('imagens/coracao_vermelho.png')
        self.coracao_vermelho = pygame.transform.scale(self.coracao_vermelho, (30, 30))
        self.coracao_branco = pygame.image.load('imagens/coracao_branco.png')
        self.coracao_branco = pygame.transform.scale(self.coracao_branco, (30, 30))

        # Botões principais de navegação e controle
        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 540), (150, 40)),
            text="Voltar ao Menu",
            manager=self.manager
        )
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
        # Botão Histórico - inicialmente oculto
        self.botao_historico = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((80, 450), (200, 40)),
            text="Histórico",
            manager=self.manager
        )
        
        # Esconde botões de fim de jogo inicialmente        
        self.botao_historico.hide()
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()

        # Criação dos botões para escolha da operação matemática (+, -, *)
        self.botoes_operacoes = []
        largura_botao = 100
        altura_botao = 50
        espacamento = 50
        total_largura = (largura_botao * 3) + (espacamento * 2)
        op_x_inicio = (self.tela.get_width() - total_largura) // 2
        op_y = 250
        for i, op in enumerate(['+', '-', '*']):
            x = op_x_inicio + i * (largura_botao + espacamento)
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, op_y), (largura_botao, altura_botao)),
                text=op,
                manager=self.manager
            )
            self.botoes_operacoes.append(botao)

        # Flags e variáveis de controle do jogo
        self.voltar_para_main = False
        self.pontos = 0
        self.vidas = 3
        self.tempo_total = 30  # tempo total do desafio em segundos
        self.inicio = None  # timestamp do início do jogo (define quando começa o cronômetro)

        # Variáveis para pergunta, resposta e botões de alternativas
        self.pergunta = ""
        self.resposta_certa = 0
        self.alternativas = []
        self.botoes = []

        self.jogo_ativo = False
        self.operacao_escolhida = None

        # NOVO: Histórico das partidas
        self.historico_partidas = []

        # NOVO: Janela do histórico (para controlar abertura/fechamento)
        self.janela_historico = None
        self.fim_de_jogo_exibido = False


    def gerar_pergunta(self):
        # Gera uma pergunta e três alternativas (uma correta + duas incorretas)
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operacao = self.operacao_escolhida

        if operacao == "+":
            resultado = a + b
        elif operacao == "-":
            resultado = a - b
        else:
            resultado = a * b

        self.pergunta = f"{a} {operacao} {b}"

        # Cria lista de alternativas e embaralha para apresentar
        opcoes = [resultado, resultado + random.randint(1, 5), resultado - random.randint(1, 5)]
        random.shuffle(opcoes)

        self.resposta_certa = resultado
        self.alternativas = opcoes

    def criar_botoes(self):
        # Cria botões para as alternativas das respostas
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
        # Exibe botões de respostas e esconde botões de fim de jogo
        for botao in self.botoes:
            botao.show()
        self.botao_voltar.show()
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()

    def mostrar_botoes_fim(self):
        # Esconde botões de resposta e exibe botões de recomeçar e voltar ao menu
        for botao in self.botoes:
            botao.hide()    
        self.botao_voltar.hide()

        largura_tela = self.tela.get_width()
        largura_botao = 200
        altura_botao = 50
        espaco_entre = 40

        total_largura = largura_botao * 3 + espaco_entre * 2
        x_inicio = (largura_tela - total_largura) // 2
        y = 450 

        self.botao_recomecar.set_position((x_inicio, y))
        self.botao_recomecar.set_dimensions((largura_botao, altura_botao))
        self.botao_voltar_menu.set_position((x_inicio + largura_botao + espaco_entre, y))
        self.botao_voltar_menu.set_dimensions((largura_botao, altura_botao))
        self.botao_historico.set_position((x_inicio + (largura_botao + espaco_entre) * 2, y))
        self.botao_historico.set_dimensions((largura_botao, altura_botao))

        self.botao_recomecar.show()
        self.botao_voltar_menu.show()
        self.botao_historico.show() 

    def process_event(self, evento):
        # Processa eventos da UI, incluindo escolha de operação, respostas e navegação
        self.manager.process_events(evento)

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            # Se ainda não escolheu operação, trata escolha
            if self.operacao_escolhida is None:
                for botao in self.botoes_operacoes:
                    if evento.ui_element == botao:
                        self.operacao_escolhida = botao.text
                        self.inicio = pygame.time.get_ticks()  # inicia o cronômetro
                        self.gerar_pergunta()
                        self.criar_botoes()
                        self.jogo_ativo = True
                        for b in self.botoes_operacoes:
                            b.hide()
                        return

            # Botão voltar ao menu
            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True
                return

            # NOVO: Botão Histórico abre/fecha janela do histórico
            if evento.ui_element == self.botao_historico:
                if self.janela_historico is not None:
                    self.janela_historico.kill()
                    self.janela_historico = None
                else:
                    largura = 400
                    altura = 300
                    x = (self.tela.get_width() - largura) // 2
                    y = (self.tela.get_height() - altura) // 2
                    self.janela_historico = pygame_gui.elements.UIWindow(
                        pygame.Rect((x, y), (largura, altura)),
                        self.manager,
                        window_display_title="Histórico"
                    )
                    texto = "\n".join(self.historico_partidas) if self.historico_partidas else "Nenhuma partida feita."
                    self.texto_historico = pygame_gui.elements.UITextBox(
                        html_text=texto,
                        relative_rect=pygame.Rect((10, 10), (largura - 20, altura - 20)),
                        manager=self.manager,
                        container=self.janela_historico
                    )
                return
            # Se jogo não ativo, controla botões de recomeçar e voltar do fim
            if not self.jogo_ativo:
                if evento.ui_element == self.botao_recomecar:
                    self.reset_jogo()
                elif evento.ui_element == self.botao_voltar_menu:
                    self.voltar_para_main = True
                return
                       

            # Checagem de respostas durante o jogo ativo
            for botao in self.botoes:
                if evento.ui_element == botao:
                    # Acertou a resposta: soma ponto; errou: perde vida
                    if int(botao.text) == self.resposta_certa:
                        self.pontos += 1
                    else:
                        self.vidas -= 1
                        if self.vidas <= 0:
                            # Game over: finaliza jogo e mostra opções
                            self.jogo_ativo = False
                            self.pontos = self.pontos

                            # Salva no histórico
                            #self.historico_partidas.append(registro)
    
                            self.mostrar_botoes_fim()
                            return

                    # Se ainda ativo, gera nova pergunta e atualiza botões
                    if self.jogo_ativo:
                        self.gerar_pergunta()
                        for i in range(3):
                            self.botoes[i].set_text(str(self.alternativas[i]))

        # Suporte para tecla ESC: sair para menu
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.voltar_para_main = True

    def update(self, time_delta):
        # Atualiza o gerenciador de UI a cada frame
        self.manager.update(time_delta)

    def draw(self):
        # Renderiza fundo, interface, tempo, vidas, pontos e perguntas
        self.tela.blit(self.fundo, (0, 0))

        # Se operação ainda não escolhida, mostra instrução e botões de operação
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

        # Calcula tempo decorrido desde o início do jogo (cronômetro)
        if self.inicio is None:
            tempo_passado = 0
        else:
            tempo_passado = (pygame.time.get_ticks() - self.inicio) / 1000

        tempo_restante = max(0, int(self.tempo_total - tempo_passado))

        # Título do jogo na tela
        texto = self.fonte_grande.render("Desafio de Matemática", True, (255, 255, 255))
        self.tela.blit(texto, (self.tela.get_width() // 2 - texto.get_width() // 2, 150))

        # Verifica fim do tempo ou do jogo para mudar interface
        if tempo_restante <= 0 or not self.jogo_ativo:
            self.jogo_ativo = False
            if not self.fim_de_jogo_exibido:
                agora = datetime.datetime.now()
                registro = f"{agora.strftime('%d/%m/%Y %H:%M:%S')} - Pontuação: {self.pontos}"
                self.historico_partidas.append(registro)
                
                self.mostrar_botoes_fim()
                self.fim_de_jogo_exibido = True

            # Mensagem de fim de jogo e pontuação final
            texto_fim = self.fonte.render("Fim de jogo!", True, (255, 255, 255))
            pos_x = self.tela.get_width() // 2 - texto_fim.get_width() // 2
            pos_y = 350
            self.tela.blit(texto_fim, (pos_x, pos_y))

            pontos_str = f"Sua pontuação: {self.pontos}"
            texto_pontos_fim = self.fonte.render(pontos_str, True, (255, 255, 255))
            pos_x_pontos = self.tela.get_width() // 2 - texto_pontos_fim.get_width() // 2
            self.tela.blit(texto_pontos_fim, (pos_x_pontos, 260))

        else:
            # Jogo ativo: mostra perguntas e botões de resposta
            self.jogo_ativo = True
            self.mostrar_botoes_jogo()

            texto_pergunta = self.fonte.render(f"Quanto é: {self.pergunta} ?", True, (255, 255, 255))
            self.tela.blit(texto_pergunta, (self.tela.get_width() // 2 - texto_pergunta.get_width() // 2, 215))

        # Mostra corações preenchidos e vazios para vidas restantes
        if self.jogo_ativo:
            for i in range(3):
                if i < self.vidas:
                    self.tela.blit(self.coracao_vermelho, (20 + i * 40, 20))
                else:
                    self.tela.blit(self.coracao_branco, (20 + i * 40, 20))
        
        # Mostra pontos e tempo restantes durante o jogo ativo
        if self.jogo_ativo:

            texto_pontos = self.fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
            self.tela.blit(texto_pontos, (self.tela.get_width() - 230, 20))

            texto_tempo = self.fonte.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))
            self.tela.blit(texto_tempo, (self.tela.get_width() // 2 - texto_tempo.get_width() // 2, 70))

        self.manager.draw_ui(self.tela)

    def reset_jogo(self):
        # Reseta variáveis do jogo para o estado inicial, aguardando escolha da operação
        self.pontos = 0
        self.vidas = 3
        self.inicio = None  # reseta cronômetro
        self.operacao_escolhida = None
        self.jogo_ativo = False
        self.fim_de_jogo_exibido = False


        # Esconde botões de resposta e fim, mostra botões de operação
        for botao in self.botoes:
            botao.hide()
        self.botao_recomecar.hide()
        self.botao_voltar_menu.hide()
        self.botao_historico.hide()
        for botao in self.botoes_operacoes:
            botao.show()
