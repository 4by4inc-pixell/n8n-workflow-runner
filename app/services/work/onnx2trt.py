from multiprocessing import Pool
import traceback
import ray
import os
from config import settings
import shutil
from services.work.base import WorkBase


@ray.remote(num_cpus=4, num_gpus=1)
def _task(params: dict):
    print(f"ray get {params}")
    package_dir = os.environ["PYTHONPATH"]
    if os.path.exists(package_dir):
        os.system(f"pip uninstall {package_dir}")
        shutil.rmtree(package_dir)  # 폴더 삭제
    commands = [
        f"git clone https://{params['github_id']}:{params['github_token']}@{params['github_nvidia_processor_url']} {package_dir}",
        f"pip install {package_dir}",
        f"cd {package_dir} && python tools/build_plan.py {params['model_name']}",
    ]
    for command in commands:
        print(f"Run command: {command}")
        os.system(command)


def _subprocess_runner(params: dict):
    try:
        params["github_id"] = settings.github_id
        params["github_token"] = settings.github_token
        params["github_nvidia_processor_url"] = settings.github_nvidia_processor_url
        ray.init(
            f"ray://{params['address']}:{params['port']}",
            runtime_env={
                "pip": ["pms-model-manager"],
                "env_vars": {
                    "PYTHONPATH": f"/workspace/workflow.nvidia-processor",
                    "MLFLOW_TRACKING_URI": settings.MLFLOW_TRACKING_URI,
                    "MLFLOW_REGISTRY_URI": settings.MLFLOW_REGISTRY_URI,
                    "AWS_ACCESS_KEY_ID": settings.AWS_ACCESS_KEY_ID,
                    "AWS_SECRET_ACCESS_KEY": settings.AWS_SECRET_ACCESS_KEY,
                    "AWS_DEFAULT_REGION": settings.AWS_DEFAULT_REGION,
                },
            },
        )
        ray.get(_task.remote(params))
        ray.shutdown()
        return (True, "success")
    except Exception as e:
        traceback_message = "".join(
            traceback.format_exception(None, e, e.__traceback__)
        )
        error_message = f"ERROR for {params}!\nType: {type(e).__name__}\nMessage: {str(e)}\nTraceback details\n{traceback_message}"
        print(error_message)
        return (False, error_message)


class ONNX2TRTTaskRunner(WorkBase):
    def __init__(self, task: dict):
        super().__init__(task)

    def execute(self) -> str:
        params = self.task.params
        with Pool(processes=1) as pool:
            result, message = pool.map(_subprocess_runner, [params])[0]
        if result is not True:
            raise Exception(message)
        return message
