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
    return dot
