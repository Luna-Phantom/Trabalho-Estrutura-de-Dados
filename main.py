import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
import random
import time

class Comp:
    def __init__(self, ip):
        self.ip = ip
        self.inf = False
        self.enc = False
        self.esq = None
        self.dir = None

def check_ip(ip):
    partes = ip.split('.')
    if len(partes) != 4:
        return False
    for p in partes:
        if not p.isdigit() or int(p) < 0 or int(p) > 255:
            return False
    return True

def add_filhos(r, ip):
    partes = ip.split('.')
    base = int(partes[-1])
    pref = '.'.join(partes[:-1])
    
    f1 = []
    for i in [-10, 10]:
        novo_ip = f"{pref}.{base + i}"
        if check_ip(novo_ip):
            f1.append(novo_ip)
    
    f2 = []
    for ip in f1:
        sub_base = int(ip.split('.')[-1])
        for i in [-5, 5]:
            novo_ip = f"{pref}.{sub_base + i}"
            if check_ip(novo_ip):
                f2.append(novo_ip)
    
    for ip in f1 + f2:
        r = add(r, ip)
    return r

def add(r, ip):
    if r is None:
        return Comp(ip)
    if ip < r.ip:
        r.esq = add(r.esq, ip)
    else:
        r.dir = add(r.dir, ip)
    return r

def virus(r, ip, prob, c, app):
    if r is None:
        return
    if r.ip == ip:
        r.inf = True
        app.draw()
        c.update()
        time.sleep(0.5)
        if r.esq and random.random() < prob:
            r.esq.inf = True
            app.draw()
            c.update()
            time.sleep(0.5)
        if r.dir and random.random() < prob:
            r.dir.inf = True
            app.draw()
            c.update()
            time.sleep(0.5)
    elif ip < r.ip:
        virus(r.esq, ip, prob, c, app)
    else:
        virus(r.dir, ip, prob, c, app)

def encap(r, c, app):
    if r is None:
        return
    if r.inf:
        r.enc = True
        app.draw()
        c.update()
        time.sleep(0.5)
        if r.esq:
            r.esq.enc = True
            app.draw()
            c.update()
            time.sleep(0.5)
        if r.dir:
            r.dir.enc = True
            app.draw()
            c.update()
            time.sleep(0.5)
    else:
        encap(r.esq, c, app)
        encap(r.dir, c, app)

def get_dados(r):
    d = []
    def perc(no):
        if no is None:
            return
        estado = "INFECTADO" if no.inf else "SAUDÁVEL"
        if no.enc:
            estado += " + ENCAPSULADO"
        d.append((no.ip, estado))
        perc(no.esq)
        perc(no.dir)
    perc(r)
    return d

def relatorio(r):
    d = get_dados(r)
    if not d:
        return "Nada na rede."
    return "\n".join(f"IP {ip}: {estado}" for ip, estado in d)

def save_csv(r):
    d = get_dados(r)
    if not d:
        return
    with open('relatorio.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(["IP", "Estado", "Encapsulado"])
        for ip, estado in d:
            enc = "SIM" if "ENCAPSULADO" in estado else "NÃO"
            est = "INFECTADO" if "INFECTADO" in estado else "SAUDÁVEL"
            w.writerow([ip, est, enc])

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Rede")
        self.r = None
        self.c = tk.Canvas(root, width=800, height=500, bg='white')
        self.c.pack()
        tk.Button(root, text="Add IP", command=self.add_ip).pack()
        tk.Button(root, text="Infectar", command=self.inf_ip).pack()
        tk.Button(root, text="Relatorio", command=self.show_rel).pack()
        tk.Button(root, text="CSV", command=self.save_csv).pack()
        tk.Button(root, text="Sair", command=root.quit).pack()

    def draw_no(self, no, x, y, dx, n, c):
        if no is None:
            return
        if no.enc:
            cor = "red"
        elif no.inf:
            cor = "green"
        else:
            cor = "orange"
        c.create_oval(x-30, y-30, x+30, y+30, fill=cor)
        estado = "INFECTADO" if no.inf else "SAUDÁVEL"
        if no.enc:
            estado += "\nENCAPSULADO"
        c.create_text(x, y, text=f"{no.ip}\n{estado}")
        if no.esq:
            c.create_line(x, y+30, x-dx, y+100-30)
            self.draw_no(no.esq, x-dx, y+100, dx/2, n+1, c)
        if no.dir:
            c.create_line(x, y+30, x+dx, y+100-30)
            self.draw_no(no.dir, x+dx, y+100, dx/2, n+1, c)

    def draw(self):
        self.c.delete("all")
        if self.r:
            self.draw_no(self.r, 400, 50, 200, 1, self.c)

    def add_ip(self):
        ip = simpledialog.askstring("IP", "Digite o IP:")
        if check_ip(ip):
            if self.r is None:
                self.r = add(self.r, ip)
                self.r = add_filhos(self.r, ip)
                messagebox.showinfo("Ok", "IP e filhos adicionados.")
            else:
                self.r = add(self.r, ip)
                messagebox.showinfo("Ok", "IP adicionado.")
            self.draw()
        else:
            messagebox.showerror("Erro", "IP errado.")

    def inf_ip(self):
        ip = simpledialog.askstring("Infectar", "Digite o IP:")
        if check_ip(ip):
            virus(self.r, ip, 0.5, self.c, self)
            encap(self.r, self.c, self)
            messagebox.showinfo("Ok", "Vírus espalhado e encapsulado.")
        else:
            messagebox.showerror("Erro", "IP errado.")

    def show_rel(self):
        if self.r is None:
            messagebox.showinfo("Relatório", "Nada na rede.")
            return
        texto = relatorio(self.r)
        win = tk.Toplevel(self.root)
        win.title("Relatório")
        txt = tk.Text(win, width=50, height=20)
        txt.pack()
        txt.insert(tk.END, texto)
        txt.config(state='disabled')

    def save_csv(self):
        if self.r is None:
            messagebox.showinfo("Aviso", "Nada na rede.")
            return
        save_csv(self.r)
        messagebox.showinfo("Ok", "CSV salvo.")

root = tk.Tk()
root.geometry("800x600")
app = App (root)
root.mainloop()