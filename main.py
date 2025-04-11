from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from screens.login import LoginScreen
from screens.cadastro import CadastroScreen
from screens.home import HomeScreen
from screens.verificacao import VerificacaoScreen

"""
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self.add_widget(
            MDLabel(
                text="Bem-vindo ao PoupaLar!",
                halign="center",
                font_style="H5"
            )
        )
"""
class PoupaLarApp(MDApp):
    def build(self):
        self.title = "PoupaLar"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(CadastroScreen())
        sm.add_widget(VerificacaoScreen(name="verificacao"))
        sm.add_widget(HomeScreen())
        return sm


if __name__ == "__main__":
    PoupaLarApp().run()