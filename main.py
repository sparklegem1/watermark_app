from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from tkinter.filedialog import askopenfilename


files = []


def open_file():
    message.set(' ')
    init_image = askopenfilename()
    files.append(init_image)
    browse_text.set('Choose Logo')
    browse_btn.configure(command=choose_watermark)
    howto.config(text='Now choose an image as the watermark logo!')

def  choose_watermark():

    global files

    try:
        # GET IMAGE
        image = Image.open(files[0]).convert('RGBA')
        wm = askopenfilename()
        watermark = Image.open(wm)
        resized_image = watermark.resize((round(image.size[0] * .35), round(image.size[1] * .35)))
        mask = resized_image.convert('RGBA')

        #SET IMAGE POSITION
        position = (image.size[0] - resized_image.size[0], image.size[1] - resized_image.size[1])

        # MASK
        pseudo_img = Image.new('RGBA', image.size, (0, 0, 0, 0))
        pseudo_img.paste(image, (0, 0))
        pseudo_img.paste(mask, position, mask=mask)
        pseudo_img.show()

        # RESULT
        final_img = pseudo_img.convert('RGB')
        final_img_path = files[0][:-4] + ' WM.jpg'
        final_img.save(final_img_path)
        message.set(f'Success!  File saved to {final_img_path}.')

    except UnidentifiedImageError:
        message.set('im sorry but this file type is not supported, try converting it to .jpg or .png')

    # RESET EVERYTHING
    howto.config(text='First choose a photo to watermark.')
    browse_btn.configure(command=open_file)
    browse_text.set('choose pic')
    files = []


def quit():
    root.destroy()


#GUI
root = tk.Tk()
root.title('Easy Watermark')

canvas = tk.Canvas(root, width=600, height=500)
canvas.grid(columnspan=5, rowspan=4)

logo = Image.open("images/fairytale.png")
logo = logo.resize((200, 200))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=3, row=0)

# HOW-TO TEXT
howto = tk.Label(root, text='First choose a photo to watermark.', font='Arial')
howto.grid(columnspan=5, column=0, row=1)

# CHOOSE FILE BUTTON
browse_text = tk.StringVar()
browse_btn = tk.Button(root, command=open_file, textvariable=browse_text, font='Arial', bg='#fcaca7', fg='black',
                       height=2, width=15)
browse_text.set('choose pic')
browse_btn.grid(column=2, row=2)

# MESSAGES
message = tk.StringVar()
message.set(' ')
message_label = tk.Label(root, textvariable=message)
message_label.grid(columnspan=5, column=0, row=3)


quit_button = tk.Button(root, text='close', command=quit, font='Arial', bg='#cffca7', fg='black', height=2, width=15)
quit_button.grid(column=4, row=2, padx=10)

root.mainloop()