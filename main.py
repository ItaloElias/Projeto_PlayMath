import pygame
import pygame_gui
import webbrowser
from tela_jogo import TelaJogo         
from tela_instrucoes import TelaInstrucoes 
from opcoes import TelaOpcoes          

pygame.init()  # Inicializa módulos do pygame
screen = pygame.display.set_mode((800, 600))  # Cria janela do jogo
pygame.display.set_caption("Jogo")  # Define o título da janela

fundo = pygame.image.load('imagens/fundo.jpg')  # Carrega imagem de fundo
fundo = pygame.transform.scale(fundo, (800, 600))  # Redimensiona imagem

fontawesome = pygame.font.Font('fa-solid-900.ttf', 40)  # Fonte para ícone

# Cores para botões e ícones
cor_normal = (255, 255, 255)
cor_clicado = (180, 180, 180)
cor_hover = (255, 255, 180)

# Gerenciador de interface com tema personalizado
manager = pygame_gui.UIManager((800, 600), 'theme.json')

# Botão "Jogar"
botao_jogar = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((260, 215), (280, 50)),
    text='Jogar',
    manager=manager
)
# Botão "Instruções"
botao_instrucao = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 275), (200, 50)),
    text='Instruções',
    manager=manager
)
# Botão "Sair"
botao_sair = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 335), (200, 50)),
    text='Sair',
    manager=manager
)

clock = pygame.time.Clock()  # Relógio do jogo
rodando = True  # Controle principal do loop

# Estados do clique e hover
clicado = False
hover_hamburguer = False

# Ícone do Instagram
instagram_icon = pygame.image.load('imagens/instagram.png')
instagram_icon = pygame.transform.scale(instagram_icon, (40, 40))
instagram_pos = (10, 600 - 50)

instagram_clicado = False
hover_instagram = False

tela_atual = "main"  # Define tela inicial

# Instancia as telas
tela_jogo = TelaJogo(screen)
tela_instrucoes = TelaInstrucoes(screen)
tela_opcoes = TelaOpcoes(screen)

# Função para desenhar o fundo da tela principal
def desenhar_tela_principal():
    screen.blit(fundo, (0, 0))

# Loop principal do jogo
while rodando:
    time_delta = clock.tick(60) / 1000.0  # Tempo entre frames
    mouse_pos = pygame.mouse.get_pos()  # Posição do mouse

    for evento in pygame.event.get():  # Loop de eventos
        if evento.type == pygame.QUIT:  # Fecha o jogo
            rodando = False

        if tela_atual == "main":
            if evento.type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == botao_sair:  # Clique no botão "Sair"
                    rodando = False
                elif evento.ui_element == botao_jogar:  # Clique no botão "Jogar"
                    tela_atual = "jogo"
                    tela_jogo.reset_jogo()
                elif evento.ui_element == botao_instrucao:  # Clique no botão "Instruções"
                    tela_atual = "instrucoes"

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Detecta clique no ícone hambúrguer
                texto_icone_temp = fontawesome.render('\uf0c9', True, cor_normal)
                icone_rect_temp = texto_icone_temp.get_rect(topleft=(800 - 60, 10))
                if icone_rect_temp.collidepoint(evento.pos):
                    clicado = True

                # Detecta clique no ícone do Instagram
                icon_rect = instagram_icon.get_rect(topleft=instagram_pos)
                if icon_rect.collidepoint(evento.pos):
                    instagram_clicado = True

            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica clique completo no hambúrguer
                texto_icone_temp = fontawesome.render('\uf0c9', True, cor_normal)
                icone_rect_temp = texto_icone_temp.get_rect(topleft=(800 - 60, 10))
                if icone_rect_temp.collidepoint(evento.pos) and clicado:
                    tela_atual = "opcoes"  # Abre a tela de opções

                clicado = False

                # Abre o link do Instagram
                icon_rect = instagram_icon.get_rect(topleft=instagram_pos)
                if icon_rect.collidepoint(evento.pos) and instagram_clicado:
                    webbrowser.open("https://www.instagram.com/seu_perfil_aqui/")
                instagram_clicado = False

            manager.process_events(evento)  # Passa eventos para o pygame_gui

        elif tela_atual == "jogo":
            tela_jogo.process_event(evento)  # Encaminha evento para tela do jogo

        elif tela_atual == "instrucoes":
            tela_instrucoes.process_event(evento)  # Encaminha evento para instruções

        elif tela_atual == "opcoes":
            tela_opcoes.process_event(evento)  # Encaminha evento para opções

    # Hover no ícone hambúrguer
    texto_icone_hover = fontawesome.render('\uf0c9', True, cor_normal)
    icone_rect_hover = texto_icone_hover.get_rect(topleft=(800 - 60, 10))
    hover_hamburguer = icone_rect_hover.collidepoint(mouse_pos)

    # Hover no ícone do Instagram
    icon_rect = instagram_icon.get_rect(topleft=instagram_pos)
    hover_instagram = icon_rect.collidepoint(mouse_pos)

    # Renderiza a tela conforme o estado atual
    if tela_atual == "main":
        desenhar_tela_principal()
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Ícone hambúrguer com efeito visual
        cor_hamburguer = cor_clicado if clicado else (cor_hover if hover_hamburguer else cor_normal)
        texto_icone = fontawesome.render('\uf0c9', True, cor_hamburguer)
        screen.blit(texto_icone, (800 - 60, 10))

        # Efeito visual no ícone do Instagram
        if instagram_clicado:
            screen.blit(instagram_icon, (instagram_pos[0] + 3, instagram_pos[1] + 3))
        elif hover_instagram:
            icone_branco = instagram_icon.copy()
            icone_branco.fill((255, 255, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(icone_branco, instagram_pos)
        else:
            screen.blit(instagram_icon, instagram_pos)

    elif tela_atual == "jogo":
        tela_jogo.update(time_delta)
        tela_jogo.draw()
        if tela_jogo.voltar_para_main:  # Verifica se jogo pediu retorno ao menu
            tela_atual = "main"
            tela_jogo.voltar_para_main = False

    elif tela_atual == "instrucoes":
        tela_instrucoes.update(time_delta)
        tela_instrucoes.draw()
        if tela_instrucoes.voltar_para_main:  # Retorna ao menu se solicitado
            tela_atual = "main"
            tela_instrucoes.voltar_para_main = False

    elif tela_atual == "opcoes":
        tela_opcoes.update(time_delta)
        tela_opcoes.draw()
        if tela_opcoes.voltar_para_main:  # Retorna ao menu se solicitado
            tela_atual = "main"
            tela_opcoes.voltar_para_main = False

    pygame.display.flip()  # Atualiza a tela

pygame.quit()  # Encerra o jogo
