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

        self.voltar_para_main = False  # flag para controlar retorno ao menu principal

        self.pontos = 0  # inicializa pontos do jogador
        self.vidas = 3  # número inicial de vidas
        self.tempo_total = 60  # tempo total do jogo em segundos
        self.inicio = pygame.time.get_ticks()  # marca o tempo inicial do jogo

        self.pergunta = ""  # string da pergunta atual
        self.resposta_certa = 0  # resposta correta da pergunta atual
        self.alternativas = []  # opções de resposta (botões)
        self.botoes = []  # lista de botões para alternativas

        self.gerar_pergunta()  # gera primeira pergunta
        self.criar_botoes()  # cria botões para respostas

        self.jogo_ativo = True  # flag que indica se o jogo está em andamento

    def gerar_pergunta(self):
        a = random.randint(1, 10)  # primeiro número aleatório
        b = random.randint(1, 10)  # segundo número aleatório
        operacao = random.choice(["+", "-", "*"])  # escolhe operação aleatória

        if operacao == "+":  # calcula resultado dependendo da operação
            resultado = a + b
        elif operacao == "-":
            resultado = a - b
        else:
            resultado = a * b

        self.pergunta = f"{a} {operacao} {b}"  # cria string da pergunta
        # cria lista com a resposta certa e duas opções erradas próximas
        opcoes = [resultado, resultado + random.randint(1, 5), resultado - random.randint(1, 5)]
        random.shuffle(opcoes)  # embaralha opções para não ficar previsível

        self.resposta_certa = resultado  # salva resposta correta
        self.alternativas = opcoes  # salva alternativas

    def criar_botoes(self):
        espaco_y = 300  # posição vertical inicial dos botões
        self.botoes.clear()  # limpa lista de botões
        for i in range(3):  # cria 3 botões para as alternativas
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((300, espaco_y + i * 70), (200, 50)),  # posição e tamanho
                text=str(self.alternativas[i]),  # texto do botão é a alternativa
                manager=self.manager
            )
            self.botoes.append(botao)  # adiciona botão à lista

    def mostrar_botoes_jogo(self):
        for botao in self.botoes:
            botao.show()  # mostra botões das alternativas
        self.botao_voltar.show()  # mostra botão voltar
        self.botao_recomecar.hide()  # esconde botão recomeçar (não é momento)
        self.botao_voltar_menu.hide()  # esconde botão voltar menu fim

    def mostrar_botoes_fim(self):
        for botao in self.botoes:
            botao.hide()  # esconde botões de alternativas no fim do jogo
        self.botao_voltar.hide()  # esconde botão voltar do jogo

        largura_tela = self.tela.get_width()  # pega largura da tela
        largura_botao = 200  # largura dos botões de fim de jogo
        espaco_entre = 40  # espaço entre os botões

        total_largura = largura_botao * 2 + espaco_entre  # total largura ocupada pelos dois botões
        x_inicio = (largura_tela - total_largura) // 2  # calcula posição horizontal inicial para centralizar

        self.botao_recomecar.set_position((x_inicio, 450))  # posiciona botão recomeçar
        self.botao_voltar_menu.set_position((x_inicio + largura_botao + espaco_entre, 450))  # posiciona botão voltar menu

        self.botao_recomecar.show()  # mostra botão recomeçar
        self.botao_voltar_menu.show()  # mostra botão voltar ao menu no fim

    def process_event(self, evento):
        self.manager.process_events(evento)  # repassa eventos para o gerenciador de UI

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:  # se algum botão foi pressionado
            if not self.jogo_ativo:  # se o jogo terminou
                if evento.ui_element == self.botao_recomecar:
                    self.reset_jogo()  # reinicia jogo se apertar recomeçar
                elif evento.ui_element == self.botao_voltar_menu:
                    self.voltar_para_main = True  # sinaliza para voltar ao menu principal
                return

            if evento.ui_element == self.botao_voltar:
                self.voltar_para_main = True  # voltar ao menu durante o jogo

            for botao in self.botoes:  # checa se alguma alternativa foi escolhida
                if evento.ui_element == botao:
                    if int(botao.text) == self.resposta_certa:
                        self.pontos += 1  # acerto: incrementa pontos
                    else:
                        self.vidas -= 1  # erro: perde uma vida
                        if self.vidas <= 0:  # se não tiver mais vidas
                            self.jogo_ativo = False  # termina o jogo
                            self.pontos = 0  # zera pontos
                            self.mostrar_botoes_fim()  # mostra botões do fim de jogo
                            return

                    if self.jogo_ativo:
                        self.gerar_pergunta()  # gera nova pergunta
                        for i in range(3):
                            self.botoes[i].set_text(str(self.alternativas[i]))  # atualiza texto dos botões

        if evento.type == pygame.KEYDOWN:  # se tecla pressionada
            if evento.key == pygame.K_ESCAPE:  # se for ESC, volta ao menu
                self.voltar_para_main = True

    def update(self, time_delta):
        self.manager.update(time_delta)  # atualiza gerenciador da UI com tempo decorrido

    def draw(self):
        tempo_passado = (pygame.time.get_ticks() - self.inicio) / 1000  # calcula tempo decorrido em segundos
        tempo_restante = max(0, int(self.tempo_total - tempo_passado))  # tempo restante não pode ser negativo

        self.tela.blit(self.fundo, (0, 0))  # desenha fundo na tela

        texto = self.fonte_grande.render("Desafio de Matemática", True, (255, 255, 255))  # título do jogo
        self.tela.blit(texto, (self.tela.get_width() // 2 - texto.get_width() // 2, 150))  # centraliza e desenha título

        if tempo_restante <= 0 or not self.jogo_ativo:  # se acabou o tempo ou jogo não ativo
            self.jogo_ativo = False  # marca jogo como não ativo
            self.mostrar_botoes_fim()  # mostra botões de fim

            texto_fim = self.fonte.render("Fim de jogo!", True, (255, 255, 255))  # texto fim
            pos_x = self.tela.get_width() // 2 - texto_fim.get_width() // 2
            pos_y = 350
            self.tela.blit(texto_fim, (pos_x, pos_y))  # desenha texto fim

            pontos_str = f"Sua pontuação: {self.pontos}"  # mostra pontuação final
            texto_pontos_fim = self.fonte.render(pontos_str, True, (255, 255, 255))
            pos_x_pontos = self.tela.get_width() // 2 - texto_pontos_fim.get_width() // 2
            self.tela.blit(texto_pontos_fim, (pos_x_pontos, 260))  # desenha pontuação

        else:  # jogo ativo e tempo restante
            self.jogo_ativo = True
            self.mostrar_botoes_jogo()  # mostra botões das alternativas

            texto_pergunta = self.fonte.render(f"Quanto é: {self.pergunta}?", True, (255, 255, 255))  # pergunta
            pos_x = (self.tela.get_width() - texto_pergunta.get_width()) // 2
            pos_y = 220
            self.tela.blit(texto_pergunta, (pos_x, pos_y))  # desenha pergunta

            texto_tempo = self.fonte.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))  # tempo restante
            texto_pontos = self.fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))  # pontos atuais
            self.tela.blit(texto_tempo, (10, 10))  # desenha tempo no canto superior esquerdo
            self.tela.blit(texto_pontos, (20, 60))  # desenha pontos abaixo do tempo

            for i in range(3):  # desenha corações que indicam vidas
                x = self.tela.get_width() - (i + 1) * (self.coracao_vermelho.get_width() + 5) - 10  # posição X
                y = 10  # posição Y
                if i < self.vidas:
                    self.tela.blit(self.coracao_vermelho, (x, y))  # coração cheio para vida restante
                else:
                    self.tela.blit(self.coracao_branco, (x, y))  # coração vazio para vida perdida

        self.manager.draw_ui(self.tela)  # desenha elementos da interface gráfica

    def reset_jogo(self):
        self.pontos = 0  # reseta pontos
        self.vidas = 3  # reseta vidas
        self.inicio = pygame.time.get_ticks()  # reseta tempo inicial
        self.gerar_pergunta()  # gera nova pergunta
        for i in range(3):
            self.botoes[i].set_text(str(self.alternativas[i]))  # atualiza texto dos botões

        self.mostrar_botoes_jogo()  # mostra botões do jogo
        self.jogo_ativo = True  # ativa o jogo
        self.voltar_para_main = False  # reseta flag para voltar ao menu
