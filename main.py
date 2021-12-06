import cv2 as cv
from pyzbar.pyzbar import decode
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageTk


def decoder(image):
    gray_img = cv.cvtColor(image, 0)
    barcode = decode(gray_img)
    barcodeData = None

    for obj in barcode:
        #print(obj)
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data" + str(barcodeData) + "| Type" + str(barcodeType)
        #cv.putText(image, string, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        #print("Barcode: " + barcodeData + "| Type" + barcodeType)
    return barcodeData


def load_database(item):
    data = pd.read_excel(item,
                          sheet_name="orders",
                          header=0,
                          index_col=4)

    '''It is very important to make sure that the "Tracking Number*" is located on column number 4 starts from Zero'''
    '''To make it easier we change the index to "Tracking" '''
    data.index = data.index.rename('Tracking')

    '''Remove all other Data except the main columns we need'''
    data = data.drop(data.columns.difference(['Product Name', 'Quantity', 'Variation Name']), 1, inplace=False)

    '''make sure that columns names are correct and short'''
    data.rename(columns={"Product Name": "Product", "Quantity": "Quantity", "Variation Name": "Variation"}, inplace=True)

    return data


def show_pl(PL):
    win2 = tk.Tk()
    win2.geometry('700x800')
    close_win2 = tk.Button(win2, text="Close", pady=15, padx=25, bg='red', fg='white', command=win2.destroy)
    close_win2.grid(row=23, column=0)
    header_message = tk.Label(win2, text=str(PL))
    header_message.grid(row=50, column=0)
    win2.mainloop()


def pl_show_pl(PL):
    ''' Designing the Fonts '''
    font_headline = ImageFont.truetype('impact.ttf', 20)
    font_text2 = ImageFont.truetype('arial.ttf', 14)

    width = 1000
    height = 700
    lot = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
    lot_text = ImageDraw.Draw(lot)
    logo = Image.open("logo.jpg")
    logo = logo.resize((100, 150))
    lot.paste(logo, (900, 550))
    ''' Inserting the Header '''
    lot_text.text((10, 10), 'Product', fill=(0, 0, 0), font=font_headline)
    lot_text.text((800, 10), 'Variation', fill=(0, 0, 0), font=font_headline)
    lot_text.text((900, 10), 'Quantity', fill=(0, 0, 0), font=font_headline)
    ''' Inserting the information'''
    if PL.size > 3:
        for i in range(0, int(PL.size / 3)):
            spacer = 50 * (i+1)
            lot_text.text((10, spacer), PL.Product[i], fill=(0, 0, 0), font=font_text2)
            lot_text.text((800, spacer), str(PL.Variation[i]), fill=(0, 0, 0), font=font_text2)
            lot_text.text((900, spacer), str(PL.Quantity[i]), fill=(0, 0, 0), font=font_text2)
    else:
        lot_text.text((10, 50), PL.Product, fill=(0, 0, 0), font=font_text2)
        lot_text.text((800, 50), str(PL.Variation), fill=(0, 0, 0), font=font_text2)
        lot_text.text((900, 50), str(PL.Quantity), fill=(0, 0, 0), font=font_text2)

    lot.show()


def activate_camera():
    barcodeData = None
    cap = cv.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        barcodeData = decoder(frame)

        if barcodeData:
            print('The Tracking number is {}\n'.format(barcodeData))
            PL = data.loc[barcodeData]
            print(PL)
            break

        cv.imshow("Image", frame)
        code = cv.waitKey(10)
        if code == ord('q'):
            PL = None
            break
    print('The Bar code is detected')

    '''here we should proceed to show the result.'''
    #tk.messagebox.showinfo(title="Product list", message=str(PL))
    cv.destroyWindow('Image')
    cap.release()

#    show_pl(PL)
    pl_show_pl(PL)
    return PL


item = 'Today.xlsx'
data = load_database(item)
print(data.head())


win = tk.Tk()
win.geometry('300x100')
win.title('Packing List of Shopee')

start_scaning = tk.Button(win, text="Scan a Parcel ", pady=15, padx=25, bg='green', fg='white', command=activate_camera)
start_scaning.grid(row=23, column=0)

close1 = tk.Button(win, text="Log Out", pady=15, padx=25, bg='red', fg='white', command=win.destroy)
close1.grid(row=23, column=2)



win.mainloop()










