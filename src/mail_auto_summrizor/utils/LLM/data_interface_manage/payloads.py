'''This file stores payloads for request.'''

def create_payload(
        description:str,
        model:str,
        schema:dict,
        system_content:str
    ) -> dict:
    return {
        "model": model,
        "messages":[
            {
                "role":"system",
                "content":system_content
            },
            {
                "role":"user",
                "content":f'posting:\n{description}'
            }
        ],
        "format":schema,
        "stream":False,
        "think":False,
        "keep_alive":"10m",
        "options":{
            "temperature": 0.1,
            "num_predict": 512
        }
    }

# ================================================
# System contents
# ================================================

RULE_SCRIRT = '''
You=professional recruiting analytics.
Rule:
1 Extract information only when it is supported by posting
2 Do not invent or assume unstated info
3 If info unavailable return empty string or empty array according to schema
'''

COMPANY_SYS_CONTENT = RULE_SCRIRT + '''
Get company name
'''

JOB_TITLE_SYS_CONTENT = RULE_SCRIRT + '''
\n4 Preserve title as written in posting.
Get job title.
'''

CMP_JT_SYS_CONTENT = RULE_SCRIRT + '''
\n4 Preserve name and title as written in posting.
Get company name and job title.
'''

RESPONSIBILITIES_SYS_CONTENT = RULE_SCRIRT + '''
\n4 Preserve important technical details and purpose of each task.
Get all distinct job responsibilities explicitly described in posting. 
'''

SKILLS_SYS_CONTENT = RULE_SCRIRT + '''
\n4 required_skills: Technical skills stated as required qualification. Includes programming languages, frameworks, tools. etc. Convert each skill into concise, standardize tag.
5. preferred_skills: Technical skills stated as preferred or anvantageous. Use same tagging rule.
6. experience_requirements: Explicit degree or relevant work experience requirements. e.g) ["Bachelor degree.CS","Field experience.3Y+"]
'''

SOFT_SKILLS_SYS_CONTENT = RULE_SCRIRT + '''
\n4 Soft_skills: Extract explicitly stated non-technical skills, personal attributes, and interpersonal abilities required or preferred for the job.
5 employment_type: Find is it fulltime, parttime or intern.etc.
'''