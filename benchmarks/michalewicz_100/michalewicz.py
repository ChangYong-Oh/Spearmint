import math


def michalewicz(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    m = 10.0

    d = len(xx)
    result = 0
    for ii in range(d):
        xi = (xx[ii] + 1) * 0.5 * math.pi
        i = ii + 1
        new = math.sin(xi) * math.pow((math.sin(i * math.pow(xi, 2) / math.pi)), (2 * m))
        result += new
    result /= float(d)
    print('Result = %f' % -result)

    return -result


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return michalewicz(params)
