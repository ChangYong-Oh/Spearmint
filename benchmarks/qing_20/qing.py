import math


def qing(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    sum_ = 0
    for ii in range(d):
        xi = xx[ii] * 500.0
        new = (xi ** 2 - (ii + 1)) ** 2
        sum_ += new
    sum_ /= float(d)

    return sum_


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return qing(params)
