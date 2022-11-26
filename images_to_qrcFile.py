import os

qrc = '<!DOCTYPE RCC><RCC version="1.0">\n'
qrc += '<qresource>\n'
for p, d, f in os.walk("../"):
    imgs = ""  # 图片部分
    for ff in f:
        if ff.endswith(".png") or ff.endswith(".jpg"):  # 图片文件
            imgs += f"<file>{p + '/' + ff}</file>\n".replace('\\', '/')
    if imgs:  # 该目录内有图片才会加入该目录
        qrc += imgs
qrc += "</qresource>\n"
qrc += "</RCC>"
with open(r"images.rc", "w") as f:
    f.write(qrc)

with os.popen(r"pyside6-rcc images.rc -o ./images.py") as f:
    s = f.read()
    print(s)
