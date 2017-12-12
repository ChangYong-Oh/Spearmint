import numpy as np


def generate_orthogonal_matrix(ndim):
    x = np.exp(np.sin(np.linspace(-ndim ** 0.5, ndim ** 0.5, ndim)))
    x_repeated = np.tile(x, (ndim, 1))
    gram_mat = np.exp(-(x_repeated - x_repeated.T) ** 2)
    return np.linalg.qr(gram_mat, 'complete')[0]


def rotatedstyblinskitang(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    d = len(xx)
    result = 0
    xx = generate_orthogonal_matrix(d).dot(xx)
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
    return rotatedstyblinskitang(params)
