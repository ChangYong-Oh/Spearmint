import sys
import os.path
import subprocess
from datetime import datetime
from shutil import copy


def run_spearmint(exp_dir, n_eval):
	logfile_name = os.path.join(exp_dir, exp_type + '_' + tag + '.log')
	mongodb_folder_name = os.path.join(exp_dir, 'mongodb')
	if not os.path.exists(mongodb_folder_name):
		os.makedirs(mongodb_folder_name)

	cmd_str = 'mongod --fork --logpath ' + logfile_name + ' --dbpath ' + mongodb_folder_name + ';'
	cmd_str += 'python ./spearmint/main.py ' + exp_dir + ' --evals ' + str(n_eval)

	process = subprocess.Popen(cmd_str, shell=True)
	process.wait()
	print('Spearmint exit with %d' % process.returncode)

if __name__ == '__main__':
	folder_name = os.path.abspath(sys.argv[1])
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
	run_spearmint(exp_dir, int(sys.argv[2]))
