import requests
import json
import threadpool
import datetime

total_page = 25
pool = threadpool.ThreadPool(8)
songs_dict = {}


def get_page(page_num):
    print('爬取第' + str(page_num + 1) + '页,(' + str(20 * page_num) + ' ~ ' + str(20 * (page_num + 1)) + ')')
    r = requests.get('https://beatsaver.com/api/search/text/' + str(page_num) + '?sortOrder=Relevance&ranked=true')
    docs = json.loads(r.content)['docs']
    songs_dict[page_num] = []
    for song in docs:
        songs_dict[page_num].append({
            'hash': song['versions'][0]['hash'],
            'levelid': 'custom_level_' + song['versions'][0]['hash']})


def get_saber_rank():
    st = datetime.datetime.now()
    
    result_dict = {'playlistTitle': "RankSongs", 'playlistAuthor': "Rin", 'playlistDescription': "by rin", 'songs': []}
    songs_list = []
    
    reqs = threadpool.makeRequests(get_page, create_arg_list(total_page))
    [pool.putRequest(req) for req in reqs]
    
    pool.wait()

    for index in range(total_page):
        songs_list += songs_dict[index]
    
    result_dict['songs'] = songs_list
    ed = datetime.datetime.now()
    print("总共用时： " + str((ed - st).total_seconds()) + "秒， 正在导出文件...")
    json.dump(result_dict, open('rank_songs.json', "w"), ensure_ascii=False)
    
    return 0


def create_arg_list(tp):
    arg_list = []
    for i in range(tp):
        arg_list.append(i)
    return arg_list
    

get_saber_rank()
