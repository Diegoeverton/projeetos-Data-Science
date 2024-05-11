import streamlit as st
import time 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# https://github.com/Data-Science-at-SWAST/handover_poc

st.set_page_config(page_title='Tempoo de ambulancias',
                   layout='wide',
                   page_icon='swast_handove_delay/images/ambulance.png')

t1, t2 = st.columns((0.07,1))

t1.image('images/ambulance.png')
t2.title('Sergiço de ambulacias - Report hospital de handover')
t2.markdown(" **tel:** 234234234**| site: dsgfasdgsadfgfdgs **| email: ** afdfasdfaf@sfdfasdf")


with st.spinner('Updating Report...'):

    hosp_df = pd.read_excel("DataforMock.xlsx", sheet_name="Hospitals")
    hosp = st.selectbox('Esc9olha o hospital', hosp_df, help = 'Filtre o relatorio para moistrar um hospital')

    m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))

    todf = pd.read_excel('DataforMock.xlsx', sheet_name='metrics')
    to = todf[(todf['Hospital Attended'] == hosp) & (todf['Metric'] == 'Total Outstanding')]
    ch = todf[(todf['Hospital Attended'] == hosp) & (todf['Metric'] == 'Current Handover Average Mins')]
    hl = todf[(todf['Hospital Attended'] == hosp) & (todf['Metric'] == 'Hours Lost to Handovers Over 15 Mins')]

    m1.write('')
    m2.metric(label = 'Total Outstanding Handovers',
              value = int(to['Value']),
              delta = str(int(to['Previous']))+' Compared tp 1 hour ago',
               delta_color='inverse')
    m3.metric(label = 'Current Handover Average',
              value = str(int(ch['Value']))+ ' Mins',
              delta= str(int(ch['Previous']))+ ' Compared to 1 hour ago',
              delta_color='inverse')
    m4.metric(label = 'Time lost today (above 15 MIns)',
             value = str(int(hl['Value']))+ ' Hours', 
             delta = str(int(hl['Previous']))+' Compared to yesterday')
    m1.write('')

    # NUmber of completed Handovers by hour
    g1, g2, g3 = st.columns((1,1,1))
    fgdf = pd.read_excel('DataforMock.xlsx', sheet_name='Graph')
    fgdf = fgdf[fgdf['Hospital Attended'] == hosp]

    fig = px.bar(
        fgdf,
        x = 'Arrived Destination Resolved', y = 'Number of Handovers',
        template = 'seaborn')
    fig.update_traces(marker_color = '#264653')
    fig.update_layout(title_text = 'Number completed Handovers by hour',
                      title_x =0, 
                      margin = dict(
                          l=0,
                          r=10,
                          b=10,
                          t=30
                      ),
                      yaxis_title= None, xaxis_title = None)
    g1.plotly_chart(fig, use_container_width=True)

    # Predicted N*mber Arrivals
    fcst = pd.read_excel('DataforMock.xlsx', sheet_name='Forecast')
    fcst = fcst[fcst['Hospital Attended'] == hosp]

    fig = px.bar(
        fcst,
        x = 'Arrived Destination Resolved', y = 'y', template='seaborn'
    )
    fig.update_traces(marker_color = '#7A9E9F')
    fig.update_layout(title = 'Predicted Number of Arrivals',
                      title_x = 0, 
                      margin = dict(l=0, r=10, b=10, t=30),
                      yaxis_title=None,
                      xaxis_title=None)
    g2.plotly_chart(fig, use_container_width=True)

    # Average Completed Duration by Hour
    fig = px.bar(fgdf,
                 x='Arrived Destination Resolved',
                 y='Average Duration',
                 color='Average Duration',
                 template = 'seaborn',
                 color_continuous_scale=px.colors.diverging.Temps)
    fig.add_scatter(x=fgdf['Arrived Destination Resolved'],
                    y=fgdf['Target'],
                    mode='lines',
                    line= dict(color='black'),
                    name='Target')
    fig.update_layout(title_text='Average Completed Handover Duration by Hour',
                      title_x=0, margin = dict(l=0, r=10, b=10, t=30),
                      yaxis_title=None,
                      xaxis_title=None,
                      legend = dict(orientation="h", yanchor= "bottom", y=0.9, xanchor="right", x=0.99))

    g3.plotly_chart(fig, use_container_width=True)

    # wainting Hando vers table
    cw1, cw2 = st.columns((2.5, 1.7))

    whdf = pd.read_excel('DataforMock.xlsx', sheet_name='WaitingHandovers')

    colourcode = []

    for i in range(0,9):
        colourcode.append(whdf['c'+str(i)].tolist())

    whdf = whdf[['Hospital Attended ',	'Expected',	'Inbound ',	'Arrived ',	'Waiting',	'0 - 15 Mins',	'15 - 30 Mins ',	'30 - 60 Mins ',	'60 - 90 Mins',	'90 + Mins ',
]]
    
    
    fig= go.Figure(
        data = [go.Table(columnorder= [0,1,2,3,4,5,6,7,8,9], columnwidth= [30,10,10,10,10,15,15,15,15],
                         header = dict(
                             values = list(whdf.columns),
                             font = dict(size=12, color ='white'),
                             fill_color = 'rgba(255,255,255,0.2)',
                             align = ['left', 'center'],
                             #text wraping
                             height=20
                         ),
                         cells=dict(
                             values = [whdf[K].tolist() for K in whdf.columns],
                             font = dict(size=12),
                             align = ['left', 'center'],
                             fill_color = colourcode,
                             line_color = 'rgba(255,255,255,0.2)',
                             height=20))])
    fig.update_layout(title_text='Current Waiting Handover', title_font_color = '#264653', title_x=0,
                      margin = dict(l=0, r=10, b=10, t=30), height=480)
    cw1.plotly_chart(fig, use_container_width=True)

    # Current Wainting tabele
    cwdf = pd.read_excel('DataforMock.xlsx', sheet_name='CurrentWaitingCallsigns') 

    if hosp == 'All':
        cwdf = cwdf
    elif hosp != 'All':
        cwdf = cwdf[cwdf['Hospital Attended'] == hosp]
    
    fig = go.Figure(
        data = [go.Table (columnorder = [0,1,2,3], columnwidth = [15, 40,20,],
                          header = dict (
                              values = list(cwdf.columns),
                              font=dict(size=12, color='white'),
                              fill_color = '#264653',
                              align = 'left',
                              height=20
                          )
                          ,cells = dict(
                              values=[cwdf[K].tolist() for K in cwdf.columns],
                              font=dict(size=12),
                              align = 'left',
                              fill_color = '#f0f2f6',
                              height=20))])
    fig.update_layout(title_text='Current Waiting Cellsigns', title_font_color = '#264653',
                      title_x=0, margin=dict(l=0, r=10,b=10,t=30), height=480)
    cw2.plotly_chart(fig, use_container_width=True)


