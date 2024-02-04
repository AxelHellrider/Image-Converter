from PIL import Image
from tkinter import filedialog, Tk, Label, Button, messagebox, ttk
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
def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_label.config(text="Input Folder: " + folder_selected)
    convert_button.config(state="normal")
    convert_button['command'] = lambda: convert_images(input_folder=folder_selected)


# Image Conversion on UI
def convert_images(input_folder):
    output_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'converted-images')
    try:
        progress_bar = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
        progress_bar.pack(pady=5)

        convert_images_to_webp(input_folder, output_folder, progress_bar)
        output_folder_label.config(text="Output Folder: " + output_folder)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# UI Initialization
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_window_x = (screen_width - 500) // 2
center_window_y = (screen_height - 180) // 2
root.geometry(f"500x180+{center_window_x}+{center_window_y}")
root.title("Image Converter")

input_folder_label = Label(root, text="Input Folder: ")
input_folder_label.pack()

select_folder_button = Button(root, text="Select Input Folder", command=select_input_folder)
select_folder_button.pack()

convert_button = Button(root, text="Convert Images", state="disabled")
convert_button.pack()

output_folder_label = Label(root, text="Output Folder: ")
output_folder_label.pack()

root.mainloop()
