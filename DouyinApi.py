
import flask
import json
import requests
import re
from urllib import parse
from gevent import pywsgi
from flask_cors import CORS
api = flask.Flask(__name__)
CORS(api, supports_credentials=True)
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}



# 'index'是接口路径，methods不写，默认get请求
@api.route('/getuuidApi', methods=['get'])
# post方式访问
def index():
    url = flask.request.values.get('url')
    pttype = flask.request.values.get('type')
    if pttype == 'dy':
        cdxurl = requests.get(url=url, headers=headers)
        uid = re.findall('video/(.+?)/', cdxurl.url)
        infourl = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + uid[0]
        itemurl = json.loads(requests.get(url=infourl, headers=headers).text)
        if itemurl['item_list'][0]['video']['vid']:
            data = {
                'nickname': itemurl['item_list'][0]['author']['nickname'],
                'signature': itemurl['item_list'][0]['author']['signature'],
                'videourl': itemurl['item_list'][0]['video']['play_addr']['url_list'][0],
                'coverurl': itemurl['item_list'][0]['video']['cover']['url_list'][0]
            }
            itemlist = {'data': data, 'msg_code': 200}
            # json.dumps 序列化时对中文默认使用的ascii编码.想输出中文需要指定ensure_ascii=False
            return itemlist
    elif pttype == 'ks':
        cdxurl = requests.get(url=url, headers=headers)
        urldata = parse.parse_qs(parse.urlparse(str(cdxurl.url)).query)
        Cookie = {
            'did': cdxurl.cookies.get('did'),
            'didv': cdxurl.cookies.get('didv')
        }
        kpn = urldata.get('kpn')[0]
        data = {
            'kpn': urldata.get('kpn')[0],
            'env': "SHARE_VIEWER_ENV_TX_TRICK",
            'h5Domain': "v.m.chenzhongtech.com",
            'isLongVideo': False,
            'shareChannel': "share_copylink",
            'photoId': urldata.get('photoId')[0],
            'fid': urldata.get('fid')[0],
            'shareObjectId': urldata.get('shareObjectId')[0],
            'shareMethod': urldata.get('shareMethod')[0],
            'shareResourceType': urldata.get('shareResourceType')[0],
            'shareToken': urldata.get('shareToken')[0],
            'subBiz': urldata.get('subBiz')[0],
        }
        headers['Referer'] = str(cdxurl.url)
        headers['Content-Type'] = 'application/json'
        infourl = f'https://v.m.chenzhongtech.com/rest/wd/photo/info?kpn={kpn}&captchaToken='
        itemurl = json.loads(requests.post(url=infourl, data=json.dumps(data), headers=headers, cookies=Cookie).text)
        retdata = {
            'nickname': itemurl['photo']['userName'],
            'signature': itemurl['photo']['caption'],
            'videourl': itemurl['mp4Url'],
            'coverurl': itemurl['photo']['coverUrls'][0]['url']
        }
        itemlist = {'data': retdata, 'msg_code': 200}
        # json.dumps 序列化时对中文默认使用的ascii编码.想输出中文需要指定ensure_ascii=False
        return itemlist




# else:
#     path = os.getcwd()
#     nickname = itemurl['item_list'][0]['author']['nickname'],
#     os.makedirs(nickname)


if __name__ == '__main__':
    #api.run(port=4000, debug=True)  # 启动服务
    server = pywsgi.WSGIServer(('0.0.0.0', 4000), api)
    server.serve_forever()
    # debug=True,改了代码后，不用重启，它会自动重启
    # 'host='127.0.0.1'别IP访问地址
