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
components.html(
        """
       <html>
<style>
.navbar {
    display: flex;
    justify-content: flex-start;
    align-items: center;
     padding: 20px;
  background-color: 	#cccccc;
  border:1px solid #000;
  border-radius : 30px
}
a {
  display: block;
  padding: 8px;
  background-color: #cccccc;
  margin-left:20px;
  border:1px solid #000;
  border-radius : 15px
}
b {
   display: block;
  padding: 8px;
  background-color: 	#cccccc;
  margin-left :20px;
  border:0;
  border-radius : 15px;
  font-family: Sans-serif;
   font-size: 14px;
  }
</style>


<body>

<div class='navbar'>
    <a><img src="http://www4.comp.polyu.edu.hk/~csi_inception/img/logos/polyuLogo.png" style=" float:centre; margin:0px 0px 15px 15px;cursor:pointer; cursor:hand; border:0" width="500" height="100" alt="polyu" /></a>

    <a><img src="https://www.polyu.edu.hk/lsgi/uusspec/images/headers/lsgi-logo.0104e4fbcd4f.png" style=" float:centre; margin:0px 0px 15px 15px;cursor:pointer; cursor:hand; border:0" width="500" height="100" alt="polyu" /></a>
    <b><h1>Data Management Platform for Qleak, Tsing Yi </h1></b>
    
</div>
</body>
</html>""",height = 200)



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
    now_date_time = datetime.now() +  timedelta(hours = 8)
    
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
        
    elif mode == 'Real Time': 
    

        if T =="Past 1 hour":
            endtime = str(now_date_time.strftime('%Y-%m-%d+%H:%M'))
            starttime = str(last_hour_date_time.strftime('%Y-%m-%d+%H:%M'))
        elif T =="Past 24 hours" :
            endtime = str(now_date_time.strftime('%Y-%m-%d+%H:%M'))
            starttime = str(last_24hour_date_time.strftime('%Y-%m-%d+%H:%M'))
    
    else: 

        if T =="Past 1 hour":
            SIM_date_time = last_hour_date_time - timedelta(minutes = 2) 
            SIM_END = now_date_time - timedelta(minutes = 2)
            starttime = str(SIM_date_time.strftime('%Y-%m-%d+%H:%M'))
            endtime = str(SIM_END.strftime('%Y-%m-%d+%H:%M'))
        if T =="Past 24 hours":
            SIM_date_time = last_24hour_date_time - timedelta(minutes = 2) 
            SIM_END = now_date_time - timedelta(minutes = 2)
            starttime = str(SIM_date_time.strftime('%Y-%m-%d+%H:%M'))
            endtime = str(SIM_END.strftime('%Y-%m-%d+%H:%M'))
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
def format_date_for_dataframe(raw):
    y = int(raw[6:10])
    mo = int(raw[3:5])
    d = int(raw[0:2])
    t = raw[11:].split(':')
    h = int(t[0])
    m = int(t[1])
    print (m)
    x = datetime.datetime(y, mo, d,h,m)
    
    
    
    return x
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
                formated_date = format_date_for_dataframe(raw_date)
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
    
    
def Compute_Moving_Average(window,source):
    i = 0
    MA_list = []
    for each in source:
        if i >window :
            MA = (sum(source[int(i-window):i]))/window
            MA_list.append(MA)  
        i+=1
    for ii in range(window+1):
        MA_list.insert(ii,MA_list[0])
    return MA_list

def LS_Prediction(y,Deg):
    X = []
    
    for i in range(len(y)):
        X.append(i)
 
   
        
    poly = np.polyfit(X, y, deg=Deg)
    
    return poly
def main(P,T,N,window,data_mode,Deg):
    

    x = 2

    
    if x ==2:
        print("Once")
        current_time = datetime.datetime.now()
        st.metric('Request Time : ', current_time.strftime("%d/%m/%Y, %H:%M:%S"))
        data = download_data(data_mode,P,T,N)
        
        
        status = check_downloaded(data)
        if status:
            print ("ok")
        else: 
            st.write("Oh, there are errors so data is not available.")
            
        node_list = open_file(data,N)
        
        df = data_cleaning (node_list)
        
        col1,col2= st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.metric('Moving Average Time Window : ',window )
            st.metric('Time Period :', add_selectbox1)
            st.metric("GV : ",user_input)
            
        
           
        
        
        
        ndf = df[["flow_pressure","Flow_Rate"]]
        hd = [ df['flow_pressure'].tolist(), df['Flow_Rate'].tolist()]
        ndf.index = df['Time'].tolist()
        
        
        
       
        df_p = df["flow_pressure"].to_frame()
        df_r = df["Flow_Rate"].to_frame()
        
        
        
        MA_source_P =  df['flow_pressure'].tolist()
        MA_source_R =  df['Flow_Rate'].tolist()
        
        MA_P = Compute_Moving_Average(window,MA_source_P)
        MA_R = Compute_Moving_Average(window,MA_source_R)
        
        
        
        
        df_p['MA'] = MA_P
        df_r['MA'] = MA_R
        
        df_p_poly = LS_Prediction(MA_P,Deg)
        df_r_poly = LS_Prediction(MA_R,Deg)
        
        df_p['Fitting'] = np.polyval(df_p_poly, df_p.index)
        df_r['Fitting'] = np.polyval(df_r_poly, df_r.index)
        
        
        
        x_data = np.arange(0,len(MA_P))
        print(x_data)
          
        y_data = MA_P
        print(y_data)
        
        ylog_data = np.log(y_data)
        print(ylog_data)
          
        curve_fit = np.polyfit(x_data, ylog_data, 1)
        print(curve_fit)
        
        y = np.exp(curve_fit[1]) * np.exp(curve_fit[0]*x_data)
  
        print(y)
        df_p['log'] = y
        df_p.index = df['Time'].tolist()  
        df_r.index = df['Time'].tolist()
        
        st.subheader('Historical Pressure Data of : '+N)
      
       
      

        
        st.line_chart(df_p,height=800,width=1600)
        st.write('The computed unknow parameters of the polynimoal is : ')
        st.text(df_p_poly)
        st.subheader('Historical Flow Rate Data of : '+N)
        
        
        st.line_chart(df_r,height=800,width=1600)
        st.write('The computed unknow parameters of the polynimoal is : ')
        st.text(df_r_poly)
        
        #result = LS_Prediction(MA_R,Deg,1)
        #st.line_chart(result,height=800,width=1600)
            

    
st.sidebar.header("Select the operation mode : ")
genre = st.sidebar.radio(
     "Mode:",
     ('Real-time visualization', 'Adding remark', 'Historical Data','Developing : NLC'))

if genre == 'Adding remark':
    with st.container():
        

    # You can call any Streamlit command, including custom components:
        components.html(
        """
         <style>
      iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: 0
       
}
      
    </style>
        <iframe  height="1000" src="https://lsgi-polyu.maps.arcgis.com/apps/webappviewer/index.html?id=a5e83eebf5b546cd98de4ba633f27ef2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """
        ,height=1200)
    
elif genre == 'Real-time visualization':

     

     with st.container():
        

    # You can call any Streamlit command, including custom components:
        components.html(
        """
         <style>
      iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: 0;
      }
    </style>
        <iframe width="2000" height="1000" src="https://lsgi-polyu.maps.arcgis.com/apps/dashboards/9d4c608d6f6a47aba56cdf1704248090" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen ></iframe>
        """
        ,height=1200
    )
        
elif genre == 'Historical Data':
    
    st.title('Get Historical Data')


    add_selectbox1 = st.selectbox(
    "Please select the time period: ",
    ("Past 1 hour", "Past 24 hours")
)

    user_input = st.text_input("Please select GV : ", "GV72")
    window = st.slider('Time Window of Moving Average (minutes)', 0, 60, 10)
    Deg = st.slider('Degree of Polynomial', 0, 10, 3)
    data_mode = st.radio(
     "Data Mode : ",
     ('Real Time', 'Simulated Time','Real Time with 2 mins latency'))
    if st.button('Get Data'):
        main('',add_selectbox1,user_input,window,data_mode,Deg)

elif genre == 'Developing : LNC':

     

     with st.container():
        

    # You can call any Streamlit command, including custom components:
        components.html(
        """
         <style>
      iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: 0;
      }
    </style>
        <iframe width="2000" height="1000" src="https://en.wikipedia.org/wiki/Leak_noise_correlator" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen ></iframe>
        """
        ,height=1200
    )
        


    
