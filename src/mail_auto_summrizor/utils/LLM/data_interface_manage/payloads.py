'''This file stores payloads for request.'''
import psutil

def create_payload(
        description:str,
        model:str,
        schema:dict,
        system_content:str
    ) -> dict:

    memory_info = psutil.virtual_memory()
    flush_model = memory_info.percent > 95.0

    return {
        "model": model,
        "messages":[
            {
                "role":"system",
                "content":system_content.strip()
            },
            {
                "role":"user",
                "content":f'posting:\n{description.strip()}'
            }
        ],
        "format":schema,
        "stream":False,
        "think":False,
        "keep_alive":0 if flush_model else '10m',
        "options":{
            "temperature": 0.0,
            "num_predict": 4096
        }
    }

# ================================================
# System contents
# ================================================

RULE_SCRIRT = '''
You are job posting information extractor
Rules:
1 Extract information only when it is supported by posting
2 Do not invent or assume unstated info
3 Use empty strings or null only as allowed by the schema
4 Distinguish required, preferred, and unspecified information
'''

JOB_TITLE_SYS_CONTENT = RULE_SCRIRT + '''
Task:Classify the job title
1 Select exactly one primary job_family
2 Select multiple specializations when applicable
3 Use domain_tags for technology or industry domains
4 Determine seniority only from explicit title or experience evidence
5 Do not treat employment type as seniority
6 Remove company names and hiring slogans from title interpretation
7 Use the closest available enum when classification is possible
8 Use Other when no listed job_family fits
Tag examples:
- specializations: slam, computer_vision, robot_learning
- domain_tags: robotics, physical_ai, autonomous_driving
'''

RESPONSIBILITIES_SYS_CONTENT = RULE_SCRIRT + '''
Task: Extract job responsibilities

Rules:
- Extract distinct and meaningful responsibilities.
- Merge closely related or overlapping tasks.
- Do not create separate tasks for minor details
  of the same responsibility.
- Preserve important technical details.
- Use concise snake_case task descriptions.
- Use short, standardized task_tag values.
- task_tag must represent a category or concept,
  not repeat the entire task description.
- Keep evidence concise and directly supported
  by the original posting.
- Do not invent responsibilities.
- Prefer a concise and comprehensive result
  over an excessively long task list.
- Return valid JSON matching the provided schema.
- Each task must represent a unique activity or responsibility.
- Before generating the final JSON, check for duplicate tasks

Examples:
- "Develop SLAM algorithms"
  -> task_tag: slam_development
- "Integrate ROS 2 navigation"
  -> task_tag: ros2_navigation_integration
- "Validate robot performance in simulation"
  -> task_tag: simulation_validation
'''

SKILLS_SYS_CONTENT = RULE_SCRIRT + '''
Task: Extract technical skills and experience requirements

Technical skills:
1 required_skills: Tech skills explicitly required by the posting
2 preferred_skills: Tech skills explicitly described as preferred, optional,
   advantageous, or a plus
3 other_skills: Tech skills mentioned without a clear required/preferred status
4 Do not duplicate the same skill across arrays
5 Group closely related technologies into one meaningful skill
   when they describe the same capability
6 Select the closest category from the schema
7 Keep evidence short and supported by the source

Experience:
1 Extract explicit degree, professional experience, project experience,
    internship, and certification requirements
2 Distinguish required and preferred conditions
3 Convert explicit experience durations to numeric years
4 Use null for unknown min_years or max_years
5 Use degree_level only for degree requirements
6 Do not convert a degree requirement into years of experience
7 Do not assume that a job requires experience when none is stated

Examples:
- "At least 3 years of experience"
  -> professional_experience, min_years: 3
- "3 to 5 years of experience"
  -> professional_experience, min_years: 3, max_years: 5
- "Master's degree preferred"
  -> degree, requirement: preferred, degree_level: master
- "Experience with ROS 2 is a plus"
  -> preferred_skills, tag: ros2
'''

SOFT_SKILLS_SYS_CONTENT = RULE_SCRIRT + '''
Task: Extract non-technical skills and personal attributes

Rules:
1 Extract explicitly stated interpersonal, cognitive,
   self-management, leadership, work attitude, and learning skills
2 Do not include programming languages, frameworks, or technical tools
3 Normalize equivalent expressions to consistent snake_case tags
4 Distinguish required and preferred attributes
5 Use unspecified when requirement status is unclear
6 Merge synonymous attributes
7 Do not infer personality traits from job responsibilities
8 Return an empty array when no soft skills are stated

Tag examples:
- communication
- teamwork
- problem_solving
- analytical_thinking
- leadership
- adaptability
- time_management
- continuous_learning
'''