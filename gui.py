import pygame as pg

pg.init()


class InputBox:
    def __init__(self, x, y, w, h, func, text='', color_inactive=pg.Color(1, 161, 255), color_active=pg.Color(0, 99, 151), text_color=pg.Color(255, 255, 255), font=pg.font.Font(None, 32)):
        self.rect = pg.Rect(x, y, w, h)
        self.w = w
        self.func = func

        self.color_inactive = color_inactive
        self.color_active = color_active
        self.text_color = text_color
        self.font = font

        self.color = color_inactive
        self.text = text
        self.txt_surface = font.render(text, True, text_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.func(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.text_color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, x, y, w, h, radius, func, text, button_color=pg.Color(1, 161, 255), click_color=pg.Color(0, 99, 151), text_color=pg.Color(255, 255, 255), text_font=pg.font.Font(None, 32)):
        self.rect = pg.Rect(x, y, w, h)
        self.radius = radius
        self.func = func

        self.color = button_color

        self.text = text
        self.text_font = text_font
        self.text_color = text_color
        self.text_surface = text_font.render(text, True, text_color)
        self.button_color = button_color
        self.click_color = click_color

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.color = self.click_color
                self.func()
        else:
            self.color = self.button_color

    def update(self):
        pass

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, border_radius=self.radius)
        # Blit the text.
        screen.blit(self.text_surface, (self.rect.centerx - (self.text_surface.get_width()/2), self.rect.centery - (self.text_surface.get_height()/2)))


class SlideBar:
    def __init__(self, x, y, l, func, slide_color=pg.Color(1, 161, 255), line_color=pg.Color(29, 27, 30)):
        self.slide = pg.Rect(x-7, y-10, 15, 30)
        self.line = pg.Rect(x, y, l, 10)
        self.func = func

        self.slide_color = slide_color
        self.line_color = line_color

        self.delta = 1 / l
        self.val = 0
        self.is_active = False

    def handle_event(self, event):
        buttons = pg.mouse.get_pressed()
        if buttons[0]:
            if self.slide.collidepoint(event.pos):
                self.is_active = True
            
            if self.is_active:
                self.slide.x = min(max(pg.mouse.get_pos()[0], self.line.x), self.line.x + self.line.width) - (self.slide.width / 2)
                self.val = (self.delta * (self.slide.centerx - self.line.x))
                
                self.func(self.val)
        else:
            self.is_active = False


    def update(self):
        pass

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.line_color, self.line, border_radius=5)
        pg.draw.rect(screen, self.slide_color, self.slide, border_radius=20)
