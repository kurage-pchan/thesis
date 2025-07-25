import cv2
import numpy as np
import os
import glob
import json

folder_path = "D:/Code/research/task10/outputbox"
output_dir = "D:/Code/research/task10/Outputtxt"
os.makedirs(output_dir, exist_ok=True)

# 画像ファイル一覧取得
path = glob.glob(os.path.join(folder_path, "*.jpg"))
data = [cv2.imread(p, cv2.IMREAD_GRAYSCALE) for p in path]

def list_from_mask_coco(images):
    images_box = []
    for img in images:
        spread = cv2.connectedComponentsWithStats(255 - img)
        img_box = []
        _, _, stats, centroids = spread
        for i in range(1, len(centroids)):  # 0は背景なので1から
            x_min = int(stats[i][0])
            y_min = int(stats[i][1])
            width = int(stats[i][2])
            height = int(stats[i][3])
            img_box.append([0, x_min, y_min, width, height])  # 0はクラスID
        images_box.append(img_box)
    return images_box

images_box_coco = list_from_mask_coco(data)

for i, (image, img_path) in enumerate(zip(images_box_coco, path)):
    img = cv2.imread(img_path)
    height, width = img.shape[:2]
    image_info = {
        "id": int(i),
        "file_name": os.path.basename(img_path),
        "width": int(width),
        "height": int(height)
    }
    annotations = []
    for j, sub in enumerate(image):
        ann = {
            "id": int(j),
            "image_id": int(i),
            "category_id": 0,
            "bbox": [int(sub[1]), int(sub[2]), int(sub[3]), int(sub[4])],
            "area": int(sub[3]) * int(sub[4]),
            "iscrowd": 0
        }
        annotations.append(ann)
    coco_dict = {
        "images": [image_info],
        "annotations": annotations,
        "categories": [
            {"id": 0, "name": "Kanji"}
        ]
    }
    path_w = os.path.join(output_dir, f"testcoco_{i}.json")
    with open(path_w, mode='w', encoding='utf-8') as f:
        json.dump(coco_dict, f, ensure_ascii=False, indent=2)