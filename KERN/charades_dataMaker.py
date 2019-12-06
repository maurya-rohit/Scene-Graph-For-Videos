from __future__ import unicode_literals

import os
import glob
import logging
import shutil
from shutil import copy

logging.basicConfig(filename="charades.log",
                    format='%(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

# Mapping should contain file name, batch no. , Start frame,  end frame and video file name too

def backup(out_path, bkp_path):
    files = glob.glob(out_path + '*')

    if not os.path.exists(bkp_path):
        os.makedirs(bkp_path)
   
    for f in files:
        copy(f, bkp_path)

def cleanData(data_path):
    files = glob.glob(data_path + '*')
    for f in files:
        os.remove(f)

def extract_frames(videoid, cur_file, f, startNum, out_path):
    cmd = 'ffmpeg -i {0} -vf "select=eq(pict_type\,I)" -vsync vfr -start_number {1} {2}%d.jpg -hide_banner -loglevel quiet'.format(f, startNum, out_path)
    os.system(cmd)

    list_indir = os.listdir(out_path)

    cur_file.write(videoid + " " + str(startNum) + " " + str(startNum + len(list_indir)-1) + "\n")
    return len(list_indir)


def moveFromCacheToData(cache_path, data_path):
    files = glob.glob(cache_path + '*')
    for f in files:
        shutil.move(f, data_path)
       
       


if __name__ == '__main__':

    data_path = "/home/asamalusc/KERN/data/VG_100K/"
    # data_path = "D:\\USC\\Assignments\\CSCI566\\KERN\\KERN\\FD_dataLoader\\data\\"
    # data_path = "/Users/skamalakkannan/Documents/usc_study/DL/project_code/mapping_videos_toframes/data/"
   
    video_path = '/home/asamalusc/KERN/video/'
    # video_path = 'D:\\USC\\Assignments\\CSCI566\\KERN\\KERN\\FD_dataLoader\\video\\'
    # video_path = "/Users/skamalakkannan/Documents/usc_study/DL/project_code/mapping_videos_toframes/video/"

    backp_path = "/home/asamalusc/KERN/dataBK/"
    # bkp_path = 'D:\\USC\\Assignments\\CSCI566\\KERN\\KERN\\FD_dataLoader\\dataBK\\'
    # backp_path = "/Users/skamalakkannan/Documents/usc_study/DL/project_code/mapping_videos_toframes/dataBK/"

    cache_path = "/home/asamalusc/KERN/cache/"
    # cache_path = 'D:\\USC\\Assignments\\CSCI566\\KERN\\KERN\\FD_dataLoader\\cache\\'
    # cache_path = "/Users/skamalakkannan/Documents/usc_study/DL/project_code/mapping_videos_toframes/cache/"

    batch_size = 500

    videoFiles = glob.glob(video_path + '*')
    i=1
    fileIdx=1
    batchnum = 1

    bkp_path = backp_path + str(batchnum)
    filename = "/home/asamalusc/KERN/mappings/mapping"
    cur_file = open(filename + "_" + str(batchnum), "w")

    for f in videoFiles:
        video_id = f.split("/")[-1].split(".mp4")[0]

        fileCount = extract_frames(video_id, cur_file, f, fileIdx, cache_path)
        fileIdx = fileIdx + fileCount
      
        backup(cache_path, bkp_path)
        moveFromCacheToData(cache_path, data_path)
        
        print ("Processed:"+video_id)

        if(i%batch_size == 0):
            cur_file.close()
            kernCMD = 'python models/eval_rels.py -m sgdet -p 100 -clip 5 -ckpt checkpoints/kern_sgdet.tar -test -b 1 -use_ggnn_obj -ggnn_obj_time_step_num 3 -ggnn_obj_hidden_dim 512 ' \
                       '-ggnn_obj_output_dim 512 -use_obj_knowledge -obj_knowledge prior_matrices/obj_matrix.npy -use_ggnn_rel -ggnn_rel_time_step_num 3 -ggnn_rel_hidden_dim 512 ' \
                       '-ggnn_rel_output_dim 512 -use_rel_knowledge -rel_knowledge prior_matrices/rel_matrix.npy -cache caches/kern_sgdet_' + str(batchnum) + '.pkl' \
                                                                                                                                                  ' -save_rel_recall results/kern_rel_recall_sgdet' + str(batchnum) + '.pkl'

            os.system(kernCMD)
            print("KERN command ran for batch"+ str(batchnum))
            i=0
            fileIdx = 1
            batchnum += 1
            bkp_path = backp_path + str(batchnum)
            #cur_file.close()
            if (i != len(videoFiles)):
                cur_file = open(filename + "_" + str(batchnum), "w")
            cleanData(data_path)

 
        i = i+1
        
    cleanData(data_path)
