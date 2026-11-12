# How to manage DB

### What service do we provide?
1. Table/graph when does job posting email sended.
2. Monthly recruiting type rank (job title, full time/part time/intern. etc., required experiences)
3. Monthly required technical skills rank (required skills/preferred skills)
4, Responsibilities per job titles

### What condition de i have to consider?
1. Make seperate tables for all tags

### Table structure
1. Posting summary table
| Posting id | Company label | Date label | Job title id | Responsibility ids | Skill ids | Experience ids | Employment type ids |

2. Job title table
| Job title id | Job title label | Industrial domain ids | Job family id | Seniority id |

3. Industrial domain table
| Industrial domain id | Industrial domain label |

4. Job family table
| Job family id | Job family label |

5. Seniority table
| Seniority id | Seniority label |

6. Responsibility table
| Responsibility Id | Responsibility label | Task area id |
- Responsibility label is summary of the task.

7. Task area table
| Task area id | Task area label |

8. Skill table
| Skill id | Skill label | Skill category id |

9. Skill category table
| Skill category id | Skill category label |

10. Experience table
| Experience id | Experience type id | Industrial domain id | Requirement id | Min yaer label | Max year label | Degree level   label |
