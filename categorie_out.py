# requirements:
#   - Cython
#   - pycocotools
#   - requests
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import requests

dataDir='..'
dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)

coco=COCO(annFile)

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['apple']);
imgIds = coco.getImgIds(catIds=catIds );

print("[INFO] Copyng images...")
total_images = len(imgIds)
count = 0

for img in imgIds:
    count = count + 1
    if count % 50 == 0:
        print("[INFO] Copied {} of {} images".format(count, total_images))

    image = coco.loadImgs(img)[0]
    img_data = requests.get(image['coco_url']).content
    with open('../apple/' + image['file_name'], 'wb') as handler:
        handler.write(img_data)

'''
with open('annotations_download_' + classes + '.csv', mode='w', newline='') as annot:
    for im in images:
        annIds = coco.getAnnIds(imgIds=im['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        for i in range(len(anns)):
            annot_writer = csv.writer(annot)
            annot_writer.writerow(['downloaded_images/' + im['file_name'],
                int(round(anns[i]['bbox'][0])),
                int(round(anns[i]['bbox'][1])),
                int(round(anns[i]['bbox'][0] + anns[i]['bbox'][2])),
                int(round(anns[i]['bbox'][1] + anns[i]['bbox'][3])),
                classes])
            annot.close()
'''
