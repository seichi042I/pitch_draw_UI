from concurrent.futures import ProcessPoolExecutor
import time


def func_1():
    for i in range(2):
        time.sleep(3)
        print('func_1：{}回目'.format(i+1))


def func_2(bro_1, bro_2):
    for i in range(2):
        time.sleep(2)
        print('func_2：{}回目　兄：{}　弟：{}'.format(i+1, bro_1, bro_2))


if __name__ == '__main__':
    print('開始')
    with ProcessPoolExecutor() as executor:
        executor.submit(func_1)
        executor.submit(func_2, 'マリオ', 'ルイージ')# 関数に引数がある場合は左記のように渡す
    print('終了')