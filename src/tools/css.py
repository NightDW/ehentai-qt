import re

from PySide6.QtGui import QPixmap


class SubSprite:
    __urlRe = re.compile(r'url\((.*)\)')
    __leftTopRe = re.compile(r'(-?[0-9]+)(px)? (-?[0-9]+)(px)?')
    __widthRe = re.compile(r'width\s*:\s*([0-9]+)(px)?')
    __heightRe = re.compile(r'height\s*:\s*([0-9]+)(px)?')
    __paramName = "sub.sprite"

    def __init__(self, url: str, left: int, top: int, width: int, height: int):
        """
        CSS精灵子图配置（即精灵图中的其中一张小图片）
        """
        self.url: str = url
        self.left: int = left
        self.top: int = top
        self.width: int = width
        self.height: int = height

    def toUrl(self) -> str:
        """
        将所有信息拼接成一个url；将top等参数作为请求参数进行传递（方便程序内透传）
        """
        sep = '?' if self.url.find('?') < 0 else '&'
        return f'{self.url}{sep}{SubSprite.__paramName}={self.left}_{self.top}_{self.width}_{self.height}'

    def cut(self, fullPic: QPixmap) -> QPixmap:
        if not self.width or not self.height:
            return fullPic
        return fullPic.copy(-self.left, -self.top, self.width, self.height)

    @staticmethod
    def parseByUrl(url: str) -> 'SubSprite':
        left, top, width, height = 0, 0, 0, 0

        idx = url.find('?')
        if idx >= 0:
            for kv in url[idx+1:].split('&'):
                k, v = kv.split('=')
                if k == SubSprite.__paramName:
                    l, t, w, h = v.split('_')
                    left, top, width, height = int(l), int(t), int(w), int(h)
                    break
            url = url[0:idx]

        return SubSprite(url, left, top, width, height)

    @staticmethod
    def parseByStyle(style: str) -> 'SubSprite':
        url = SubSprite.__urlRe.search(style).group(1)
        ltm = SubSprite.__leftTopRe.search(style)
        width = int(SubSprite.__widthRe.search(style).group(1))
        height = int(SubSprite.__heightRe.search(style).group(1))
        return SubSprite(url, int(ltm.group(1)), int(ltm.group(3)), width, height)
