import os
import streamlit as st

def save_uploaded_files(uploaded_files):
    if uploaded_files:
        uploaded_folder = "./uploaded_files"
        os.makedirs(uploaded_folder,exist_ok=True)
    save_path_list=[]
    for file in uploaded_files:
        save_path = os.path.join(uploaded_folder,file.name)
        save_path_list.append(save_path)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
    # st.success(f"All files saved successfully.")
    return save_path_list

def delete_uploaded_files(path):
            if os.path.exists(path):
                os.remove(path)