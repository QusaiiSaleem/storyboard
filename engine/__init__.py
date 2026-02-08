# engine/__init__.py
# Template engine package for Storyboard Generator
#
# This package provides "template-as-code" builders that create
# production-ready DOCX and PPTX documents matching the exact
# visual design of the original templates.
#
# DOCX Usage:
#   from engine.docx_engine import TestBuilder, ActivityBuilder, VideoBuilder
#   from engine.docx_engine import ObjectivesBuilder, SummaryBuilder
#   from engine.docx_engine import InfographicBuilder, DiscussionBuilder, AssignmentBuilder
#
# PPTX Usage:
#   from engine.pptx_engine import LectureBuilder

from engine.docx_engine import (
    DocxBuilder,
    TestBuilder,
    ActivityBuilder,
    VideoBuilder,
    ObjectivesBuilder,
    SummaryBuilder,
    InfographicBuilder,
    DiscussionBuilder,
    AssignmentBuilder,
)

try:
    from engine.pptx_engine import LectureBuilder
    __all__ = [
        "DocxBuilder",
        "TestBuilder",
        "ActivityBuilder",
        "VideoBuilder",
        "ObjectivesBuilder",
        "SummaryBuilder",
        "InfographicBuilder",
        "DiscussionBuilder",
        "AssignmentBuilder",
        "LectureBuilder",
    ]
except ImportError:
    # pptx_engine may not exist yet (Task #4)
    __all__ = [
        "DocxBuilder",
        "TestBuilder",
        "ActivityBuilder",
        "VideoBuilder",
        "ObjectivesBuilder",
        "SummaryBuilder",
        "InfographicBuilder",
        "DiscussionBuilder",
        "AssignmentBuilder",
    ]
