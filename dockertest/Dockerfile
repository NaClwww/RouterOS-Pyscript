ARG PYTHON_VERSION=3.12

FROM alpine AS builder
ARG PYTHON_VERSION

# 安装构建依赖、Python和UPX
RUN apk add --no-cache python3~=${PYTHON_VERSION} upx binutils

# 复制项目文件
COPY hello.py /app/main.py

# 安装librouteros
COPY librouteros /usr/lib/python${PYTHON_VERSION}/site-packages/librouteros
WORKDIR /usr/lib/python${PYTHON_VERSION}/site-packages
RUN python -m compileall -o 2 -b .

# 编译Python字节码并删除源文件
WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN python -m compileall -o 2 .
RUN find . -name "*.cpython-*.opt-2.pyc" | awk '{print $1, $1}' | sed 's/__pycache__\///2' | sed 's/.cpython-[0-9]\{2,\}.opt-2//2' | xargs -n 2 mv
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +

# 使用UPX压缩Python解释器和共享库
# RUN strip /usr/bin/python3 && \
#     upx --best --lzma /usr/bin/python3

# 压缩libpython共享库
RUN strip /usr/lib/libpython${PYTHON_VERSION}.so.1.0 && \
    upx --best --lzma /usr/lib/libpython${PYTHON_VERSION}.so.1.0 || true

# 压缩Alpine中的所有库文件
RUN find /usr/lib -name "*.so*" -type f -exec strip {} \; 2>/dev/null || true
RUN find /lib -name "*.so*" -type f -exec strip {} \; 2>/dev/null || true
RUN find /usr/lib -name "*.so*" -type f -exec upx --best --lzma {} \; 2>/dev/null || true
RUN find /lib -name "*.so*" -type f -exec upx --best --lzma {} \; 2>/dev/null || true

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