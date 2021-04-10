# 建立 python3.7 环境
FROM python:3.7

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置pip源为国内源
COPY pip.conf /root/.pip/pip.conf

# 在容器内/var/www/html/下创建 mysite1文件夹
RUN mkdir -p /var/www/html/mysite1

# 设置容器内工作目录
WORKDIR /var/www/html/mysite1

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
ADD . /var/www/html/mysite1

# 利用 pip 安装依赖
RUN pip install -r requirements.txt

#创建java目录
RUN mkdir /usr/local/java

#解压jdk
ADD jdk12.tar.gz /usr/local/java/jdk


ENV JAVA_HOME /usr/local/java/jdk/jdk-12.0.1 
ENV PATH ${JAVA_HOME}/bin:$PATH 
