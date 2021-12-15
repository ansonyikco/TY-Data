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
#import plotly.figure_factory as ff
import matplotlib 
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


    
    
def check_downloaded(current_time):
    
    path = 'C:\\Users\lsgi_util_lab\Downloads'
    current_min = current_time.minute
    current_hour = current_time.hour
    current_day = current_time.day
    current_month = current_time.month
    current_year = current_time.year
    
    list_of_files = glob.glob(path+'/*.txt') +glob.glob(path+'/*.csv')# * means all if need specific format then *.csv
    
    latest_file = max(list_of_files, key=os.path.getctime)
    
    created = os.path.getctime(latest_file)
    
    year,month,day,hour,minute,second=time.localtime(created)[:-3]
    
    

    if minute >= current_min and hour>=current_hour and day>=current_day and month>=current_month and year>=current_year :
        print("file downloaded after click"+'\n')
        return latest_file
    else: 
        return "No file downloaded"


def download_data(mode,P,T,gv):

    
    if gv != "all": gv = "site:"+gv
        
    from datetime import datetime, timedelta
    last_hour_date_time = datetime.now() - timedelta(hours = 1)
    last_24hour_date_time = datetime.now() - timedelta(hours = 24)
    now_date_time = datetime.now()
    
    st.write(str(now_date_time.strftime('%Y-%m-%d+%H:%M')))

    if mode =="Simulated Time" :
        if T =="Past 1 hour":
            SIM_date_time = datetime.now() - timedelta(hours = 241) 
            SIM_END = SIM_date_time + timedelta(hours = 1)
            starttime = str(SIM_date_time.strftime('%Y-%m-%d+%H:%M'))
            endtime = str(SIM_END.strftime('%Y-%m-%d+%H:%M'))
        if T =="Past 24 hours":
            SIM_date_time = datetime.now() - timedelta(hours = 240) -  timedelta(hours = 24)
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
    webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
    webbrowser.get('chrome').open(url,new=0)

def data_simulator(fn,item):
    data = "Site,"+item+",s,s"+item+"\n"
    return data 
def open_file(filename,item):

    node_list = []
    with open(filename) as f:
        lines = f.read()
        if 'export' not in filename :
            lines = data_simulator(filename,item)+lines
            
        
    GV_data = lines.split("Site,")
    for each in GV_data:
        if "GV" in each or "FM" in each:
            each = re.split(',|\*|\n',each)
            
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
    while x ==1:
        current_time = datetime.datetime.now()
        if current_time.minute%5 ==0:
        
            download_data()
            time.sleep(40)
            file = check_downloaded(current_time)
            
            node_list = open_file(file)
            df = data_cleaning (node_list)
            print (df)
            time.sleep(20)
            
        else:
            time.sleep(30)
    
    if x ==2:
        print("Once")
        current_time = datetime.datetime.now()
        download_data("Simulated Time",P,T,N)
        st.write("Downloading Data")
        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.2)
            my_bar.progress(percent_complete + 1)
        my_bar.empty()
        
        file = check_downloaded(current_time)
        
        node_list = open_file(file,N)
        df = data_cleaning (node_list)
        st.write(df)
        ndf = df[["flow_pressure","Flow_Rate"]]
        hd = [ df['flow_pressure'].tolist(), df['Flow_Rate'].tolist()]
        ndf.index = df['Time'].tolist()
        st.subheader('Historical Data of : '+N)
        
       
        import plotly.express as px

        
        fig = px.line(df, x='Time', y="flow_pressure")
        fig.update_layout(height=400,width=1600)

        
        st.plotly_chart(fig,height=400,width=1600)
        
        
        fig1 = px.line(df, x='Time', y="Flow_Rate")
        fig1.update_layout(height=400,width=1600)
        fig1.update_yaxes(autorange=True)
        st.plotly_chart(fig1,height=400,width=1600)
        
        
        
        
            

    # You can call any Streamlit command, including custom components:
 
    # Some number in the range 0-23
       
        
        










    
    
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




    
