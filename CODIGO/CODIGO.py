from flet import *
import sqlite3

conexao = sqlite3.connect("dados.db", check_same_thread=False)
cursor = conexao.cursor()

cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)
    '''
)

class App(UserControl):
    def __init__(self):
        super().__init__()

        self.todos_dados = Column(auto_scroll=True)
        self.adicionar_dados = TextField(label="NOME DO DADO")
        self.editar_dado = TextField(label="EDITAR")
    
    def deletar(self, x, y):
        cursor.execute("DELETE FROM clientes WHERE id = ?", [x])
        y.open = False

        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def atualizar(self, x, y, z):
        cursor.execute("UPDATE clientes SET nome = ? WHERE id = ?", (y, x))
        conexao.commit()

        z.open = False

        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def abrir_acoes(self, e):
        id_user = e.control.subtitle.value
        self.editar_dado.value = e.control.title.value
        self.update()

        alerta_dialogo = AlertDialog(
            title=Text(f"Editar ID{id_user}"),
            content=self.editar_dado,

            actions=[
                ElevatedButton(
                    'APAGAR',
                    color='white', bgcolor='red',
                    on_click= lambda e:self.deletar(id_user, alerta_dialogo)
                ),
                ElevatedButton(
                    'ATUALIZAR',
                    on_click= lambda e:self.atualizar(id_user, self.editar_dado.value, alerta_dialogo)
                )
            ],
            actions_alignment='spaceBetween'
        )  

        self.page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        self.page.update()
        
    def renderizar_todos(self):
        cursor.execute("SELECT * FROM clientes")
        conexao.commit()

        meus_dados = cursor.fetchall()

        for dado in meus_dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_acoes
                )
            )
        self.update()

    def ciclo(self):
        self.renderizar_todos()
        
    def adicionar_novo_dado(self, e):
        cursor.execute("INSERT INTO clientes (nome) VALUES (?)", [self.adicionar_dados.value])
        conexao.commit()

        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    def build(self):
        return Column([
            Text("CRUD COM SQLITE", size=20, weight='bold'),
            self.adicionar_dados,
            ElevatedButton(
                'ADICIONAR',
                on_click=self.adicionar_novo_dado,
            ),
            self.todos_dados,
        ])

def main(page:Page):
    page.update()
    minha_aplicacao = App()

    page.add(
        minha_aplicacao,
    )

app(target=main)