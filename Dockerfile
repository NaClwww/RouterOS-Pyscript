ARG PYTHON_VERSION=3.12
# The architecture will be determined automatically by buildx

FROM --platform=$TARGETPLATFORM alpine AS builder
ARG PYTHON_VERSION
ARG TARGETPLATFORM

# 根据目标平台设置架构变量
RUN case "${TARGETPLATFORM}" in \
        "linux/amd64")  echo "x86_64" > /tmp/arch  ;; \
        "linux/arm64")  echo "aarch64" > /tmp/arch ;; \
        "linux/arm/v7") echo "arm" > /tmp/arch     ;; \
        *) echo "Unsupported platform: ${TARGETPLATFORM}" && exit 1 ;; \
    esac

# 安装构建依赖和Python
RUN apk add --no-cache python3~=${PYTHON_VERSION} py3-pip upx binutils

# 复制项目文件
COPY . /app/
WORKDIR /app

# 安装librouteros
COPY librouteros /usr/lib/python${PYTHON_VERSION}/site-packages/librouteros
WORKDIR /usr/lib/python${PYTHON_VERSION}/site-packages
RUN python -m compileall -o 2 -b .

# 编译Python字节码并删除源文件
WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN python -m compileall -o 2 .
RUN find . -name "*.cpython-*.opt-2.pyc" -exec sh -c 'mv "$1" "${1/__pycache__\//}"' _ {} \;
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +

# 压缩Python解释器和库文件
RUN arch=$(cat /tmp/arch) && \
    real_python=$(readlink -f /usr/bin/python3) && \
    strip $real_python && upx --best $real_python && \
    if [ -f /lib/ld-musl-${arch}.so.1]; then \
        strip /lib/ld-musl-${arch}.so.1 && upx --best /lib/ld-musl-${arch}.so.1; \
    fi

# 第二阶段：创建最终镜像
FROM --platform=$TARGETPLATFORM alpine
ARG PYTHON_VERSION
ARG TARGETPLATFORM

# 从临时文件读取架构
COPY --from=builder /tmp/arch /tmp/arch

# 从构建阶段复制必要的文件
COPY --from=builder /usr/bin/python3 /usr/bin/python3
COPY --from=builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/libpython${PYTHON_VERSION}.so.1.0
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /app/main.py /app/main.py

# 挂载scripts目录
VOLUME /app/scripts

# 设置工作目录
WORKDIR /app

# 容器启动命令
ENTRYPOINT ["/usr/bin/python3", "/app/main.py"]
