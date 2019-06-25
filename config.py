"""Configuration shared program constant variables"""
from typing import List


SKILL_FIELD_REPEATS: List[str] = \
    ['relevancy', 'priority', 'score', 'notes', 'current_capacity',
     'targeted_capacity']
NO_SCORER_SKILL_FIELDS: List[str] = ['current_capacity', 'targeted_capacity']
SKILLS: List[str] = \
    ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'C1', 'C2', 'C3',
     'C4', 'C5', 'C6', 'C7', 'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2',
     'F3', 'F4', 'F5', 'F6', 'F7', 'G1', 'G2', 'H1', 'H2', 'H3', 'I1', 'I2',
     'J1', 'J2', 'K1', 'K2', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5',
     'N1', 'N2', 'O1', 'O2', 'P1', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7',
     'Q8', 'Q9', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'S1', 'S2', 'S3', 'T1',
     'T2', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'V1', 'W1',
     'X1', 'X2', 'X3']
SKILL_DATA_FIELDS: List[str] = [
    '{}_{}'.format(skill, field_type)
     for skill in SKILLS
     for field_type in SKILL_FIELD_REPEATS]
