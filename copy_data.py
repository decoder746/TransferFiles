import os

rdir = "/media/hdd2/anshul/transfer"
domains = ["soccer","birthday","wedding","friends","surveillance","techtalk"]
root_dir = "/media/hdd1/home/vishal/data/"
budgets = ["60","90","120","150","180"]
algo = ["dr-dsn","vasnet-last","vasnet-max","vslstm-max","vslstm-last"]
for domain in domains:
    for budget in budgets:
        for al in algo:
            path = os.path.join(root_dir,domain,budget,al)
            cp_path = os.path.join(rdir,"submission"+al,domain,budget,"dr-dsn")
            cmd = "mkdir -p {}".format(cp_path)
            print(cmd)
            os.system(cmd)
            cmd2 = "cp {}/* {}/".format(path,cp_path)
            print(cmd2)
            os.system(cmd2)
