# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 12:10:48 2023

@author: syeds
"""

import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.subplots as sp
import plotly.graph_objs as go

df = pd.read_csv("COVID-19-global-data.csv")


df.columns = df.columns.str.strip().str.lower()

region_mapper = {
    'EMRO': 'Eastern Mediterranean Region',
    'EURO': 'European Region',
    'AFRO': 'African Region',
    'WPRO': 'Western Pacific Region',
    'AMRO': 'Region of the Americas',
    'SEARO': 'South-East Asia Region',
    'Other':'Other'
}

df['region_name'] = df['region'].map(region_mapper)

country_region_dict = pd.Series(df['region_name'].values,index=df['country']).to_dict()



def deaths_by_regions():
    # Group the data by region and sum the deaths by day
    df_deaths_by_region = df.groupby(['region', 'date_reported'])['deaths'].sum().reset_index()
    
    #title for subplots
    title_mapper = {
        'AMRO': 'America',
        'EURO': "Europe",
        'SEARO': 'South-East Asia',
        'EMRO': 'Eastern Mediterranean'
        }
    
    # Get the top 4 regions by total deaths
    top_regions = df_deaths_by_region.groupby('region')['deaths'].sum().sort_values(ascending=False).head(4).index.tolist()
    
    # Create the subplots using Plotly
    fig = sp.make_subplots(rows=2, cols=2, subplot_titles=[title_mapper[reg] for reg in top_regions])
    
    # Define the color palette
    colors = ['rgb(0, 123, 255)', 'rgb(40, 167, 69)', 'rgb(255, 193, 7)', 'rgb(220, 53, 69)']
    
    
    for i, region in enumerate(top_regions):
        # Filter the data to include only the current region
        df_region = df_deaths_by_region[df_deaths_by_region['region'] == region]
    
        # Filter the data to start from February 2020
        df_region = df_region[df_region['date_reported'] >= '2020-02-01']
    
        # Add the trace for the current region to the plot
        trace = go.Bar(x=df_region['date_reported'], y=df_region['deaths'], name=title_mapper[region], marker=dict(color=colors[i]))
        fig.add_trace(trace, row=i//2+1, col=i%2+1)
    
        # Add the total deaths text to the plot
        total_deaths = df_region['deaths'].sum()
        fig.add_annotation(x=df_region['date_reported'].iloc[100], y= max(df_region['deaths']),
                           text=f"Total deaths in {region}: {total_deaths:,}",
                           showarrow=False, font=dict(size=14),
                           row=i//2+1, col=i%2+1)
    
        # Update the subplot's x-axis and y-axis labels
        fig.update_xaxes(title_text='Date', range=['2020-02-01', df_deaths_by_region['date_reported'].max()], row=i//2+1, col=i%2+1)
        fig.update_yaxes(title_text='Daily deaths', row=i//2+1, col=i%2+1)
    
    # Update the layout
    fig.update_layout(title=dict(text='COVID Daily Deaths: Top 4 Regions', font=dict(size=24)),
                      height=800, width=1500, showlegend=False, title_x=0.5,
                      plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3')
    
    return fig


def top6_countries_confirmed_cases():
    
    # Filter for top 6 countries by confirmed cases
    top_6_countries = df.groupby('country')['cumulative_cases (confirmed cases)'].max().sort_values(ascending=False).head(6).index.tolist()
    df_top_6 = df[df['country'].isin(top_6_countries)]
    
    # Filter for 2020 onwards
    df_top_6 = df_top_6[df_top_6['date_reported'] >= '2020-02-01']
    
    
    # calculate daily confirmed cases
    df_top_6['daily_confirmed_cases'] = df_top_6.groupby('country')['cumulative_cases (confirmed cases)'].diff()
    
    
    # Group by country and date and sum cases
    df_top_6_grouped = df_top_6.groupby(['country', 'date_reported']).sum().reset_index()
    
    # Create subplots for each country
    fig = sp.make_subplots(rows=2, cols=3, subplot_titles=top_6_countries)
    
    # Iterate through each country and add to subplot
    for i, country in enumerate(top_6_countries):
        # Filter data for specific country
        df_country = df_top_6_grouped[df_top_6_grouped['country'] == country]
    
        # Add bar plot of confirmed cases
        fig.add_trace(
            go.Scatter(
                x=df_country['date_reported'],
                y=df_country['daily_confirmed_cases'],
                name="Confirmed Cases"
            ),
            row=(i // 3) + 1, col=(i % 3) + 1
        )
    
        # Add annotation for total cases
        total_cases = df_country['cumulative_cases (confirmed cases)'].iloc[-1]
        fig.add_annotation(
            x=df_country['date_reported'].iloc[100],
            y=df_country['daily_confirmed_cases'].max(),
            text=f"Total Cases: {total_cases}",
            showarrow=False,
            arrowhead=1,
            font=dict(color="black", size=12,),
            row = i // 3 + 1, 
            col = i % 3 + 1
            
        )

    # Update layout
    fig.update_layout(
        height=800,
        width = 1500,
        title_text="Top 6 Countries by Confirmed Cases",
        title_font=dict(size=24),
        legend=dict(title=""),
        xaxis=dict(title="Date", tickfont=dict(size=12)),
        yaxis=dict(title="Confirmed Cases", tickfont=dict(size=12)),
        showlegend=False, title_x=0.5,
                      plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3',
    )
    
    
    return fig

def view7():
    # Assuming your data is stored in a pandas DataFrame called `df`
    region_treemap = px.treemap(df, path=['region_name', 'country'], values='cases', )
    
    region_treemap.update_layout(
        title='COVID-19 Cases by Country and Region',
        font=dict(family='Arial', size=14),
        showlegend=False,
        width=1000,
        height=500,
    
        treemapcolorway=['#F6D55C', '#ED553B', '#3CAEA3', '#20639B', '#173F5F',  '#343A40'],
        # margin=dict(l=0, r=0, t=50, b=0), # Add margin to the top of the figure to make room for the title
       
        )
    
    
    
    
    df_top20 = df.groupby('country').sum().sort_values('cases', ascending=False).head(20).reset_index()
    df_top20['region_name'] = df_top20['country'].map(country_region_dict)
    df_top20 = df_top20.sort_values('cases', ascending=False)
    
    region_barplot = px.bar(df_top20, x= 'country', y='cases', color='region_name', color_discrete_sequence=px.colors.qualitative.Pastel,)
    region_barplot.update_layout(xaxis={'categoryorder':'total descending'})
    region_barplot.update_layout(
        title='COVID-19 Cases by Country and Region',
        font=dict(family='Arial', size=14),
        xaxis=dict(title='Cases'),
        yaxis=dict(title='Country'),
        showlegend=True,
        legend=dict(title='Region'),
        width=1000,
        height=800,
        margin=dict(l=0, r=0, t=50, b=0),
        plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3',
        bargap=0.1,
        )
    return region_treemap, region_barplot
# asd
def view8():
    # Create a scatter plot

    df_comp_country = df.loc[df['country'].isin(['Brazil', 'India', 'Canada', 'United States of America'])]
    
    cum_cases_line_chart = px.line(df_comp_country, x="date_reported", y="cumulative_cases (confirmed cases)", color="country",
                     title="Compare Countries Overtime", markers=True)
    cum_cases_line_chart.add_annotation(x='2020-09-09', y=4370128,
                text="INDIA",
                showarrow=True,
                arrowhead=1)
    cum_cases_line_chart.add_annotation(x='2020-08-16', y=5258565,
                text="UNITED STATES",
                showarrow=True,
                arrowhead=1)
    cum_cases_line_chart.add_annotation(x='2020-08-14', y=3164785,
                text="BRAZIL",
                showarrow=True,
                arrowhead=1)
    cum_cases_line_chart.add_annotation(x='2020-08-11', y=119451,
                text="CANADA",
                showarrow=True,
                arrowhead=1)
    cum_cases_line_chart.update_layout(
           
            title_font=dict(size=24),
            legend=dict(title=""),
            xaxis=dict(title="", tickfont=dict(size=12)),
            yaxis=dict(title="Covid 19 Cases: Confirmed", tickfont=dict(size=12)),
            showlegend=True, title_x=0.5,
                          plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3',
        )
    
    
    
    df_reg_country = df.groupby(['region_name', 'country'])['cases'].sum().reset_index().reset_index()
    
    df_region_country_sum = px.scatter(df_reg_country, x='index', y="cases", color="region_name", 
                                       hover_data=['country', 'region_name', 'cases']
                     )
    df_region_country_sum.update_traces(marker={'size': 15})
    df_region_country_sum.update_layout(
               title = "Explore Relationships",
            title_font=dict(size=24),
            legend=dict(title=""),
            xaxis=dict(title="", tickfont=dict(size=12)),
            yaxis=dict(title="Covid 19 Cases: Confirmed", tickfont=dict(size=12)),
            showlegend=True, title_x=0.5,
                          plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3',
        )
    df_region_country_sum.add_annotation(x=186, y=7341406,
                text="United States of America",
                showarrow=True,
                arrowhead=1)
    df_region_country_sum.add_annotation(x=192, y=6685082,
                text="India",
                showarrow=True,
                arrowhead=1)
    df_region_country_sum.add_annotation(x=145, y=4915289,
                text="BRAZIL",
                showarrow=True,
                arrowhead=1)
    df_region_country_sum.add_annotation(x=147, y=166156,
                text="CANADA",
                showarrow=True,
                arrowhead=1)

    
    return cum_cases_line_chart, df_region_country_sum

# asd

# cum_cases_line_chart, df_region_country_sum = view8()

# plot(df_region_country_sum)


# plot(cum_cases_line_chart)

# region_treemap, region_barplot = view7
# plot(region_treemap)

# plot(region_barplot)


# plot(deaths_by_regions())


# plot(top6_countries_confirmed_cases())


# view 1
# Group the data by country to get the cumulative confirmed cases
df_cumulative = df.groupby(['country'])['cumulative_cases (confirmed cases)'].max().reset_index()

# Create a Plotly figure showing a choropleth map of the cumulative confirmed cases
world_map_covid = px.choropleth(df_cumulative, locations='country', locationmode='country names', color='cumulative_cases (confirmed cases)',
                    hover_name='country', range_color=[0, max(df_cumulative['cumulative_cases (confirmed cases)'])],
                    title='Confirmed Cases Cumulative Around the World')


# View 2
# Group the data by country to get the total cases, cases newly reported, deaths total, and deaths newly reported
df_country = df.groupby(['country'])['cumulative_cases (confirmed cases)', 'cases', 'cumulative_deaths (confirmed deaths)', 'deaths'].max().reset_index()

# Pivot the data to create a table showing the total cases, cases newly reported, deaths total, and deaths newly reported by country
table = pd.pivot_table(df_country, values=['cumulative_cases (confirmed cases)', 'cases', 'cumulative_deaths (confirmed deaths)', 'deaths'], index='country', aggfunc='sum')

# Sort the table by the _Cumulative_cases_(confirmed_cases) column in descending order
table = table.sort_values(by='cumulative_cases (confirmed cases)', ascending=False)


# fig=px.bar(df,x="date_reported",y="deaths")
# fig.show()


# region_mapper = {
#     'EMRO': 'Eastern Mediterranean Region',
#     'EURO': 'European Region',
#     'AFRO': 'African Region',
#     'WPRO': 'Western Pacific Region',
#     'AMRO': 'Region of the Americas',
#     'SEARO': 'South-East Asia Region',
#     'Other':'Other'
# }

# df['region_name'] = df['region'].map(region_mapper)

# df_region_total = df.groupby('region_name')['cases'].sum().sort_values(ascending=False).reset_index()
# df_region_total = df_region_total.loc[df_region_total['region_name']!='Other']

# region_hbarplot = px.bar(df_region_total, x="cases", y="region_name",
#                         text=[f"{region}: {cases}" for region, cases in zip(df_region_total['region_name'], df_region_total['cases'])],
#                           labels={'cases': 'Total Cases', 'region_name': 'Region'},

#                           color='region_name', orientation='h')


# # update plot layout
# region_hbarplot.update_layout(title='Region-wise Total Cases')
# plot(region_hbarplot)














































