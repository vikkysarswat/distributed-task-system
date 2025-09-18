"""Unit tests for Task model."""

import pytest
from datetime import datetime
from uuid import uuid4

from src.models.task import Task, TaskStatus, TaskPriority


class TestTaskModel:
    """Test cases for Task model."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(
            name="Test Task",
            task_type="test",
            priority=TaskPriority.HIGH
        )
        
        assert task.name == "Test Task"
        assert task.task_type == "test"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING
        assert task.progress == 0
        assert task.retry_count == 0
        assert task.is_active is True
    
    def test_task_status_update(self):
        """Test task status updates."""
        task = Task(
            name="Test Task",
            task_type="test"
        )
        
        # Test running status
        task.update_status(TaskStatus.RUNNING)
        assert task.status == TaskStatus.RUNNING
        assert task.started_at is not None
        
        # Test completion
        task.update_status(TaskStatus.SUCCESS)
        assert task.status == TaskStatus.SUCCESS
        assert task.completed_at is not None
    
    def test_task_retry_logic(self):
        """Test task retry functionality."""
        task = Task(
            name="Test Task",
            task_type="test",
            status=TaskStatus.FAILED,
            max_retries=3,
            retry_count=1
        )
        
        assert task.can_retry is True
        
        # Exceed max retries
        task.retry_count = 3
        assert task.can_retry is False
    
    def test_task_completion_check(self):
        """Test task completion status."""
        task = Task(
            name="Test Task",
            task_type="test"
        )
        
        # Pending task
        assert task.is_completed is False
        
        # Completed task
        task.status = TaskStatus.SUCCESS
        assert task.is_completed is True
        
        # Failed task
        task.status = TaskStatus.FAILED
        assert task.is_completed is True
    
    def test_task_to_dict(self):
        """Test task dictionary conversion."""
        task = Task(
            name="Test Task",
            task_type="test",
            parameters={"key": "value"},
            tags=["test", "unit"]
        )
        
        task_dict = task.to_dict()
        
        assert task_dict["name"] == "Test Task"
        assert task_dict["task_type"] == "test"
        assert task_dict["parameters"] == {"key": "value"}
        assert task_dict["tags"] == ["test", "unit"]
        assert "id" in task_dict
        assert "created_at" in task_dict