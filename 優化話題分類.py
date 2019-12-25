# coding: utf-8
# coding: utf-8
from sqlalchemy import create_engine
import re
import cymysql
import pandas as pd
ENGINE = create_engine(‘mysql+cymysql://acc:pass@host/db_name’,encoding=‘utf-8’)
pattern = re.compile(r’CS1.*|專題.*|.*分類|.*導航框|.*模板.*|.*討論頁|.*標識符|.*主題首頁.*|.*維基資源|引文格式.*|.*小作品.*|可能帶有.*|.*頁面|.*定向|包含.*|缺少.*|使用.*|.*鏈接.*|.*條目.*|引文格式.*|.*維基.*|已拒絕.*|....年.*|已完成.*|.*消歧義|.*使用者|部分地區的觀點|各種主題的物品|.*subpages|.*動員令貢獻一覽|依.*劃分.*|.*的作品|不含.*|.*templates.*|自....年.*|.*condition.*|.*章節|.*翻譯.*|輸入錯誤.*|.*計畫成果|.*應用衝突|生者傳記|..世紀.*‘)
output_check = pd.DataFrame()
output_auto = pd.DataFrame()

file_name=‘’
with open(file_name, ‘r’,encoding=“utf-8”) as file:
    for line in file:
        if ‘“’ in line:
            line = line.replace(‘“’,‘’)
            line = line.strip()
        result = ENGINE.execute(“SELECT cl_to,cl_sortkey FROM categorylinks WHERE cl_sortkey =“+”‘“+ line+“’”+“;”) 
        res = result.fetchall()
        sql_dict={}
        sql_dict_auto={}
        for i in range(len(res)): 
            cl_to=res[i][0].decode(‘utf-8’)
            match = pattern.search(cl_to)
            if match == ‘’ or match is None:
                sql_dict[cl_to] = ‘,’+res[i][1].decode(‘utf-8’)  
            else:
                sql_dict_auto[cl_to] = ‘,’+res[i][1].decode(‘utf-8’)                              
            for_concat = pd.DataFrame(list(sql_dict.items()))
            for_concat_auto = pd.DataFrame(list(sql_dict_auto.items()))            
        output_check = pd.concat([output_check,for_concat])
        output_auto = pd.concat([output_auto,for_concat_auto])

output_check.columns = [‘cl_to’,‘cl_sortkey’]
output_auto.columns = [‘cl_to’,‘cl_sortkey’]
output_file_name_check=‘優化話題分類_手動_‘+file_name
output_file_name_auto=‘優化話題分類_自動_‘+file_name
output_check.to_csv(output_file_name_check, sep=‘\t’, index=False) 
output_auto.to_csv(output_file_name_auto, sep=‘\t’, index=False) 
