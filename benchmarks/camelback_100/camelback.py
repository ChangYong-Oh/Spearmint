import math


def camelback(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    n_repeat = d / 2
    sum_ = 0
    for ii in range(n_repeat):
        xi0 = xx[2 * ii] * 3.0
        xi1 = xx[2 * ii + 1] * 2.0
        new = (4.0 - 2.1 * xi0 ** 2 + xi0 ** 4 / 3.0) * xi0 ** 2 + xi0 * xi1 + 4 * (xi1 ** 2 - 1.0) * xi1 ** 2
        sum_ += new
    sum_ /= float(n_repeat)

    return sum_


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return camelback(params)
