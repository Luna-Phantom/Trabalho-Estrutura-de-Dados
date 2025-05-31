from graphviz import Digraph

class Computador:
    def __init__(self, ip):
        self.ip = ip
        self.esquerdo = None
        self.direito = None

def inserir(raiz, ip):
    if raiz is None:
        return Computador(ip)
    if ip < raiz.ip:
        raiz.esquerdo = inserir(raiz.esquerdo, ip)
    else:
        raiz.direito = inserir(raiz.direito, ip)
    return raiz

def desenhar(raiz):
    dot = Digraph(format='png')
    dot.attr('node', shape='egg', style='filled', color='purple')

    def desenho_recursivo(no):
        if no is None:
            return
        dot.node(str(no.ip))

        if no.esquerdo:
            dot.edge(str(no.ip), str(no.esquerdo.ip), label="esq")
            desenho_recursivo(no.esquerdo)
        if no.direito:
            dot.edge(str(no.ip), str(no.direito.ip), label="dir")
            desenho_recursivo(no.direito)

    desenho_recursivo(raiz)
    return dot

raiz = None
for ip in [100, 50, 150, 25, 75, 125, 175, 80, 10]:
    raiz = inserir(raiz, ip)

dot = desenhar(raiz)
dot.render('imagens/arvore', view=True)
