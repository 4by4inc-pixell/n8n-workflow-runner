# n8n-workflow-runner

이 저장소는 database를 통해 n8n과 상호 작용하여 복잡한 코드 기반의 작업을 수행하기 위해 만들어졌습니다.

n8n(혹은 다른 서비스)에서 작업을 정의하여 db에 기록하면, 이 서비스는 해당 작업을 실행합니다.

## 주요 기능

Docker 환경: Docker를 사용해 다양한 시스템에서 일관된 실행 환경을 제공합니다.

자동 워크플로우 실행: 설정에 따라 n8n 워크플로우를 자동으로 실행합니다.

api 제공: fast api를 기반으로 동작하므로, Request를 통해 작업을 등록할 수 있습니다.

## 사전 요구사항

Docker: 시스템에 Docker가 설치되어 있어야 합니다.

Docker Compose: 서비스를 오케스트레이션하기 위해 필요합니다.

## 시작하기

### 1.	저장소 클론
```bash
git clone https://github.com/4by4inc-pixell/n8n-workflow-runner.git
cd n8n-workflow-runner
```
### 2.	환경 변수 설정

.env 파일을 프로젝트 루트 디렉터리에 생성한 후, 워크플로우 실행에 필요한 환경 변수를 지정합니다.

필요한 환경변수는 docker/Dockerfile을 참조하세요.

### 3. 서비스 빌드 및 실행:
```bash
docker-compose up --build
```

## 커스터마이징

### Work 추가

[WorkBase Class](app/services/work/base.py)를 상속하여 새로운 work를 정의합니다.

[async def execute_task(self, task: N8NTaskRead):](https://github.com/4by4inc-pixell/n8n-workflow-runner/blob/1bc77d87929708d3837b7b51e914615c9afd03c0/app/services/n8n/excuter.py#L57)에 task_type에 대한 처리를 추가합니다.
