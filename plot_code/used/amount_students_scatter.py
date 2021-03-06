import pandas as pd
from statistics import mean
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import show, output_file
from bokeh.models import Legend
from bokeh.models import HoverTool


def best_fit_line(xs, ys):

    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))

    b = mean(ys) - m*mean(xs)

    return m, b


def main():

    # file where .html should be saved
    output_file('docs/amount_students_scatter.html',
                title='Scatterplot: Amount of Students')

    # reads df from file
    df = pd.read_csv('../../university_ranking.csv', index_col=0)

    colormap = {2016: 'red',
                2017: 'green',
                2018: 'blue'}

    years = [2016, 2017, 2018]

    # gets top 800 for every year and puts into list
    dfs = [df.loc[df['year'] == year].head(200) for year in years]
    df = dfs[0].append(dfs[1].append(dfs[2]))

    # changes float to integer for more correct scatterplot
    # df['pct_intl_student'] = df['pct_intl_student'] * 100
    df.no_student = df.no_student.astype(int)

    # creates all data we need
    year_list = []

    # creates list of years for every datapoint
    for year in years:
        for i in range(200):
            year_list.append(year)

    # creates list of colors for every datapoint
    colors = [colormap[x] for x in df['year']]

    # all data collected in a dictionary
    data = {
            'ranking': df['ranking'],
            'Amount_Students': df['no_student'],
            'years': year_list,
            'color': colors,
            'university': df['university_name']
    }

    m, b = best_fit_line(df['ranking'], df['no_student'])
    m = round(m, 4)
    b = round(b, 4)

    x = [i for i in range(201)]
    y = [m * x + b for x in range(len(x))]

    source = ColumnDataSource(data)

    hover = HoverTool(
                tooltips=[('Year', '@years'),
                          ('Ranking', '@ranking'),
                          ('Amount of Students', '@Amount_Students'),
                          ('University', '@university')],
                names=['scatter'])

    p = figure(tools=[hover], title="Scatterplot: Amount of Students")
    p.xaxis.axis_label = 'International Ranking'
    p.yaxis.axis_label = 'Amount of Students'
    p.scatter('ranking', 'Amount_Students', source=source,
              color='color', name='scatter', legend='years')
    r1 = p.line(x, y, line_width=2, color='black')
    legend = Legend(items=[
                ("{0}x + {1}".format(m, b), [r1])])

    p.add_layout(legend, 'above')

    show(p)


if __name__ == "__main__":
    main()
