import cmath
import math
import random
import sys

from PySide6.QtCore import Qt, QPropertyAnimation, Property, QParallelAnimationGroup, Slot, QTimer, QLine, QPoint, \
    QRect, QSize
from PySide6.QtGui import QIcon, QPainter, QPen, QPolygon, QPainterPath, QColor, QLinearGradient, QFont
from PySide6.QtWidgets import QApplication, QWidget, QPushButton

from images import *

text = """
2020
泪眼问花花不语
till one day I lost you
日日思君不见君
You had me at “hello”
Years stationed in the belief
for reality is better than a dream
乱红飞过秋千去
I fear I will fall in love with you
长逝入君怀
only you are my unique rose
日日思君不见君
驻守岁月的信念
Brief is life, but love is long
春柳春花满画楼
It was love at first sight
杨柳岸，晓风残月
The deepest love I think, later than apart,
I will live as you like
若是前生未有缘，待重结、来生愿。
竟夕起相思
I just keep losting in your eyes
莫待无花空折枝
只有相思无尽处
执子之手，与子偕老
More than 50 years of solitude
此情无计可消除
I know you like this song most
All this I did without you
一日不见兮，思之如狂
Only if you asked to see me, our meeting would be meaningful to me
半缘修道半缘君
All this I want to do with you.
"""


class Lines():
    """统一绘制的线"""

    def __init__(self, lines, pen=None):
        self.lines = lines
        self.pen = pen


class Polygons():
    """统一绘制的多边形"""

    def __init__(self, polygons, pen=None, fill=None):
        self.polygons = polygons
        self.pen = pen
        self.fill = fill
        self.painter_path = QPainterPath()
        for p in polygons:
            self.painter_path.addPolygon(p)


class Text():
    def __init__(self, texts, pen=None, font=None):
        self.texts = texts
        self.pen = pen
        self.font = font


class Layer():
    """批量绘制类似元素"""

    def __init__(self, content=None, rotation=0, translation=(0, 0), mode=QPainter.CompositionMode_SourceOver):
        self.rotation = rotation
        self.translation = translation
        self.content = content
        self.mode = mode


class Heart(QWidget):
    """爱心界面"""

    def set_close_count_down(self, count_down):
        self.count_down = count_down  # 倒计时
        self.close_button.setText(str(int(count_down)))
        if count_down == 0:
            self.close()

    def get_close_count_down(self):
        return self.count_down

    close_count_down = Property(float, get_close_count_down, set_close_count_down)

    def __init__(self, *args, **kwargs):
        super(Heart, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(":love.png"))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        self.close_button = QPushButton(self, icon=QIcon(":love.png"), text="关闭", clicked=self.end, shortcut="ctrl+w")
        self.close_button.move((self.width() - self.close_button.width()) // 2,
                               self.height() - self.close_button.height() - 50)
        self.close_button.resize(70, 70)
        self.close_button.setIconSize(QSize(30, 30))
        self.close_button.setStyleSheet("QPushButton{background-color:rgba(255,255,255,0);color:white}")
        self.close_button.show()

        self.count_down = 10  # 倒计时
        self.time = 0  # 全局时长,所有动画通过这个实现
        self.shapes = []  # 绘制的所有线
        self.color = [QColor(120 + i * 20, 90 + i * 9, 150 + i * 20) for i in range(50)]  # 颜色
        self.selector = [[ii for ii in range(100) if random.randint(1, 1000) % 4 < 1] for i in range(50)]
        self.selector2 = [[ii for ii in range(100) if random.randint(1, 1000) % 8 < 1] for i in range(50)]
        self.random_num = random.random()
        self.enable_perspective = True  # 只有开启了才会有效
        self.text = text.split("\n")
        self.text = [i for i in self.text if i]
        self.custom_seed = [random.randint(0, i) for i in range(100)]
        self.button_heart = []
        self.offset = 0  # 时间偏移

        timer = QTimer(self)
        timer.setInterval(10)
        timer.timeout.connect(self.time_count)
        timer.start()

    def time_count(self):
        self.time += 10
        self.shapes = []
        self.polygons = []
        width = self.width()
        height = self.height()
        self.offset = self.time / 10
        if 3 > self.offset % 10 > 1:  # 每10次才更新绘图，避免卡顿
            offset = int(self.offset / 10)
        else:
            return
        min_w = min(width // 2, height // 2)

        # 连接的爱心
        w = int(min_w * 0.75)
        ln = 7 if offset < 100 else min(16, offset)
        ln2 = ln // 2
        for i in range(ln):
            phase = offset / 4 - abs(i - ln2)
            if phase > 0:
                phase = phase if phase < 10 else math.sin(offset / 2) * offset  # 先成形再跳动
                w1 = h1 = w if offset < 10 else int(
                    20 + (w + math.sin(offset * 0.75) * 0.1 * w) / max(1, offset / 30))
                x = w * i + (width // 2 - w * ln2)
                heart_lines1 = self.generate_heart1_line(width=w1, height=h1, phase=phase)
                self.shapes.append(Layer(Lines(heart_lines1, QPen(QColor(230, 50, 130), 3)), translation=(x, w / 4)))

                heart_lines2 = self.generate_heart1_line(width=w1, height=h1, phase=phase + 1)
                self.shapes.append(Layer(Lines(heart_lines2, QPen(QColor(200, 60, 100, 100), 3)),
                                         translation=(x, w / 4)))

                heart_lines2 = self.generate_heart1_line(width=w1, height=h1, phase=phase + 2)
                self.shapes.append(Layer(Lines(heart_lines2, QPen(QColor(200, 30, 100, 150), 3)),
                                         translation=(x, w / 4)))
            if phase > 5:
                phase = phase - 5 if phase < 10 else math.sin(offset / 2) * offset  # 先成形再跳动
                quan = (abs(min(100 - offset, 0)) / offset)
                w1 = h1 = w if offset < 15 else int(
                    5 + (w + math.sin(offset * 0.7) * 0.1 * w) / max(1, offset / 30))
                x = (w * i + (width // 2 - w * ln2)) * (1 - quan) + (w1 * i + (width // 2 - w1 * ln2)) * quan
                heart_lines3 = self.generate_heart1_line(width=w1, height=h1, phase=phase)

                heart_lines4 = self.generate_heart1_line(width=w1, height=h1, phase=phase + 1)

                self.shapes.append(Layer(Lines(heart_lines3, QPen(QColor(230, 70, 80), 3)),
                                         translation=(x, w * 2.5), rotation=180))

                self.shapes.append(Layer(Lines(heart_lines4, QPen(QColor(200, 70, 70, 150), 2)),
                                         translation=(x, w * 2.5), rotation=180))
        # """透视空间"""
        if offset > 60:
            for ray in range(40):  # 共细分为40个部分
                radius = max(width, height) / 2  # 绘制的半径
                o = offset - 60
                # 块
                if o * 2 - ray > 0:
                    polygons = self.generate_persepective_polygons(radius=radius, intercept=(
                        15.001 - ray * 0.375, 15.001 - (ray + 1) * 0.375), num=15)
                    s = []
                    for i in self.selector[(ray - o + 2) % 50]:
                        s.append(polygons[i % 60])
                    polygons = s
                    self.shapes.append(Layer(Polygons(polygons, Qt.NoPen, self.color[(-offset + ray + 2) % 50]),
                                             translation=(width / 2, height / 2), rotation=90))

                    # 块
                    polygons = self.generate_persepective_polygons(radius=radius, intercept=(
                        15.001 - ray * 0.375, 15.001 - (ray + 1) * 0.375), num=20)
                    s = []
                    for i in self.selector[(ray - o) % 50]:
                        s.append(polygons[i % 80])
                    polygons = s
                    self.shapes.append(Layer(Polygons(polygons, Qt.NoPen, self.color[(-offset + ray) % 50]),
                                             translation=(width / 2, height / 2), rotation=0))

        # 实心
        if offset > 30:
            o = offset - 30
            hs = []  # 用于绘图排序
            for i in range(40):
                seed1 = math.sin(i + math.pi) * math.cos(i / 15) * 2 * math.cos(i / 7) + self.random_num
                seed2 = math.sin(i / 13) * math.cos(i + math.pi) * 2 * math.cos(i / 3) - self.random_num
                aseed = abs(seed1)
                n = (o - i * 5) ** 1.2 % 150 if o > i * 5 else 0  # 缩放值
                w = int(max(min(abs(seed2), 1) * min_w * n / 200, 3))
                h = w * (1 + seed1 * 0.1)
                ty = seed1 * 10 % 9
                if n > 0.5:
                    if ty > 6:  # 分类
                        heart_lines4 = self.generate_heart2(width=w, height=h, type=seed1 * 10 % 2)
                        o1 = int(offset // 2 % w)  # 色彩偏移
                        pen1 = QPen(
                            QColor(230 + seed1 * 5, 100 - seed2 * 10, 150 + seed1 * 20,
                                   220 - max(1, n) * 1.5 + seed1 * 20),
                            max(2 * aseed, 2), Qt.CustomDashLine)
                        pen1.setDashPattern([1, 3, 1])
                        hs.append((n,
                                   Layer(Lines(heart_lines4[:o1], pen1),
                                         translation=(width / 2 + (seed1 - seed2) * w * 2,
                                                      height / 2 - w * 2 * (seed2 + seed1)),
                                         rotation=360 * seed1)))
                        pen2 = QPen(
                            QColor(220 + seed2 * 20, 80 + seed1 * 20, 180 - seed2 * 5,
                                   230 - max(1, n) * 1.5 + seed2 * 20),
                            max(aseed, 1), Qt.CustomDashLine)
                        pen2.setDashPattern([1, 5, 1])
                        hs.append((n,
                                   Layer(Lines(heart_lines4[o1:], pen2),
                                         translation=(width / 2 + (seed1 - seed2) * w * 2,
                                                      height / 2 - w * 2 * (seed2 + seed1)),
                                         rotation=360 * seed1)))
                    elif ty > 2:
                        heart_lines3 = self.generate_heart2(width=w, height=h, type=seed2 * 3 % 2)
                        hs.append((n,
                                   Layer(
                                       Lines(heart_lines3,
                                             QPen(QColor(220 - seed1 * 20, 100 + seed2 * 10, 120 - seed2 * 10,
                                                         255 - max(1, math.sqrt(n)) * 1.5 - seed2 * 10), 1)),
                                       translation=(width / 2 - seed2 * w * 2 - seed2 * w,
                                                    height / 2 + w * 2 * seed2 + seed1 * w), rotation=360 * seed2)))
                    else:
                        if n < 5:
                            self.custom_seed[
                                i] = random.random() * 17 if random.random() < 0.5 else -random.random() * 19
                        else:
                            text = self.text[int((i + self.custom_seed[i]) % len(self.text))]
                            hs.append(
                                (n, Layer(
                                    Text(((0, 0, text)),
                                         QPen(QColor(seed2 * 20 + 120, seed1 * 30 + 100, seed2 * 20 + 150)),
                                         QFont("华文琥珀", max(abs(seed2) / math.sqrt(len(text)) * n, 1))),
                                    translation=(
                                        width / 2 - seed1 * w * 2 + seed2 + self.custom_seed[i] / 10 * w,
                                        height / 2 + w * 2 * seed2 - self.custom_seed[i] / 10 * w),
                                    rotation=seed1 * self.custom_seed[i])))
            hs.sort(key=lambda k: k[0])
            for s in hs:
                self.shapes.append(s[1])
        # 点击
        l1 = []
        l2 = []
        l3 = []
        next_bh = []
        for tp in self.button_heart:
            t, p, rotation = tp
            t1 = self.offset - t
            translation = (p.x(), p.y())
            if t1 < 120:
                w = int(10 + t1 * 0.3)
                l1.append(Layer(Lines(self.generate_heart2(width=w, height=w, type=2),
                                      QPen(QColor(220 + t1 % 30, t1 % 3, 150 + t1 % 3, 230 - t1 * 3), 2)),
                                translation=translation, rotation=rotation))
            if t1 < 150:
                w = int(min(max(t1 - 50, 0), 1) * (t1 * 0.3 + 10) + max(t1 - 50, 0) * 0.25)
                if w:
                    l2.append(Layer(Lines(self.generate_heart2(width=w, height=w, type=2),
                                          QPen(QColor(210 + t1 % 30, 50 + t1 % 50, 100 + t1 % 30, 150 - t1 * 1),
                                               2)),
                                    translation=translation, rotation=rotation))
            if t1 < 180:
                w = int(min(max(t1 - 50, 0), 1) * (t1 * 0.3 + 10) + max(t1 - 50, 0) * 0.2)
                if w:
                    l3.append(Layer(Lines(self.generate_heart2(width=w, height=w, type=1),
                                          QPen(QColor(200 + t1 % 30, 100 - t1 % 30, 100 + t1 % 30, 50 - t1 * 0.25), 2)),
                                    translation=translation, rotation=rotation))
                next_bh.append(tp)
        self.shapes.extend(l3)
        self.shapes.extend(l2)
        self.shapes.extend(l1)
        self.button_heart = next_bh
        self.repaint()

    @Slot()
    def end(self):
        a = QPropertyAnimation(self, b"windowOpacity", self)
        a.setStartValue(1)
        a.setDuration(3000)
        a.setEndValue(0)

        c = QPropertyAnimation(self, b"close_count_down", self)
        c.setStartValue(3)
        c.setDuration(3000)
        c.setEndValue(0)

        g = QParallelAnimationGroup(self)
        g.addAnimation(a)
        g.addAnimation(c)
        g.start()

    def heart1_line(self, x, x_range, phase):
        """心形线方程
        xrange指的是x的取值范围
        phase 相位，产生动画效果"""
        x = ((x - x_range / 2) / x_range) * 4
        y = abs(x) ** (2 / 3) + math.exp(1) / 3 * (cmath.sqrt(math.pi - x ** 2).real) * math.sin(phase * math.pi * x)
        return -y.real

    def generate_heart1_line(self, width=None, height=None, phase=None):
        if not width:
            width = self.width()
        if not height:
            height = self.height()
        if not phase:
            phase = 0
        heart_lines = []
        w = width // 2
        prex = 0
        prey = self.heart1_line(prex, width, phase) / 5 * height + height * 3 / 5
        for x in range(2, width):
            y = self.heart1_line(x, width, phase) / 5 * height + height * 3 / 5
            heart_lines.append(QLine(prex - w, prey, x - w, y))
            prex = x
            prey = y
        return heart_lines

    def heart2_line_top(self, x, x_range):
        """上半部分"""
        x = ((x - x_range / 2) / x_range) * 4
        y = cmath.sqrt(2 * cmath.sqrt(x ** 2) - x ** 2)
        return -y.real

    def heart2_line_bottom1(self, x, x_range):
        """下半部分"""
        x = ((x - x_range / 2) / x_range) * 4
        y = -2.14 * cmath.sqrt(math.sqrt(2) - math.sqrt(abs(x)))
        return -y.real

    def heart2_line_bottom2(self, x, x_range):
        """第二种下半部分"""
        x = ((x - x_range / 2) / x_range) * 4
        y = cmath.asin(abs(x) - 1) - math.pi / 2
        return -y.real

    def generate_heart2(self, width=None, height=None, type=1):
        if not width:
            width = self.width()
        if not height:
            height = self.height()
        heart_lines = []
        w = width // 2
        h = height // 2
        prex = 0
        heart2_line_bottom = self.heart2_line_bottom1 if type == 1 else self.heart2_line_bottom2
        prey_top = self.heart2_line_top(prex, width) / 4 * height + height / 4
        prey_bottom = heart2_line_bottom(prex, width) / 4 * height + height / 4
        for x in range(1, width):
            y_top = self.heart2_line_top(x, width) / 4 * height + height / 4
            y_bottom = heart2_line_bottom(x, width) / 4 * height + height / 4
            heart_lines.append(QLine(prex - w, prey_top - h, prex - w, prey_bottom - h))
            prex = x
            prey_bottom = y_bottom
            prey_top = y_top
        return heart_lines

    def generate_ray(self, num=20, radius=100, interpect_range=(0.1, 1), angel_range=(0, 360), phase=0):
        lines = []
        for r in range(int(angel_range[0]), int(angel_range[1]),
                       int((int(angel_range[1]) - int(angel_range[0])) / num)):
            r = (r + phase) / 360 * math.pi * 2
            xs = radius * math.sin(r) * interpect_range[0]
            ys = radius * math.cos(r) * interpect_range[0]
            xe = radius * math.sin(r) * interpect_range[1]
            ye = radius * math.cos(r) * interpect_range[1]
            lines.append(QLine(xs, ys, xe, ye))
        return lines

    def generate_persepective_ray(self, num=10, radius=100, intercept=(0.01, 1)):
        """透视线"""
        lines = []
        x1 = radius ** 2 / (intercept[0] * radius + radius)  # 简化版 intercept[0]不等于0
        x2 = radius ** 2 / (intercept[1] * radius + radius)  # 简化版 intercept[0]不等于0
        for i in range(num):
            yn1 = x1 * i / num
            yn2 = x2 * i / num
            lines.append(QLine(x1, -yn1, x2, -yn2))
            lines.append(QLine(x1, yn1, x2, yn2))
            lines.append(QLine(-x1, yn1, -x2, yn2))
            lines.append(QLine(-x1, -yn1, -x2, -yn2))
        return lines

    def generate_persepective_polygons(self, num=10, radius=100, intercept=(0.01, 1)):
        """透视线"""
        polygons = []
        x1 = radius ** 2 / (intercept[0] * radius + radius)  # 简化版 intercept[0]不等于0
        x2 = radius ** 2 / (intercept[1] * radius + radius)  # 简化版 intercept[0]不等于0
        for i in range(num):
            yn1 = x1 * i / num
            yn2 = x2 * i / num
            polygons.append(QPolygon([QPoint(x1, yn1), QPoint(x1, 0), QPoint(x2, 0), QPoint(x2, yn2)]))
            polygons.append(QPolygon([QPoint(x1, -yn1), QPoint(x1, 0), QPoint(x2, 0), QPoint(x2, -yn2)]))
            polygons.append(QPolygon([QPoint(-x1, -yn1), QPoint(-x1, 0), QPoint(-x2, 0), QPoint(-x2, -yn2)]))
            polygons.append(QPolygon([QPoint(-x1, yn1), QPoint(-x1, 0), QPoint(-x2, 0), QPoint(-x2, yn2)]))
        return polygons

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.button_heart.append((self.offset, event.position(), 0))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() & Qt.LeftButton:
            if self.button_heart:
                l = self.button_heart[-1]
                if self.offset - l[0] > 1 and math.sqrt(
                        (l[1].x() - event.position().x()) ** 2 + (l[1].y() - event.position().y()) ** 2) > 3:
                    x = event.position().x() - l[1].x()
                    if x == 0:
                        rotation = 90
                    elif x > 0:
                        rotation = math.atan(
                            (event.position().y() - l[1].y()) / (event.position().x() - l[1].x())) / math.pi * 180 + 90
                    else:
                        rotation = math.atan(
                            (event.position().y() - l[1].y()) / (event.position().x() - l[1].x())) / math.pi * 180 + 270
                    self.button_heart.append((self.offset, event.position(), rotation))
            else:
                self.button_heart.append((self.offset, event.position(), 0))
        super().mouseMoveEvent(event)

    def paintEvent(self, event) -> None:
        super(Heart, self).paintEvent(event)
        p = QPainter(self)
        g = QLinearGradient(QPoint(self.width() / 2, 0), QPoint(self.width() / 2, self.width() / 2))
        g.setColorAt(0.1, QColor(0, 0, 0, 210))
        g.setColorAt(0.45, QColor(5, 0, 5, 170))
        g.setColorAt(0.49, QColor(50, 50, 50, 150))
        g.setColorAt(0.51, QColor(50, 50, 50, 150))
        g.setColorAt(0.65, QColor(5, 0, 5, 170))
        g.setColorAt(0.9, QColor(0, 0, 0, 210))
        p.fillRect(QRect(0, 0, self.width(), self.height()), g)
        for shape in self.shapes:
            content = shape.content
            if content:
                p.save()
                p.setCompositionMode(shape.mode)
                p.translate(*shape.translation)
                p.rotate(shape.rotation)
                match shape.content:
                    case Lines():
                        if shape.content.pen and content:
                            p.setPen(content.pen)
                            p.drawLines(content.lines)
                    case Polygons():
                        if shape.content.pen:
                            p.setPen(shape.content.pen)
                            if shape.content.fill:
                                p.setBrush(shape.content.fill)
                            p.drawPath(shape.content.painter_path)
                        elif shape.content.fill:
                            p.setBrush(shape.content.fill)
                            p.drawPath(shape.content.painter_path)
                        else:
                            pass
                    case Text():
                        if shape.content.texts and shape.content.pen:
                            p.setPen(shape.content.pen)
                            if shape.content.font:
                                p.setFont(shape.content.font)
                            p.drawText(*shape.content.texts)

                p.restore()


def main():
    app = QApplication(sys.argv)
    heart = Heart()
    heart.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
# nuitka --standalone --output-dir=E:\缓存\nuiktaoutput\heart --windows-disable-console  --windows-icon-from-ico=F:\Work\coding\Box\apps\ins_job\love.ico   --windows-company-name=阿莫莫    --windows-product-name=爱心  --windows-file-version=1 --plugin-enable=pyside6  --windows-product-version=1  --windows-file-description=阿莫莫的爱心表白 --onefile F:\Work\coding\Box\apps\ins_job\heart.py
# --show-progress --show-memory
