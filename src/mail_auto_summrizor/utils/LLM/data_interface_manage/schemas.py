# This file stores schemas that llm should follow.
# Schema is data format that llm follows when response.


# ============================
# Evidence extracting schema
# ============================
def make_evidence_extraction_schema(subjects: list[str]) -> dict:
    """Build an evidence schema using exact TagEmbeddingSearch taxonomy names."""
    if not subjects:
        raise ValueError("[WARNING] At least one evidence subject must be provided.")

    return {
        "type": "object",
        "properties": {
            "evidences": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "enum": subjects,
                            "description": "Exact taxonomy subject relevant to this evidence.",
                        },
                        "text": {
                            "type": "string",
                            "description": (
                                "Original sentence or consecutive sentences copied from "
                                "the posting, preserving requirement wording and context."
                            ),
                        },
                    },
                    "required": ["subject", "text"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["evidences"],
        "additionalProperties": False,
    }

# ============================
# Job title schema
# ============================
JOB_TITLE_SCHEMA = {
    "type": "object",
    "properties": {
        "industrial_domain_tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Existing industrial-domain tag IDs; empty if none apply.",
        },
        "job_family_tag": {
            "type": ["string", "null"],
            "description": "One existing primary job-family tag ID, or null if unsupported.",
        },
        "seniority_tag": {
            "type": ["string", "null"],
            "description": "One existing seniority tag ID, or null if unsupported.",
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "enum": [
                            "industrial_domain_tags",
                            "job_family_tag",
                            "seniority_tag",
                        ],
                    },
                    "text": {"type": "string"},
                },
                "required": ["subject", "text"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "industrial_domain_tags", "job_family_tag", "seniority_tag", "evidence"
    ],
    "additionalProperties": False,
}

# ============================
# Responsibilities schema
# ============================
TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_area_tag": {
            "type": ["string", "null"],
            "description": "Existing task-area tag ID, or null if no candidate fits.",
        },
        "task_summary": {
            "type": "string",
            "description": "Concise summary of one distinct job responsibility.",
        },
        "evidence": {
            "type": "string",
            "description": "Exact original sentence(s) supporting the task and its classification.",
        },
    },
    "required": ["task_area_tag", "task_summary", "evidence"],
    "additionalProperties": False,
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
#   - label => skill의 세부 정보 (c, python, java)
#   - category => skill 분류(programming language)
# ============================
SKILL_SCHEMA = {
    "type": "object",
    "properties": {
        "label_tag": {
            "type": ["string", "null"],
            "description": "Existing specific-skill tag ID, or null if no candidate fits.",
        },
        "category_tag": {
            "type": ["string", "null"],
            "description": "Existing skill-category tag ID, or null if no candidate fits.",
        },
        "evidence": {
            "type": "string",
            "description": "Exact original sentence supporting the skill and its requirement status.",
        },
    },
    "required": ["label_tag", "category_tag", "evidence"],
    "additionalProperties": False,
}

EXPERIENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "experience_type_tag": {
            "type": ["string", "null"],
            "description": "Existing experience-type tag ID; null for degree-only requirements.",
        },
        "industrial_domain_tag": {
            "type": ["string", "null"],
            "description": "Existing domain tag ID when explicitly supported; otherwise null.",
        },
        "requirement": {
            "type": "string",
            "enum": ["required", "preferred", "unspecified"],
        },
        "min_years": {
            "type": ["number", "null"],
            "description": "Explicit minimum years; null if no minimum is stated.",
        },
        "max_years": {
            "type": ["number", "null"],
            "description": "Explicit maximum years; null if no maximum is stated.",
        },
        "degree_level": {
            "type": ["string", "null"],
            "enum": ["bachelor", "master", "doctorate", "other", None],
            "description": "Explicit education level; this is an attribute, not a taxonomy tag.",
        },
        "evidence": {
            "type": "string",
            "description": "Exact original sentence supporting this requirement.",
        },
    },
    "required": [
        "experience_type_tag", "industrial_domain_tag", "requirement",
        "min_years", "max_years", "degree_level", "evidence"
    ],
    "additionalProperties": False,
}

SKILLS_SCHEMA = {
    "type": "object",
    "properties": {
        "required_skills": {"type": "array", "items": SKILL_SCHEMA},
        "preferred_skills": {"type": "array", "items": SKILL_SCHEMA},
        "other_skills": {"type": "array", "items": SKILL_SCHEMA},
        "experience_requirements": {"type": "array", "items": EXPERIENCE_SCHEMA},
    },
    "required": [
        "required_skills", "preferred_skills", "other_skills",
        "experience_requirements"
    ],
    "additionalProperties": False,
}