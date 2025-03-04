from random import randrange, shuffle
import unittest
import sys
import argparse


def rsample(stream, size=10):
    """
    Produce a simple random sample with `size` elements from `stream`
    using reservoir sampling, without collecting stream into memory
    """
    reservoir = []  # 初始化 reservoir 为空，用于存储随机取样的数字
    """
    蓄水池抽样法的步骤是：
    1.首先将前k个元素放入蓄水池（reservoir）中。
    2.对于第i个元素（i从k+1开始到N），生成一个随机数j，范围是0到i。如果j小于k，就用第i个元素替换蓄水池中的第j个元素。
    3.打乱蓄水池中的数字
    4.最终蓄水池中的k个元素就是所需的样本。
    
    假如你输入的数字是1，2，3，4，5，6，7，8，9，现在要从中抽4个，步骤如下：
    
    放入前四个数字，reservoir状态为：1，2，3，4
    
    轮到5，随机生成一个数字，若生成2，则将reservoir中第二个数字替换掉，reservoir状态为：1，5，3，4
    轮到6，随机生成一个数字，若生成1，则将reservoir中第一个数字替换掉，reservoir状态为：6，5，3，4
    
    轮到7，随机生成一个数字，若生成5，由于5大于四，将7加入reservoir，reservoir状态为：1，5，3，4，7
    
    轮到8，随机生成一个数字，若生成3，则将reservoir中第三个数字替换掉，reservoir状态为：1，5，8，4，7
    
    轮到9，随机生成一个数字，若生成6，由于6大于四，将9加入reservoir，reservoir状态为：1，5，3，4，7，9
    
    打乱reservoir中数字顺序，reservoir状态为：5，1，3，4，9，7
    取前四个作为抽样结果，即5，1，3，4
    """

    for i, item in enumerate(stream):  # 遍历输入流，逐个处理，防止数据过大，避免内存溢出
        if i < size:
            reservoir.append(item)  # 将前K个元素放入reservoir中
        else:
            j = randrange(0, i + 1)  # 生成随机数，范围是0到i+1
            if j < size:  # 如果随机数小于K，则替换reservoir中的对应元素
                reservoir[j] = item
    # 打乱结果以确保当size等于数据流长度时顺序不同
    shuffle(reservoir)
    return reservoir[:size]  # 返回随机取样的结果


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=10, help='Sample size')
    args = parser.parse_args()
    size = args.n

    # 从标准输入读取数据流，逐行处理
    sample = rsample(sys.stdin, size)
    for item in sample:
        print(item, end='')


class rsampleTest(unittest.TestCase):

    def test_defaults(self):
        g = (i ** 2 for i in range(20))
        s = rsample(g)
        self.assertEqual(len(s), 10)

    def test_too_small_input(self):
        d = range(5)
        s = rsample(d)
        self.assertEqual(set(s), set(d))

    def test_string(self):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        s = rsample(letters, 26)
        self.assertEqual(set(s), set(letters))

    def test_permutation(self):
        n = 100
        d = range(n)
        s = rsample(d, n)
        self.assertEqual(len(s), n)
        self.assertNotEqual(s, list(d))

    def test_not_begin(self):
        n = int(1e6)
        d = range(n)
        s = rsample(d)
        self.assertTrue(1000 < max(s))

    def test_not_end(self):
        n = int(1e6)
        d = range(n)
        s = rsample(d)
        self.assertTrue(min(s) < (n - 1000))
