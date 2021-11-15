# This is Synchronization folder maker, recursively make all folders as dir1
# To use this program, insert the name of source directory in source variable
# and the name of destination directory in destination variable, The directory names
# must be of full pathname
import os
from shutil import copy2
from time import time,ctime

source = 'D:\OpenSSL'
destination = 'E:\OpenSSL'
initime = time()
source = os.path.normcase(source)
destination = os.path.normcase(destination)
FilesToBeCopied = []
# At first make directory listing of all directory of dir1
dir1 = []
for rootlist,dirlist,filelist in os.walk(source):
        dir1.append(rootlist)
#print(dir1) #######################           DEBUG
# Then make directory listing for the folder to be synchronized
dir2 = []
for tt in dir1:
        dir2.append(tt.replace(source,destination))

# Make only the directories in the target folder
for items in dir2:
        if os.path.exists(items):
                pass
        else:
                os.mkdir(items)

dirtuple = []
for items in range(len(dir1)):
    dirtuple.append((dir1[items],dir2[items]))

#################                
del dir1,dir2   # Is it necessary ?
#################

def fsync(pdir,sdir):
    pfiles = []
    pfiles2 = []
    sfiles = []
    sfiles2 = []
    for roots,dirs,files in os.walk(pdir):
        pfiles.extend(files)
        break       # This break is for making list of files of only the given folder , not the embedded ones
    for filname in pfiles: # This loop is used to convert the filenames into full qualified names
            pfiles2.append(os.path.join(pdir,filname))
    
    for roots,dirs,files in os.walk(sdir):
        sfiles.extend(files)
        break       # This break is for making list of files of only the given folder , not the embedded ones
    for filname in sfiles: # This loop is used to convert the filenames into full qualified names
            sfiles2.append(os.path.join(sdir,filname))
    ###################
    del pfiles,sfiles # Is it necessasry ?
    ###################
    for items in pfiles2: # Here actual copy process occurs for files only
        if items not in sfiles2:
            copy2(items, sdir)
            FilesToBeCopied.append(items)
        else:
                if os.path.getmtime(items)!= os.path.getmtime(os.path.join(sdir,items)):
                        copy2(items, sdir)
                        FilesToBeCopied.append(items)
                else:
                        pass
print('Please wait while this script synchronizes your directories...')
for couples in dirtuple:
    a,b = couples
    fsync(a,b)
############################ Main work done ###########################################
os.chdir(destination)
f = open('log.txt','w')
f.write('This folder has been synchronized with '+ source + ' on '+ ctime())
fintime = time()
f.write('\n\n')
f.write('Following files are copied to this directory and beneath this directory:')
f.write('\n\n')
for gg in FilesToBeCopied:
        f.write(gg)
        f.write('\n')
f.close()
print('Succesfully synchronized directory ','"',destination,'"','to directory ','"',source,'"')
print('Total time required for synchronization : ',str(fintime-initime)[:4],' Second(s)')

