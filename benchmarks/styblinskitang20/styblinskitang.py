def styblinskitang(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    result = 0
    for ii in range(d):
        xi = xx[ii]
        new = 312.5 * xi ** 4 - 200.0 * xi ** 2 + 12.5 * xi
        result += new

    result /= float(d)

    print('Result = %f' % result)

    return result


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return styblinskitang(params)
