"""
Generate BPM files with background with degrees
"""
from PIL import Image, ImageDraw, ImageFont


def generate():
    for i in range(-60, 61):
        offset = (0, 15)
        if len(str(i)) == 1:
            offset = (35, 15)
        elif len(str(i)) == 2:
            offset = (17, 15)
        elif len(str(i)) == 3:
            offset = (3, 15)
        if i >= 18:
            color = 'red'
        elif i <= -5:
            color = 'blue'
        else:
            color = 'purple'
        image = Image.new('RGB', (100, 100), color=color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("resources\\arial.ttf", size=65)
        draw.text(offset, str(i), font=font, align='center')
        image.save(f'resources\\{i}.bmp')


if __name__ == '__main__':
    generate()
