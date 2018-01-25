import sys
import time
import os.path
import subprocess
import pickle
from datetime import datetime
from shutil import copy
import numpy as np


def run_spearmint(exp_dir, n_eval, grid_shift=0):

	exp_dir = os.path.realpath(exp_dir)
	parent_dir = os.path.split(exp_dir)[0]
	func_name = '_'.join((parent_dir.split('/')[-1]).split('_')[:-1])
	if not os.path.exists(exp_dir):
		os.makedirs(exp_dir)
	if not os.path.exists(os.path.join(exp_dir, 'config.json')):
		copy(os.path.join(parent_dir, 'config.json'), os.path.join(exp_dir, 'config.json'))
	if not os.path.exists(os.path.join(exp_dir, func_name + '.py')):
		copy(os.path.join(parent_dir, func_name + '.py'), os.path.join(exp_dir, func_name + '.py'))

	logfile = open(os.path.join(exp_dir, os.path.split(exp_dir)[1] + '.log'), 'w')
	cmd_str = 'python ./spearmint/main.py ' + exp_dir + ' --evals ' + str(n_eval) + ' --gridseed ' + str(grid_shift) + ' --parallel'

	print(cmd_str)

	return
	process = subprocess.Popen(cmd_str, shell=True, stdout=logfile, stderr=logfile)
	return process


if __name__ == '__main__':
	run_spearmint(sys.argv[1], int(sys.argv[2]), np.random.randint(1, 20000))
