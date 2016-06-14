import web
import pandas as pd
render = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/analysis', 'Analysis'
)


class Index:
    def __init__(self):
        db = web.database(dbn='mysql', user='root', pw='ccpl_817', db='opinion', host='192.168.8.3')
        posts = db.select('posts')

        self.posts = posts

    def GET(self):
        return render.index(self.posts)


class Analysis:
    def __init__(self):
        db = web.database(dbn='mysql', user='root', pw='ccpl_817', db='opinion', host='192.168.8.3')
        titles = db.select('reports', what="description", limit=10)
        res = db.select('reports', limit=1)
        reports = []
        for r in res:
            report = {}
            report['description'] = r['description']
            report['analysis'] = r['analysis']
            report['dates'] = pd.date_range(r['date_start'], r['date_end']).tolist()
            c_attitudes = [int(x) for x in r['c_attitudes'].split(',')]
            report['c_attitudes'] = [c_attitudes[0:14], c_attitudes[14:28], c_attitudes[28:42]]
            report['c_weibo_3days'] = [int(x) for x in r['c_weibo_3days'].split(',')]
            report['c_keywords_dqe'] = [k.split(' ') for k in r['c_keywords_dqe'].split('\t')]
            report['c_user_types'] = [int(x) for x in r['c_user_types'].split(',')]
            report['c_emotions'] = [[_x for _x in x.split(',')] for x in r['c_emotions'].split('\t')]
            report['t_trend'] = r['t_trend']
            report['weibo'] = [x for x in r['weibo'].split('\t')]
            report['flag'] = r['flag']
            reports.append(report)
        self.titles = titles
        self.report = reports[0]

    def GET(self):
        return render.analysis(self.report, self.titles)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
