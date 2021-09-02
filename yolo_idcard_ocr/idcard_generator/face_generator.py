import os

# face dataset(lfw_funneled) download url
# http://vis-www.cs.umass.edu/lfw/

folder_path = './lfw_funneled/'
out_path = './face/'
folder_list = os.listdir(folder_path)

for folder in folder_list:
    file_list = os.listdir(folder_path+folder)
    try:
        print(file_list[0])
        os.rename(folder_path+folder+'/'+file_list[0], out_path + file_list[0])
    except:
        #print(folder)
        pass        