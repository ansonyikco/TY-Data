# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 13:56:55 2021

@author: lsgi_util_lab
"""
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import numpy as np
import os.path, time
import os
import datetime
import webbrowser
import csv
import re
import pandas as pd
import glob

import requests
st.set_page_config(layout="wide")

col1, col2, col3 = st.columns(3)

with col1:
    components.html(
        """
        
        <img src="http://www4.comp.polyu.edu.hk/~csi_inception/img/logos/polyuLogo.png" style=" float:centre; margin:0px 0px 15px 15px;cursor:pointer; cursor:hand; border:0" width="500" height="100" alt="polyu" />
        """
        ,height=120
    )

with col2:
   st.title('TY Data Management')

with col3:
    components.html(
        """
        
        <img src="https://www.polyu.edu.hk/lsgi/uusspec/images/headers/lsgi-logo.0104e4fbcd4f.png" style=" float:centre; margin:0px 0px 15px 15px;cursor:pointer; cursor:hand; border:0" width="500" height="100" alt="polyu" />
        """
        ,height=120
    )
    

import time

from PIL import Image

@st.cache


    
    
def check_downloaded(data):
    if "Error" in data: 
        status = False
    else :
        status = True 
        
    return status
    


def download_data(mode,P,T,gv):

    
    if gv != "all": gv = "site:"+gv
        
    from datetime import datetime, timedelta
    last_hour_date_time = datetime.now() - timedelta(hours = 1)
    last_24hour_date_time = datetime.now() - timedelta(hours = 24)
    now_date_time = datetime.now()
    
    st.write(str(now_date_time.strftime('%Y-%m-%d+%H:%M')))

    if mode =="Simulated Time" :
        if T =="Past 1 hour":
            SIM_date_time = datetime.now() - timedelta(hours = 241) +timedelta(hours = 8) 
            SIM_END = SIM_date_time + timedelta(hours = 1)
            starttime = str(SIM_date_time.strftime('%Y-%m-%d+%H:%M'))
            endtime = str(SIM_END.strftime('%Y-%m-%d+%H:%M'))
        if T =="Past 24 hours":
            SIM_date_time = datetime.now() - timedelta(hours = 240) -  timedelta(hours = 24) +timedelta(hours = 8)
            SIM_END = SIM_date_time + timedelta(hours = 24)
            starttime = str(SIM_date_time.strftime('%Y-%m-%d+%H:%M'))
            endtime = str(SIM_END.strftime('%Y-%m-%d+%H:%M'))
        
    else: 
    

        if T =="Past 1 hour":
            endtime = str(now_date_time.strftime('%Y-%m-%d+%H:%M'))
            starttime = str(last_hour_date_time.strftime('%Y-%m-%d+%H:%M'))
        elif T =="Past 24 hours" :
            endtime = str(now_date_time.strftime('%Y-%m-%d+%H:%M'))
            starttime = str(last_24hour_date_time.strftime('%Y-%m-%d+%H:%M'))
    
    
    url = "http://59.148.216.10/datagate/api/DataExportAPI.ashx?format=csv&user=lsgi&pass=P@ssw0rd&logger="+gv+"&period=5&startdate="+starttime+"&enddate="+endtime+"&flowunits=1&pressureunits=1&enablestitching=True&interval=1"
    print (url)
    r = requests.post(url)
    print (r.text)
    return r.text

def data_simulator(item):
    data = "Site,"+item+",s,s"+item+"\n"
    return data 
def open_file(lines,item):

    node_list = []
    if item != 'all':
        lines = data_simulator(item)+lines

    GV_data = lines.split("Site,")
    for each in GV_data:    
        if "GV" in each or "FM" in each:
            each = re.split(',|\*|\n|\r\n',each)
            
            node_list.append(each)
    return node_list
def format_date_for_arcgis(raw):
    y = raw[6:10]
    m = raw[3:5]
    d = raw[0:2]
    t = raw[11:]
    return (y+"-"+m+"-"+d+" "+t)
def data_cleaning (node_list):
    date_time = []
    flow_pressure = []
    Flow_Rate = []
    GV = []

    time_index = []
    
    for each in node_list:
        epoch_number = (len(each)-8)/4
        if epoch_number>=1 :
            for i in range(int(epoch_number)):
                time_index.append(int(epoch_number)-i-1)
                raw_date = (each[7+(i)*4])
                formated_date = format_date_for_arcgis(raw_date)
                date_time.append(formated_date)
                flow_pressure.append(float(each[8+(i)*4]))
                Flow_Rate.append(float (each[9+(i)*4]))
                GV.append(each[0])
     
                
            
        else:
            st.header ("Quite : " +str(each[0])+'\n')
                
    df = pd.DataFrame(list(zip(GV, date_time,flow_pressure,Flow_Rate,time_index)),
               columns =["GV","Time","flow_pressure","Flow_Rate","Update_Ranking"])
    
    df.to_csv('file_name.csv', encoding='utf-8')
    gkk = df.groupby(['Time'])
    
    return df
    
    
    


def main(P,T,N):
    

    x = 2

    
    if x ==2:
        print("Once")
        current_time = datetime.datetime.now()
        data = download_data("Simulated Time",P,T,N)
        st.write("Downloading Data")
        
        status = check_downloaded(data)
        if status:
            print ("ok")
        else: 
            st.write("Oh, there are errors so data is not available.")
            
        node_list = open_file(data,N)
        
        df = data_cleaning (node_list)
        st.write(df)
        df_p = df["flow_pressure"]
        df_r = df["Flow_Rate"]
        hd = [ df['flow_pressure'].tolist(), df['Flow_Rate'].tolist()]
        df_p.index = df['Time'].tolist()
        df_r.index = df['Time'].tolist()
        
        st.subheader('Historical Data of : '+N)
        
       
      

        import altair as alt
        chart = alt.Chart(df_p).mark_line().encode(
            x=alt.X('Time', axis=alt.Axis(labelOverlap="greedy",grid=False)),
            y=alt.Y('ODO'))
        st.altair_chart(chart, use_container_width=False)
        
        st.line_chart(df_p,height=400,width=1600)
        
        
        
        st.line_chart(df_r,height=400,width=1600)
        
        
        

    
st.header("Select the operation mode : ")
genre = st.radio(
     "Mode:",
     ('Real-time visualization', 'Adding remark', 'Historical Data'))

if genre == 'Adding remark':
    with st.container():
        

    # You can call any Streamlit command, including custom components:
        components.html(
        """
        
        <iframe width="2000" height="1000" src="https://lsgi-polyu.maps.arcgis.com/apps/webappviewer/index.html?id=a5e83eebf5b546cd98de4ba633f27ef2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """
        ,height=1200
    )
    
elif genre == 'Real-time visualization':

     

     with st.container():
        

    # You can call any Streamlit command, including custom components:
        components.html(
        """
        
        <iframe width="2000" height="1000" src="https://lsgi-polyu.maps.arcgis.com/apps/dashboards/9d4c608d6f6a47aba56cdf1704248090" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen ></iframe>
        """
        ,height=1200
    )
        
else: 
    st.sidebar.title('Get Historical Data')


    add_selectbox1 = st.sidebar.selectbox(
    "Please select the time period: ",
    ("Past 1 hour", "Past 24 hours")
)

    user_input = st.sidebar.text_input("Please select GV : ", "all")
    if st.sidebar.button('Get Data'):

        st.sidebar.write('Time Period :', add_selectbox1)
        st.sidebar.write("GV : "+user_input)
        main('',add_selectbox1,user_input)


