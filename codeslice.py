from PIL import Image
import os

input_dir = 'AllKanjiPositionAN'  # 入力ディレクトリ
output_dir = 'output_boxes'  # 出力ディレクトリ

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 切り取るサイズをここで指定する
tile_width = 500
tile_height = 500

# フォルダ内の画像ファイルをすべて取得
image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

a = 100 #画像ファイルの番号

# 処理
for image_file in image_files:
    image_path = os.path.join(input_dir, image_file)

    # 読み込み
    img = Image.open(image_path)
    img_width, img_height = img.size

    for i in range(0, img_width, tile_width):
        for j in range(0, img_height, tile_height):
            # 切り取る領域を定義
            box = (i, j, i + tile_width, j + tile_height)
            cropped_img = img.crop(box)

            # ファイル名を指定
            output_file = os.path.join(output_dir, f'tile_{a}.jpg')
            cropped_img.save(output_file)
            a += 1

print("すべての画像の切り取りが完了しました。")
