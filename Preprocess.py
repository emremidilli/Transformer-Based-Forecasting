# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:55:10 2020

@author: yunus emre midilli
"""

import pandas as pd
from Connect_to_Database import execute_sql


# PREASSUMPTIONS:
    # tbl_feature_values include row data where each time stamp is correctly sequenced.

def dfGetFeatureValues(iModelId, iModelFeatureId, sFromTimeStamp = "DEFAULT", sToTimeStamp = "DEFAULT" ):
    sql = "EXEC SP_GET_TIME_STEPS "+ str(iModelId) +","+ str(iModelFeatureId)
    dfTimeSteps =  execute_sql(sql, "")
    

    if not sFromTimeStamp == "DEFAULT":
        sFromTimeStamp = "'" + str(sFromTimeStamp) + "'"
        
    if not sToTimeStamp == "DEFAULT":
        sToTimeStamp = "'" + str(sToTimeStamp) + "'"     
    
    sql_feature_value = "EXEC  [SP_GET_MODEL_FEATURE_VALUES] "+str(iModelId)+", "+ str(iModelFeatureId) +" ,"+sFromTimeStamp+", "+sToTimeStamp

    df_all_feature_values = execute_sql(sql_feature_value)
    
    df_all_feature_values = df_all_feature_values.set_index("TIME_STAMP")

    dfFeatureValues = pd.DataFrame()
    for i_index, i_row in dfTimeSteps.iterrows():
        time_step_id = i_row["ID"]
        time_step = int(i_row["TIME_STEP"])
        feature_id = i_row["FEATURE_ID"]
        boundary= i_row["BOUNDARY"]

        

        if boundary == 0:
            dfFeatureValues[time_step_id] = 0
            
        else:

            df = df_all_feature_values[df_all_feature_values["FEATURE_ID"]==feature_id]
            df_values = df["VALUE"]
            df_values = pd.DataFrame(df_values)
            
            df_values = df_values["VALUE"].shift(-time_step)
            dfFeatureValues[time_step_id] = df_values

    dfFeatureValues.sort_index(ascending=False)
    dfFeatureValues = dfFeatureValues.dropna()
    
    dfTimeSteps = dfTimeSteps.transpose()
        
    dfTimeSteps.columns = dfFeatureValues.columns 

    if iModelFeatureId == "1":
        dfFeatureValues, dfTimeSteps = dfAddSeasonalFeatures(dfFeatureValues, dfTimeSteps)

    return dfFeatureValues, dfTimeSteps



def dfAddSeasonalFeatures(dfFeatureValues, dfTimeSteps):
    dfTimeSteps = dfTimeSteps.transpose()
    aUniqueTimeSteps = dfTimeSteps.TIME_STEP.unique()
    
    exec("dfIndex = dfFeatureValues.index")
    
    
    aSeasonalFeatures = ["year","month", "day", "dayofweek", "hour"]
    
    
    iId = -1
    iModelFeatureID = -1
    
    for sSeasonalFeature in aSeasonalFeatures:
    
        for iTimeStep in aUniqueTimeSteps:

            sFeatureId = sSeasonalFeature
            
            dfTimeSteps = dfTimeSteps.append({'TIME_STEP': iTimeStep, 'MODEL_FEATURE_ID':iModelFeatureID, 'ID':iId, 'FEATURE_ID': sFeatureId}, ignore_index=True)
            
            exec("dfFeatureValues[iId] = dfIndex." + sSeasonalFeature)
            
            iId = iId -1 
            
        iModelFeatureID =  iModelFeatureID - 1 
    
            
    dfTimeSteps = dfTimeSteps.sort_values(by=['TIME_STEP', 'MODEL_FEATURE_ID'], ascending=[True, False])
    
    aColumnOrders =dfTimeSteps["ID"]
            
    dfTimeSteps = dfTimeSteps.transpose()
    
    dfFeatureValues = dfFeatureValues[aColumnOrders]

    return dfFeatureValues, dfTimeSteps
        
        

def aGetFeatureStatistics(iFeatureID):
    sSql = "SELECT * FROM TBL_FEATURE_VALUES WHERE FEATURE_ID = " + str(iFeatureID)
    dfFeatureValues = execute_sql(sSql, "")
    aFeatureStatistics = dfFeatureValues.describe()
    
    return aFeatureStatistics
    
    

def dfGetDimensionSize(dfTimeSteps):
    feature_size = dfTimeSteps.loc[["MODEL_FEATURE_ID"]].transpose().MODEL_FEATURE_ID.unique().size
    window_length = dfTimeSteps.loc[["TIME_STEP"]].transpose().TIME_STEP.unique().size
    return feature_size, window_length


def main(iModelId):
    df_input, dfTimeSteps_input= dfGetFeatureValues(iModelId, "1")
    df_target, dfTimeSteps_target = dfGetFeatureValues(iModelId, "2")
    df_merged =pd.merge(df_input, df_target, left_index=True, right_index=True)
        
    df_input = df_merged[df_input.columns]
    df_target= df_merged[df_target.columns]
    
    return  df_input, df_target ,dfTimeSteps_input, dfTimeSteps_target
