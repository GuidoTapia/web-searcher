from django.http import HttpResponse
from django.core.files import File

import json

def get_word(line):
    idx = line.find('\t')
    key = line[:idx]
    words = line[idx + 1:].split(';')
    value = ['0'] * 10
    for word in words[:-1]:
        s = word.find(':')
        n = int(word[s - 5:s - 4])
        value[n - 1] = word[s + 1:]

    return key, value


def build_index():
    f = open('data', 'r')
    lines = f.readlines()
    mapper = dict()
    for line in lines:
        key, value = get_word(line)
        mapper[key] = value

    f.close()
    return mapper


def get_doc(line):
    idx = line.find(']')
    return float(line[idx + 3: -2])


def get_ranked():
    f = open('ranked', 'r')
    lines = f.readlines()
    doc_rank = []
    for line in lines:
        doc_rank.append(get_doc(line))

    f.close()
    return doc_rank


index = build_index()
rank = get_ranked()

def query_word(request, word):
    response=''
    query = word
    if index.get(query) is None:
        #print('Your search _{query}_ did not match any documents')
        response=json.dumps([{'response':'error','body':'Your search _'+str(query)+'_ did not match any documents'}])
    else:
        #print('Found on: ')
        arr = []
        for i, found in enumerate(index.get(query)):
            if found != '0':
                #print(f'file{i + 1}')
                arr.append(rank[i])

        arr = list(reversed(sorted(arr)))
        #print(arr)
        #print('With PageRank')
        responseArr=[]
        for item in arr:
            #print(f'file{rank.index(item) + 1}')
            responseArr.append({'response':f'file{rank.index(item) + 1}'})
        response=json.dumps(responseArr)
    return HttpResponse(response, content_type='text/json')

"""def get_word(request, word):
    response=json.dumps([{'word':str(word)}])
    return HttpResponse(response, content_type='text/json')"""