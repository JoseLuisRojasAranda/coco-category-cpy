import sys
import cv2
import json

def main():
    render_image("../copied_images/000000434201.jpg")

def render_image(img_path):
    image = cv2.imread(img_path)
    with open(img_path + ".json") as json_file:
        data = json.load(json_file)
        for box in data["bboxes"]:
            x = int(box["center_x"])
            y = int(box["center_y"])
            w = int(box["width"])
            h = int(box["height"])

            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)

    cv2.imshow("test_ssd", image)
    cv2.waitKey(0)

main()

