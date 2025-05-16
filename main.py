import pygame
import pygame_gui
import webbrowser
from opcoes import TelaOpcoes
from tela_regras import TelaRegras
from tela_jogo import TelaJogo

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jogo")

# Carrega e ajusta a imagem de fundo para a tela principal
fundo = pygame.image.load('fundo.jpg')
fundo = pygame.transform.scale(fundo, (800, 600))

# Fonte do FontAwesome para o ícone hambúrguer no canto superior direito
fontawesome = pygame.font.Font('fa-solid-900.ttf', 40)

# Cores para estados do ícone hambúrguer (normal, clicado, hover)
cor_normal = (255, 255, 255)
cor_clicado = (180, 180, 180)
cor_hover = (255, 255, 180)

# Gerenciador da interface pygame_gui para a tela principal
manager = pygame_gui.UIManager((800, 600))

# Botões da tela principal: Jogar, Regras e Sair
botao1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((260, 215), (280, 50)),
    text='Jogar',
    manager=manager
)
botao2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 275), (200, 50)),
    text='Regras',
    manager=manager
)
botao3 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 335), (200, 50)),
    text='Sair',
    manager=manager
)

clock = pygame.time.Clock()  # Controla os FPS do jogo
rodando = True  # Flag para manter o loop principal ativo

# Controle dos estados de clique e hover do ícone hambúrguer
clicado = False
hover_hamburguer = False

# Carrega o ícone do Instagram e define sua posição na tela
instagram_icon = pygame.image.load('instagram.png')
instagram_icon = pygame.transform.scale(instagram_icon, (40, 40))
instagram_pos = (10, 600 - 50)

instagram_clicado = False
hover_instagram = False

# Controla qual tela está ativa: main, opcoes, regras ou jogo
tela_atual = "main"

# Instancia as classes de cada tela, passando a tela principal para elas
tela_opcoes = TelaOpcoes(screen)
tela_regras = TelaRegras(screen)
tela_jogo = TelaJogo(screen)  # Tela do jogo com botão para voltar

# Função para desenhar a tela principal (fundo + botões gerenciados pelo pygame_gui)
def desenhar_tela_principal():
    screen.blit(fundo, (0, 0))

# Loop principal do jogo
while rodando:
    # Controla o tempo para atualização da UI e FPS
    time_delta = clock.tick(60) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    # Processa todos os eventos da fila do pygame
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False  # Sai do loop ao fechar a janela

        if tela_atual == "main":
            # Eventos de clique nos botões da tela principal
            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == botao3:  # Botão Sair
                    rodando = False
                elif evento.ui_element == botao1:  # Botão Jogar
                    tela_atual = "jogo"
                elif evento.ui_element == botao2:  # Botão Regras
                    tela_atual = "regras"

            # Eventos para detectar clique no ícone hambúrguer
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                texto_icone_temp = fontawesome.render('\uf0c9', True, cor_normal)
                icone_rect_temp = texto_icone_temp.get_rect(topleft=(800 - 60, 10))
                if icone_rect_temp.collidepoint(evento.pos):
                    clicado = True

                # Clique no ícone do Instagram
                icon_rect = instagram_icon.get_rect(topleft=instagram_pos)
                if icon_rect.collidepoint(evento.pos):
                    instagram_clicado = True

            elif evento.type == pygame.MOUSEBUTTONUP:
                texto_icone_temp = fontawesome.render('\uf0c9', True, cor_normal)
                icone_rect_temp = texto_icone_temp.get_rect(topleft=(800 - 60, 10))
                # Ao soltar clique no hambúrguer, abre tela de opções
                if icone_rect_temp.collidepoint(evento.pos):
                    tela_atual = "opcoes"
                clicado = False

                # Abre o Instagram no navegador se clicado
                icon_rect = instagram_icon.get_rect(topleft=instagram_pos)
                if icon_rect.collidepoint(evento.pos) and instagram_clicado:
                    webbrowser.open("https://www.instagram.com/seu_perfil_aqui/")
                instagram_clicado = False

            # Passa eventos para o pygame_gui gerenciar os botões da main
            manager.process_events(evento)

        elif tela_atual == "opcoes":
            # Passa evento para a tela de opções processar
            tela_opcoes.process_event(evento)

        elif tela_atual == "regras":
            # Passa evento para a tela de regras processar
            tela_regras.process_event(evento)

        elif tela_atual == "jogo":
            # Passa evento para a tela de jogo processar (inclui botão voltar)
            tela_jogo.process_event(evento)

    # Detecta hover do mouse sobre o ícone hambúrguer
    texto_icone_hover = fontawesome.render('\uf0c9', True, cor_normal)
    icone_rect_hover = texto_icone_hover.get_rect(topleft=(800 - 60, 10))
    hover_hamburguer = icone_rect_hover.collidepoint(mouse_pos)

    # Detecta hover do mouse sobre o ícone Instagram
    icon_rect = instagram_icon.get_rect(topleft=instagram_pos)
    hover_instagram = icon_rect.collidepoint(mouse_pos)

    # Desenha a tela atual
    if tela_atual == "main":
        desenhar_tela_principal()
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Altera a cor do ícone hambúrguer conforme estado (normal, hover, clicado)
        if clicado:
            cor_hamburguer = cor_clicado
        elif hover_hamburguer:
            cor_hamburguer = cor_hover
        else:
            cor_hamburguer = cor_normal

        texto_icone = fontawesome.render('\uf0c9', True, cor_hamburguer)
        screen.blit(texto_icone, (800 - 60, 10))

        # Efeito hover e clicado para o ícone Instagram
        if instagram_clicado:
            screen.blit(instagram_icon, (instagram_pos[0] + 3, instagram_pos[1] + 3))
        elif hover_instagram:
            icone_branco = instagram_icon.copy()
            icone_branco.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(icone_branco, instagram_pos)
        else:
            screen.blit(instagram_icon, instagram_pos)

    elif tela_atual == "opcoes":
        # Atualiza e desenha a tela de opções
        tela_opcoes.update(time_delta)
        tela_opcoes.draw()
        # Verifica se a tela de opções sinalizou para voltar ao menu principal
        if tela_opcoes.voltar_para_main:
            tela_atual = "main"
            tela_opcoes.voltar_para_main = False

    elif tela_atual == "regras":
        # Atualiza e desenha a tela de regras
        tela_regras.update(time_delta)
        tela_regras.draw()
        # Verifica se a tela de regras sinalizou para voltar ao menu principal
        if tela_regras.voltar_para_main:
            tela_atual = "main"
            tela_regras.voltar_para_main = False

    elif tela_atual == "jogo":
        # Atualiza e desenha a tela de jogo (com botão voltar implementado na classe)
        tela_jogo.update(time_delta)
        tela_jogo.draw()
        # Verifica se a tela de jogo sinalizou para voltar ao menu principal
        if tela_jogo.voltar_para_main:
            tela_atual = "main"
            tela_jogo.reset_voltar()  # Método para resetar flag da tela de jogo

    pygame.display.flip()  # Atualiza a tela

pygame.quit()  # Encerra o pygame ao sair do loop
