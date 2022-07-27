import pandas as pd
from pypxlib import Table

def update_db(df_path, ps_path, db_path, make, ps_model, ps_retail, ps_cost, wholesaleActive, ps_dealer):
    df_model ='MODEL'
    df_retail = 'RETAIL'
    df_dealer = 'DEALER'
    df_cost = 'COST'
    df_make = 'MAKE'

    table = Table(db_path)
    df = pd.read_csv(df_path)
    ps = pd.read_excel(ps_path, dtype=str, index_col=None)
    ps.columns = ps.columns.str.lower()
    print(type(ps.columns))
    print(ps.columns)
    print(type(df_path))
    print(make)
    print(ps_model)
    print(ps_retail)

    maker = df.loc[df[df_make] == make] #Creating a new df of just the make
    print(maker)
    ru = maker.loc[maker[df_model].isin(ps[ps_model])] #Created a subsequent df for models that appear in database and price sheet

    def replace(df_model,df_replace,ps_model,ps_replace):
        m = ps.set_index(ps_model)[ps_replace].to_dict() #Indexing models with replacement value
        v = ru.loc[:, ru.columns.str.match(df_model)] #locating all values in model and replacement columns in df and assigning to variables
        s = ru.loc[:, ru.columns.str.match(df_replace)]
        ru[s.columns] = v.replace(m) #replacing columns in df

    #Calling function for retail, dealer, and cost
    df_list = [df_retail,df_cost]
    replace(df_model,df_retail,ps_model,ps_retail)
    replace(df_model,df_cost,ps_model,ps_cost)
    if wholesaleActive:
        replace(df_model,df_dealer,ps_model,ps_dealer)
        df_list = [df_retail,df_cost,df_dealer]
    
    
    try:
        for q in range(len(df_list)): #Iterating through the database replacement columns
            for i in range(len(ru.index)): #Iterating through the updated prices by row
                rr = int(ru.iloc[i].name) #Assigning row replacement variable to the row name which is the original database index
                uv = float(ru.iloc[i][df_list[q]]) #Assinging update value variable to the item in the current replacement column
                row = table[rr] #Assiging row to the current table replacement row
                row[df_list[q]] = uv #Replacing the row value of the current replacement column with the updated value
                row.save()
    finally:
        table.close()
    return len(df_list)*len(ru.index)

