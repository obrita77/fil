from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, ListProperty
import random

# Dicionário com os filmes por gênero
FILMES_POR_GENERO = {
    'Ação': [
        'Matrix', 'John Wick', 'Mad Max: Estrada da Fúria',
        'Duro de Matar', 'Missão Impossível', 'Gladiador'
    ],
    'Comédia': [
        'Se Beber, Não Case', 'As Branquelas', 'Debi & Loide',
        'Escola de Rock', 'Superbad', 'Apertem os Cintos'
    ],
    'Animação': [
        'Toy Story', 'Procurando Nemo', 'Shrek',
        'Frozen', 'Os Incríveis', 'Divertidamente'
    ]
}

class TelaBoasVindas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Título
        titulo = Label(
            text='Bem-vindo ao Sugestor de Filmes!',
            font_size=24,
            size_hint_y=0.3
        )
        
        # Input para nome
        self.nome_input = TextInput(
            hint_text='Digite seu nome',
            size_hint_y=0.2,
            multiline=False
        )
        
        # Botão continuar
        btn_continuar = Button(
            text='Continuar',
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_continuar.bind(on_press=self.ir_para_sugestao)
        
        layout.add_widget(titulo)
        layout.add_widget(self.nome_input)
        layout.add_widget(btn_continuar)
        
        self.add_widget(layout)
    
    def ir_para_sugestao(self, instance):
        nome = self.nome_input.text.strip()
        if nome:
            # Passa o nome para a próxima tela
            self.manager.get_screen('sugestao').nome_usuario = nome
            self.manager.current = 'sugestao'
        else:
            self.nome_input.hint_text = 'Por favor, digite seu nome!'

class TelaSugestaoFilmes(Screen):
    nome_usuario = StringProperty('')
    filme_sugerido = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Label de boas-vindas
        self.label_boas_vindas = Label(
            font_size=20,
            size_hint_y=0.2
        )
        
        # Spinner para seleção de gênero
        self.spinner_genero = Spinner(
            text='Selecione um gênero',
            values=['Ação', 'Comédia', 'Animação'],
            size_hint_y=0.2
        )
        
        # Botão sugerir filme
        btn_sugerir = Button(
            text='Sugerir Filme',
            size_hint_y=0.2,
            background_color=(0.8, 0.2, 0.6, 1)
        )
        btn_sugerir.bind(on_press=self.sugerir_filme)
        
        # Label para mostrar o filme sugerido
        self.label_filme = Label(
            text='',
            font_size=18,
            size_hint_y=0.3,
            color=(0, 0.5, 0, 1)
        )
        
        # Botão voltar
        btn_voltar = Button(
            text='Voltar',
            size_hint_y=0.2,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        
        layout.add_widget(self.label_boas_vindas)
        layout.add_widget(self.spinner_genero)
        layout.add_widget(btn_sugerir)
        layout.add_widget(self.label_filme)
        layout.add_widget(btn_voltar)
        
        self.add_widget(layout)
    
    def on_nome_usuario(self, instance, value):
        self.label_boas_vindas.text = f'Olá, {value}! Escolha um gênero:'
    
    def sugerir_filme(self, instance):
        genero = self.spinner_genero.text
        if genero in FILMES_POR_GENERO:
            filme = random.choice(FILMES_POR_GENERO[genero])
            self.filme_sugerido = f'🎬 Sugestão: {filme}'
            self.label_filme.text = self.filme_sugerido
        else:
            self.label_filme.text = 'Por favor, selecione um gênero válido!'
    
    def voltar(self, instance):
        self.manager.current = 'boas_vindas'
        self.label_filme.text = ''
        self.spinner_genero.text = 'Selecione um gênero'

class GerenciadorTelas(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Adiciona as telas
        self.add_widget(TelaBoasVindas(name='boas_vindas'))
        self.add_widget(TelaSugestaoFilmes(name='sugestao'))

class SugestorFilmesApp(App):
    def build(self):
        self.title = 'Sugestor de Filmes'
        return GerenciadorTelas()

if __name__ == '__main__':
    SugestorFilmesApp().run()