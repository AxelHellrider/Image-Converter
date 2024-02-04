from PIL import Image
from tkinter import filedialog, Tk, Label, Button, messagebox, StringVar, Entry, Progressbar
from ttkthemes import ThemedStyle
import os


# Background Conversion Task
def convert_images_to_webp(input_folder, output_folder, progress_bar):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        all_files = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]
        image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.tiff', '.jpeg', '.png', '.bmp'))]

        # Progress Bar on Screen
        total_files = len(image_files)
        progress_bar["maximum"] = total_files

        for i, file in enumerate(image_files, start=1):
            progress_bar["value"] = i
            progress_bar.update()

            # Conversion Logic
            user_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.webp')

            with Image.open(user_path) as img:
                if img.mode == "P" and "transparency" in img.info:
                    img = img.convert("RGBA")
                elif img.mode != "RGBA":
                    img = img.convert("RGBA")

                img.save(output_path, 'WEBP')

        messagebox.showinfo("Success", "Conversion completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Folder Selection
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        input_folder_var.set(folder_selected)


# Image Conversion on UI
def convert_images():
    input_folder = input_folder_var.get()
    output_folder = os.path.join(os.path.expanduser("~"), "Documents", "converted-images")

    progress_bar = Progressbar(root, mode="determinate", length=300)
    progress_bar.grid(row=5, column=0, columnspan=4, pady=(10, 20))

    convert_images_to_webp(input_folder, output_folder, progress_bar)


# UI Initialization
root = Tk()

style = ThemedStyle(root)
style.set_theme("equilux")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_window_x = (screen_width - 400) // 2
center_window_y = (screen_height - 180) // 2
root.geometry(f"400x180+{center_window_x}+{center_window_y}")
root.title("WEBP Image Converter")

input_folder_var = StringVar()
Label(root, text="Image Converter", font=("Aptos", 12)).grid(row=0, column=0, columnspan=3, pady=(10, 5))
Label(root, text="Input Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
Entry(root, textvariable=input_folder_var, width=30).grid(row=1, column=1, pady=5)
Button(root, text="Select Folder", command=select_folder).grid(row=1, column=2, padx=5, pady=5)
Button(root, text="Convert", command=convert_images).grid(row=2, column=0, columnspan=3, pady=10)


root.mainloop()
