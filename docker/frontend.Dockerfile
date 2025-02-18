FROM python:3.10-slim

WORKDIR /app

# 配置apt使用国内镜像源
RUN echo "deb https://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 使用国内镜像源加速pip安装
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

# 复制应用代码
COPY frontend/ frontend/

# 设置环境变量
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "frontend/app.py"]