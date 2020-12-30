from math import pi, cos, sin


import sdl2.ext
import sdl2.sdlttf
import sdl2


class Point:
    def __init__(self, x, y=None):
        if y is None:
            x, y = x
        self.x = x
        self.y = y

    def __getitem__(self, item):
        return self.y if item else self.x

    def __setitem__(self, key, value):
        if key:
            self.y = value
        else:
            self.x = value

    def __iter__(self):
        for c in (self.x, self.y):
            yield c

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + Point(-other.x, -other.y)

    def __mul__(self, constant):
        return Point(self.x * constant, self.y * constant)

    def __truediv__(self, constant):
        return Point(self.x / constant, self.y / constant)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __len__(self):
        return 2

    def rotate(self, angle, x=(0, 0), y=None):
        if y is None:
            x, y = x
        return Point(x + (self.x - x) * cos(angle) - (self.y - y) * sin(angle),
                     y + (self.x - x) * sin(angle) + (self.y - y) * cos(angle))

    def round(self, n=None):
        return Point(int(self.x), int(self.y))

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Edge:
    def __init__(self, p1, p2):
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2
        self.p1, self.p2 = p1, p2

    def det(self):
        return self.x1 * self.y2 - self.x2 * self.y1

    def intersect(self, other):
        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
        return ccw(self.p1,other.p1, other.p2) != ccw(self.p2,other.p1,other.p2) and ccw(self.p1,self.p2,other.p1) != ccw(self.p1,self.p2,other.p2)

    def intersection(self, other):
        d = (other.y2 - other.y1) * (self.x2 - self.x1) - (other.x2 - other.x1) * (self.y2 - self.y1)
        if not d:
            return
        uA = ((other.x2 - other.x1) * (self.y1 - other.y1) - (other.y2 - other.y1) * (self.x1 - other.x1)) / d
        uB = ((self.x2 - self.x1) * (self.y1 - other.y1) - (self.y2 - self.y1) * (self.x1 - other.x1)) / d
        if not (0 <= uA <= 1 and 0 <= uB <= 1):
            return

        return Point(self.x1 + uA * (self.x2 - self.x1), self.y1 + uA * (self.y2 - self.y1))

    def __repr__(self):
        return "{}<>{}".format(self.p1, self.p2)


class Shape:
    def __init__(self, shape):
        self.shape = shape

    def draw(self, drawerer, color=sdl2.ext.Color(255, 255, 255)):
        drawerer.move(self.shape[0][0])
        for p, doDraw in self.shape[1:]:
            if doDraw:
                drawerer.draw(p, color=color)
            else:
                drawerer.move(p)

    def move(self, x, y=None):
        if y is None:
            x, y = x
        point = Point(x, y)
        return Shape([(p + point, do) for p, do in self.shape])

    def rotate(self, angle, x=(0, 0), y=None):
        return Shape([(p.rotate(angle, x, y), do) for p, do in self.shape])

    def __mul__(self, const):
        return Shape([(p * const, do) for p, do in self.shape])

    def center(self):
        return sum((p for p, do in self.shape if do), Point(0, 0)) / len([p for p, do in self.shape if do])

    def edges(self):
        edges = []
        prev = self.shape[0][0]
        for p, do in self.shape[1:]:
            if do:
                edges.append(Edge(p, prev))
            prev = p

        return edges

    def intersect(self, other):
        for edge1 in self.edges():
            for edge2 in other.edges():
                inter = edge1.intersection(edge2)
                if inter:
                    return inter

    def edge_intersect(self, edge):
        for edge1 in self.edges():
            inter = edge1.intersection(edge)
            if inter:
                return inter

    # by conv edge.p1 is start
    def ray_intersect(self, edge):
        inter = edge.p2
        for edge2 in self.edges():
            inter_iter = edge.intersection(edge2)
            if inter_iter and edge.p1.dist(inter_iter) < edge.p1.dist(inter):
                inter = inter_iter
        return inter


projectile = Shape([
    (Point(0, 0), True),
    (Point(3, 0), True),
    (Point(3, 3), True),
    (Point(0, 3), True),
    (Point(0, 0), True),
])


class WireEngine:
    def __init__(self, background=sdl2.ext.Color(127, 127, 127), name="test", items=None):
        self.current = 0, 0
        self.pos = Point(1000, 100)
        self.back = background
        self.angle = 0
        self.items = items
        sdl2.ext.init()
        bound = sdl2.SDL_Rect()
        sdl2.SDL_GetDisplayBounds(0, bound)
        self.shape = bound.w, bound.h
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 0)
        window = sdl2.ext.Window(name, self.shape, flags=sdl2.SDL_WINDOW_FULLSCREEN)
        window.show()
        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")

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

    def inside(self, x, y=None):
        if y is None:
            x, y = x
        return 0 <= x <= self.shape[0] and 0 <= y <= self.shape[1]

    def start(self):
        dangle = 0
        dp = Point(0, 0)
        do_shoot = False
        do_laser = False
        projectiles = []
        intersections = []
        shoot_wait = 0

        ratio = 0
        coef = 3

        font = sdl2.ext.FontManager(font_path="D:\home\python_workshop\minecraft.ttf", size=46)
        factory = sdl2.ext.SpriteFactory(renderer=self.renderer)

        while True:
            frame_start = sdl2.SDL_GetTicks()

            self.renderer.present()
            self.renderer.clear()
            self.renderer.fill((0, 0, *self.shape), self.back)

            self.angle += dangle * ratio
            prev = self.pos
            self.pos += dp.rotate(self.angle) * ratio
            jump = Edge(self.pos, prev)

            cur = self.items[0].rotate(self.angle).move(self.pos)

            for i in self.items[1:]:
                inter = i.intersect(cur)
                if not inter:
                    inter = i.edge_intersect(jump)
                if inter:
                    intersections.append((100, inter.round()))
                    self.angle -= dangle * ratio
                    dangle = 0
                    self.pos -= dp.rotate(self.angle) * ratio
                    dp = Point(0, 0)

            cur.draw(self)

            if do_shoot and shoot_wait > 3:
                shoot_wait = 0
                projectiles.append((Point(0, 2).rotate(self.angle), projectile.rotate(self.angle).move(self.pos + Point(-1.5, 22).rotate(self.angle))))
            else:
                shoot_wait += ratio

            for item in self.items[1:]:
                item.draw(self)

            new_p = []
            for vec, p in projectiles:
                prev = p.center()
                p = p.move(vec * ratio)
                jump = Edge(p.center(), prev)
                if self.inside(p.center()):
                    intersected = False
                    for i in self.items[1:]:
                        inter = i.intersect(p)
                        if inter is None:
                            inter = i.edge_intersect(jump)
                        if inter is not None:
                            intersections.append((100, inter))
                            intersected = True
                    if not intersected:
                        new_p.append((vec, p))
            projectiles = new_p
            for _, p in projectiles:
                p.draw(self)

            if do_laser:
                ray = Edge(self.pos, self.pos + Point(0, 10000).rotate(self.angle))
                inter = Point(0, 10000).rotate(self.angle)
                for i in self.items[1:]:
                    iter_inter = i.ray_intersect(ray)
                    if iter_inter and self.pos.dist(iter_inter) < self.pos.dist(inter):
                        inter = iter_inter
                self.renderer.draw_line([*((self.pos + Point(0, 25).rotate(self.angle)).round()), *inter.round()], color=sdl2.ext.Color(255, 0, 0))

            new_inter = []
            for wait, point in intersections:
                if wait != 0:
                    projectile.move(point - projectile.center()).draw(self, sdl2.ext.Color(255, 0, 0))
                    new_inter.append((wait - 1, point))
            intersections = new_inter

            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_QUIT:
                    return
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        return
                    if event.key.keysym.sym == sdl2.SDLK_w:
                        dp = Point(0, 1)
                    if event.key.keysym.sym == sdl2.SDLK_s:
                        dp = Point(0, -1)
                    if event.key.keysym.sym == sdl2.SDLK_d:
                        dangle = 0.01
                    if event.key.keysym.sym == sdl2.SDLK_a:
                        dangle = -0.01
                    if event.key.keysym.sym == sdl2.SDLK_SPACE:
                        do_shoot = True
                    if event.key.keysym.sym == sdl2.SDLK_LCTRL:
                        do_laser = True
                    if event.key.keysym.sym == sdl2.SDLK_EQUALS:
                        coef += 0.1
                    if event.key.keysym.sym == sdl2.SDLK_MINUS:
                        coef -= 0.1
                    if event.key.keysym.sym == sdl2.SDLK_0:
                        coef = 3

                if event.type == sdl2.SDL_KEYUP:
                    if event.key.keysym.sym == sdl2.SDLK_w or event.key.keysym.sym == sdl2.SDLK_s:
                        dp = Point(0, 0)
                    if event.key.keysym.sym == sdl2.SDLK_d or event.key.keysym.sym == sdl2.SDLK_a:
                        dangle = 0
                    if event.key.keysym.sym == sdl2.SDLK_SPACE:
                        do_shoot = False
                    if event.key.keysym.sym == sdl2.SDLK_LCTRL:
                        do_laser = False
            delta = sdl2.SDL_GetTicks() - frame_start
            if coef <= 0:
                coef = 0.1

            ratio = delta / coef

            if delta == 0:
                delta = 1

            text = factory.from_text("{:03d} particles, {:.1f} coef, {:03d} fps".format(len(projectiles) + len(intersections), coef, int(1000.0 / delta)), fontmanager=font)
            self.renderer.copy(text, dstrect= (0,0,text.size[0],text.size[1]))


#   2\---------/3
#     \       /
#      \     /
#       \   /
#        \ /
#         V
#         1,4

arrow = Shape([
    (Point(0, 25), True),
    (Point(-9, 0), True),
    (Point(9, 0), True),
    (Point(0, 25), True),
])

box = Shape([
    (Point(0, 0), True),
    (Point(100, 0), True),
    (Point(100, 100), True),
    (Point(0, 100), True),
    (Point(0, 0), True),
]).move(300, 300)

big_box = Shape([
    (Point(10, 10), True),
    (Point(1900, 10), True),
    (Point(1900, 1000), True),
    (Point(10, 1000), True),
    (Point(10, 10), True),
])


# drawer = WireDrawer()
#
# center = drawer.shape[0] // 2, drawer.shape[1] // 2
# drawer.move(center)
# drawer.draw(center)
#
# arrow = arrow.move(Point(center) + Point(300, 0)) * 1.1 # Start position
#
# amount = 40
#
# for _ in range(amount):
#     arrow.draw(drawer)
#     arrow = arrow.rotate(2 * pi / amount, center)
#
# drawer.done()

drawer = WireEngine(items=[arrow, box, box.move(1000, 300), big_box])
drawer.start()
