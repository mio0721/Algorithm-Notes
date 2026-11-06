# 轨迹规划基础
# Python 3；直接运行文件，修改示例数据可继续练习。
# 先给出起终位置、速度和加速度要求。

import math

# 对满足静止边界条件的五次多项式采样，返回时间、位置、速度、加速度。
def quintic_trajectory(distance, duration, steps=40):
    if duration <= 0 or steps < 1:
        # 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
        raise ValueError('总时间和采样步数必须为正')
    result = []
    for i in range(steps + 1):
        # 把物理时间转换为0到1的归一化时间；求导后仍需除以实际时长。
        tau = i / steps
        position = distance * (10 * tau ** 3 - 15 * tau ** 4 + 6 * tau ** 5)
        # 一次时间导数带1/T，得到米每秒。
        velocity = distance / duration * (30 * tau ** 2 - 60 * tau ** 3 + 30 * tau ** 4)
        # 二次时间导数带1/T²，得到米每二次方秒。
        acceleration = distance / duration ** 2 * (60 * tau - 180 * tau ** 2 + 120 * tau ** 3)
        result.append((duration * tau, position, velocity, acceleration))
    return result

# 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
def main():
    # 二次时间导数带1/T²，得到米每二次方秒。
    distance, max_velocity, max_acceleration = (10, 2, 1)
    duration = max(15 / 8 * abs(distance) / max_velocity, math.sqrt(10 * math.sqrt(3) / 3 * abs(distance) / max_acceleration))
    # 输出计算结果，便于与课程例子或自行推演的答案核对。
    print('T:', duration)
    print('t,s,v,a')
    for row in quintic_trajectory(distance, duration):
        print(','.join((f'{value:.6f}' for value in row)))
if __name__ == '__main__':
    main()
