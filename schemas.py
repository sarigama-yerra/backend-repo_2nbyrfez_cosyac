"""
Database Schemas for Open Source Sharing Platform

Define MongoDB collection schemas using Pydantic models.
Each Pydantic model maps to a collection whose name is the lowercase of the class.

Examples:
- Dataset -> "dataset"
- Tool -> "tool"
- Snippet -> "snippet"
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Core platform schemas

class Dataset(BaseModel):
    """
    Open datasets shared by the community
    Collection: "dataset"
    """
    name: str = Field(..., description="Dataset name")
    description: str = Field(..., description="What this dataset contains")
    url: HttpUrl = Field(..., description="Primary download or landing page URL")
    repo_url: Optional[HttpUrl] = Field(None, description="Repository URL if versioned on Git or similar")
    license: Optional[str] = Field(None, description="License name or SPDX identifier")
    maintainer: Optional[str] = Field(None, description="Maintainer or organization name")
    size_mb: Optional[float] = Field(None, ge=0, description="Approximate size in MB")
    tags: List[str] = Field(default_factory=list, description="Topic tags for discovery")

class Tool(BaseModel):
    """
    Open source tools/libraries shared by the community
    Collection: "tool"
    """
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="What this tool does")
    repo_url: HttpUrl = Field(..., description="Repository URL")
    homepage_url: Optional[HttpUrl] = Field(None, description="Project website")
    license: Optional[str] = Field(None, description="License name or SPDX identifier")
    tags: List[str] = Field(default_factory=list, description="Topic tags for discovery")

class Snippet(BaseModel):
    """
    Reusable code snippets or example notebooks
    Collection: "snippet"
    """
    title: str = Field(..., description="Snippet title")
    description: str = Field(..., description="Context or usage notes")
    language: str = Field(..., description="Primary language, e.g., python, js, sql")
    code: str = Field(..., description="Code content")
    repo_url: Optional[HttpUrl] = Field(None, description="Related repository URL")
    tags: List[str] = Field(default_factory=list, description="Topic tags for discovery")

# Keep a couple of example schemas for reference (not used by app directly)
class User(BaseModel):
    name: str
    email: str

class Product(BaseModel):
    title: str
    price: float
