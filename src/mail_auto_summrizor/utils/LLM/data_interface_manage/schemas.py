'''
This file stores schemas that llm should follow.
Schema is data format that llm follows when response.
'''

# ============================
# Job title schema
# ============================
JOB_TITLE_SCHEMA = {
    "type":"object",
    "properties":{
        "industrial_domain_tags": {
            "type": "array",
            "items": {"type":"string"},
        },
        "job_family_tag":{"type":"string"},
        "seniority_tag": {"type": "string"},
        "evidence":{"type":"string"}
    },
    "required":[
        "industrial_domain_tags",
        "job_family_tag",
        "seniority_tag",
        "evidence"
    ],
    "additionalProperties":False
}

# ============================
# Responsibilities schema
# ============================
TASK_SCHEMA = {
    "type":"object",
    "properties": {
        "task_areas_tag": {"type":"string"},
        "task_summary": {"type":"string"},
        "evidence":{"type":"string"}
    },
    "required":[
        "task_areas_tag",
        "task_summary",
        "evidence"
    ],
    "additionalProperties":False
}

RESPONSIBILITIES_SCHEMA = {
    "type":"object",
    "properties":{
        "tasks": {
            "type": "array",
            "items": TASK_SCHEMA
        }
    },
    "required":[
        "tasks"
    ],
    "additionalProperties":False
}

# ============================
# Skills schema
# skills.tags.json has 2 tag types
#   - label
#   - category
# ============================
SKILL_SCHEMA = {
    "type":"object",
    "properties":{
        "label_tag": {"type":"string"},
        "category_tag": {"type":"string"},
        "evidence":{"type": "string"}
    },
    "required":[
        "label_tag",
        "category_tag",
        "evidence"
    ],
    "additionalProperties": False
}

EXPERIENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "experience_category_tag": {"type": "string"},
        "industrial_domain_tag": {"type":"string"},
        "requirement": {
            "type": "string",
            "enum": [
                "required",
                "preferred",
                "unspecified"
            ]
        },
        "min_years": {
            "type": ["number", "null"],
            "description": "Minimum required years of experience. null if not specified"
        },
        "max_years": {
            "type": ["number", "null"],
            "description": "Maximum required years of experience. null if not specified"
        },
        "degree_tag": {
            "type": "string",
            "enum": [
                "Bachelor",
                "Master",
                "Doctorate",
                "Unspecified",
                "null"
            ]    
        },
        "evidence": {"type": "string"}
    },
    "required": [
        "experience_category_tag",
        "industrial_domain_tag",
        "requirement",
        "min_years",
        "max_years",
        "degree_tag",
        "evidence"
    ],
    "additionalProperties": False
}

SKILLS_SCHEMA = {
    "type":"object",
    "properties":{
        "required_skills":{
            "type":"array",
            "items":SKILL_SCHEMA
        },
        "preferred_skills":{
            "type":"array",
            "items":SKILL_SCHEMA
        },
        "other_skills":{
            "type":"array",
            "items":SKILL_SCHEMA
        },
        "experience_requirements":{
            "type":"array",
            "items":EXPERIENCE_SCHEMA
        }
    },
    "required":[
        "required_skills",
        "preferred_skills",
        "other_skills",
        "experience_requirements"
    ],
    "additionalProperties":False
}
