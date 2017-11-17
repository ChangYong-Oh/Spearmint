import sys
import time
import os.path
import subprocess
from datetime import datetime
from shutil import copy
import numpy as np


def run_spearmint(exp_path, n_eval, grid_shift=False):
	folder_name = os.path.abspath(exp_path)
	func_name = ''.join([c for c in os.path.split(folder_name)[1] if not c.isdigit()])
	exp_type = os.path.split(folder_name)[1]
	tag = datetime.now().strftime('%Y%m%d-%H:%M:%S:%f')
	exp_dir = os.path.join(folder_name, exp_type + '_' + tag)
	if not os.path.exists(exp_dir):
		os.makedirs(exp_dir)
	if not os.path.exists(os.path.join(exp_dir, 'config.json')):
		copy(os.path.join(folder_name, 'config.json'), os.path.join(exp_dir, 'config.json'))
	if not os.path.exists(os.path.join(exp_dir, func_name + '.py')):
		copy(os.path.join(folder_name, func_name + '.py'), os.path.join(exp_dir, func_name + '.py'))

	logfile_name = open(os.path.join(exp_dir, exp_type + '_' + tag + '.log'), 'w')
	cmd_str = 'python ./spearmint/main.py ' + exp_dir + ' --evals ' + str(n_eval)
	if grid_shift:
		cmd_str += ' --gridseed ' + str(np.random.randint(0, 20000))
	process = subprocess.Popen(cmd_str, shell=True, stdout=logfile_name, stderr=logfile_name)
	return process


def run_spearmint_multiple(benchmarks_root_dir, exp_list, n_eval_list, grid_shift=False):
	benchmarks_root_dir = os.path.realpath(benchmarks_root_dir)
	n_exp = len(exp_list)
	assert n_exp == len(n_eval_list)
	if n_exp > 6:
		print('Assuming 32 cores, running more than 6 spearmint may cause frequent context switching')
		exit()
	dbpath_tag = datetime.now().strftime('%Y%m%d-%H:%M:%S:%f')
	dbpath_tag += '_' + '-'.join([exp_list[i] + '[' + str(n_eval_list[i]) + ']' for i in range(n_exp)])
	dbpath = os.path.join(os.path.split(benchmarks_root_dir)[0], 'mongodb', dbpath_tag)
	if not os.path.exists(dbpath):
		os.makedirs(dbpath)
	mongodb_logfile_name = os.path.join(dbpath, 'mongodb.log')
	cmd_str = 'mongod --fork --logpath ' + mongodb_logfile_name + ' --dbpath ' + dbpath
	if '/var/scratch/' in os.path.realpath(__file__):
		cmd_str = '/var/scratch/coh/mongodb/mongodb-linux-x86_64-3.4.10/bin/' + cmd_str
	os.system(cmd_str)

	exp_path_list = [os.path.join(benchmarks_root_dir, elm) for elm in exp_list]
	process_list = []
	for exp_path, n_eval in zip(exp_path_list, n_eval_list):
		process_list.append(run_spearmint(exp_path, n_eval, grid_shift))
	n_running = n_exp
	while n_running > 0:
		time.sleep(60)
		running = [elm.poll() is None for elm in process_list]
		n_running = running.count(True)
		print('%d/%d is still running %s' % (n_running, n_exp, time.strftime("%H:%M:%S")))
		for e in range(n_exp):
			if running[e]:
				print('    %s' % exp_path_list[e])
	cmd_str = 'mongod --shutdown --dbpath ' + dbpath
	if '/var/scratch/' in os.path.realpath(__file__):
		cmd_str = '/var/scratch/coh/mongodb/mongodb-linux-x86_64-3.4.10/bin/' + cmd_str
	os.system(cmd_str)


if __name__ == '__main__':
	exp_list = []
	n_eval_list = []
	for i in range(2, len(sys.argv), 2):
		exp_list.append(sys.argv[i])
		n_eval_list.append(int(sys.argv[i + 1]))
	run_spearmint_multiple(sys.argv[1], exp_list, n_eval_list, sys.argv[-1] == '--grid_shift')
