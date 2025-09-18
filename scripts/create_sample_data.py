#!/usr/bin/env python3
"""Script to create sample data for development and testing."""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import get_settings
from src.models.base import Base
from src.models.task import Task, TaskStatus, TaskPriority


async def create_sample_tasks(session: AsyncSession) -> None:
    """Create sample tasks for development."""
    
    sample_tasks = [
        {
            "name": "Data Processing Pipeline",
            "description": "Process customer data for analytics",
            "task_type": "data_processing",
            "parameters": {
                "data_source": "/data/customers.csv",
                "processing_type": "analytics",
                "output_format": "parquet"
            },
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.SUCCESS,
            "created_by": "data_team",
            "tags": ["analytics", "customers", "etl"]
        },
        {
            "name": "ML Model Training",
            "description": "Train recommendation model",
            "task_type": "ml_training",
            "parameters": {
                "model_type": "collaborative_filtering",
                "dataset_size": 1000000,
                "epochs": 10,
                "learning_rate": 0.001
            },
            "priority": TaskPriority.URGENT,
            "status": TaskStatus.RUNNING,
            "progress": 65,
            "created_by": "ml_team",
            "tags": ["ml", "training", "recommendations"]
        },
        {
            "name": "Weekly Report Generation",
            "description": "Generate weekly performance report",
            "task_type": "report_generation",
            "parameters": {
                "report_type": "weekly_performance",
                "date_range": "last_7_days",
                "format": "pdf",
                "recipients": ["management@company.com"]
            },
            "priority": TaskPriority.NORMAL,
            "status": TaskStatus.PENDING,
            "scheduled_at": datetime.utcnow() + timedelta(hours=1),
            "created_by": "reporting_system",
            "tags": ["reports", "weekly", "automated"]
        },
        {
            "name": "Email Campaign Delivery",
            "description": "Send promotional emails to subscribers",
            "task_type": "email_campaign",
            "parameters": {
                "template_id": "promo_2024_q1",
                "recipient_count": 50000,
                "send_rate": "1000/hour",
                "personalization": True
            },
            "priority": TaskPriority.NORMAL,
            "status": TaskStatus.FAILED,
            "retry_count": 2,
            "error_message": "SMTP server connection timeout",
            "created_by": "marketing_team",
            "tags": ["email", "marketing", "campaign"]
        },
        {
            "name": "Database Backup",
            "description": "Daily database backup to S3",
            "task_type": "backup",
            "parameters": {
                "database": "production",
                "destination": "s3://backups/daily/",
                "compression": "gzip",
                "retention_days": 30
            },
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.SUCCESS,
            "created_by": "system",
            "tags": ["backup", "daily", "maintenance"]
        }
    ]
    
    for task_data in sample_tasks:
        task = Task(**task_data)
        session.add(task)
    
    await session.commit()
    print(f"Created {len(sample_tasks)} sample tasks")


async def main():
    """Main function to create sample data."""
    settings = get_settings()
    
    # Create database engine
    engine = create_async_engine(settings.database_url, echo=True)
    
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        await create_sample_tasks(session)
    
    await engine.dispose()
    print("Sample data creation completed!")


if __name__ == "__main__":
    asyncio.run(main())