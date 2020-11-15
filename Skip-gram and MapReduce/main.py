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
            total_dict[item[0]]=int(item[1])
        else:
            total_dict[item[0]]=total_dict[item[0]]+int(item[1])
    return total_dict



if __name__ == "__main__":

    # Create multiprocessing pool
    pool = Pool()

    # Map
    print("Map Stage...")
    with open("web1t.baby",encoding='UTF-8') as f:
        baby1t = f.read().splitlines()
    skipgram_count = [row for row in pool.map(mapper, baby1t) if row]
    skipgram_count.sort(key=lambda x: x[0])
    # fileObject = open('mapperTmp.txt', 'w')
    # for item in skipgram_count:
    #     fileObject.write(str(item))
    #     fileObject.write('\n')
    # fileObject.close()
    # skipgram_count:
    # [
    #   ... ,
    #   (('of the', 1), 12345678),
    #   (('of the', 1), 123),
    #   (('at the', 2), 456),
    #   ...
    # ]
    # Reduce
    print("Reduce Stage...")
    # skipgram_count=[]
    # with open("mapperTmp.txt",'r') as f:
    #     for data in f:
    #         data=f.readline().strip()
    #         data=eval(data)
    #         newdata=(data[0],int(data[1]))
    #         skipgram_count.append(newdata)    
    total_dict=reducer(skipgram_count)
    out = sorted(total_dict.items(), key=lambda x: x[1], reverse=True)

    fileObject = open('ReduceTmp.txt', 'w')

    for i in range(100):
        print(out[i])
        fileObject.write(str(out[i]))
        fileObject.write('\n')
    fileObject.close()


