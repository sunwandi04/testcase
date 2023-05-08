#基于的基础镜像
FROM python:3.10
#代码添加到code文件夹
ADD . /code
# 设置code文件夹是工作目录
WORKDIR /code
# 安装支持
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip                                                            3.5s
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt