"""
The majors dict contains the available majors offered at Princeton
at any one time. The key will be the abbreviation, and the value will
be the department name.

A similar pattern holds for the certificates dict.

These dictionaries will have to be updated whenever the unviersity 
changes any abbreviation or department name.
"""

MAJOR_TO_CODE = {
    'African American Studies' : ['AAS'],
    'Anthropology': ['ANT'],
    'Architecture': ['ARC'],
    'Art and Archaeology': ['ART'],
    'Astrophysical Sciences': ['AST'],
    'Chemical and Biological Engineering':['CBE'],
    'Chemistry': ['CHM'],
    'Civil and Environmental Engineering': ['CEE'],
    'Classics': ['CLA'],
    'Comparative Literature': ['COM'],
    'Computer Science': ['COS'],
    'East Asian Studies': ['EAS'],
    'Ecology and Evolutionary Biology': ['EEB'],
    'Economics': ['ECO'],
    'Electrical Engineering': ['ELE'],
    'English': ['ENG'],
    'French and Italian': ['FRE', 'ITA'],
    'Geosciences': ['GEO'],
    'German': ['GER'],
    'History': ['HIS'],
    'Mathematics': ['MAT'],
    'Mechanical and Aerospace Engineering': ['MAE'],
    'Molecular Biology': ['MOL'],
    'Music': ['MUS'],
    'Near Eastern Studies': ['NES'],
    'Neuroscience': ['NEU'],
    'Operations Research and Financial Engineering': ['ORF'],
    'Philosophy': ['PHI'],
    'Physics': ['PHY'],
    'Politics': ['POL'],
    'Psychology': ['PSY'],
    'Public Policy': ['SPI'],
    'Religion': ['REL'],
    'Slavic Languages and Literatures': ['SLA'],
    'Sociology': ['SOC'],
    'Spanish and Portuguese': ['POR', 'SPA'],
    'Woodrow Wilson School of Public and International Affairs': ['WWS']
}

CODE_TO_MAJOR = {k: oldk for oldk, oldv in MAJOR_TO_CODE.items() for k in oldv}

CODE_TO_CERTIFICATE = {
    1: 'African American Studies',
    2: 'African Studies',
    3: 'American Studies',
    4: 'Applications of Computing',
    5: 'Applied and Computational Mathematics',
    6: 'Architecture and Engineering',
    7: 'Art and Archaeology',
    8: 'Asian American Studies',
    9: 'Biophysics',
    10: 'Cognitive Science',
    11: 'Contemporary European Politics and Society',
    12: 'Creative Writing',
    13: 'Dance',
    14: 'East Asian Studies',
    15: 'Engineering and Management Systems',
    16: 'Engineering Biology',
    17: 'Engineering Physics',
    18: 'Entrepreneurship',
    19: 'Environmental Studies',
    20: 'Ethnographic Studies',
    21: 'European Cultural Studies',
    22: 'Finance',
    23: 'Gender and Sexuality Studies',
    24: 'Geological Engineering',
    25: 'Global Health and Health Policy',
    26: 'Hellenic Studies',
    27: 'History and the Practice of Diplomacy',
    28: 'Humanistic Studies',
    29: 'Jazz Studies',
    30: 'Journalism',
    31: 'Judaic Studies',
    32: 'Language and Culture',
    33: 'Latin American Studies',
    34: 'Latino Studies',
    35: 'Linguistics',
    36: 'Materials Science and Engineering',
    37: 'Medieval Studies',
    38: 'Music Performance',
    39: 'Music Theater',
    40: 'Near Eastern Studies',
    41: 'Neuroscience',
    42: 'Planets and Life',
    43: 'Quantitative and Computational Biology',
    44: 'Robotics and Intelligent Systems',
    45: 'Russian, East European and Eurasian Studies',
    46: 'South Asian Studies',
    47: 'Statistics and Machine Learning',
    48: 'Sustainable Energy',
    49: 'Teacher Preparation',
    50: 'Technology and Society',
    51: 'Theater',
    52: 'Translation and Intercultural Communication',
    53: 'Urban Studies',
    54: 'Values and Public Life',
    55: 'Visual Arts'
}

CERTIFICATE_TO_CODE = {value:key for key, value in CODE_TO_CERTIFICATE.items()}