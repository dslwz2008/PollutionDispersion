# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com

from __future__ import division
import math


class Wind(object):
    def __init__(self, speed=0.0, phi=0.0):
        self.speed = speed
        self.phi = phi


class Canyon(object):
    def __init__(self, h_upw, h_downw, width):
        self.h_upw = h_upw
        self.h_downw = h_downw
        self.width = width


class Receptor(object):
    def __init__(self, position):
        # 在街道峡谷中的绝对位置，从背风侧起算，目前是一维
        self.position = position


class Traffic(object):
    def __init__(self, n_veh, speed, single_area):
        self.n_veh = n_veh
        self.speed = speed
        self.single_area = single_area


def trapezoid_shape(canyon):
    l_t = canyon.h_upw  # l_vortex是h_upw的2倍
    l_rec = 2 * l_t  # 假设的循环区下边长度
    l_s1 = l_s2 = 0.5 * math.sqrt(math.pow(canyon.h_upw, 2) + math.pow(0.5 * l_rec, 2))
    ratio = canyon.width / l_rec
    if ratio <= 0.5:
        print('strange canyon shape')
        return None
    h_min = 2 * canyon.h_upw * (l_rec - canyon.width) / l_rec
    if canyon.h_downw < h_min:
        # 先计算出起作用的位置，然后使用该位置计算
        pos = 0.5 * l_rec * canyon.h_downw / canyon.h_upw
        ratio = 1 - pos / l_rec

    if 0.5 < ratio <= 0.75:
        l_s2 = 0
        l_s1 = math.sqrt(math.pow(canyon.h_upw - canyon.h_downw, 2) + math.pow(canyon.width - 0.5 * l_rec, 2))
    elif 0.75 < ratio <= 1:
        # l_s1 = l_s2
        x = (1 - ratio * l_rec) * l_s1 * 4 / l_rec
        l_s2 -= x
    return l_t, l_s1, l_s2


def ospm_main(q, wind, canyon, traffic, receptor):
    # 1.直接排放贡献
    h0 = 2
    u_t = wind.speed
    H = (canyon.h_upw + canyon.h_downw) / 2
    p = min(1, canyon.h_upw / H)
    u_b = u_t * math.log(h0) * (1 - 0.2 * p * math.sin(math.radians(wind.phi))) / math.log(H)

    # 车辆产生的湍流
    alpha = 0.1
    b = 0.3
    lamda = 0.1
    sigma_w0 = b * math.sqrt(traffic.n_veh * traffic.speed * traffic.single_area)
    sigma_w = math.sqrt(math.pow(alpha * u_b, 2) + math.pow(sigma_w0, 2))
    sigma_wt = math.sqrt(math.pow(lamda * u_t, 2) + 0.4 * math.pow(sigma_w0, 2))

    l_vortex = 2 * canyon.h_upw  # 风速小于2m/s时，线性减小，线性因子？
    l_rec = min(canyon.width, l_vortex * math.sin(math.radians(wind.phi)))
    l_max = math.fabs(receptor.position - l_rec) / math.sin(math.radians(wind.phi))
    c_d = math.sqrt(2 / math.pi) * q * math.log((sigma_w * l_max / u_b + h0) / h0) / \
          (sigma_w * canyon.width)

    # 风向与街道轴向夹角很小的时候，背风侧污染物受到循环区外的影响
    if wind.phi < 45 and receptor.position < l_rec:
        r = min(0.5 * u_t, 1)
        R = math.cos(2 * r * math.radians(wind.phi))
        l_max_out = (canyon.width - l_rec) / math.sin(math.radians(wind.phi))
        c_d_out = math.sqrt(2 / math.pi) * q * math.log((sigma_w * l_max_out / u_b + h0) / h0) / \
                  (sigma_w * canyon.width)
        c_d += (R * c_d_out)

    # 2.循环贡献
    l_t, l_s1, l_s2 = trapezoid_shape(canyon)
    c_rec = q * l_rec / canyon.width / (sigma_wt * l_t + u_t * l_s1 + u_b * l_s2)
    return c_d + c_rec


def test1():
    wind = Wind(2.0, 45.0)
    canyon = Canyon(20.0, 20.0, 30.0)
    traffic = Traffic(200, 20.0, 4.0)
    for pos in range(31):
        receptor = Receptor(pos)
        print(ospm_main(5, wind, canyon, traffic, receptor))


if __name__ == '__main__':
    test1()
