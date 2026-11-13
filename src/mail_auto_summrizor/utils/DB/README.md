# How to manage DB

### What service do we provide?
1. Table/graph when does job posting email sended.
2. Monthly recruiting type rank (job title, full time/part time/intern. etc., required experiences)
3. Monthly required technical skills rank (required skills/preferred skills)
4. Responsibilities per job titles

### What condition do i have to consider?
1. Make seperate tables for all taxonomy tags
2. Distinct skills, responsibilities and experience saved as postings row.
3. Use junction table to represent relationship of postings and tags
4. Seperate taxonomy tag and job posting analyze.

### Table structure
There will be 3 types of tables
- Posting table: Represent individual job posting. This table works as root table that binds all properties of individual posting.
- Tag table: Stores taxonomy tags.
- Junction table: Work as mapper of posting data and tags.

[Tree structure of tables]
```txt
├── Posting table
│
├── Tag table
│   ├── Company Tag table
│   ├── Industrial domain Tag table
│   ├── Seniority Tag table
│   ├── Job family Tag table
│   ├── Task area Tag table
│   ├── Skill name Tag table
│   ├── Skill category Tag table
│   └── Experience type Tag table
│
└── Junction table
    ├── Posting - Job title table
    ├── Posting - Responsibility table
    ├── Posting - Skill table
    ├── Posting - Experience table
    ├── Skill name - Skill category table
    └── Job title - Industrial domain table
```

**Posting table**<br>
| Id | Company id | Job title id | Date | Source url | Employment type label |
| --- | --- | --- | --- | --- | --- |
| PK | FK | FK | DATETIME | TEXT | TEXT |

**Tag tables**<br>
All tag table has singular form.<br>
| Id | Label |
| --- | --- |
| PK | TEXT |

**Junction tables**<br>
Posting - Job title table<br>
| Id | Job title label | Job family Id | Seniority Id |
| --- | --- | --- | --- |
| PK | TEXT | FK | FK |

Posting - Responsibility table<br>
| Id | Summary | Task area Id | Posting id |
| --- | --- | --- | --- |
| PK | TEXT | FK | FK |

Posting - Skill table<br>
| Id | Posting id | Skill id | Requirement type label |
| - | - | - | - |
|PK|FK|FK|TEXT|

Posting - Experience table<br>
| Id | Experience Type Id | degree level label | Industrial domain Id | Max yaer | Min year | Requirement label | Posting Id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PK | FK | TEXT | FK | INTEGERNULL | INTEGERNULL | TEXT | FK |

Skill name - Skill category table<br>
| Id | Skill label name label | Skill category Id |
| --- | --- | --- |
| PK | TEXT | FK |

Job title - Industrial domain table<br>
| Id | Job title Id | Industrial domain Id |
| --- | --- | --- |
| PK | FK | FK |
