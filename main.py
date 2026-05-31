from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import hex_colormap, colormap
from kivy.animation import Animation
from kivy.metrics import sp, dp
from kivy.uix.image import Image
from kivy import platform
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def go_game(self, *args):
        self.manager.current = "game"
        self.manager.transition.direction = "left"

    def go_settings(self, *args):
        self.manager.current = "settings"
        self.manager.transition.direction = "up"

    def exit_app(self, *args):
        app.stop()


class Settings(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_menu(self, *args):
        self.manager.current = "menu"
        self.manager.transition.direction = "down"

class Fish(Image):
    anim_play = False
    interaction_block = True
    COEF_MULT = 1.5
    fish_current = None
    fish_index = 0
    hp_current = None
    angle = NumericProperty(0)

    click_music = SoundLoader.load("assets/audios/bubble01.mp3")
    defeate_music = SoundLoader.load("assets/audios/fish_def.ogg")

    def on_kv_post(self, base_weight):
        self.GAME_SCREEN = self.parent.parent.parent

        return super().on_kv_post(base_widget)

    def new_fish(self, *args):
        self.fish_current = app.LEVELS[app.LEVEL][self.fish_index]
        self.source = app.FISHES[self.finish_current]["source"]
        self.hp_current = app.FISHES[self.fish_current]["hp"]

        self.swim()

    def swim(self):
        self.pos = (self.GAME_SCREEN.x - self.width, self.GAME_SCREEN.height / 2)
        self.opacity = 1
        swim = Animation(x = self.GAME_SCREEN.width / 2 - self,width / 2, duration = 1)
        swim.start(self)
        swim.bind(on_complete=lambda w, a: setattr(self, "interaction_block", False))

        def defeated(self):
            self.interaction_block = True
            anim = Animation(angle = self.angle + 360, d = 1, t="in_cublic")

            old_size = self.size.copy()
            old_pos = self.pos.copy()

            new_size = (self.size[0] * self.COEF_MULT * 3, self.size[1] * self.COEF_MULT * 3)

            new_pos = (self.pos[0] - (new_size[0] - self.size[0]) / 2, self.pos[1] - (new_size[0] - self.size[1]) / 2)

            anim &= Animation(size=(new_size), t="in_out_bounce") + Animation(size=(old_size), duration = 0)
            anim &= Animation(pos=(new_pos), t="in_out_bounce") + Animation(size=(old_pos), duration=0)

            anim &= Animation(opacity = 0)
            anim.start(self)

            self.defeate_music.play()

        def on_touch_down(self, touch):
            if not self.collide_point(*touch.pos) or self.anim_play or self.interaction_block:
                return
            if not self.anim_play and not self.interaction_block:
                self.hp_current -= 1
                self.GAME_SCREEN.score += 1
                self.click_music.play()
                if self.hp_current > 0:
                    old_size = self.size.copy()
                    old_pos = self.pos.copy()
                    new_size = (self.size[0] * self.COEF_MULT, self.size[1] * self.COEF_MULT)
                    new_pos = (self.pos[0] - (new_size[0] - self.size[0]) / 2,self.pos[1] - (new_size[0] - self.size[1]) / 2)
                    zoom_anim = Animation(size=(new_size), duration = 0.05) + Animation(size=(old_size), duration = 0.05)
                    zoom_anim &= Animation(size=(new_pos), duration=0.05) + Animation(size=(old_pos), duration=0.05)

