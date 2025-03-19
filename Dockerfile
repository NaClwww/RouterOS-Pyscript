#Reference: https://github.com/CrafterKolyan/tiny-python-docker-image

ARG PYTHON_VERSION=3.12

FROM alpine AS builder
ARG PYTHON_VERSION

# 安装构建依赖、Python
RUN apk add --no-cache python3~=${PYTHON_VERSION} py3-pip

# 复制项目文件
COPY main.py /app/main.py

# 安装必要库
RUN pip install --no-cache-dir --break-system-packages librouteros APScheduler && pip cache purge
WORKDIR /usr/lib/python${PYTHON_VERSION}/site-packages
RUN python -m compileall -o 2 -b .


# 编译Python字节码并删除源文件
WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN python -m compileall -o 2 .
RUN find . -name "*.cpython-*.opt-2.pyc" | awk '{print $1, $1}' | sed 's/__pycache__\///2' | sed 's/.cpython-[0-9]\{2,\}.opt-2//2' | xargs -n 2 mv
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +

# 删除pip和安装工具
RUN apk del py3-pip
RUN rm -rf /usr/lib/python${PYTHON_VERSION}/site-packages/pip* \
    /usr/lib/python${PYTHON_VERSION}/site-packages/setuptools* \
    /usr/lib/python${PYTHON_VERSION}/site-packages/pkg_resources* \
    /usr/lib/python${PYTHON_VERSION}/ensurepip

# 压缩libpython共享库,arm压了会导致无法运行
# RUN strip /usr/lib/libpython${PYTHON_VERSION}.so.1.0 && \
#     upx --best --lzma /usr/lib/libpython${PYTHON_VERSION}.so.1.0 || true

FROM alpine
ARG PYTHON_VERSION

# 从构建阶段仅复制必要的运行时文件
COPY --from=builder /usr/bin/python3 /
COPY --from=builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/libpython${PYTHON_VERSION}.so.1.0
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /app/main.py /app/main.py

# 挂载scripts目录
VOLUME /app/scripts

# 设置工作目录
WORKDIR /app

# 容器启动命令
ENTRYPOINT ["/python3", "/app/main.py"]