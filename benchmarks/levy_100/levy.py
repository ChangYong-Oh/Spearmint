import math


def levy(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    xi = (xx[0] * 10.0 - 1.0) / 4.0 + 1.0
    result = math.sin(math.pi * xi) ** 2.0
    for ii in range(d - 1):
        xi = (xx[ii] * 10.0 - 1.0) / 4.0 + 1.0
        new = (xi - 1.0) ** 2 * (1.0 + 10.0 * math.sin(math.pi * xi + 1.0) ** 2.0)
        result += new
    xi = (xx[d - 1] * 10.0 - 1.0) / 4.0 + 1.0
    new = (xi - 1.0) ** 2 * (1.0 + math.sin(2.0 * math.pi * xi) ** 2.0)
    result += new

    print('Result = %f' % result)

    return result


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return levy(params)
