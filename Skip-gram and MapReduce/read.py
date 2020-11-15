import fileinput
from tqdm import tqdm
from collections import Counter
from multiprocessing import Pool



def mapper(row):
    i=0
    try:
        data=row.split("\t")
        cnt=data[1]
        strings=data[0].split(" ")
        first=strings[0]
        end=strings[-1]
        skiped=len(strings)-1

        if(skiped==0):
            return None
        return ((first+' '+end,skiped),cnt)
    except:
        return None


def reducer(data):
    total_dict = {}

    for item in data:
        if(total_dict.get(item[0])==None):
            print(item)
            total_dict[item[0]]=item[1]
        else:
            total_dict[item[0]]=total_dict[item[0]]+item[1]
    return total_dict


skipgram_count=[]


with open("mapperTmp.txt", 'r') as f:
    lines = f.readlines()
    for data in lines:
        try:
            data=eval(data)
            newdata=(data[0],int(data[1]))
            skipgram_count.append(newdata)
        except:
            pass

fileObject = open('ReduceTmp.txt', 'w')

total_dict=reducer(skipgram_count)
out=sorted(total_dict.items(), key=lambda x:x[1],reverse=True)
for item in out:
    fileObject.write(str(item))
    fileObject.write('\n')
fileObject.close()
