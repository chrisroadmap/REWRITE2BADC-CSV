
import pandas as pd




# %%
fp_example = 'ar6_ch6_rcmipfigs/data_in/SSPs_badc-csv/ERF_ssp119_1750-2500.csv'
fp_example_test = 'ar6_ch6_rcmipfigs/data_in/SSPs_badc-csv/ERF_ssp119_1750-2500_test.csv'

fp_orig_example = 'ar6_ch6_rcmipfigs/data_in/SSPs/ERF_ssp119_1750-2500.csv'
print('hallo')

# %%
def get_header_length(fp):
    """
    Finds the header length in a BADC csv file
    :param fp: file path
    :return:
    """
    cnt_data=0
    with open(fp) as f:
        line = f.readline()
        cnt = 1
        while line:
            l_sp = line.split(',')
            if l_sp[0].strip() == 'data':
                cnt_data = cnt
                break
            line = f.readline()
            cnt += 1


    return cnt_data


# %%
def read_csv_badc(fp,**kwargs):
    # %%
    kwargs ={'index_col':0}
    fp = fp_example
    # %%
    length_header = get_header_length(fp)
    df = pd.read_csv(fp, header=length_header, **kwargs, )
    if df.index[-1] =='end_data':
        print('hallo')
        df = df.drop('end_data',axis=0)


    # %%
    return df
# %%
def get_global_FaIR(fp ):

    df = pd.read_csv(fp, header=None)
    df_glob = df[df.iloc[:,1] == 'G']
    return df_glob
    # %%

def get_variable_FaIR(fp ):
    df = pd.read_csv(fp, header=None)
    df_vars = df[df.iloc[:,1] != 'G']
    return df_vars
# %%
def write_badc_header(
        fp_orig,
        fp_out,
        add_global_info,
        #variable_dic,
        #read_csv_kwargs=None,
        fp_global_default ,
        fp_var_default,
        default_unit = 'W/m2'
):
    """

    :param fp_orig: original file
    :param fp_out: output file name
    :param add_global_info: Added info to global header in hte form of a list of lists
    :param fp_global_default: path to header template
    :param fp_var_default: path to header template
    :param default_unit: if variable in file, not in header, choose this unit.
    :return:
    """
    #fp_global_default = path_FaIR_header_general_info
    #add_global_info = [['comments','G','Scenario: SSP1-1.9'],]
    #fp_var_default = path_FaIR_header_general_info
    #read_csv_kwargs=None
    #fp_orig = fp_orig_example


    df_glob = get_global_FaIR(fp=fp_global_default)
    df_var = get_variable_FaIR(fp = fp_var_default)
    df_glob.head()
    #if global_info_dic is not None:
    #    df_glob

    df_extra_glob = pd.DataFrame(add_global_info)
    df_glob = df_glob.append(df_extra_glob)

    df_orig = pd.read_csv(fp_orig, index_col=0,header=None)
    var_labs =  [df_orig.index[0]] + list(df_orig.iloc[0,:])


    _df = pd.read_csv(fp_orig,index_col=None, header=None)
    df_header = df_glob
    for var in var_labs:
        print(var)
        lines = df_var.iloc[:,1]==var
        #print(lines)
        df_header = df_header.append(df_var[lines])

        if len(df_var[lines])==0:
            # no set info:
            fix =  pd.DataFrame([['metdb_short_name', var,var, default_unit],
                                   ['long_name', var, var, default_unit],
                                   ['type', var, 'float',],],)
            df_header = df_header.append(fix)

    df_header = df_header.append(pd.DataFrame(['data']))

    df_out = df_header.append(_df)
    df_out = df_out.append(pd.DataFrame(['end_data']))
    #df_out.append(pd)
    df_out.to_csv(fp_out,header=False, index=False )

    return df_out
# %%


