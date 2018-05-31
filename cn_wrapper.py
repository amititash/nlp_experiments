'''
A wrapper that makes queries to CN API and 
tries to describe the concept in a english text
'''

import requests



def cn_api(topic):
    
    # create the topic url for the endpoint
    topicURl = 'http://api.conceptnet.io/query?node=/c/en/'+topic
    obj = requests.get(topicURl).json()

    # Loop through the result and create a list of start, end, rel
    # for each edge

    print(obj)

    graph_edge = obj['edges']
    # graph_view = obj['view']

    # print(graph_view)

    for gr in graph_edge:
        
        sentence = gr['start']['label']+" "+gr['rel']['label']+" "+gr['end']['label']
        print(sentence)
        print('----')
        



cn_api('linkedin')
