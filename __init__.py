"""
L-ZIP Package Initialization
Logic-based Zero-redundancy Information Prompting

Author: ezixen
Version: 1.0.0
License: MIT

This package provides a token compression system for AI prompts,
reducing token usage by 40-70% while maintaining clarity and precision.
"""

from lzip import LZIPTranslator, LZIPConfig, create_translator
from mcp_server import LZIPMCPServer, create_server

__version__ = "1.0.0"
__author__ = "ezixen"
__copyright__ = "Copyright 2026 ezixen"
__license__ = "MIT"
__all__ = [
    "LZIPTranslator",
    "LZIPConfig",
    "LZIPMCPServer",
    "create_translator",
    "create_server",
]
