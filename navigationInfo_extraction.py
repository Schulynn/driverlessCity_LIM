# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 10:57:55 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""
import math
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

import sqlite3
from sqlite3 import Error

#01-read coordinates data of landmarks 读取landmarks坐标值
def readMatLabFig_LandmarkMap(LandmarkMap_fn):
    LandmarkMap=loadmat(LandmarkMap_fn, squeeze_me=True, struct_as_record=False)
    y=loadmat(LandmarkMap_fn)
    print(sorted(LandmarkMap.keys()))
        
    LandmarkMap_dic={} #提取.fig值
    for object_idx in range(LandmarkMap['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=LandmarkMap['hgS_070000'].children.children[object_idx].properties.XData #good
            Y=LandmarkMap['hgS_070000'].children.children[object_idx].properties.YData 
            LandmarkMap_dic[object_idx]=(X,Y)
        except:
            pass
    
    # print(LandmarkMap_dic)
    fig= plt.figure(figsize=(130,20))
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    i=0
    for key in LandmarkMap_dic.keys():
        plt.scatter(LandmarkMap_dic[key][1],LandmarkMap_dic[key][0], s=dotSizes[i],marker=markers[i], color=colors[i],linewidth=linewidths[i])
        i+=1
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    return LandmarkMap_dic

#02-read PHMI values for evaluation of AVs' on-board lidar navigation 读取PHMI值
#the PHMI value less than pow(10,-5) is scaled to show clearly------on; the PHMI value larger than pow(10,-5) is scaled to show clearly------on
#数据类型A
def readMatLabFig_PHMI_A(PHMI_fn,LandmarkMap_dic):
    PHMI=loadmat(PHMI_fn, squeeze_me=True, struct_as_record=False)
    x=loadmat(PHMI_fn)
    print(sorted(PHMI.keys()))
    
    PHMI_dic={} #提取MatLab的.fig值
    ax1=[c for c in PHMI['hgS_070000'].children if c.type == 'axes']
    if(len(ax1) > 0):
        ax1 = ax1[0]
    i=0
    for line in ax1.children:
        # print(line)
    # for object_idx in range(PHMI['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=line.properties.XData #good   
            Y=line.properties.YData 
            Z=line.properties.ZData
            PHMI_dic[i]=(X,Y,Z)
        except:
            pass
        i+=1
    
    # print(PHMI2_dic)
    fig= plt.figure(figsize=(130,20)) #figsize=(20,130)
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    
    ScalePhmi=math.pow(10,1)    
    plt.plot(PHMI_dic[0][1],PHMI_dic[0][0],marker=markers[0], color=colors[0],linewidth=linewidths[0])  
    ref=math.pow(10,-5)
    
    #for display clearly
    PHmiValue=PHMI_dic[1][2]
    replaceValue=np.extract(PHmiValue<ref,PHmiValue)*-math.pow(10,5)
    PHmiValue[PHmiValue<ref]=replaceValue
    plt.plot( PHMI_dic[0][1],PHmiValue*ScalePhmi,marker=markers[0], color=colors[1],linewidth=1)
    
    # plt.plot(PHMI_dic[1][2]*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    #plt.axvline(x=ref*ScalePhmi)
    plt.axhline(y=ref*ScalePhmi)
    
    plt.scatter(LandmarkMap_dic[1][1],LandmarkMap_dic[1][0],marker=markers[1], s=dotSizes[1],color=colors[2],linewidth=10)
    
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    
    return PHMI_dic

#数据类型B
def readMatLabFig_PHMI_B(PHMI_fn,LandmarkMap_dic):
    PHMI=loadmat(PHMI_fn, squeeze_me=True, struct_as_record=False)
    x=loadmat(PHMI_fn)
    print(sorted(PHMI.keys()))
    
    PHMI_dic={}
    for object_idx in range(PHMI['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=PHMI['hgS_070000'].children.children[object_idx].properties.XData #good
            Y=PHMI['hgS_070000'].children.children[object_idx].properties.YData 
            Z=PHMI['hgS_070000'].children.children[object_idx].properties.ZData
            PHMI_dic[object_idx]=(X,Y,Z)
        except:
            pass
    
    # print(PHMI2_dic)
    fig= plt.figure(figsize=(130,20)) #figsize=(20,130)
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    
    ScalePhmi=math.pow(10,1)
    
    plt.plot(PHMI_dic[0][1],PHMI_dic[0][0],marker=markers[0], color=colors[0],linewidth=linewidths[0])    
    
    ref=math.pow(10,-5)
    
    #for display clearly
    PHmiValue=PHMI_dic[1][2]
    replaceValue=np.extract(PHmiValue<ref,PHmiValue)*-math.pow(10,5)
    PHmiValue[PHmiValue<ref]=replaceValue
    plt.plot( PHMI_dic[0][1],PHmiValue*ScalePhmi,marker=markers[0], color=colors[1],linewidth=1)
    
    # plt.plot(PHMI_dic[1][2]*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    #plt.axvline(x=ref*ScalePhmi)
    plt.axhline(y=ref*ScalePhmi)
    
    plt.scatter(LandmarkMap_dic[1][1],LandmarkMap_dic[1][0],marker=markers[1], s=dotSizes[1],color=colors[2],linewidth=10)
    
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    
    return PHMI_dic


'''
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
'''

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
#create database and table
def main():
    database = r"./database/driverlesscity_sqlit.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


#insert     
def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid   

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

#update
def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    
#select all rows 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    for row in rows:
        print(row)

#select rows by priority
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
        
#delete by ID
def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()        

#delete all rows
def delete_all_tasks(conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    
    
def delete_tables(conn,tables):
    for table in tables:
        sql='DROP TABLE %s'%table
        with conn:
            cursor=conn.cursor()
            cursor.execute(sql)      
        
    
    
def driverlessCity_info_coordiANDphmi_2sqlite(conn,lon,lat,location_x,location_y,phmi):
    location_phmi=np.stack((location_x,location_y,phmi),axis=-1)
    landmark=np.stack((lon,lat),axis=-1)
    with conn:
        conn.executemany("insert into table_location_phmi(location_x, location_y,phmi) values (?,?,?)",location_phmi)
        conn.executemany("insert into table_landmark(lon, lat) values (?,?)",landmark)
        
        conn.commit()
        

#select all rows 
def select_table_allRows(conn,table):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s"%table)

    rows = cur.fetchall()

    return rows 
    
        
if __name__=="__main__":
    '''
    navigation_info_fp=[
                {"landmark":r'./data/04-10-2020_312LM_LM.fig',
                "phmi":r"./data/04-10-2020_312LM_PHMI.fig"
                },
        ]
    
    
    dat=navigation_info_fp[0]
    landmarks_fn=dat["landmark"]
    phmi_fn=dat["phmi"]   
    LandmarkMap_dic=readMatLabFig_LandmarkMap(landmarks_fn)
    try:
        PHMI_dic=readMatLabFig_PHMI_A(phmi_fn,LandmarkMap_dic)
        print("applied type -A")
    except:
        PHMI_dic=readMatLabFig_PHMI_B(phmi_fn,LandmarkMap_dic)
        print("applied type -B")    
    '''   
#-----------------------------------------------------------------------------    
    '''
    main()    
    conn = create_connection(database)
    # with conn:
    #     # create a new project
    #     project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    #     project_id = create_project(conn, project)        
    
    #     # tasks
    #     task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
    #     task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

    #     # create tasks
    #     create_task(conn, task_1)
    #     create_task(conn, task_2)    
    
    # with conn:
    #     update_task(conn, (2, '2015-01-04', '2015-01-06', 2))
    
    
    # with conn:
    #     print("1. Query task by priority:")
    #     select_task_by_priority(conn, 1)

    #     print("2. Query all tasks")
    #     select_all_tasks(conn)        
    
    # with conn:
    #     delete_task(conn, 2);
    #     delete_all_tasks(conn);        
    
    #delete table
    # with conn:
    #     cursor=conn.cursor()
    #     cursor.execute("DROP TABLE tasks")
    #     cursor.execute("DROP TABLE projects")
    '''
    
    
    #A- create sqlite database
    database = r"./database/driverlesscity_sqlit.db"
    conn = create_connection(database)
    
    # delete_tables(conn,tables=['table_location_phmi','sql_create_tasks_table'])
    
    '''
    # create tables
    sql_create_location_table = """ CREATE TABLE IF NOT EXISTS table_location_phmi(
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        location_x REAL,
                                        location_y REAL,
                                        phmi REAL
                                    ); """

    sql_create_landmarks_table = """CREATE TABLE IF NOT EXISTS table_landmark (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    lon REAL,
                                    lat REAL                                   
                                );"""      
    if conn is not None:
        # create table_location_phmi
        create_table(conn, sql_create_location_table)

        # create table_landmarks
        create_table(conn, sql_create_landmarks_table)
    else:
        print("Error! cannot create the database connection.")    

    

    
    lon=LandmarkMap_dic[1][0]
    lat=LandmarkMap_dic[1][1]
    location_x=PHMI_dic[0][0]
    location_y=PHMI_dic[0][1]
    phmi=PHMI_dic[1][2]
    driverlessCity_info_coordiANDphmi_2sqlite(conn,lon,lat,location_x,location_y,phmi)
    '''
    
    pts_attribute=select_table_allRows(conn,"pts_attri")
    print(pts_attribute)





    import plotly.graph_objects as go
    
    import plotly.io as pio
    #pio.renderers.default = 'svg'
    pio.renderers.default = 'browser'    
    
    import pandas as pd
    location_phmi_df=pd.DataFrame({"locationX":location_x,"locationLonY":location_y,"phmi":phmi})
    landmark_pts=pd.DataFrame({"landmarkX":lon,"landmarkY":lat,"attribute":[0]*len(lon)})
    pts_new=pd.DataFrame([[i[1],i[2],i[4]] for i in  pts_attribute],columns=['x','y','attri'])
    
    # import plotly.express as px
    # import plotly.graph_objects as go
    # fig = go.Figure()
    # fig.add_trace( go.scatter(landmark_pts, x="landmarkX", y="landmarkY", color="attribute", hover_data=['attribute'])) #size='petal_length',
    # fig.add_trace( go.scatter(pts_new, x="x", y="y", color="attri", hover_data=['attri'])) 
    
    
    
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(landmark_pts.landmarkY,landmark_pts.landmarkX,  'ro')
    ax.plot(pts_new.y,pts_new.x,'bo')
    
    fig.show()    
    
    