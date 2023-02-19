import string

import pygame
import tkinter as tk
import random
import math
import sys
from math import sin, cos, pi, log
from tkinter import *
#流星和烟花
# 屏幕大小
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT=500

NUM_METEORS = 10
MAX_SPEED = 10
MAX_LENGTH = 80
MIN_LENGTH = 40

# 颜色列表
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# 初始化pygame
pygame.init()

# 创建屏幕
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Fireworks")

background_image = pygame.image.load("../集合demo.png")
background_image = pygame.transform.scale(background_image, (700, 400))

#病名为爱
font_size_min = 5  # 字体大小最小值
font_size_max = 40  # 字体大小最大值
font = pygame.font.Font(None, 30)  # 默认字体

# 存储已放置的文本及其位置
placed_texts = []

def ill_love(content, color):
    global screen, placed_texts

    # 颜色列表
    COLORS = [color]  # 使用传入的颜色

    def place_text():
        if not placed_texts or len(placed_texts) <100:  # 限制文本数量
            # 随机生成文本位置和大小
            size = random.randint(font_size_min, font_size_max)
            # print(size)
            #添加字体
            # font_path = 'D:\流血英文.ttf'  # 替换为你的字体文件路径
            font = pygame.font.Font("D:\ZiBanZhuanTiv1.0\ZiBanZhuanTiv1.0\miaozi-mianbaoti-2.ttf", size)


            text_surface = font.render(content, True, random.choice(COLORS))

            text_rect = text_surface.get_rect()
            text_rect.x = random.randint(0, DISPLAY_WIDTH - text_rect.width)
            text_rect.y = random.randint(0, DISPLAY_HEIGHT - text_rect.height)

            # # 检查是否重叠
            # for font, text_surface, text_rect_check in placed_texts:
            #     if text_rect.colliderect(text_rect_check):
            #         return place_text()  # 如果重叠，则重新尝试放置

            # 将文本添加到列表中
            placed_texts.append((font, text_surface, text_rect))

            # 每0.5秒尝试放置一个新文本
            pygame.time.set_timer(pygame.USEREVENT, 500)
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))

    def game_loop():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                place_text()

        # 绘制文本
        for font, text_surface, text_rect in placed_texts:
            screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(10)

    place_text()
    while True:
        game_loop()

# 调用函数




class Meteor:
    def __init__(self):
        self.x = random.randint(0,DISPLAY_WIDTH)
        self.y = random.randint(-DISPLAY_HEIGHT, 0)
        self.speed = random.randint(1, MAX_SPEED)
        self.length = random.randint(MIN_LENGTH, MAX_LENGTH)

    def draw(self, surface):
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (self.x - self.length, self.y + self.length))

    def update(self):
        self.x -= self.speed
        self.y += self.speed

        if self.x < -self.length or self.y > DISPLAY_HEIGHT + self.length:
            self.__init__()


# 创建流星
meteors = []
for i in range(NUM_METEORS):
    meteors.append(Meteor())

class Trail:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(1, 5)
        self.lifetime = random.randint(30, 60)

    def update(self):
        self.pos += self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 2)

class Particle:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.trails = []
        self.explode()

    def explode(self):
        for _ in range(100):
            color = random.choice(COLORS)
            trail = Trail(self.pos.x, self.pos.y, color)
            self.trails.append(trail)

    def update(self):
        for trail in self.trails:
            trail.update()
            if trail.lifetime <= 0:
                self.trails.remove(trail)

    def draw(self, screen):
        for trail in self.trails:
            trail.draw(screen)

# 创造流星的函数
def create_meteor():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))

        for meteor in meteors:
            meteor.update()
            meteor.draw(screen)

        pygame.display.flip()
        clock.tick(40)

    pygame.quit()


def create_fireworks():
    fireworks = []
    # meteor = Meteor()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
            if len(firework.trails) == 0:
                fireworks.remove(firework)

        # 以一定概率生成新的烟花
        if random.randint(0, 100) < 5:
            fireworks.append(Particle(random.randint(0, DISPLAY_WIDTH), DISPLAY_HEIGHT))

        pygame.display.flip()
        clock.tick(40)

    pygame.quit()




def run_game():
    fireworks = []
    # meteor = Meteor()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))  # 绘制背景图片
        for meteor in meteors:
            meteor.update()
            meteor.draw(screen)

        for firework in fireworks:
            firework.update()
            firework.draw(screen)
            if len(firework.trails) == 0:
                fireworks.remove(firework)

        # 以一定概率生成新的烟花
        if random.randint(0, 100) < 5:
            fireworks.append(Particle(random.randint(0, DISPLAY_WIDTH), DISPLAY_HEIGHT))

        pygame.display.flip()
        clock.tick(40)

    pygame.quit()


CANVAS_WIDTH = 840  # 画布的宽
CANVAS_HEIGHT = 680  # 画布的高
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # 画布中心的X轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # 画布中心的Y轴坐标
IMAGE_ENLARGE = 11  # 放大比例

HEART_COLOR = "#EEAEEE"  # 引号内修改颜色！颜色代码放在文章末尾

root=Tk()
canvas=Canvas(root,bg='black',height=CANVAS_HEIGHT,width=CANVAS_WIDTH)
canvas.pack()
font = ("D:\ZiBanZhuanTiv1.0\ZiBanZhuanTiv1.0\miaozi-mianbaoti-2.ttf", 30)

def draw_text_at_center(canvas, x, y, color, text):
    """
    在给定的x, y坐标为中心以指定的颜色绘制指定的文本到Canvas上。
    :param canvas: Tkinter的Canvas对象
    :param x: 文本中心的X坐标
    :param y: 文本中心的Y坐标
    :param color: 文本颜色，格式为颜色名称或'#RRGGBB'字符串
    :param text: 要绘制的文本内容
    """
    # 设置字体和大小
    font = ("D:\ZiBanZhuanTiv1.0\ZiBanZhuanTiv1.0\miaozi-mianbaoti-2.ttf", 36)  # 你可以选择一个合适的字体和大小

    # 计算文本在Canvas中的位置，使其以给定的x, y为中心
    canvas.create_text(x, y, text=text, fill=color, font=font, anchor="center")

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    “爱心函数生成器”
    :param shrink_ratio: 放大比例
    :param t: 参数
    :return: 坐标
    """
    # 基础函数
    x = 17 * (sin(t) ** 3)
    y = -(16 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(3 * t))

    # 放大
    # x *= shrink_ratio
    # y *= shrink_ratio
    x *= IMAGE_ENLARGE
    y *= IMAGE_ENLARGE
    # 移到画布中央
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """
    随机内部扩散
    :param x: 原x
    :param y: 原y
    :param beta: 强度
    :return: 新坐标
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def shrink(x, y, ratio):
    """
    抖动
    :param x: 原x
    :param y: 原y
    :param ratio: 比例
    :return: 新坐标
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)  # 这个参数...
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """
    自定义曲线函数，调整跳动周期
    :param p: 参数
    :return: 正弦
    """
    # 可以尝试换其他的动态函数，达到更有力量的效果（贝塞尔？）
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:
    """
    爱心类
    """

    def __init__(self, generate_frame=20):
        self._points = set()  # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散效果点坐标集合
        self._center_diffusion_points = set()  # 中心扩散效果点坐标集合
        self.all_points = {}  # 每帧动态点坐标
        self.build(2000)

        self.random_halo = 1000

        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # 爱心
        for _ in range(number):
            t = random.uniform(0, 2 * pi)  # 随机不到的地方造成爱心有缺口
            x, y = heart_function(t)
            self._points.add((x, y))

        # 爱心内扩散
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        # 爱心内再次扩散
        point_list = list(self._points)
        for _ in range(10000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.27)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        # 调整缩放比例
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.420)  # 魔法参数

        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)

        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 15 * curve(generate_frame / 10 * pi)  # 圆滑的周期的缩放比例

        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []

        # 光环
        heart_halo_point = set()  # 光环的点坐标集合
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)  # 随机不到的地方造成爱心有缺口
            x, y = heart_function(t, shrink_ratio=-15)  # 魔法参数
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                # 处理新的点
                heart_halo_point.add((x, y))
                x += random.randint(-60, 60)
                y += random.randint(-60, 60)
                size = random.choice((1, 1, 2))
                all_points.append((x, y, size))
                all_points.append((x + 20, y + 20, size))
                all_points.append((x - 20, y - 20, size))
                all_points.append((x + 20, y - 20, size))
                all_points.append((x - 20, y + 20, size))

        # 轮廓
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        #内容
        for x,y in self._edge_diffusion_points:
            x,y=self.calc_position(x,y,ratio)
            size=random.randint(1,2)
            all_points.append((x,y,size))

        for x,y in self._center_diffusion_points:
            x,y=self.calc_position(x,y,ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame]=all_points

    def render(self,render_canvas,render_frame):
        for x,y,size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x,y,x+size,y+size,width=0,fill=HEART_COLOR)

def draw(main:Tk,render_canvas:Canvas,render_heart:Heart,content,color,render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas,render_frame)
    canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text=content, fill=color, font=font, anchor="center")
    main.after(1,draw,main,render_canvas,render_heart,content,color,render_frame+1)

def dreaw_heart(content,color):
    heart = Heart()
    # canvas.create_text(CANVAS_CENTER_X, CANVAS_CENTER_Y, text="王亮", fill="red", font=font, anchor="center")
    draw(root, canvas, heart,content,color)

    root.mainloop()


if __name__ == '__main__':
    ill_love("爱你", (255, 0, 0))  # 红色文本
    # create_meteor()
    # create_fireworks()
    # dreaw_heart("张舒婷","green")