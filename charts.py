# # coding: utf-8
from pyecharts.charts import Line
from pyecharts import options as opts


# 打卡统计图
def render_english_record_data(data):
    date_x = []
    for _, v in data.items():
        for d in v:
            if d not in date_x:
                date_x.append(d)
    date_x.sort()
    line = (
        Line()
        .add_xaxis(date_x)
        .set_global_opts(title_opts=opts.TitleOpts(title="打卡统计图"))
    )
    for k in data:
        line.add_yaxis(k[-1], [v for v in data.get(k).values()])
    line.render(
        path="./nginx_static/render.html"
    )


if __name__ == '__main__':
    from coolq.db.model.english_record import get_statistics_data
    render_english_record_data(get_statistics_data())