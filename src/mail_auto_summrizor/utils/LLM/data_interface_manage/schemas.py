'''
This file stores schemas that llm should follow.
Schema is data format that llm follows when response.
'''

COMPANY_SCHEMA = {
    "type":"object",
    "properties":{
        "company":{"type":"string"}
    },
    "required":[
        "company"
    ],
    "additionalProperties":False
}

JOB_TITLE_SCHEMA = {
    "type":"object",
    "properties":{
        "job_title":{"type":"string"}
    },
    "required":[
        "job_title"
    ],
    "additionalProperties":False
}

CMP_JT_SCHEMA = {
    "type":"object",
    "properties":{
        "company":{"type":"string"},
        "job_title":{"type":"string"}
    },
    "required":[
        "company",
        "job_title"
    ],
    "additionalProperties":False
}

RESPONSIBILITIES_SCHEMA = {
    "type":"object",
    "properties":{
        "responsibilities":{
            "type":"array",
            "items":{"type":"string"}
        }
    },
    "required":[
        "responsibilities"
    ],
    "additionalProperties":False
}

SKILLS_SCHEMA = {
    "type":"object",
    "properties":{
        "required_skills":{
            "type":"array",
            "items":{"type":"string"}
        },
        "preferred_skills":{
            "type":"array",
            "items":{"type":"string"}
        },
        "experience_requirements":{
            "type":"array",
            "items":{"type":"string"}
        }
    },
    "required":[
        "required_skills",
        "preferred_skills",
        "experience_requirements"
    ],
    "additionalProperties":False
}

SOFT_SKILLS_SCHEMA = {
    "type":"object",
    "properties":{
        "soft_skills":{
            "type":"array",
            "items":{"type":"string"}
        },
        "employment_type":{"type":"string"}
    },
    "required":[
        "soft_skills",
        "employment_type"
    ],
    "additionalProperties":False
}

# ================================
# Deprecated
# ================================

""" ROLE_SCHEMA = {
    "type":"object",
    "properties": {
        "job_title":{"type":"string"},
        "responsibilities":{
            "type":"array",
            "items":{"type":"string"}    
        },
        "degree_requirements":{
            "type":"array",
            "items":{"type":"string"}
        },
        "experience_requirements":{
            "type":"array",
            "items":{"type":"string"}
        },
        "required_skills":{
            "type":"array",
            "items":{"type":"string"}
        }
    },
    "required": [
        "job_title"
        "responsibilities",
        "degree_requirements",
        "experience_requirements",
        "required_skills"
    ],
    "additionalProperties": False
}

RECRUIT_SCHEMA = {
    "type":"object",
    "properties": {
        "company":{"type":"string"},
        "roles":{
            "type":"array",
            "items":ROLE_SCHEMA   
        },
        "soft_skills":{
            "type":"array",
            "items":{"type":"string"}
        },
        "employment_type":{"type":"string"}
    },
    "required": [
        "company",
        "roles",
        "soft_skills",
        "employment_type"
    ],
    "additionalProperties": False
} """