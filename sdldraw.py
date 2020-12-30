import sdl2.ext
import sdl2


class WireDrawer:
    def __init__(self, background=sdl2.ext.Color(127, 127, 127), name="test"):
        self.current = 0, 0
        sdl2.ext.init()
        bound = sdl2.SDL_Rect()
        sdl2.SDL_GetDisplayBounds(0, bound)
        self.shape = bound.w, bound.h
        window = sdl2.ext.Window(name, self.shape, flags=sdl2.SDL_WINDOW_FULLSCREEN)
        window.show()
        self.renderer = sdl2.ext.Renderer(window)
        self.renderer.fill((0, 0, *self.shape), background)

    def move(self, x, y=None):
        if y is None:
            x, y = x
        self.current = int(x), int(y)

    def draw(self, x, y=None, color=sdl2.ext.Color(255, 255, 255)):
        if y is None:
            x, y = x
        self.renderer.draw_line((*self.current, int(x), int(y)), color)
        self.move(x, y)

    def done(self):
        self.renderer.present()
        while True:
            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_QUIT:
                    return
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        return


