# coding: utf-8
from coolq.db.model.english_record import get_statistics_data
from pyecharts.charts import Bar
from pyecharts import options as opts


def render_data():
    data = get_statistics_data()
    bar = (
        Bar()
        .add_xaxis(data.keys())
        .add_yaxis("days", [d.get('days') for k, d in data.items()])
        .set_global_opts(title_opts=opts.TitleOpts(title="days"))
    )