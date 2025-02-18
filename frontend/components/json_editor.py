import streamlit as st
import json
from typing import Dict, Any

def render_json_editor(json_data: Dict[str, Any], on_change=None):
    """
    渲染JSON编辑器
    """
    if not json_data:
        st.warning("请选择一个JSON文件")
        return
    
    try:
        # 创建可编辑的文本区域
        edited_json = st.text_area(
            "JSON编辑器",
            value=json.dumps(json_data, indent=2, ensure_ascii=False),
            height=400,
            key="json_editor"
        )
        
        try:
            # 尝试解析编辑后的JSON
            parsed_json = json.loads(edited_json)
            
            # 显示验证和标注选项
            st.write("### 字段验证")
            
            for key, value in parsed_json.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{key}**: {value}")
                
                with col2:
                    is_correct = st.checkbox("正确", key=f"correct_{key}")
                
                with col3:
                    if not is_correct:
                        st.text_input("修正", key=f"correction_{key}")
            
            # 保存按钮
            if st.button("保存标注"):
                if on_change:
                    on_change(parsed_json)
                st.success("标注已保存！")
                
        except json.JSONDecodeError:
            st.error("JSON格式错误，请检查输入")
            
    except Exception as e:
        st.error(f"处理JSON时出错：{str(e)}")

def format_json_tree(json_data: Dict[str, Any], indent: int = 0) -> str:
    """
    格式化JSON数据为树形结构
    """
    result = []
    for key, value in json_data.items():
        if isinstance(value, dict):
            result.append("  " * indent + f"{key}:")
            result.append(format_json_tree(value, indent + 1))
        else:
            result.append("  " * indent + f"{key}: {value}")
    return "\n".join(result) 