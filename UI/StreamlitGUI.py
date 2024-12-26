"""
pip install streamlit
DockerFile

FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD streamlit run app.py
"""


def run_selectbox():
    import streamlit as st

    st.title('我的第一个Streamlit应用')
    st.write('你好呀，朋友~')
    number = st.slider('选个数字玩玩', 0, 100, 50)
    st.write(f'你选的数字是: {number}')


def run_chart():
    import streamlit as st
    import pandas as pd
    import numpy as np

    # 造点数据
    df = pd.DataFrame({
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '工资': [8000, 12000, 15000]
    })

    # 表格展示
    st.dataframe(df)  # 可交互的表格
    st.table(df)      # 静态表格

    # 图表展示
    st.line_chart(df['工资'])  # 折线图
    st.bar_chart(df['年龄'])   # 柱状图


def run_user_input():
    import streamlit as st

    # 侧边栏操作
    with st.sidebar:
        option = st.selectbox('选择一个功能', ['数据分析', '模型训练', '结果展示'])

    # 文件上传
    uploaded_file = st.file_uploader("上传CSV文件", type="csv")

    # 表单提交
    with st.form("my_form"):
        name = st.text_input('输入名字')
        age = st.number_input('输入年龄', min_value=0, max_value=120)
        submitted = st.form_submit_button("提交")
        if submitted:
            st.success(f'收到！{name}今年{age}岁啦~')


def run_layout():
    import streamlit as st

    col1, col2 = st.columns(2)  # 分两列

    with col1:
        st.header('左边')
        st.write('这是左边的内容')

    with col2:
        st.header('右边')
        st.write('这是右边的内容')

    # 折叠面板
    with st.expander('点击展开详情'):
        st.write('藏着的内容在这儿呢~')

    # 标签页
    tab1, tab2 = st.tabs(['第一页', '第二页'])
    with tab1:
        st.write('第一页内容')
    with tab2:
        st.write('第二页内容')


def run_widgets():
    import streamlit as st
    import time

    # 进度条
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)
        time.sleep(0.1)

    # 状态展示
    with st.status('正在处理...'):
        time.sleep(2)
        st.write('处理完成！')

    # 气球效果
    if st.button('来点气球'):
        st.balloons()

    # Session State
    if 'count' not in st.session_state:
        st.session_state.count = 0

    if st.button('点击计数'):
        st.session_state.count += 1

    st.write(f'点击次数：{st.session_state.count}')


if __name__ == '__main__':
    run_selectbox()
    # run_chart()
    # run_user_input()
    # run_layout()
    # run_widgets()
