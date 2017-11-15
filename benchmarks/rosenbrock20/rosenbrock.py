def rosenbrock(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)

    result = 0
    for ii in range(d - 1):
        xi = xx[ii] * 7.5 + 2.5
        xiplus1 = xx[ii + 1] * 7.5 + 2.5
        new = 100.0 * (xiplus1 - xi ** 2) ** 2 + (xi - 1) ** 2
        result += new

    result *= 50000.0 / ((90 ** 2 + 9 ** 2) * (d - 1))

    print('Result = %f' % result)

    return result


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return rosenbrock(params)
