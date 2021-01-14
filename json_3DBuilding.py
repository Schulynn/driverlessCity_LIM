# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 19:17:15 2021

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""



def json_3DBuilding2gp(json_3DBuilding_fp,epsg=None,boundary=None):
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Polygon,MultiPolygon
    from shapely.geometry import shape
    import numpy as np
    '''
    funtion - 读取json格式3d 建筑，转换为GeoPandas格式
    '''
    
    building_3D=pd.read_json(json_3DBuilding_fp)
    # print(building_3D)
    feature_columns=list(building_3D.iloc[0,1].keys())
    properties_columns=list(building_3D.iloc[0,1]['properties'].keys())    
    # print(feature_columns,'\n',properties_columns)
    
    for column in feature_columns:
        building_3D[column]=building_3D.features.apply(lambda row:row[column])
        
    building_3D['geometry']=building_3D.geometry.apply(shape)  
    
    mask=Polygon(boundary)
    building_3D['mask']=building_3D.geometry.apply(lambda row:row.within(mask)) 
    # print(building_3D.geometry)
    # print(building_3D.shape)
    # building_3D.drop(building_3D[building_3D['mask'] == False].index, inplace=True)
    building_3D.query('mask', inplace=True)
    # print(building_3D.shape)
    
    
    
    building_3D['height']=building_3D.properties.apply(lambda row:row['height'] if 'height' in row.keys() else 0 )
    
    if epsg is not None:
        crs_target={'init': 'epsg:%d'%epsg}
        
    crs={'init': 'epsg:4326'}    
    if epsg is not None:    
        building_3D_db=pd.DataFrame(gpd.GeoDataFrame(building_3D,crs=crs).to_crs(epsg=epsg))
        # print("+"*50)
        # print(osm_node_db)
    else:
        building_3D_db=pd.DataFrame(building_3D)        
    
    building_3D_db.geometry=building_3D_db.geometry.apply(lambda row:str(list(zip(*row.exterior.coords.xy))) )  
    
    for column in building_3D_db.columns:
        building_3D_db[column]=building_3D_db[column].apply(lambda row:str(row))
    
    
    building_3D_db_drop=building_3D_db.drop(['features'],axis=1)
    return building_3D_db_drop


def building_3D2SQLite_database(building_3D_db,db_fp):
    from sqlalchemy import create_engine 
    '''
    function - 将3D building 写入数据库
    '''
    engine = create_engine('sqlite:///'+'\\\\'.join(db_fp.split('\\')),echo=True) 
    try:
        building_3D_db.to_sql('building_3d',con=engine,if_exists='replace') #if_exists='append'
        print("data has been written into database...")
        
    except:
        print("_"*50,'\n','the building_3d table has been existed...')


if __name__=="__main__":    
    json_3DBuilding_fp=r'C:\Users\richi\omen-richiebao_s\omen_github\driverlessCity_LIM\data\raw data\Chicago_3dbuildings.json'
    epsg=32616
    boundary=[(-87.630609, 41.830851),(-87.603174, 41.831122),(-87.641234, 41.847334),(-87.603020, 41.847229)]
    building_3D_db=json_3DBuilding2gp(json_3DBuilding_fp,epsg,boundary)
    
    db_fp=r'C:\Users\richi\omen-richiebao_s\omen_github\driverlessCity_LIM\database\driverlesscity_sqlit.db'
    building_3D2SQLite_database(building_3D_db,db_fp)
