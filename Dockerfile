# Refence: https://github.com/CrafterKolyan/tiny-python-docker-image

ARG PYTHON_VERSION=3.12
ARG ARCH=x86_64
# if x86 , use i486
# ARG ARCH=i486
# if arm64 , use aarch64
# ARG ARCH=aarch64
# if arm , use arm
# ARG ARCH=arm
# see https://musl.cc/ for more information

FROM alpine AS builder
ARG PYTHON_VERSION
ARG ARCH

# 安装构建依赖和Python
RUN apk add --no-cache python3~=${PYTHON_VERSION}

# 复制项目文件
COPY main.py /app/main.py


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

FROM alpine
ARG PYTHON_VERSION
ARG ARCH

# 从构建阶段仅复制必要的运行时文件
COPY --from=builder /usr/bin/python3 /usr/bin/python3
COPY --from=builder /lib/ld-musl-${ARCH}.so.1 /lib/ld-musl-${ARCH}.so.1
COPY --from=builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/libpython${PYTHON_VERSION}.so.1.0
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /app/main.py /app/main.py

# 挂载scripts目录
VOLUME /app/scripts

# 设置工作目录
WORKDIR /app

# 容器启动命令
ENTRYPOINT ["/usr/bin/python3", "/app/main.py"]
