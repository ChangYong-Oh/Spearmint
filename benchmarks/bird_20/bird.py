import math


def bird(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    n_repeat = d / 2
    sum_ = 0
    for ii in range(n_repeat):
        xi0 = xx[2 * ii] * 2 * math.pi
        xi1 = xx[2 * ii + 1] * 2 * math.pi
        new = (xi0 - xi1) ** 2 + math.exp((1 - math.sin(xi0)) ** 2) * math.cos(xi1) + math.exp((1 - math.cos(xi1)) ** 2) * math.sin(xi0)
        sum_ += new
    sum_ /= float(n_repeat)

    return sum_


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return bird(params)
