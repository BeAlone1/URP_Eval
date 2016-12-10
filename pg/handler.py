import tornado.web
import requests
from lxml import etree
from tornado import gen
import time
from urllib import parse

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("JSESSIONID")
        if user:
        	return user.decode()
        else:
        	self.redirect('/login')

class login(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("login.html")

    @gen.coroutine
    def post(self):
        zjh = self.get_body_argument('zjh')
        mm  = self.get_body_argument('mm')
        postdata = {
        'evalue' : '',
        'zjh1' :'',
        'zjh' : zjh,
        'fs' : '',
        'v_yzm' : '',
        'lx' : '',
        'mm' : mm,
        'eflag' : '',
        'dzslh' : '',
        'tips' : ''
        }
        head = {
            "Accept-Language":"zh-CN,zh;q=0.8",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Connection":"keep-alive",
            'Referer': "http://211.82.47.2/"
        }
        res = requests.post('http://211.82.47.2/loginAction.do', data = postdata, headers=head)
        res.close()
        if len(res.content) < 2000:
            tmp = res.headers['Set-Cookie']
            #cookie = tmp[tmp.find('=')+1 : tmp.find(';')]
            self.set_secure_cookie("JSESSIONID", tmp, expires_days=None, expires=time.time()+900)
            self.redirect('/list')

        else:
            self.write("账号密码错误")

class tlist(BaseHandler):
    @gen.coroutine
    def get(self):
        uid = self.current_user
        if uid:
            #self.write('JSESSIONID: %s' % uid)
            head = {
                "Accept-Language":"zh-CN,zh;q=0.8",
                'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
                "Connection":"keep-alive",
                "Cookie" : uid
            }
            two = requests.get('http://211.82.47.2/jxpgXsAction.do?oper=listWj', headers = head)
            notPg = []
            hadPg = []
            content = etree.HTML(two.text)
            for link in content.xpath('//img')[0:-5]:
                if link.get('title') == '评估':
                    notPg.append(link.get('name').split('#@'))
                else:
                    hadPg.append(link.get('name').split('#@'))

            """ret = ''
            for i in hadPg:
                ret += i
                ret += '<br>'
            self.write(ret)"""
            self.render('teacher_list.html', notPg = notPg, hadPg = hadPg)

class toEval(BaseHandler):
    @gen.coroutine
    def get(self):
        uid = self.current_user
        if not uid:
            self.redirect('/login')
        head = dict()
        head['Content-Type'] = 'application/x-www-form-urlencoded'
        #head['Referer'] = 'http://211.82.47.2/jxpgXsAction.do'
        head['Accept-Language'] = 'zh-CN'
        head['Cache-Control'] = 'no-cache'
        head['Accept'] = 'text/html,application/xhtml+xml,application/xml'
        head['Accept-Encoding'] = 'gzip, deflate'
        head['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        head['Cookie'] = uid

        bpr  = self.get_argument('bpr')
        wjbm = self.get_argument('wjbm')
        pgnr = self.get_argument('pgnr')
        wj = {
        'bpr': bpr,
        'bprm': self.get_argument('bprm'),
        'wjmc': self.get_argument('wjmc'),
        'wjbz': 'null',
        'wjbm': wjbm,
        'pgnrm': self.get_argument('pgnrm'),
        'pgnr': pgnr,
        'pageSize': '20',
        'pageNo': '',
        'page': '1',
        'oper': 'wjShow',
        'currentPage': '1'
        }
        wj = parse.urlencode(wj, encoding='gbk').encode()
        two = requests.post('http://211.82.47.2/jxpgXsAction.do', data = wj, headers=head)
        two.close()
        self.render("eval_page.html", bpr = bpr, wjbm = wjbm, pgnr = pgnr)
        #self.write(two.text)


    @gen.coroutine
    def post(self):

        uid = self.current_user
        if not uid:
            self.redirect('/login')
        head1 = dict()
        head1['Content-Type'] = 'application/x-www-form-urlencoded'
        head1['Referer'] = 'http://211.82.47.2/jxpgXsAction.do'
        head1['Accept-Language'] = 'zh-CN'
        head1['Cache-Control'] = 'no-cache'
        head1['Accept'] = 'text/html,application/xhtml+xml,application/xml'
        head1['Accept-Encoding'] = 'gzip, deflate'
        head1['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        head1['Cookie'] = uid

        one   = self.get_body_argument('one')
        two   = self.get_body_argument('two')
        three = self.get_body_argument('three')
        four  = self.get_body_argument('four')
        zero  = self.get_body_argument('zero')
        data = {
            '0000000002': zero,
            '0000000003': zero,
            '0000000011': one,
            '0000000012': one,
            '0000000013': one,
            '0000000014': one,
            '0000000021': two,
            '0000000022': two,
            '0000000023': two,
            '0000000024': two,
            '0000000031': three,
            '0000000032': three,
            '0000000033': three,
            '0000000034': three,
            '0000000041': four,
            '0000000042': four,
            '0000000043': four,
            'bpr': self.get_body_argument('bpr'),
            'pgnr': self.get_body_argument('pgnr'),
            'wjbm': self.get_body_argument('wjbm'),
            'wjbz': 'null',
            'xumanyzg': 'zg',
            'zgpj': self.get_body_argument("zgpj")
        }
        data = parse.urlencode(data, encoding='gbk').encode()
        three = requests.post('http://211.82.47.2/jxpgXsAction.do?oper=wjpg', data=data, headers = head1)
        three.close()
        self.write(three.text)


class ResultShow(BaseHandler):
    @gen.coroutine
    def get(self):

        uid = self.current_user
        if not uid:
            self.redirect('/login')
        head1 = dict()
        head1['Content-Type'] = 'application/x-www-form-urlencoded'
        head1['Referer'] = 'http://211.82.47.2/jxpgXsAction.do?oper=listWj'
        head1['Accept-Language'] = 'zh-CN'
        head1['Cache-Control'] = 'no-cache'
        head1['Accept'] = 'text/html,application/xhtml+xml,application/xml'
        head1['Accept-Encoding'] = 'gzip, deflate'
        head1['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        head1['Cookie'] = uid

        data = {
            'bpr': self.get_argument('bpr'),
            'bprm': self.get_argument("bprm"),
            'currentPage': '1',
            'oper': 'wjResultShow',
            'page': '1',
            'pageNo': '',
            'pageSize': '20',
            'pgnr': self.get_argument("pgnr"),
            'pgnrm': self.get_argument('pgnrm'),
            'wjbm': self.get_argument('wjbm'),
            'wjbz': '',
            'wjmc': self.get_argument('wjmc')
        }
        data = parse.urlencode(data, encoding='gbk').encode()
        result = requests.post('http://211.82.47.2/jxpgXsAction.do', data = data, headers = head1)
        result.close()
        self.write(result.text)