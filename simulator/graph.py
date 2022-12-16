import framebuf


class Graph(framebuf.FrameBuffer):
    def __init__(self, width: int, height: int):
        self._height = height
        super(Graph, self).__init__(bytearray(width * height), width, height, framebuf.MONO_VLSB)
        self.fill(0)

    @property
    def center(self) -> float:
        return self._height / 2

    @property
    def height(self) -> int:
        return self._height

    def barplot(self, v: float, limits=None):
        assert -1 <= v <= 1, f"Out of band value {v} (-1..1)"

        self.scroll(1, 0)
        # plot point
        # scroll may leave a footprint of the previous colors in the FrameBuffer, keep the first line empty
        self.line(1, int(self.center), 1, int(self.center - v * self.center), 1)

    def pointplot(self, v: float):
        assert -1 <= v <= 1, f"Out of band value {v} (-1..1)"

        self.scroll(1, 0)
        # plot point
        # scroll may leave a footprint of the previous colors in the FrameBuffer, keep the first line empty
        self.pixel(1, int(self.center - v * self.center), 1)
