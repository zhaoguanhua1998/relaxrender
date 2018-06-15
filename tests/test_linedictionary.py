from relaxrender.LineDictionary import LineDictionary
import unittest


class TestLineDictionary(unittest.TestCase):
    #  测试对象的初始化工作
    def setUp(self):
        self.dim = 10
        self.angle = 45
        self.LineDictionary = LineDictionary()

    def test_create_kernel(self):
        self.LineDictionary.create_kernel(dim=self.dim, angle=self.angle)


def runTest():
    if __name__ == "__main__":
        unittest.main()


runTest()
