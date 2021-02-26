# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:23:52 2021

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""

def traffic_congestion2gp_current(csv_trafficCongestionSegs_fp,epsg=None,boundary=None):
    '''  
    function - convert traffic congestion segments dataset to geompandas format
    Parameters
    ----------
    csv_trafficCongestionSegs_fp : TYPE
        DESCRIPTION.
    epsg : TYPE, optional
        DESCRIPTION. The default is None.
    boudnary : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    traffic_congestion_db : TYPE
        DESCRIPTION.

    '''
 
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import LineString
    from shapely.geometry import Polygon,MultiPolygon
    
    traffic_congestion=pd.read_csv(csv_trafficCongestionSegs_fp,sep=',')
    #print(traffic_congestion)
    #print(traffic_congestion.columns)
    traffic_congestion['geometry']=traffic_congestion.apply(lambda row:LineString([(row['START_LONGITUDE'],row[' START_LATITUDE']),(row['END_LONGITUDE'],row[' END_LATITUDE'])]),axis=1)
    #print(traffic_congestion)
    if boundary:
        mask=Polygon(boundary)
        traffic_congestion['mask']=traffic_congestion.geometry.apply(lambda row:row.within(mask))
        traffic_congestion.query('mask',inplace=True)
    
    crs={'init': 'epsg:4326'}
    if epsg is not None: 
        traffic_congestion_db=pd.DataFrame(gpd.GeoDataFrame(traffic_congestion,crs=crs).to_crs(epsg=epsg))
    else:
        traffic_congestion_db=pd.DataFrame(traffic_congestion)

    #print(traffic_congestion_db.geometry)
    traffic_congestion_db.geometry=traffic_congestion_db.geometry.apply(lambda row:str(list(row.coords)))
    # print(traffic_congestion_db.geometry)
    #print(traffic_congestion_db.columns)
    
    return traffic_congestion_db

def traffic_congestion2gp_hitorical(csv_trafficCongestionSegs_historical_fp,segs_id=None,merge_method='mean'):
    import pandas as pd
    trafficCongestionSegs_historical=pd.read_csv(csv_trafficCongestionSegs_historical_fp,sep=',')
    # print(trafficCongestionSegs_historical.shape)
    # print(segs_id.shape)
    # print(trafficCongestionSegs_historical['SEGMENTID'].isin(segs_id))
    trafficCongestionSegs_historical_extraction=trafficCongestionSegs_historical[trafficCongestionSegs_historical['SEGMENTID'].isin(segs_id)]
    # print(trafficCongestionSegs_historical_extraction)
    if merge_method=='max':
        trCon_merge=trafficCongestionSegs_historical_extraction.groupby(['SEGMENTID']).max()
    else:
        trCon_merge=trafficCongestionSegs_historical_extraction.groupby(['SEGMENTID']).mean()
    
    # print(trCon_merge_mean)
    return trCon_merge


def df2SQLite(df,db_fp,table_name):
    '''        
    function - write dataframe type date into SQLite,given talbe name
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    db_fp : TYPE
        DESCRIPTION.
    table_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    from sqlalchemy import create_engine
    engine=create_engine('sqlite:///'+'\\\\'.join(db_fp.split('\\')),echo=True) 

    
    try:
        df.to_sql(table_name,con=engine,if_exists='replace') #if_exists='append'
        print("data has been written into database...")
        
    except:
        print("_"*50,'\n','the table has been existed...')


if __name__=="__main__":  
    csv_trafficCongestionSegs_fp=r'C:\Users\richi\omen-richiebao\omen_github\driverlessCity_LIM\data\raw data\Chicago_Traffic_Tracker_-_Congestion_Estimates_by_Segments.csv'
    epsg=32616
    # boundary=[(-87.630609, 41.830851),(-87.603174, 41.831122),(-87.603020, 41.847229),(-87.641234, 41.847334)] #IIT region
    bottom_left=(-87.652605,  41.828429)
    top_right=(-87.589944,  41.923381)
    boundary=[(bottom_left[0],bottom_left[1]),(top_right[0],bottom_left[1]),(top_right[0], top_right[1]),(bottom_left[0], top_right[1])]
    
    traffic_congestion_current_db=traffic_congestion2gp_current(csv_trafficCongestionSegs_fp,epsg=epsg,boundary=None)
    
    csv_trafficCongestionSegs_historical_fp=r'C:\Users\richi\omen-richiebao\omen_github\driverlessCity_LIM\data\raw data\Chicago_Traffic_Tracker_-_Historical_Congestion_Estimates_by_Segment_-_2011-2018.csv'
    traffic_congestion2gp_hitorical_db=traffic_congestion2gp_hitorical(csv_trafficCongestionSegs_historical_fp,segs_id=traffic_congestion_current_db.SEGMENTID)
    
    db_fp=r'C:\Users\richi\omen-richiebao\omen_github\driverlessCity_LIM\database\driverlesscity_sqlit.db'    
    df2SQLite(traffic_congestion_current_db,db_fp,table_name='trafficCongestionSegs_current')
    df2SQLite(traffic_congestion2gp_hitorical_db,db_fp,table_name='trafficCongestionSegs_historical')
    
