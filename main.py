import cv2 as cv
from pyzbar.pyzbar import decode
import numpy as np
def decoder(image):
    gray_img = cv.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        print(obj)
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data" + str(barcodeData) + "| Type" + str(barcodeType)
        cv.putText(frame, string, (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        print("Barcode: " + barcodeData + "| Type" + barcodeType)




cap = cv.VideoCapture(1)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv.imshow("Image", frame)
    code = cv.waitKey(10)
    if code == ord('q'):
        break

