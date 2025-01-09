# 1. 경량화된 Python 3.10 이미지를 기반으로 사용
FROM python:3.10-slim

# 2. 필수 종속성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. 환경 변수 설정
ENV host="0.0.0.0" \
    port="8000" \
    n8n_base_url="https://example.com/n8n" \
    github_id="github_id" \
    github_token="github_token" \
    github_nvidia_processor_url="github.com/github_id/repose_name.git" \
    DATABASE_URL="postgresql+asyncpg://id:pw@db_url/db_name" \
    AWS_ACCESS_KEY_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
    AWS_SECRET_ACCESS_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
    AWS_DEFAULT_REGION="ap-northeast-2" \
    MLFLOW_TRACKING_URI="https://example.com/mlflow" \
    MLFLOW_REGISTRY_URI="https://example.com/mlflow"

# 4. 작업 디렉토리 생성 및 코드 복사
WORKDIR /workspace
COPY . /workspace

# 5. 종속성 설치
RUN pip install --no-cache-dir .

# 6. Python 앱 실행
CMD ["python", "app"]