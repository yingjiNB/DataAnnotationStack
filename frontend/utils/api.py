import requests
from typing import Dict, Any, List, Optional
import json
import os

class APIClient:
    def __init__(self):
        # 判断是否在Docker环境中运行
        is_docker = os.getenv('DOCKER_ENV', 'false').lower() == 'true'
        
        # 根据环境选择合适的API地址
        if is_docker:
            self.base_url = os.getenv('API_URL', 'http://backend:8000/api/v1')
        else:
            # 本地开发环境使用localhost
            self.base_url = os.getenv('API_URL', 'http://localhost:8000/api/v1')
    
    def upload_file(self, file) -> Dict[str, Any]:
        """
        上传文件到后端
        """
        try:
            files = {"file": file}
            response = requests.post(f"{self.base_url}/files/upload", files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"文件上传失败：{str(e)}")
    
    def get_files(self) -> List[Dict[str, Any]]:
        """
        获取所有文件列表
        """
        try:
            response = requests.get(f"{self.base_url}/files/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取文件列表失败：{str(e)}")
    
    def get_file(self, file_id: int) -> Dict[str, Any]:
        """
        获取单个文件信息
        """
        try:
            response = requests.get(f"{self.base_url}/files/{file_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取文件信息失败：{str(e)}")
    
    def create_annotation(self, annotation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新的标注
        """
        try:
            response = requests.post(
                f"{self.base_url}/annotations/",
                json=annotation_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"创建标注失败：{str(e)}")
    
    def get_file_annotations(self, file_id: int) -> List[Dict[str, Any]]:
        """
        获取文件的所有标注
        """
        try:
            response = requests.get(f"{self.base_url}/annotations/file/{file_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取标注失败：{str(e)}")
    
    def update_annotation(
        self,
        annotation_id: int,
        annotation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新标注
        """
        try:
            response = requests.put(
                f"{self.base_url}/annotations/{annotation_id}",
                json=annotation_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"更新标注失败：{str(e)}")
    
    def get_file_content(self, file_id: int) -> bytes:
        """
        获取文件内容
        """
        try:
            response = requests.get(f"{self.base_url}/files/{file_id}/content", stream=True)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取文件内容失败：{str(e)}")
    
    def update_file_content(self, file_id: int, content: dict) -> dict:
        """
        更新文件内容
        """
        try:
            response = requests.put(
                f"{self.base_url}/files/{file_id}/content",
                json=content
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"更新文件内容失败：{str(e)}")

# 创建API客户端实例
api_client = APIClient() 