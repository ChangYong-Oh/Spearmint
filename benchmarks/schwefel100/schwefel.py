import math


def schwefel(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    result = 418.9829
    for ii in range(d):
        xi = xx[ii] * 500.0
        new = xi * math.sin(abs(xi) ** 0.5) / d
        result -= new

    print('Result = %f' % result)

    return result


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return schwefel(params)
