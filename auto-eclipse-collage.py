import os.path
import time
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading


# Return a dictionary containing dates of last change of files
def get(file_name_list):

    results = {}
    
    for file_name in file_name_list:
        file_time = os.path.getmtime(file_name)
        results[file_name] = file_time

    return results


def generate_excluded(index):

    excluded_numbers = []
    excluded_output = []
    # Open excluded file
    excluded_file = open("excluded.txt", "r")
    for line in excluded_file:
        excluded_numbers.append(int(line))
        
    for element in excluded_numbers:
        if element < 10:
            excluded_output.append(index + "00" + str(element) + ".CR2")
        elif element < 100:
            excluded_output.append(index + "0" + str(element) + ".CR2")
        else:
            excluded_output.append(index + str(element) + ".CR2")

    excluded_file.close()    
    return excluded_output


# Return a list with absolute filenames
def file_names(prefix, amount, start, filetype, excluded):
    file_name_list = []

    for n in range (start, amount + 1):
        if n < 10:
            ending = "00" + str(n)
        elif n < 100:
            ending = "0" + str(n)
        else:
            ending = str(n)

        filename = prefix + ending + "." + filetype
        if filename not in excluded:
            file_name_list.append(filename)

    return file_name_list


# Save dates of last change in a csv file
def write_to_file(results):
    file = open("output.csv", "w")
    for image_name in results:
        date = str(time.gmtime(results[image_name])[2])
        date += "." + str(time.gmtime(results[image_name])[1])
        date += "." + str(time.gmtime(results[image_name])[0])
        date += " " + str(time.gmtime(results[image_name])[3])
        date += ":" + str(time.gmtime(results[image_name])[4])
        date += ":" + str(time.gmtime(results[image_name])[5])
        
        file.write(image_name + "," + str(date) + "," + str(results[image_name]) + "\n")

    file.close()
    print("Done!")


# Calculate time-difference between files
def process(results):
    spaces = []
    previous = None
    for image_name in results:
        if previous != None:
            spaces.append(results[image_name] - previous)
        previous = results[image_name]

    print("All waiting times:")
    
    for wait_time in spaces:
        print(wait_time)
    
    print("\nAverage:\n" + str(sum(spaces) / len(spaces)))
    print("\nMinimum:\n" + str(min(spaces)))
    print("\nMaximum:\n" + str(max(spaces)) + "\n")

    return spaces


# Returning given number of files with idealy same time difference
def calculate(amount, results):
    results_reverse = {}
    results_only_time = []

    for image_name in results:
        results_reverse[results[image_name]] = image_name
        results_only_time.append(results[image_name])

    total_time = results_only_time[-1] - results_only_time[0]

    step = total_time / amount
    current_time = results_only_time[0]

    ideal_times = []
    for n in range(amount):
        ideal_times.append(current_time)
        current_time += step
    # Finding nearest imange time for every ideal time
    best_image_times = []
    
    for ideal_time in ideal_times:
        current_best_time = 0
        current_best_difference = 999999999999999999999
        
        for image_time in results_only_time:
            time_difference = abs(image_time - ideal_time)
            
            if time_difference < current_best_difference:
                current_best_difference = time_difference
                current_best_time = image_time
                
        best_image_times.append(current_best_time)


    previous = None
    all_variations = []
    best_image_names = []
    
    for n in best_image_times:
        image_name = results_reverse[n]
        best_image_names.append(image_name)
        if previous != None:
            print(image_name, "  Step:", round(n - previous, 2), end=" ")
            variation = round(abs(step - (n - previous)), 2)
            all_variations.append(variation)
            print("  (" + str(variation) + ")")
            previous = n
        else:
            print(image_name)
            previous = n

    print("\nIdeal Step:", round(step, 2))
    print("Average Variation:", sum(all_variations) / len(all_variations))
    print("Minimum Variation:", min(all_variations))
    print("Maximum Variation:", max(all_variations))

    return best_image_names


# Renaming string ending to .jpg
def to_jpg(file_names):
    output = []
    for file_name in file_names:
        chars = list(file_name)
        for n in range(3):
            del chars[-1]
        chars += "j", "p", "g"
        output.append("".join(chars))

    return output


# Adding images to one
def combine_images_downscale(file_name_list, grid_width, grid_height, factor):
    global progressbar
    images = []
    for file_name in file_name_list:
        image = Image.open(file_name)
        # Downscaling
        size_x, size_y = image.size
        image = image.resize((round(size_x / factor), round(size_y / factor)), Image.ANTIALIAS)
        images.append(image)

        percentage = file_name_list.index(file_name) / len(file_name_list) * 100
        print(str(percentage) + "%")
        progressbar.config(value=percentage)

    output_width = images[0].size[0] * grid_width
    output_height = images[0].size[1] * grid_height

    output = Image.new("RGB", (output_width, output_height))

    x_offset = 0
    y_offset = 0

    column = 0

    for image in images:
        output.paste(image, (x_offset, y_offset))
        x_offset += image.size[0]
        column += 1
        if column == grid_width:
            y_offset += image.size[1]
            x_offset = 0
            column = 0
            
        percentage = images.index(image) / len(images) * 100
        print(str(percentage) + "%")
        progressbar.config(value=percentage)

    output.save("output" + str(grid_width) + "x" + str(grid_height) + ".jpg")
    print("Done!")


def run(file_index, first_image_number, last_image_number,
        output_width, output_height, downscale_factor, excluded):
    file_name_list = calculate(output_width * output_height, get(file_names(file_index,
                                                                        last_image_number,
                                                                        first_image_number,
                                                                        "CR2", excluded)))
    file_name_list = to_jpg(file_name_list)
    combine_images_downscale(file_name_list, output_width, output_height, downscale_factor)


# GUI
def start_button_press():
    threading.Thread(target=start_button_run).start()


def start_button_run():
    global downscale, progressbar
    downscale_var = downscale.get()
    # Reading information
    file_index = file_index_entry.get()
    first_image_number = first_image_entry.get()
    first_image_number = int(first_image_number)
    last_image_number = last_image_entry.get()
    last_image_number = int(last_image_number)
    output_width = width_combobox.get()
    output_width = int(output_width)
    output_height = height_combobox.get()
    output_height = int(output_height)
    if downscale_var == 1:
        factor = round(max(output_width, output_height) / 3)
    else:
        factor = 1

    excluded = generate_excluded(file_index)
    
    # Run
    run(file_index, first_image_number, last_image_number,
        output_width, output_height, factor, excluded)

    progressbar.config(value=100)


root = tk.Tk()

root.title("Auto Eclipse Collage Generator")

root.resizable(False, False)

# Row 0
file_index_lbl = ttk.Label(root, text="File Index:")
file_index_lbl.grid(row=0, column=0, padx=3, pady=3, sticky="e")
    
file_index_entry = ttk.Entry(root)
file_index_entry.grid(row=0, column=1, padx=3, pady=3, sticky="w")

width_lbl = ttk.Label(root, text="Grid Width:")
width_lbl.grid(row=0, column=2, padx=13, pady=3, sticky="e")

width_combobox = ttk.Combobox(root, values=[2, 5, 10, 15])
width_combobox.grid(row=0, column=3, padx=3, pady=3, sticky="w")

# Row 1
first_image_lbl = ttk.Label(root, text="First Image Number:")
first_image_lbl.grid(row=1, column=0, padx=3, pady=3, sticky="e")

first_image_entry = ttk.Entry(root)
first_image_entry.grid(row=1, column=1, padx=3, pady=3, sticky="w")

height_lbl = ttk.Label(root, text="Grid Height:")
height_lbl.grid(row=1, column=2, padx=13, pady=3, sticky="e")

height_combobox = ttk.Combobox(root, values=[2, 5, 10, 15])
height_combobox.grid(row=1, column=3, padx=3, pady=3, sticky="w")

# Row 2
last_image_lbl = ttk.Label(root, text="Last Image Number:")
last_image_lbl.grid(row=2, column=0, padx=3, pady=3, sticky="e")

last_image_entry = ttk.Entry(root)
last_image_entry.grid(row=2, column=1, padx=3, pady=3, sticky="w")

downscale_lbl = ttk.Label(root, text="Downscaling:")
downscale_lbl.grid(row=2, column=2, padx=13, pady=3, sticky="e")
    
downscale = tk.IntVar()
downscale_checkbutton = tk.Checkbutton(root, variable=downscale)
downscale_checkbutton.grid(row=2, column=3, padx=3, pady=3, sticky="w")

# Row 3
start_button = ttk.Button(root, text="Start", command=start_button_press)
start_button.grid(row=3, column=3, padx=3, pady=10, ipadx=7, sticky="w")
    
progressbar = ttk.Progressbar(root, mode="determinate", value=0, length=350)
progressbar.grid(row=3, column=0, padx=13, pady=3, columnspan=3, sticky="e")

root.mainloop()

''' 
import excluded

output_width = 3
output_height = 5
file_names = calculate(output_width * output_height, get(file_names("Mond_", 563, 1, "CR2", excluded.excluded)))
file_names = to_jpg(file_names)
combine_images_downscale(file_names, output_width, output_height, 1)

for n in range(3, 30):
    file_name_list = calculate(n * n, get(file_names("Mond_", 563, 1, "CR2", excluded.excluded)))
    file_name_list = to_jpg(file_name_list)
    combine_images_downscale(file_name_list, n, n, round(n / 3))
'''

