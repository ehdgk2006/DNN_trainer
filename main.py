import pygame as pg

import sys
import matplotlib
from pygame.locals import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import threading

from gui import InputBox, Button, SlideBar
from physics_model import PhysicsModel


X = []
Y = []
X_TEST = []
Y_TEST = []
MODEL_SIZE = 1
MODEL_DEPTH = 1
MODEL_LEARNING_RATE = 10**-5
MODEL_EPOCHS = 1

MODEL = PhysicsModel(MODEL_SIZE, MODEL_DEPTH, MODEL_LEARNING_RATE, MODEL_EPOCHS)
TRAINER = threading.Thread(target = MODEL.train, args=(X, Y))


def input_data(text: str):
    global MODEL

    if not MODEL.is_training:
        try:
            tmp = text.replace(' ', '')
            tmp = text.split(',')
            X.append(float(tmp[0]))
            Y.append(float(tmp[1]))
        except:
            if len(X) > len(Y):
                X.pop()
            elif len(X) < len(Y):
                Y.pop()


def remove_data():
    global MODEL

    if not MODEL.is_training and len(X) != 0 and len(Y) != 0:
        X.pop()
        Y.pop()


def set_model_size(val: float):
    global MODEL_SIZE, MODEL

    if not MODEL.is_training:
        MODEL_SIZE = int(val*100)+1


def set_model_depth(val: float):
    global MODEL_DEPTH, MODEL

    if not MODEL.is_training:
        MODEL_DEPTH = int(val*10)+1


def set_model_learning_rate(val: float):
    global MODEL_LEARNING_RATE, MODEL
    
    if not MODEL.is_training:
        MODEL_LEARNING_RATE = 10**((val*5) - 5)


def set_model_epochs(val: float):
    global MODEL_EPOCHS, MODEL
    
    if not MODEL.is_training:
        MODEL_EPOCHS = int(val*4999)+1


def train_model():
    global MODEL_SIZE, MODEL_DEPTH, MODEL_LEARNING_RATE, MODEL_EPOCHS, MODEL, TRAINER
    
    if not MODEL.is_training:
        MODEL = PhysicsModel(MODEL_SIZE, MODEL_DEPTH, MODEL_LEARNING_RATE, MODEL_EPOCHS)
        
        TRAINER = threading.Thread(target = MODEL.train, args=(X, Y))
        TRAINER.start()


def main():
    global MODEL, X, Y, X_TEST, Y_TEST

    BACKGROUND_COLOR = (54, 52, 55)
    
    screen = pg.display.set_mode((1280, 600))
    clock = pg.time.Clock()

    title_font = pg.font.Font(None, 32)
    val_font = pg.font.Font(None, 16)

    input_data_box = InputBox(170, 45, 250, 32, input_data)
    del_data_button = Button(340, 100, 75, 30, 10, remove_data, 'Del')

    model_size_slide = SlideBar(350, 250, 200, set_model_size)
    model_depth_slide = SlideBar(350, 320, 200, set_model_depth)
    model_learning_rate_slide = SlideBar(350, 390, 200, set_model_learning_rate)
    model_epochs_slide = SlideBar(350, 460, 200, set_model_epochs)

    train_button = Button(450, 520, 100, 30, 10, train_model, 'Train')

    figure, axis = plt.subplots()
    axis.plot(X, Y, 'ro', X_TEST, Y_TEST, 'b-')
    plot_canvas = FigureCanvas(figure)  # Create a canvas to render the Matplotlib plot 

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            
            if not MODEL.is_training:
                input_data_box.handle_event(event)
                del_data_button.handle_event(event)
                model_size_slide.handle_event(event)
                model_depth_slide.handle_event(event)
                model_learning_rate_slide.handle_event(event)
                model_epochs_slide.handle_event(event)
                train_button.handle_event(event)

        input_data_box.update()
        del_data_button.update()
        model_size_slide.update()
        model_depth_slide.update()
        model_learning_rate_slide.update()
        model_epochs_slide.update()
        train_button.update()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_font.render("Add Data: ", True, pg.Color(255, 255, 255)), (50, 50))
        screen.blit(title_font.render("Model Size: ", True, pg.Color(255, 255, 255)), (50, 240))
        screen.blit(val_font.render(f"{MODEL_SIZE}", True, pg.Color(100, 100, 100)), (500, 270))
        screen.blit(title_font.render("Model Depth: ", True, pg.Color(255, 255, 255)), (50, 310))
        screen.blit(val_font.render(f"{MODEL_DEPTH}", True, pg.Color(100, 100, 100)), (500, 340))
        screen.blit(title_font.render("Model Learning Rate: ", True, pg.Color(255, 255, 255)), (50, 380))
        screen.blit(val_font.render(f"{MODEL_LEARNING_RATE:.5f}", True, pg.Color(100, 100, 100)), (500, 410))
        screen.blit(title_font.render("Model Epochs: ", True, pg.Color(255, 255, 255)), (50, 450))
        screen.blit(val_font.render(f"{MODEL_EPOCHS}", True, pg.Color(100, 100, 100)), (500, 480))

        input_data_box.draw(screen)
        del_data_button.draw(screen)
        model_size_slide.draw(screen)
        model_depth_slide.draw(screen)
        model_learning_rate_slide.draw(screen)
        model_epochs_slide.draw(screen)
        train_button.draw(screen)

        if MODEL.is_training:
            X_TEST, Y_TEST = MODEL.graph(X)

        figure, axis = plt.subplots()
        axis.plot(X, Y, 'ro', X_TEST, Y_TEST, 'b-')
        plot_canvas = FigureCanvas(figure)  # Create a canvas to render the Matplotlib plot 

        # Draw the Matplotlib plot onto the Pygame screen
        plot_canvas.draw()  # Update the Matplotlib plot if needed
        renderer = plot_canvas.get_renderer()  
        matplotlib_plot_rgba_image_data = renderer.tostring_rgb()  # Get raw image data of the plot
        plot_canvas_width, plot_canvas_height = plot_canvas.get_width_height() 

        # Convert the Matplotlib image data into a Pygame surface
        plot_surface = pg.image.fromstring(matplotlib_plot_rgba_image_data, 
                                            (plot_canvas_width, plot_canvas_height), 
                                            "RGB")

        # Display the plot on the Pygame screen
        screen.blit(plot_surface, (620, 50))

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()