import requests
from linggle import Linggle

'''
	http://thor.nlplab.cc:5566/search?q={skip_bigram}
'''

def get_sbg_stat(sbg):
    response = requests.get('http://thor.nlplab.cc:5566/search?q=' + sbg.lower())
    return response.json()

# Result: {'1': 45440, '2': 29769, '3': 3005, '4': 4111}

def getData(path):
    f = open(path)
    output = [[]]
    i=0
    data = f.read().splitlines()
    for item in data:
        try:
            output[i].append((item.split('\t')[0], item.split('\t')[1]))
        except:
            output.append([])
            i=i+1
    return output

def deleteDetect(datas):
    i = 0
    inc_index=0
    for item in datas:
        if (item[1] == 'i'):
            inc_index = i
            break
        i = i + 1
    
def deleteDetect(datas):

if __name__ == "__main__":
    datas = []
    lines = []

    datas=getData(r'./sentences.tsv')
    print(datas[0])
    print(datas[1])

    linggle = Linggle()
    print(get_sbg_stat('affected our'))

    print(linggle.query('?am replying your _ letter'))
# []
    print(linggle.query('am replying _ your letter'))
    # [['am replying to your letter', 245]]
