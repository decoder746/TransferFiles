import os

rdir = "/media/hdd2/anshul/transfer"
domains = ["soccer","birthday","wedding","friends","surveillance","techtalk"]
root_dir = "/media/hdd1/home/vishal/data/"
budgets = ["60","90","120","150","180"]
algo = ["vasnet-last","vasnet-max","vslstm-max","vslstm-last"]
for domain in domains:
    for budget in budgets:
        for al in algo:
            path = os.path.join(root_dir,domain,budget,al)
            videos = os.listdir(path)
            for video in videos:
                video_name = os.listdir(os.path.join(root_dir,domain,budget,al,video))[0]
                video_path = os.path.join(root_dir,domain,budget,al,video,video_name)
                new_summary_video = video+"_dr-dsn_"+budget
                cp_dir = os.path.join(rdir,"submission"+al,domain,budget,"dr-dsn")
                cp_path = os.path.join(rdir,"submission"+al,domain,budget,"dr-dsn",new_summary_video)
                cmd = "mkdir -p {}".format(cp_dir)
                print(cmd)
                os.system(cmd)
                cmd2 = "cp {} {}".format(video_path,cp_path)
                print(cmd2)
                os.system(cmd2)
