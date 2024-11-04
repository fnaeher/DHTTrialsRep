# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:37:33 2024

@author: AnatolFiete.Naeher
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:49:44 2024

@author: AnatolFiete.Naeher
"""
# -*- coding: utf-8 -*-
"""
Author: Fiete Näher
"""

import sys
from data_prep import data_prep1
from ctd_load import d_CTD

sys.path.append('J:\\5_Forschung\\5.6_Research overview\\Forschungsprojekte\\'
        'Representativity in Digital Real-World Trials\\'
        'Did DHT increase representativity in Clinical Trials\\Code')
   
d_CTD['CTD_2'] = data_prep1(d_CTD)

key = ["race", "ethnicity", "gender", "sex", "male", "female", "age", 
       "enrollment"]

m = {}

m = [
    item for item in d_CTD['CTD_2']['title']
    if any(key.lower() in item.lower().split() for key in key)
]

vis = ['Age',
 'Age (<60 or ≥60 years)',
 'Age (Statistics)',
 'Age (Strata per Randomization)',
 'Age (categorical)',
 'Age (years)',
 'Age (years) (categorical)',
 'Age - Part 1 population',
 'Age 65 or above',
 'Age > 15 years',
 'Age > 60 years',
 'Age >/= 60 years',
 'Age >65 years',
 'Age Categorical',
 'Age Categorical (≤65 or >65 Years Old)',
 'Age Categories',
 'Age Categorization, Female Only',
 'Age Characterization Female Only',
 'Age Classification',
 'Age Continous',
 'Age Continuous',
 'Age Continuous (China Substudy)',
 'Age Continuous (PEP)',
 'Age Continuous in Follicular Lymphoma Sub-Population',
 'Age Continuous, without Noncompliant Site',
 'Age Customized',
 'Age Customized, by Disease Type',
 'Age Group',
 'Age Range',
 'Age Strata',
 'Age Strata per Randomization',
 'Age at Enrollment',
 'Age at randomization (hours)',
 'Age at study enrollment',
 'Age at time of randomization',
 'Age by Sex',
 'Age categorical',
 'Age categories',
 'Age categorization Females Only',
 'Age continuous- adults subjects',
 'Age continuous-pediatric study',
 'Age end of study',
 'Age group',
 'Age group at randomization',
 'Age of participant',
 'Age of participants',
 'Age of participants by 10-year age groups',
 'Average of site-level mean age',
 'Average participant age +/- SD',
 'Black Race',
 'Black race',
 'Child Age',
 'Child age',
 'Child age (years), median (IQR)',
 "Child's Age",
 "Child's Age at Consent",
 "Child's Gender",
 "Child's Sex",
 "Child's Sex: Female, Male",
 "Child's age",
 'Chronological age',
 'Current Gender Identity',
 'Distribution of age',
 'Enrollment by Country',
 'Ethnicity',
 'Ethnicity ( NIH/OMB)',
 'Ethnicity (Asia)',
 'Ethnicity (NIH/OMB)',
 'Ethnicity (NIH/OMB) (Influenza Season 2015-2016)',
 'Ethnicity (NIH/OMB) (Influenza Season 2016-2017)',
 'Ethnicity Origin',
 'EudraCT Age Categories',
 'Female Age',
 'Female Age Category',
 'Female Age, Continuous',
 'Female age, customized',
 'Gender',
 'Gender (China Substudy)',
 'Gender - Part 1 Population',
 'Gender Identity',
 'Geographic Region of Enrollment',
 'Infant - age at randomization',
 'Infant mean gestational age',
 'Infant sex at birth',
 'Location at Enrollment',
 'Location of Enrollment',
 'Location of enrollment',
 'Median Age (Range)',
 'Median Age Categories',
 'Median age',
 'Participating child age (years)',
 'Patient Sex: Female, Male',
 'Patients age were between 30-69 years',
 'Patients enrolled were female gender over the age of 18.',
 'Phase I: Youth Hispanic/ Latinx Ethnicity',
 'Phase I: Youth Race',
 'Phase I: Youth age',
 'Phase II: Youth Hispanic/ Latinx Ethnicity',
 'Phase II: Youth age',
 'Primary Race',
 'Protocol-defined Age Cohorts (All Participants As Treated Population)',
 'RACE',
 'RACE (NIH/OMB)',
 'Race',
 'Race & Ethnicity',
 'Race (Asian vs Non-Asian) at Randomization',
 'Race (NIH/OMB)',
 'Race (NIH/OMB) (Influenza Season 2015-2016)',
 'Race (NIH/OMB) (Influenza Season 2016-2017)',
 'Race (PEP)',
 'Race - Peru',
 'Race - Puerto Rico',
 'Race - South Africa',
 'Race - Thailand',
 'Race - U.S.A.',
 'Race / Ethnicity',
 'Race Categories',
 'Race Class',
 'Race Customized',
 'Race [Caucasian / White]',
 'Race class',
 'Race or ethnicity',
 'Region Of Enrollment',
 'Region of Enrollment',
 'Region of enrollment',
 'Risk Factor at Enrollment: Age >= 75 Years',
 'Sex Assigned at Birth',
 'Sex and gender',
 'Sex of the Infant',
 'Sex: Female, Male',
 'Stratification Factor at Randomization Collected via IRT: Age Group',
 'Stratification Factor: Age',
 'Stratification Factor: Age Category',
 'Stratification Factor: Age Group',
 'Stratification Factor: Region of Enrollment',
 'Study Enrollment',
 'SubStudy 1: Age',
 'SubStudy 1: Ethnicity',
 'SubStudy 1: Race',
 'SubStudy 1: Sex',
 'SubStudy 2: Age',
 'SubStudy 2: Ethnicity',
 'SubStudy 2: Race',
 'SubStudy 2: Sex',
 'Subject Classification: Mean Age',
 'Subject characteristic - subject age',
 'Toddler age',
 'White race',
 'age',
 'age in years',
 'child age',
 'enrollment',
 'ethnicity',
 'race',
 'Child sex',
 'Child Sex at Birth',
 'Phase I: Youth sex',
 'Child Race',
 'Infant sex',
 'Child Ethnicity',
 'Gender of child',
 'Toddler sex',
 'Phase II: Youth sex',
 'Child Gender',
 'Participating child sex',
 'Phase II: Youth race',
 "Child's gender",
 'Age, Continuous',
 'Age, Categorical',
 'Child Hispanic Ethnicity',
 'Child gender',
 'Age, Continous: Dose Maintenance Period',
 'Age, Continuous (Influenza Season 2015-2016)',
 'Age, Continuous (Influenza Season 2016-2017)',
 'Age, Continuous, Compliant Participants',
 'Age, Customized',
 'Age, continuous: Period 2 (trial enrollment, induction ART)',
 'Age, continuous: Period 3 (randomization to once vs twice daily ABC+3TC)',
 'Age, continuous: Period 4 (randomization to stop versus continue cotrimoxazole)',
 'Age, customized',
 'Age-Categorical',
 'AgeCategorical',
 'AgeCategoricalOther',
 'Country of Enrollment',
 'Enrollment',
 'Enrollment Characteristics',
 'Enrollment Parameters',
 'Enrollment by Region',
 'Ethnicity, Customized',
 'Ethnicity, without Noncompliant Site',
 'Ethnicity/Race',
 'Ethnicity: Caucasian, Non-Caucasian',
 'Ethnicity: Spanish, Hispanic or Latino',
 'Gender at Beginning of Long term Follow-up Period',
 'Gender in patients completing study',
 'Gender, Male/Female: Compliant Participants',
 'Patient Age, Continuous',
 'Race (NIH/OMB): Dose Maintenance Period',
 'Race, Compliant Participants',
 'Race, Customized',
 'Race, without Noncompliant Site',
 'Race-Ethnicity',
 'Race/Ethnicity',
 'Race/Ethnicity, Customized',
 'Race/Ethnicity, customized',
 'Race/ethnicity',
 'Race: Extension Phase',
 'Region of Enrollment, Customized',
 'Region of Enrollment: United States',
 'Sex/Gender, Customized',
 'Sex: Female, Male (Influenza Season 2015-2016)',
 'Sex: Female, Male (Influenza Season 2016-2017)',
 'Sex: Female, Male (PEP)',
 'Sex: Female, Male: Dose Maintenance Period',
 'Study Specific Race/Ethnicity',
 'Toddler race/ethnicity',
 ' Age']
    
age = set()
race = set()
gender = set()
enrollment = set()

for item in vis:
    item_lower = item.lower()
    if 'age' in item_lower:
        age.add(item)
    elif 'race' in item_lower or 'ethnicity' in item_lower:
        race.add(item)
    elif 'gender' in item_lower or 'sex' in item_lower \
        or 'male' in item_lower or 'female' in item_lower:
        gender.add(item)
    elif 'enrollment' in item_lower in item_lower:
        enrollment.add(item)
        
