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
	func_name = ''.join([c for c in os.path.split(parent_dir)[1] if not c.isdigit()])
	if not os.path.exists(exp_dir):
		os.makedirs(exp_dir)
	if not os.path.exists(os.path.join(exp_dir, 'config.json')):
		copy(os.path.join(parent_dir, 'config.json'), os.path.join(exp_dir, 'config.json'))
	if not os.path.exists(os.path.join(exp_dir, func_name + '.py')):
		copy(os.path.join(parent_dir, func_name + '.py'), os.path.join(exp_dir, func_name + '.py'))

	logfile = open(os.path.join(exp_dir, os.path.split(exp_dir)[1] + '.log'), 'w')
	cmd_str = 'python ./spearmint/main.py ' + exp_dir + ' --evals ' + str(n_eval) + ' --gridseed ' + str(grid_shift) + ' --parallel'
	process = subprocess.Popen(cmd_str, shell=True, stdout=logfile, stderr=logfile)
	return process


def run_multiple_init(benchmarks_root_dir, exp_list, n_eval_list):
	benchmarks_root_dir = os.path.realpath(benchmarks_root_dir)
	n_exp = len(exp_list)
	assert n_exp == len(n_eval_list)
	if n_exp > 6:
		print('Assuming 32 cores, running more than 6 spearmint may cause frequent context switching')
		exit()
	dbpath_tag = datetime.now().strftime('%Y%m%d-%H:%M:%S:%f')
	dbpath_tag += '_' + '-'.join([exp_list[i] + '[' + str(n_eval_list[i]) + ']' for i in range(n_exp)])
	dbpath = os.path.relpath(os.path.join(os.path.split(benchmarks_root_dir)[0], 'mongodb', dbpath_tag))

	exp_dir_list = []
	for e in range(n_exp):
		exp_dir = os.path.relpath(os.path.join(benchmarks_root_dir, exp_list[e], exp_list[e] + '_' + datetime.now().strftime('%Y%m%d-%H:%M:%S:%f')))
		if not os.path.exists(exp_dir):
			os.makedirs(exp_dir)
		exp_dir_list.append(exp_dir)
		time.sleep(np.random.uniform() * 0.1)
	grid_shift_list = list(np.random.randint(0, 20000, n_exp))

	exp_info_filename = os.path.join(os.path.split(benchmarks_root_dir)[0], 'mongodb', dbpath_tag + '.pkl')
	exp_info_file = open(exp_info_filename, 'w')
	exp_info = {'dbpath': dbpath, 'exp_dir_list': exp_dir_list, 'n_eval_list': n_eval_list, 'grid_shift_list': grid_shift_list}
	pickle.dump(exp_info, exp_info_file)
	exp_info_file.close()

	run_multiple(dbpath, exp_dir_list, n_eval_list, grid_shift_list)


def run_multiple(dbpath, exp_dir_list, n_eval_list, grid_shift_list, parallel=False):
	if not os.path.exists(dbpath):
		os.makedirs(dbpath)
	mongodb_logfile_name = os.path.join(dbpath, 'mongodb.log')
	cmd_str = 'mongod --fork --logpath ' + mongodb_logfile_name + ' --dbpath ' + dbpath
	if '/var/scratch/' in os.path.realpath(__file__):
		cmd_str = '/var/scratch/coh/mongodb/mongodb-linux-x86_64-3.4.10/bin/' + cmd_str
	os.system(cmd_str)

	n_exp = len(exp_dir_list)
	if parallel:
		process_list = []
		for e in range(n_exp):
			process = run_spearmint(exp_dir_list[e], n_eval_list[e], grid_shift_list[e])
			process_list.append(process)
		n_running = n_exp
		while n_running > 0:
			time.sleep(60)
			running = [elm.poll() is None for elm in process_list]
			n_running = running.count(True)
			print('%d/%d is still running %s\ndb path : %s loadavg : %4.2f, %4.2f, %4.2f' % (n_running, n_exp, time.strftime("%H:%M:%S"), dbpath) + os.getloadavg())
			for e in range(n_exp):
				if running[e]:
					print('    %s' % exp_dir_list[e])
			sys.stdout.flush()
	else:
		for e in range(n_exp):
			process = run_spearmint(exp_dir_list[e], n_eval_list[e], grid_shift_list[e])
			while process.poll() is None:
				time.sleep(60)
				print('Experiment is running db path : %s exp_dir : %s(%s) loadavg %4.2f, %4.2f, %4.2f' % (dbpath, exp_dir_list[e], time.strftime("%H:%M:%S")) + os.getloadavg())
				sys.stdout.flush()
	cmd_str = 'mongod --shutdown --dbpath ' + dbpath
	if '/var/scratch/' in os.path.realpath(__file__):
		cmd_str = '/var/scratch/coh/mongodb/mongodb-linux-x86_64-3.4.10/bin/' + cmd_str
	os.system(cmd_str)
	return 0


if __name__ == '__main__':
	exp_list = []
	n_eval_list = []
	if len(sys.argv) > 2:
		for i in range(2, len(sys.argv), 2):
			exp_list.append(sys.argv[i])
			n_eval_list.append(int(sys.argv[i + 1]))
		run_multiple_init(sys.argv[1], exp_list, n_eval_list)
	else:
		exp_info_file = open(os.path.realpath(sys.argv[1]), 'r')
		exp_info = pickle.load(exp_info_file)
		exp_info_file.close()
		run_multiple(**exp_info)
