from PIL import Image

# 画像の読み込み
image = Image.open("/home/yuga/usr/yuga_ws/pyxel_puzzle/io/5.png")

# 20x20にリサイズ
resized_image = image.resize((20, 20))

# リサイズした画像の保存
resized_image.save("/home/yuga/usr/yuga_ws/pyxel_puzzle/io/5_resize.png")
