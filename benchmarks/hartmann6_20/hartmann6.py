import numpy as np


def hartmann6(params):
    xx = []
    for i in range(1, len(params.keys()) + 1):
        xx.append(float(params['x' + str(i)]))

    alpha = np.array([1.0, 1.2, 3.0, 3.2])
    a = np.array([[10.0, 3.00, 17.0, 3.50, 1.70, 8.00],
                  [0.05, 10.0, 17.0, 0.10, 8.00, 14.0],
                  [3.00, 3.50, 1.70, 10.0, 17.0, 8.00],
                  [17.0, 8.00, 0.05, 10.0, 0.10, 14.0]])
    p = np.array([[0.1312, 0.1696, 0.5569, 0.0124, 0.8283, 0.5886],
                  [0.2329, 0.4135, 0.8307, 0.3736, 0.1004, 0.9991],
                  [0.2348, 0.1451, 0.3522, 0.2883, 0.3047, 0.6650],
                  [0.4047, 0.8828, 0.8732, 0.5743, 0.1091, 0.0381]])

    d = len(xx)
    n_repeat = d / 6
    sum_ = 0
    for ii in range(n_repeat):
        xi0 = (xx[6 * ii + 0] + 1) * 0.5
        xi1 = (xx[6 * ii + 1] + 1) * 0.5
        xi2 = (xx[6 * ii + 2] + 1) * 0.5
        xi3 = (xx[6 * ii + 3] + 1) * 0.5
        xi4 = (xx[6 * ii + 4] + 1) * 0.5
        xi5 = (xx[6 * ii + 5] + 1) * 0.5
        s = 0
        for i in [0, 1, 2, 3]:
            sm = a[i, 0] * (xi0 - p[i, 0]) ** 2
            sm += a[i, 1] * (xi1 - p[i, 1]) ** 2
            sm += a[i, 2] * (xi2 - p[i, 2]) ** 2
            sm += a[i, 3] * (xi3 - p[i, 3]) ** 2
            sm += a[i, 4] * (xi4 - p[i, 4]) ** 2
            sm += a[i, 5] * (xi5 - p[i, 5]) ** 2
            s += -alpha[i] * np.exp(-sm)
        sum_ += s
    sum_ /= float(n_repeat)

    return sum_


def main(job_id, params):
    print('Anything printed here will end up in the output directory for job #%d' % job_id)
    print(params)
    return hartmann6(params)
