import math


def branin(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    a = 1
    b = 5.1 / (4 * math.pi ** 2)
    c = 5.0 / math.pi
    r = 6
    s = 10
    t = 1.0 / (8 * math.pi)

    d = len(xx)
    n_repeat = d / 2
    sum_ = 0
    for ii in range(n_repeat):
        xi0 = xx[2 * ii] * 7.5 + 2.5
        xi1 = xx[2 * ii + 1] * 7.5 + 7.5
        new = a * (xi1 - b * xi0 ** 2 + c * xi0 - r) ** 2 + s * (1 - t) * math.cos(xi0) + s
        sum_ += new
    sum_ /= float(n_repeat)


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return branin(params)
