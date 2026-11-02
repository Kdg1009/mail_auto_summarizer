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
        "job_family":{
            "type":"string",
            "enum": [
                "Robotics Engineering",
                "AI/ML Engineering",
                "Software Engineering",
                "Embedded Software Engineering",
                "Mechanical Engineering",
                "Research Engineering",
                "Simulation Engineering",
                "Hardware Engineering",
                "System Engineering",
                "Project Manager",
                "Other",
                "unspecified"
            ]
        },
        "specializations": {
            "type": "array",
            "items": {"type":"string"}
        },
        "seniority": {
            "type": "string",
            "enum": [
                "intern",
                "junior",
                "mid",
                "senior",
                "lead",
                "manager",
                "director",
                "executive",
                "other",
                "unspecified"
            ]
        },
        "domain_tags": {
            "type": "array",
            "items": {"type":"string"},
            "description":"Normalized detailed domain of job title e.g., simulation"
        }
    },
    "required":[
        "job_family",
        "specializations",
        "seniority",
        "domain_tags"
    ],
    "additionalProperties":False
}

# ============================
# Responsibilities schema
# ============================
TASK_SCHEMA = {
    "type":"object",
    "properties": {
        "category": {
            "type":"string",
            "enum": [
                "algorithm_development",
                "software_development",
                "system_integration",
                "ai_model_development",
                "testing_validation",
                "research",
                "deployment",
                "maintenance",
                "management",
                "other",
                "unspecified"
            ]},
        "task": {
            "type":"string",
            "description":"Specific task summarized based on postings"    
        },
        "task_tag": {
            "type":"string",
            "description":"Normalized detailed task tag. e.g., slam_development"
        },
        "evidence":{
            "type":"string",
            "description":"Original text evidence extracted from posting"
        }
    },
    "required":[
        "category",
        "task",
        "task_tag",
        "evidence"
    ],
    "additionalProperties":False
}

RESPONSIBILITIES_SCHEMA = {
    "type":"object",
    "properties":{
        "summary":{"type":"string"}, # Human readable responsibilities summary,
        "tasks": {
            "type": "array",
            "items": TASK_SCHEMA
        }
    },
    "required":[
        "summary",
        "tasks"
    ],
    "additionalProperties":False
}

# ============================
# Skills schema
# ============================
SKILL_SCHEMA = {
    "type":"object",
    "properties":{
        "name": {
            "type":"string",
            "description":"Name of tech mentioned in posting"
        },
        "category": {
            "type":"string",
            "enum":[
                "programming_language",
                "framework_library",
                "robotics_middleware",
                "robotics_algorithm",
                "ai_machine_learning",
                "ai_model",
                "simulation_platform",
                "embedded_system",
                "hardware_interface",
                "operating_system",
                "development_tool",
                "cloud_infrastructure",
                "hardware",
                "technology",
                "software",
                "other",
                "unspecified"
            ]},
        "evidence":{"type": "string"}
    },
    "required":[
        "name",
        "category",
        "evidence"
    ],
    "additionalProperties": False
}

EXPERIENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": [
                "degree",
                "professional_experience",
                "project_experience",
                "internship",
                "certification",
                "other"
            ]
        },
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
        "degree_level": {
            "type": "string",
            "enum": [
                "high_school",
                "associate",
                "bachelor",
                "master",
                "doctorate",
                "any",
                "unspecified"
            ]
        },
        "field": {
            "type": "string",
            "description": "Major or required field of study/experience. Empty string if not applicable"
        }
    },
    "required": [
        "category",
        "requirement",
        "min_years",
        "max_years",
        "degree_level",
        "field"
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

# ============================
# Soft skills schema
# ============================
SOFT_SKILL_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": [
                "interpersonal",
                "cognitive",
                "self_management",
                "leadership",
                "work_attitude",
                "learning",
                "other"
            ]
        },
        "name": {
            "type": "string",
            "description": "Name of the soft skill"
        },
        "tag": {
            "type": "string",
            "description": "Normalized soft skill tag. e.g., communication"
        },
        "requirement": {
            "type": "string",
            "enum": [
                "required",
                "preferred",
                "unspecified"
            ]
        },
        "evidence": {
            "type": "string",
            "description": "Original text evidence from the job posting"
        }
    },
    "required": [
        "category",
        "name",
        "tag",
        "requirement",
        "evidence"
    ],
    "additionalProperties": False
}

SOFT_SKILLS_SCHEMA = {
    "type": "object",
    "properties": {
        "soft_skills": {
            "type": "array",
            "items": SOFT_SKILL_SCHEMA
        }
    },
    "required": [
        "soft_skills"
    ],
    "additionalProperties": False
}