import streamlit as st
import requests
from pathlib import Path
import json
import os
from components.pdf_viewer import render_pdf
from components.json_editor import render_json_editor
from utils.api import api_client
import io

# 配置页面
st.set_page_config(
    page_title="简历标注工具",
    page_icon="📝",
    layout="wide"
)

# 会话状态管理
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'selected_json' not in st.session_state:
    st.session_state.selected_json = None

def main():
    st.title("简历JSON标注工具")
    
    # 创建三列布局
    file_tree_col, pdf_viewer_col, json_editor_col = st.columns([1, 2, 2])
    
    with file_tree_col:
        st.subheader("文件浏览器")
        # 文件上传
        uploaded_files = st.file_uploader(
            "上传PDF或JSON文件",
            type=["pdf", "json"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for file in uploaded_files:
                try:
                    response = api_client.upload_file(file)
                    if response:
                        st.success(f"文件 {file.name} 上传成功！")
                except Exception as e:
                    st.error(f"文件 {file.name} 上传失败：{str(e)}")
        
        # 显示文件列表
        try:
            files = api_client.get_files()
            if files:
                st.write("### 已上传文件")
                for file in files:
                    if st.button(f"📄 {file['filename']}", key=file['id']):
                        st.session_state.selected_file = file
                        # 如果选择的是JSON文件，更新JSON预览
                        if file['file_type'] == 'json':
                            st.session_state.selected_json = file
        except Exception as e:
            st.error(f"获取文件列表失败：{str(e)}")
    
    with pdf_viewer_col:
        st.subheader("PDF预览")
        if st.session_state.selected_file and st.session_state.selected_file['file_type'] == 'pdf':
            try:
                # 通过API获取PDF文件内容
                file_content = api_client.get_file_content(st.session_state.selected_file['id'])
                pdf_file = io.BytesIO(file_content)
                render_pdf(pdf_file)
            except Exception as e:
                st.error(f"无法加载PDF文件：{str(e)}")
        else:
            st.info("请选择一个PDF文件进行预览")
    
    with json_editor_col:
        st.subheader("JSON编辑器")
        if st.session_state.selected_json:
            try:
                # 通过API获取JSON文件内容
                file_content = api_client.get_file_content(st.session_state.selected_json['id'])
                json_data = json.loads(file_content.decode('utf-8'))
                
                def on_json_change(updated_json):
                    try:
                        # 通过API保存更新后的JSON
                        api_client.update_file_content(
                            st.session_state.selected_json['id'],
                            updated_json
                        )
                        st.success("JSON已更新")
                    except Exception as e:
                        st.error(f"保存JSON失败：{str(e)}")
                
                render_json_editor(json_data, on_json_change)
            except Exception as e:
                st.error(f"无法加载JSON文件：{str(e)}")
        else:
            st.info("请选择一个JSON文件进行编辑")

if __name__ == "__main__":
    main() 