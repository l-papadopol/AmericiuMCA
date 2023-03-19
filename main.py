#####################################################################
# Copyright(c) 2023, All rights reserved.
# Author:   Papadopol Lucian Ioan l.papadopol@campus.uniurb.it
# Date:     17.01.2023
# Version:  v1.0
# Function: Reading NIM Data from shared memory and use it
#####################################################################

# Load libraries
import pygame
import numpy as np
import time
from pygame.locals import *
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.ticker as ticker

# Load EPICS CA Tools
from epics import caget, caput, cainfo
from epics import PV

# Load configuration file (configuration.py)
import configuration as config

# Load global variables
from globals import *


# Initialize EPICS CA channel access
def init_ca():
    global spectra_array
    global m_process_var
    spectra_array = np.ndarray(config.SPECTRA_SIZE, dtype=np.uint32, order='C')
    spectra_array.fill(0)
    # Create the Process Variable Object
    m_process_var = PV(config.PV_NAMES[m_adc])
    # Printout the information about the Process Variable
    cainfo(config.PV_NAMES[m_adc])
    time.sleep(2)


# Get data from EPICS CA and map over
def get_data():
    global m_process_var, spectra_array
    if config.INTERFACE == '556AIM':
        # Access the Process Variable
        samples = m_process_var.get(as_numpy=True)
        n = 0
        input_divisor = int(config.PV_LENGTH[m_adc] / config.NUM_OF_CHANNELS)
        for i in range(0, config.PV_LENGTH[m_adc], input_divisor):
            max = 0
            for j in range(0, input_divisor, 1):
                if max < samples[i + j]:
                    max = samples[i + j]

            spectra_array[n] = max  # Copy samples into spectra array
            n = n + 1


# Textual keywords handling
def commands():
    global input_string
    global acq_status
    global start
    global e_time
    global e_time_old
    global calib_x, calib_y
    global spectra_array

    if input_string == "resume":
        caput(config.PV_NAMES[m_adc]+"Start", 1)
        input_string = "OK!"
        acq_status = True
        start = timer()
        e_time_old = e_time
    if input_string == "start":
        caput(config.PV_NAMES[m_adc]+"EraseStart", 1)
        input_string = "OK!"
        acq_status = True
        time.sleep(1)
        start = timer()
        e_time_old = 0
    if input_string == "stop":
        caput(config.PV_NAMES[m_adc]+"Stop", 1)
        input_string = "OK!"
        acq_status = False
    if input_string == "plt":
        if calib_x[0] != 0 or calib_x[1] != 0 or calib_x[2] != 0: 
            polyfit(calib_x, calib_y)
            input_string = "OK!"
        else:
            input_string = "Provide three calibration points first!"
    if input_string == "plot":
        if calib_x[0] != 0 or calib_x[1] != 0 or calib_x[2] != 0: 
            cali_plt(spectra_array, calib_x, calib_y)
            input_string = "OK!"
        else:
            input_string = "Provide three calibration points first!"
			
			
# Polynomial fitting
def polyfit(calib_x, calib_y):
    # Fit the data to a polynomial of degree 2
    coefficients = np.polyfit(calib_x, calib_y, 2)
    polynomial = np.poly1d(coefficients)
    # Plot the original data and the polynomial fit
    plt.plot(calib_x, calib_y, 'o', label='Original data')
    plt.plot(calib_x, polynomial(calib_x), 'r', label='Fitted curve')
    plt.title(coefficients)
    plt.grid(linestyle='--', color='gray')
    plt.xlabel('Channel number')
    plt.ylabel('Energy "keV"')
    plt.legend()
    plt.show()

# Plot with calibration
def cali_plt(spectra_array, calib_x, calib_y):
    # Fit the data to a polynomial of degree 2
    coefficients = np.polyfit(calib_x, calib_y, 2)
    polynomial = np.poly1d(coefficients)
    #create an empty array
    indices_array = np.zeros(1024)
    #calibration indices loop
    for i in range(1024):
        indices_array[i] = int(polynomial(i))
    plot_xy(indices_array, spectra_array)
    
def plot_xy(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y, color='black', linewidth=1)
   
    # Set the major grid interval to 100 and the minor grid interval to 10
    major_interval = 100
    minor_interval = 25
    ax.xaxis.set_major_locator(ticker.MultipleLocator(major_interval))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(minor_interval))
    ax.grid(True, which='both', linestyle='--', color='grey', alpha=0.5, linewidth=0.5)
    ax.set_xlabel('Energy keV')
    ax.set_ylabel('Lin - Pulses')
    ax.set_title('Calibrated spectra')

    # Add button to switch between linear and logarithmic scale
    def toggle_scale(label):
        if ax.get_yscale() == 'linear':
            ax.set_yscale('log')
            ax.set_ylabel('Log - Pulses')
            ax.callbacks.connect('ylim_changed', update_label)
            button.label.set_text('Log->Lin')
        else:
            ax.set_yscale('linear')
            ax.set_ylabel('Lin - Pulses')
            ax.callbacks.disconnect(update_label)
            button.label.set_text('Lin->Log')
        fig.canvas.draw()

    # Function to update y-axis label when changing to logarithmic scale
    def update_label(ax):
        ax.set_ylabel('Log - Pulses')

    # Add button widget
    axbutton = plt.axes([0.8, 0.9, 0.1, 0.05])
    button = plt.Button(axbutton, 'Lin->Log')
    button.on_clicked(toggle_scale)
    # Maximize plot window
    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.showMaximized()
    plt.show()

# FWHM calculator
def fwhm(ch_l, ch_r):
    global spectra_array
    pk_area = 0
    if ch_l > ch_r:
        a = ch_l
        b = ch_r
        ch_l = b
        ch_r = a
    baseline = (spectra_array[ch_l] + spectra_array[ch_r]) / 2
    iterations = ch_r - ch_l
    for ctrLoop in range(iterations):
        pk_area = (pk_area + spectra_array[ctrLoop + ch_l]) - baseline

    ch_pk_value = (spectra_array[ch_l:ch_r].max()) - baseline
    centroid = (spectra_array[ch_l:ch_r].argmax()) + ch_l
    FWHM = (0.939 * pk_area / ch_pk_value)
    FWHM_percentual = FWHM / centroid * 100
    return pk_area, FWHM, FWHM_percentual, centroid



# Main loop
def main():
    running = True
    cursor = 0
    marker_l_value = 0
    marker_r_value = 0
    marker_l = False
    marker_r = False
    global input_string
    global acq_status
    pk_area = 0
    FWHM = 0
    FWHM_percentual = 0
    centroid = 0
    global e_time
    global e_time_old
    calib_a = 0
    calib_b = 0
    calib_c = 0
    global calib_x, calib_y

    pygame.init()
    pygame.display.set_caption("AmericiuMCA")
    pygame_icon = pygame.image.load('multimedia/rsuit.ico')
    pygame.display.set_icon(pygame_icon)
    # Set up the drawing window
    screen = pygame.display.set_mode([1322, 640])
    font = pygame.font.Font('multimedia/Consolas.ttf', 16)

    if config.INTERFACE == '556AIM':
        init_ca()

    # Run until the user asks to quit
    while running:
        commands()
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.unicode.isalpha() or event.unicode.isdigit():
                    input_string += event.unicode
                elif event.key == K_BACKSPACE:
                    input_string = input_string[:-1]
                elif event.key == K_RETURN:
                    input_string = ""
                elif event.key == K_LEFT:
                    if cursor > 9:
                        cursor = cursor - 10
                elif event.key == K_RIGHT:
                    if cursor < 1014:
                        cursor = cursor + 10
                elif event.key == pygame.K_a:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        calib_a = cursor
                elif event.key == pygame.K_b:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        calib_b = cursor
                elif event.key == pygame.K_c:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        calib_c = cursor
                elif event.key == pygame.K_l:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        marker_l = True
                elif event.key == pygame.K_r:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        marker_r = True
                elif event.key == pygame.K_x:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        marker_l = False
                        marker_l_value = 0
                        marker_r = False
                        marker_r_value = 0
            elif event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                cursor = cursor + event.y
                if cursor < 0:
                    cursor = cursor + 1
                if cursor > 1023:
                    cursor = cursor - 1

        # Fill the background with white
        screen.fill((0, 0, 0))
        # Draw frame rects
        pygame.draw.rect(screen, (0, 255, 0), (1, 1, 1321, 638), 1)
        pygame.draw.rect(screen, (0, 255, 0), (3, 3, 1317, 634), 1)
        # Draw x,y axes
        pygame.draw.line(screen, (0, 255, 0), (255, 20), (255, 520))
        pygame.draw.line(screen, (0, 255, 0), (255, 520), (1278, 520))
        # Draw command rect
        pygame.draw.rect(screen, (0, 255, 0), (255, 600, 1023, 26), 1)
        # Draw separator
        pygame.draw.line(screen, (0, 255, 0), (255, 540), (1278, 540))
        # X and Y axes captions
        x_label = font.render("Ch.", True, (0, 255, 0))
        screen.blit(x_label, (1285, 513))
        y_label = font.render("Count", True, (0, 255, 0))
        screen.blit(y_label, (233, 5))

        # Get data and draw spectra
        if acq_status == True:
            get_data()
            end = timer()

        ch_maxcount = np.max(spectra_array)
        if ch_maxcount > 500:
            scale_factor = ch_maxcount / 500
        else:
            scale_factor = 1

        eachPass = 0
        for eachPass in range(1024):
            pos_x = eachPass + 255
            pos_y = 520 - int(spectra_array[eachPass]/scale_factor)
            #pygame.draw.circle(screen, (200, 200, 0), (pos_x, pos_y), 1, 0)
            pygame.draw.line(screen, (200, 200, 0),(pos_x, pos_y), (pos_x, pos_y))

        if acq_status == False:
            cursor_y = 520
            ch_cnt_caption = font.render(str(0), True, (255, 0, 0))
        else:
            cursor_y = 520 - int(spectra_array[cursor]/scale_factor)
            ch_cnt_caption = font.render(
                str(spectra_array[cursor]), True, (255, 0, 0))

        # Draw moving cursor
        pygame.draw.line(screen, (255, 0, 0), (cursor + 255,
                         cursor_y - 10), (cursor + 255, cursor_y))
        pygame.draw.line(screen, (255, 0, 0), (cursor + 250,
                         cursor_y), (cursor + 255, cursor_y))

        # X and Y axes moving labels
        ch_en_caption = font.render(str(cursor), True, (255, 0, 0))
        rect = ch_en_caption.get_rect()
        rect.center = (cursor + 255, 531)
        screen.blit(ch_en_caption, rect)
        rect = ch_cnt_caption.get_rect()
        rect.topright = (252, cursor_y)
        screen.blit(ch_cnt_caption, rect)

        # Set and draw marker_left and marker_right if activated
        if marker_l == True:
            marker_l_value = cursor
            marker_l = False

        if marker_r == True:
            marker_r_value = cursor
            marker_r = False

        if marker_r_value != 0:
            pos_y = 520 - int(spectra_array[marker_r_value]/scale_factor)
            pygame.draw.line(screen, (0, 0, 255), (marker_r_value +
                             255, pos_y - 20), (marker_r_value + 255, pos_y))
            pygame.draw.line(screen, (0, 0, 255), (marker_r_value +
                             260, pos_y - 20), (marker_r_value + 255, pos_y - 20))

        if marker_l_value != 0:
            pos_y = 520 - int(spectra_array[marker_l_value]/scale_factor)
            pygame.draw.line(screen, (0, 0, 255), (marker_l_value +
                             255, pos_y - 20), (marker_l_value + 255, pos_y))
            pygame.draw.line(screen, (0, 0, 255), (marker_l_value +
                             250, pos_y - 20), (marker_l_value + 255, pos_y - 20))

        if marker_l_value != 0 and marker_r_value != 0:
            pos_yl = 520 - int(spectra_array[marker_l_value]/scale_factor)
            pos_yr = 520 - int(spectra_array[marker_r_value]/scale_factor)
            pygame.draw.line(screen, (0, 0, 255), (marker_l_value +
                             255, pos_yl), (marker_r_value + 255, pos_yr))
            pk_area, FWHM, FWHM_percentual, centroid = fwhm(
                marker_l_value, marker_r_value)

        # Draw calibration markers
        if calib_a > 0:
            if input_string.isdecimal():
                calib_x[0] = calib_a
                calib_y[0] = int(input_string)
                input_string = "OK, chn: " + str(calib_x[0]) + " = " + str(calib_y[0]) + "keV" 
                calib_a = 0
            else:
                calib_a = 0
                input_string="Digit channel enrgy first (in keV) then press Ctrl + A to set calibration point A"

        if calib_b > 0:
            if input_string.isdecimal():
                calib_x[1] = calib_b
                calib_y[1] = int(input_string)
                input_string = "OK, chn: " + str(calib_x[1]) + " = " + str(calib_y[1]) + "keV" 
                calib_b = 0
            else:
                calib_b = 0
                input_string="Digit channel enrgy first (in keV) then press Ctrl + B to set calibration point B"

        if calib_c > 0:
            if input_string.isdecimal():
                calib_x[2] = calib_c
                calib_y[2] = int(input_string)
                input_string = "OK, chn: " + str(calib_x[2]) + " = " + str(calib_y[2]) + "keV" 
                calib_c = 0
            else:
                calib_c = 0
                input_string="Digit channel enrgy first (in keV) then press Ctrl + C to set calibration point C"
            
        for i in range(3):
            if calib_x[i] > 0:
                pos_y = 520 - int(spectra_array[calib_x[i]] / scale_factor)
                pygame.draw.circle(screen, (127, 0, 127), (calib_x[i] + 255, pos_y), 5, 0)
                label = font.render(chr(65 + i), True, (127, 0, 127))
                screen.blit(label, (calib_x[i] + 250, pos_y - 25))


        # Grab key pressed and write command
        block = font.render(input_string, True, (127, 127, 0))
        rect = block.get_rect()
        rect.center = (755, 613)
        screen.blit(block, rect)

        color_time = (200, 200, 0)

        if acq_status == True:
            e_time = end - start + e_time_old
            color_time = (255, 0, 0)

        # Left infobox labels
        labels = [
            ("Time: " + str(int(e_time)), color_time),
            ("Area: " + str(int(pk_area)) + " cnt", (200, 200, 0)),
            ("Centroid: " + str(centroid) + " ch.", (200, 200, 0)),
            ("FWHM: " + str(int(FWHM)) + " ch. " + str(round(FWHM_percentual, 2)) + "%", (200, 200, 0))
        ]

        for i, (label, color) in enumerate(labels):
            rendered_label = font.render(label, True, color)
            screen.blit(rendered_label, (10, 10 + 20 * i))

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


# ========= Main Entry Point =========
if __name__ == "__main__":
    main()