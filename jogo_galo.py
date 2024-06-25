# 96859 Filipe Resendes

"""
Recebe um argumento de qualquer tipo e devolve True se o seu argumento
corresponde a um tabuleiro e False caso contrario
"""
def eh_tabuleiro(tab):
    if not isinstance(tab, tuple) or len(tab) != 3:
        return False
    for tup in tab:
        if not isinstance(tup, tuple) or len(tup) != 3:
            return False
        for pos in tup:
            if not isinstance(pos, int) or isinstance(pos, bool) or pos < -1 or pos > 1:
                return False
    return True

"""
Recebe um argumento de qualquer tipo e devolve True se o seu argumento
corresponde a uma posicao e False caso contrario
"""
def eh_posicao(pos):
    if not isinstance(pos, int) or isinstance(pos, bool) or pos < 1 or pos > 9:
        return False
    return True

"""
Recebe um tabuleiro e um inteiro com valor de 1 a 3 que representa o numero
da coluna, e devolve um vector com os valores dessa coluna
"""
def obter_coluna(tab, col):
    if not eh_tabuleiro(tab) or not isinstance(col, int) or col < 1 or col > 3 or isinstance(col, bool):
        raise ValueError("obter_coluna: algum dos argumentos e invalido")
    return tab[0][col - 1], tab[1][col - 1], tab[2][col - 1]

"""
Recebe um tabuleiro e um inteiro com valor de 1 a 3 que representa o numero
da linha, e devolve um vector com os valores dessa linha.
"""
def obter_linha(tab, lin):
    if not eh_tabuleiro(tab) or not isinstance(lin, int) or lin < 1 or lin > 3 or isinstance(lin, bool):
        raise ValueError("obter_linha: algum dos argumentos e invalido")
    return tab[lin - 1]

"""
Recebe um tabuleiro e um inteiro e devolve um vector com os valores dessa diagonal.
"""
def obter_diagonal(tab, dia):
    if not eh_tabuleiro(tab) or not isinstance(dia, int) or dia < 1 or dia > 2 or isinstance(dia, bool):
        raise ValueError("obter_diagonal: algum dos argumentos e invalido")
    if dia == 1:
        return tab[0][0], tab[1][1], tab[2][2]
    else:
        return tab[2][0], tab[1][1], tab[0][2]

"""
Recebe um tabuleiro e devolve a cadeia de caracteres que o representa.
"""
def tabuleiro_str(tab):
    if not eh_tabuleiro(tab):
        raise ValueError("tabuleiro_str: o argumento e invalido")
    strg = ""
    for tup in tab:
        for pos in tup:
            if pos == 1:
                strg += " X"
            elif pos == -1:
                strg += " O"
            else:
                strg += "  "
            strg += " |"
        strg = strg[:-1]
        strg += "\n-----------\n"
    return strg[:-13]

"""
Recebe um tabuleiro e uma posicao, e devolve True se a posicao corresponde
a uma posicao livre do tabuleiro e False caso contrario.
"""
def eh_posicao_livre(tab, pos):
    if not eh_tabuleiro(tab) or not eh_posicao(pos):
        raise ValueError("eh_posicao_livre: algum dos argumentos e invalido")
    if tab[(pos - 1) // 3][(pos - 1) % 3] == 0:
        return True
    else:
        return False

"""
Recebe um tabuleiro, e devolve o vector ordenado com todas as posicoes
livres do tabuleiro.
"""
def obter_posicoes_livres(tab):
    if not eh_tabuleiro(tab):
        raise ValueError("obter_posicoes_livres: o argumento e invalido")
    cont = 1
    pos_livres = []
    for tup in tab:
        for pos in tup:
            if pos == 0:
                pos_livres.append(cont)
            cont += 1
    return tuple(pos_livres)

"""
Recebe um tabuleiro, e devolve um valor inteiro a indicar o jogador que
ganhou a partida no tabuleiro passado por argumento.
"""
def jogador_ganhador(tab):
    if not eh_tabuleiro(tab):
        raise ValueError("jogador_ganhador: o argumento e invalido")
    for i in range(1, 4):
        if obter_coluna(tab, i) == (1, 1, 1) or obter_linha(tab, i) == (1, 1, 1):
            return 1
        if obter_coluna(tab, i) == (-1, -1, -1) or obter_linha(tab, i) == (-1, -1, -1):
            return -1
    for d in range(1, 3):
        if obter_diagonal(tab, d) == (1, 1, 1):
            return 1
        if obter_diagonal(tab, d) == (-1, -1, -1):
            return -1
    return 0

"""
Recebe um tabuleiro, um inteiro identificando um jogador e uma posicao livre, e devolve um novo tabuleiro modificado
com uma nova marca do jogador nessa posicao.
"""
def marcar_posicao(tab, jog, pos):
    if not eh_tabuleiro(tab) or not eh_posicao(pos) or (jog != 1 and jog != -1):
        raise ValueError("marcar_posicao: algum dos argumentos e invalido")
    if not eh_posicao_livre(tab, pos):
        raise ValueError("marcar_posicao: algum dos argumentos e invalido")
    new_tup = tab[(pos - 1) // 3][:(pos - 1) % 3] + (jog,) + tab[(pos - 1) // 3][(pos - 1) % 3 + 1:]
    return tab[:(pos - 1) // 3] + (new_tup,) + tab[(pos - 1) // 3 + 1:]

"""
Realiza a leitura de uma posicao introduzida manualmente por um jogador
e devolve esta posicao escolhida.
"""
def escolher_posicao_manual(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('escolher_posicao_manual: o argumento e invalido')
    pos_man = int(input('Turno do jogador. Escolha uma posicao livre: '))
    if not eh_posicao(pos_man) or not eh_posicao_livre(tab, pos_man):
        raise ValueError('escolher_posicao_manual: a posicao introduzida e invalida')
    return pos_man

"""
Considera em ordem os criterios 1 e 2.
"""
def estrategia_1_2(tab, pos, jog):
    if eh_posicao_livre(tab, pos):
        tab_prov = marcar_posicao(tab, jog, pos)
        if jogador_ganhador(tab_prov):
            return True
        tab_prov = marcar_posicao(tab, jog * (-1), pos)
        if jogador_ganhador(tab_prov):
            return True
    return False

"""
Verifica se a posicao dada e ocupada pelo jogador pretendido
"""
def posicao_ocupada_jog(tab, pos, jog):
    if tab[(pos - 1) // 3][(pos - 1) % 3] == jog:
        return True
    return False

"""
Verifica se há bifurcacao 
"""
def bifurcacao(tab, jog, pos):
    cont = 0
    if eh_posicao_livre(tab, pos):
        if jog in obter_linha(tab, ((pos - 1) // 3) + 1):
            cont += 1
        if jog in obter_coluna(tab, ((pos - 1) % 3) + 1):
            cont += 1
        if pos in (1, 5, 9) and jog in obter_diagonal(tab, 1):
            cont += 1
        if pos in (3, 5, 7) and jog in obter_diagonal(tab, 2):
            cont += 1
    if cont == 2:
        return True
    return False

"""
Considera em ordem os criterios 5, 7 e 8.
"""
def estrategia_basico(tab):
    if eh_posicao_livre(tab, 5):
        return 5
    for pos in range(1, 10, 2):
        if eh_posicao_livre(tab, pos):
            return pos
    for pos in range(2, 9, 2):
        if eh_posicao_livre(tab, pos):
            return pos

"""
Considera em ordem os criterios 1, 2, 5, 6, 7 e 8.
"""
def estrategia_normal(tab, jog):

    for pos in range(1, 9):
        if estrategia_1_2(tab, pos, jog):
            return pos
    if eh_posicao_livre(tab, 5):
        return 5
    cnt = 9
    for pos in range(1, 10, 2):
        if posicao_ocupada_jog(tab, pos, jog * (-1)) and eh_posicao_livre(tab, cnt):
            return cnt
        cnt -= 2
    for pos in range(1, 10, 2):
        if eh_posicao_livre(tab, pos):
            return pos
    for pos in range(2, 9, 2):
        if eh_posicao_livre(tab, pos):
            return pos
"""
Considera em ordem todos os criterios
"""
def estrategia_perfeito(tab, jog):
    for pos in range(1, 9):
        if estrategia_1_2(tab, pos, jog):
            return pos
    for pos in range(1, 10):
        if bifurcacao(tab, jog, pos):
            return pos
    for pos in range(1,10):
        if bifurcacao(tab, jog*(-1), pos):
            return pos
    if eh_posicao_livre(tab, 5):
        return 5
    cnt = 9
    for pos in range(1, 10, 2):
        if posicao_ocupada_jog(tab, pos, jog * (-1)) and eh_posicao_livre(tab, cnt):
            return cnt
        cnt -= 2
    for pos in range(1, 10, 2):
        if eh_posicao_livre(tab, pos):
            return pos
    for pos in range(2, 9, 2):
        if eh_posicao_livre(tab, pos):
            return pos

"""
Recebe um tabuleiro, um inteiro identicando um jogador e uma cadeia de carateres correspondente a estrategia, e
devolve a posicao escolhida automaticamente de acordo com a estrategia seleccionada.
"""
def escolher_posicao_auto(tab, jog, estrategia):
    if not eh_tabuleiro(tab) or (jog != 1 and jog != -1) or not isinstance(estrategia, str):
        raise ValueError('escolher_posicao_auto: algum dos argumentos e invalido')
    if estrategia != "basico" and estrategia != "normal" and estrategia != "perfeito":
        raise ValueError('escolher_posicao_auto: algum dos argumentos e invalido')
    if estrategia == "basico":
        return estrategia_basico(tab)
    elif estrategia == "normal":
        return estrategia_normal(tab, jog)
    elif estrategia == "perfeito":
        return estrategia_perfeito(tab, jog)


"""
Funcao principal que permite jogar um jogo completo de Jogo
do Galo de um jogador contra o computador.
"""
def jogo_do_galo(jog, estrategia):
    if not isinstance(jog, str) or not isinstance(estrategia, str):
        raise ValueError('jogo do galo: algum dos argumentos e invalido')
    if (jog != "X" and jog != "O") or estrategia not in ("basico", "normal", "perfeito"):
        raise ValueError('jogo do galo: algum dos argumentos e invalido')
    print("Bem-vindo ao JOGO DO GALO.\nO jogador joga com '%s'." % jog)
    run = True
    tab = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    cont = 0
    while run:
        if jog == "O":
            print("Turno do computador (%s):" % estrategia)
            tab = marcar_posicao(tab, 1, escolher_posicao_auto(tab, 1, estrategia))
        else:
            tab = marcar_posicao(tab, 1, escolher_posicao_manual(tab))
        print(tabuleiro_str(tab))
        cont += 1
        if jogador_ganhador(tab):
            return 'X'
        elif cont == 9:
            run = False
        else:
            if jog == "X":
                print("Turno do computador (%s):" % estrategia)
                tab = marcar_posicao(tab, -1, escolher_posicao_auto(tab, -1, estrategia))
            else:
                tab = marcar_posicao(tab, -1, escolher_posicao_manual(tab))
            print(tabuleiro_str(tab))
            cont += 1
            if jogador_ganhador(tab):
                return 'O'
    return 'EMPATE'

