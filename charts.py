# # coding: utf-8
from coolq.db.model.english_record import get_statistics_data
from pyecharts.charts import Bar, Line
from pyecharts import options as opts


def render_data(data):
    date_x = []
    for _, v in data.items():
        for d in v:
            if d not in date_x:
                date_x.append(d)
    date_x.sort()
    line = (
        Line()
        .add_xaxis(date_x)
    )
    for k in data:
        line.add_yaxis(k, [v for v in data.get(k).values()])
    line.render()


render_data(get_statistics_data())