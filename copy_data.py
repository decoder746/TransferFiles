import os

rdir = "/media/hdd2/anshul/results2"
domains = ["soccer","birthday","wedding","friends","surveillance","techtalk"]
root_dir = "/media/hdd1/home/vishal/data/"
budgets = ["60","90","120","150","180"]
algo = ["vasnet-last","vasnet-max","vslstm-max","vslstm-last"]
algo = ["mixture-cfg6"]
for domain in domains:
    for budget in budgets:
        for al in algo:
            path = os.path.join(root_dir,domain,budget,al)
            videos = os.listdir(path)
            for video in videos:
                # video_name = os.listdir(os.path.join(root_dir,domain,budget,al,video))[0]
                video_name =video.split(al)[0][:-1]
                # video_path = os.path.join(root_dir,domain,budget,al,video,video_name)
                video_path = os.path.join(root_dir,domain,budget,al,video)
                new_summary_video = video_name+"_dr-dsn_"+budget+".json"
                cp_dir = os.path.join(rdir,"submission"+al,domain,budget,"dr-dsn")
                cp_path = os.path.join(rdir,"submission"+al,domain,budget,"dr-dsn",new_summary_video)
                cmd = "mkdir -p {}".format(cp_dir)
                print(cmd)
                os.system(cmd)
                cmd2 = "cp {} {}".format(video_path,cp_path)
                print(cmd2)
                os.system(cmd2)

# for domain in domains:
#     for budget in budgets:
#         for al in algo:
#             path = os.path.join(root_dir,domain,budget,al)
#             videos = os.listdir(path)
#             for video in videos:
#                 video_name = os.listdir(os.path.join(root_dir,domain,budget,al,video))[0]
#                 video_path = os.path.join(root_dir,domain,budget,al,video,video_name)
#                 # new_summary_video = video+"_dr-dsn_"+budget+".json"
#                 cp_dir = os.path.join(rdir,domain,budget,al)
#                 cp_path = os.path.join(rdir,domain,budget,al,video_name)
#                 cmd = "mkdir -p {}".format(cp_dir)
#                 print(cmd)
#                 os.system(cmd)
#                 cmd2 = "cp {} {}".format(video_path,cp_path)
#                 print(cmd2)
#                 os.system(cmd2)
