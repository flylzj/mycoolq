# # coding: utf-8
from pyecharts.charts import Line, Bar
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
        Line(opts.InitOpts(page_title="打卡统计图"))
        .add_xaxis(date_x)
        .set_global_opts(title_opts=opts.TitleOpts(title="打卡统计图"))
    )
    for k in data:
        line.add_yaxis(
            k[-1],
            [v[1] for v in sorted(data.get(k).items(), key=lambda item: item[0])],
            is_smooth=True
        )
    line.render(
        path="./nginx_static/render.html",
    )


if __name__ == '__main__':
    from coolq.db.model.english_record import get_statistics_data
    render_english_record_data(get_statistics_data())