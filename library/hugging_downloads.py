import os
from pathlib import Path
from huggingface_hub import hf_hub_download

def download_model(repo_id: str, model_filename: str, model_dir: str = 'model') -> Path:
    """
    下载指定的模型文件并保存到根目录下的 model 文件夹。
    
    参数:
    repo_id (str): Hugging Face 上的模型仓库 ID。
    model_filename (str): 要下载的模型文件的名称。
    model_dir (str): 存储模型文件的目录。默认为 'model'。
    
    返回:
    Path: 下载的模型文件的路径。
    """
    # 创建 model 目录（如果不存在的话）
    model_dir_path = Path(model_dir)
    model_dir_path.mkdir(parents=True, exist_ok=True)
    # 下载模型文件
    downloaded_model_path = hf_hub_download(repo_id=repo_id, filename=model_filename, cache_dir=model_dir_path)
    
    return Path(downloaded_model_path)

if __name__ == "__main__" :
    repo_id = 'SmilingWolf/wd-v1-4-swinv2-tagger-v2'
    model_filename = 'model.onnx'
    
    model_file_path = download_model(repo_id, model_filename)
    print(f"模型已下载到: {model_file_path}")