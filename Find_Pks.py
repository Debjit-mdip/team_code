import streamlit as st

def extract_pks_from_bteqs(input_df, keyword="PRIMARY INDEX"):
    extracted_list = []
    ddl_list = input_df['DDL'].values.tolist()
    Object_list = input_df['Object Name'].values.tolist()
    obj_idx = 0
    for idx, content in enumerate(ddl_list):
        extracted_objects = []
        try:
            start = content.index(keyword) + len(keyword)
            paren_start = content.index('(', start)
            paren_end = content.index(')', paren_start)
            object_str = content[paren_start + 1:paren_end]
            extracted_objects.append([Object_list[obj_idx],object_str])

        except ValueError as ve:
            extracted_objects.append([Object_list[obj_idx],"Primary key not found"])
        except Exception as e:
            extracted_objects.append([Object_list[obj_idx],e])
        finally:
            obj_idx+=1
        extracted_list.extend(extracted_objects)
    return extracted_list


def extract_updt_column(table_name, ddl, updt_column_lst):
    obj_idx = 0
    for idx, keyword in enumerate(updt_column_lst):
        if keyword in ddl:
            return keyword
    return -1




