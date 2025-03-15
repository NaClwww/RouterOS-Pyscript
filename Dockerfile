# 构建阶段 - 使用Alpine作为构建环境
FROM python:3.10-alpine AS builder

# 安装构建依赖
RUN apk add --no-cache gcc musl-dev libffi-dev upx

# 复制项目文件
COPY . /app/
WORKDIR /app

# 安装PyInstaller和项目依赖
RUN pip install --no-cache-dir pyinstaller
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# 使用PyInstaller创建单一可执行文件
RUN pyinstaller --onefile --clean main.py

# 进一步压缩二进制文件
RUN upx --best --lzma /app/dist/main

# 最终极简镜像 - 使用scratch (空白基础镜像)
FROM scratch

# 从构建阶段仅复制必要的运行时文件
COPY --from=builder /app/dist/main /app/main
COPY --from=builder /lib/ld-musl-*.so.1 /lib/
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# 挂载scripts目录
VOLUME /app/main/scripts

# 设置工作目录
WORKDIR /app

# 容器启动命令
ENTRYPOINT ["/app/main"]
