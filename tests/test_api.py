import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os
import json

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_file(tmp_path):
    # 创建测试文件
    test_file = tmp_path / "test.json"
    test_data = {"name": "Test User", "email": "test@example.com"}
    test_file.write_text(json.dumps(test_data))
    
    # 上传文件
    with open(test_file, "rb") as f:
        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.json", f, "application/json")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.json"
    assert data["file_type"] == "json"

def test_get_files():
    response = client.get("/api/v1/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_annotation():
    annotation_data = {
        "file_id": 1,
        "json_path": "name",
        "original_value": "Test User",
        "is_correct": True
    }
    
    response = client.post(
        "/api/v1/annotations/",
        json=annotation_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["file_id"] == 1
    assert data["json_path"] == "name"
    assert data["original_value"] == "Test User" 