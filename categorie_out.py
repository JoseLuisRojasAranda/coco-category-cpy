# requirements:
#   - Cython
#   - pycocotools
#   - requests
#   - Pillow
from pycocotools.coco import COCO
import numpy as np
from PIL import Image
import os
import json
import requests

def main():
    dataDir='..'
    dataType='train2017'
    categories_to_download = ["apple"]
    categories_of_anns = categories_to_download
    num_imgs_to_download = 1 # -1 para todas, 1 para seleccionar un indice
    selected_index = 3

    # Cargado de las imagenes
    print("[INFO] Loading images...")

    annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
    coco=COCO(annFile)

    catIds = coco.getCatIds(catNms=categories_to_download)
    anns_cat_ids = coco.getCatIds(catNms=categories_of_anns)
    imgIds = coco.getImgIds(catIds=catIds)



    # Copia una imagen a otra carpeta y crea json con anotaciones
    # Argumentos:
    #   image: coco image object
    #   anns: image annotation object
    #   copy_type: si se va a copiar de forma local o desde el servidor
    #   folder: nombre de la carpeta donde se va a copiar la imagen 
    #   local_path: path the las imagenes locales
    def cpy_image(image, anns=None, copy_type="LOCAL", folder="copied_images", local_path="../images/"):
        if not os.path.exists("../" + folder):
            os.makedirs("../" + folder)

        if copy_type == "SERVER":
            img_data = requests.get(image["coco_url"]).content
            with open("../" + folder + "/" + image["file_name"], "wb") as handler:
                handler.write(img_data)
        elif copy_type == "LOCAL":
            img_data = Image.open(local_path + image["file_name"])
            img_data.save("../" + folder + "/" + image["file_name"])

        if anns:
            data = { }
            data["filename"] = image["file_name"]
            data["width"] = image["width"]
            data["height"] = image["height"]

            bboxes = []
            for a in anns:
                x, y, w, h = a["bbox"]
                bbox = {}
                bbox["category_id"] = coco.loadCats(a["category_id"])[0]["name"]
                bbox["center_x"] = x
                bbox["center_y"] = y
                bbox["width"] = w
                bbox["height"] = h
                bboxes.append(bbox)

            data["bboxes"] = bboxes
            with open("../" + folder + "/" + image["file_name"] + ".json", 'w') as outfile:
                    json.dump(data, outfile)


    print("[INFO] Copyng images...")
    total_images = len(imgIds)
    count = 0

    if num_imgs_to_download == -1 or num_imgs_to_download > 1:
        if num_imgs_to_download == -1:
            num_imgs_to_download = total_images

        for i in range(num_imgs_to_download):
            img = imgIds[i]

            count = count + 1
            if count % 50 == 0:
                print("[INFO] Copied {} of {} images".format(count, total_images))

            image = coco.loadImgs(img)[0]
            annIds = coco.getAnnIds(imgIds=image["id"], catIds=anns_cat_ids, iscrowd=None)
            anns = coco.loadAnns(annIds)
            cpy_image(image, anns=anns)

    elif num_imgs_to_download == 1:
        img = imgIds[selected_index]
        image = coco.loadImgs(img)[0]
        annIds = coco.getAnnIds(imgIds=image["id"], catIds=anns_cat_ids, iscrowd=None)
        anns = coco.loadAnns(annIds)
        cpy_image(image, anns=anns)

main()


