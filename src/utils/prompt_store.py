SYSTEM_CONTEXT =\
'''\
You are an expert in contractual agreements and extracting key terms.
'''

PROMPT_0_INITIAL_KEY_TERM_EXTRACTION = \
'''\
(NOTE: DO NOT CAPTURE KEY TERMS FROM TABLE OF CONTENTS)
It is important to carefully read and analyze the text closely, paying close attention to sections related to financial terms.
Look for terms that have an impact on the financial aspects of the document, such as payment terms, costs, interest rates,
fees, awards, bonuses, salary, penalties, obligations, travel expenses, commitments, payment dates, etc.

Provide a comprehensive list of all key terms, quantities, numbers, time durations and amounts.
The goal is to capture all terms that allow for accurate calculation/estimation of the total cost/value of the contract.

Start the list with summary information on the document. Then list the key terms.

Summary Format:
The 'contract_type' indicates the type of contract
The 'contract_synopsis' describes the contract summary

Key term format:
The 'title' will represent a hierarchy or path of categories/subcategories, separated by slashes (/).  Should be general enough to be applied to multiple similar contracts.
There is no limit to the depth of hierarchy.
Each category should contain no more than 5 words.
The 'description' should be summary of the key term.
Every 'quantity' extracted should include the following fields:
unit: The type of unit (e.g. days, dollars, hours, year, month, percentage).
value: 2000 (money), 2018 (year), 30 April (date), 12 (percentage)
subject: Indicates what entity this refers to
key_term_importance: 0-10 float value to indicate how important is this key term in the document.
frequency: How often the amount is applied (e.g., monthly, annually, one-time).
text: The relevant text from the document which contains the key term
Example:

Input Text:
"An employee under this agreement is eligible to join health insurance plan, valued at $225 per month."

Expected Output:
[
    {
       "contract_type": "Employement Agreement",
       "contract_synopsis": "An employement agreement for a new employee with company x"
    },
    {
        "title": "Benefits/Insurance Plan",
        "description": "Eligible employee will receive $225 per month for health insurance"
        "quantities": [
            {
                "value": "225",
                "unit": "dollars",
                "frequency": "monthly",
            }
        ],
        "relevant_party": "employee",
        "key_term_importance": 10.0,
        "text": "An employee under this agreement is eligible to join health insurance plan, valued at $225 per month."
    }, ...
]
'''

PROMPT_X_REMOVE_UNIMPORTANT_CHARACTERS_AND_TEXT =\
'''\
Strip out all the unimportant formatting white space and remove all unimportant content then return the complete 
cleaned text:\n\n'
'''

PROMPT_1_ITERATIVE_KEY_TERM_EXTRACTION =\
'''\
Re-read the document expanding the list to cover ALL additional key terms not captured in the list so far.\n\n
PROVIDE ONLY THE NEW TERMS (IF NO NEW TERMS CAN BE FOUND RESPOND WITH A EMPTY LIST)\n\n'
'''



def construct_prompt_2_append_and_edit(text_chunk, keyterms_so_far):
    return f'''\
You are compiling a comprehensive list of key terms for a document.

The key terms you found so far:
{keyterms_so_far}

Here is an excerpt of text from the document:

{text_chunk}

(NOTE: DO NOT CAPTURE KEY TERMS FROM TABLE OF CONTENTS)
It is important to carefully read and analyze the text closely, paying close attention to sections related to financial terms.
Look for terms that have an impact on the financial aspects of the document, such as payment terms, costs, interest rates,
fees, awards, bonuses, salary, penalties, obligations, travel expenses, commitments, payment dates, etc.

Provide a comprehensive list of all key terms, quantities, numbers, time durations and amounts.
The goal is to capture all terms that allow for accurate calculation/estimation of the total cost/value of the contract.

Key term format:
The 'title' will represent a hierarchy or path of categories/subcategories, separated by slashes (/).  (NOTE: MUST BE GENERAL ENOUGH to be applied to multiple similar contracts.)
There is no limit to the depth of hierarchy.
Each category should contain no more than 5 words.
The 'description' should be summary of the key term.
Every 'quantity' extracted should include the following fields:
unit: The type of unit (e.g. days, dollars, hours, year, month, percentage).
value: 2000 (money), 2018 (year), 30 April (date), 12 (percentage)
subject: Indicates what entity this refers to
key_term_importance: 0-10 float value to indicate how important is this key term in the document.
frequency: How often the amount is applied (e.g., monthly, annually, one-time).
text: The relevant text from the document which contains the key term
Example:

Input Text:
"An employee under this agreement is eligible to join health insurance plan, valued at $225 per month."

Expected Output:
[
    {{
       "contract_type": "Employment Agreement",
       "contract_synopsis": "An employment agreement for a new employee with company x"
    }},
    {{
        "title": "Benefits/Insurance Plan",
        "description": "Eligible employee will receive $225 per month for health insurance"
        "quantities": [
            {{
                "value": "225",
                "unit": "dollars",
                "frequency": "monthly",
            }}
        ],
        "relevant_party": "employee",
        "key_term_importance": 10.0,
        "text": "An employee under this agreement is eligible to join health insurance plan, valued at $225 per month."
    }}, ...
]

Given the excerpt of text from the document respond with a list of only the new key terms as well as any edits that should be made
to the existing keyterms.

To signify an edit indicate the id of the existing key term then re-write the new key term with the modified values.
If the key-term should be removed indicate this.

For example if the key term list were:
[
    {{
        "id": 1,
        "title": "Driver aka Antron Brown's Contact Information/Phone Number",
        "description": "phone number is 702-132-1008",
        "relevant_party": "Driver",
        "key_term_importance": 10.0,
        "text": "The driver Antron Brown's contact cell phone number is 702-132-1008"
    }},
    {{
        "id": 2,
        "title": "Contact Information/Cell Number",
        "description": "A phone number is 702-132-1008",
        "key_term_importance": 10.0,
        "text": "The driver Antron Brown's contact cell phone number is 702-132-1008"
    }},
    {{
        "id": 3,
        "title": "Term and Agreement Territory/Initial Term",
        "description": "Initial Term is from 1/1/1902 to 12/31/1903"
        "text": "Initial Term: Effective Date: 1/1/1902 to Expiration Date: 12/31/1903",
        "key_term_importance": 8.0,
    }},
    {{
        "id": 4,
        'title': "Driver's Services/Production Days/Photo Sessions/Duration", 
        'description': 'Each session not to exceed six (6) hours', 
        'quantities': [{{'value': '6', 'unit': 'hours', 'frequency': 'per session'}}], 
        'relevant_party': 'Driver', 'key_term_importance': 7.0, 'text': 'Each session not to exceed six (6) hours'
        "key_term_importance": 7.5,
    }},
    {{
        "id": 5,
        "title": "Driver Services/Email Campaigns",
        "description": "Driver will forward Toyota\u2019s promotional email campaigns to Driver\u2019s database of users upon request.",
        "quantities": [],
        "relevant_party": "Antron Brown",
        "key_term_importance": 7.0,
        "text": "Driver will forward Toyota\u2019s promotional email campaigns to Driver\u2019s database of users upon request."
    }}
]
Your edits would be (NOTE: YOU CAN OMIT FIELDS THAT HAVE STAYED THE SAME):
[
    {{
        "id": 1,
        "title": "Contact Information/Phone Number", # Rename, make more general
        "quantities":[{{
            "value": "702-132-1008',
            "unit": "phone number",
            "type": "cell"
        }}],
        "relevant_party": "Antron Brown", # relevant party made more specific
        "key_term_importance": 7.0, # importance decreased
        "edits": ["key_term_importance", "relevant_party","important_values","title"]
    }},
    {{
        "id": 2,
        "action": "Remove",
        "reason": "Duplicate"
    }},
    {{
        "id": 3,
        "title": "Agreement Duration/Initial Term", # Improved generality, made more descriptive and applicable to multiple documents
        "quantities": [ # Added quantities
            {{
                "value": "1/1/1902",
                "unit": "date",
                "subject": "Initial Term Start",
                "frequency": "one-time"
            }},
            {{
                "value": "12/31/1903",
                "unit": "date",
                "subject": "Initial Term End",
                "frequency": "one-time"
            }}
        ],
        "key_term_importance": 10.0, # importance increased
        "edits": ["key_term_importance", "relevant_party","important_values","title"]
    }},
    {{
        "id": 4,
        'title': "Services/Production Days/Photo Sessions/Duration", # Made more generic and applicable to multiple documents
        'relevant_party': 'Antron Brown', # Disambiguated relevant party
        "key_term_importance": 10.0, # importance increased
        'edits_made': ["key_term_importance", "title","relevant_party"] # Fields changed
    }}
]

Structure your response as a python dictionary:
{{
    "new_key_terms": [{{...}}, ...],
    "edits": [{{...}}, ...]
}}
    '''


def construct_hypothetical_keyterms_post_process_prompt(synopsis_info, title_info_only):
    return f'''\
{title_info_only}

Given the document:
{synopsis_info}

Construct a good Taxonomy for this type of document. (NOTE: Categories/Sub-Categories should not have any document specific 
entity names in them).  A good taxonomy should be abstractable and able to be applied to any document of a similar 
type.
Provide a comprehensive and complete list of the keyterm categories and sub-categories you would
expect to find in this document.

For example an employment agreement might have:

Parties/Employer Information
Parties/Employee Information
Position and Duties/Job Title
Position and Duties/Job Description and Responsibilities
Position and Duties/Reporting Structure
Compensation/Salary or Wages
Compensation/Bonus or Incentive Plans
Compensation/Other/Expense Reimbursement
Benefits/Health Insurance
Benefits/Retirement
Work Hours and Breaks/Schedule
Work Hours and Breaks/Overtime Policy
Confidentiality and Non-Disclosure/Confidential Information
Confidentiality and Non-Disclosure/Non-Disclosure Agreements
Term and Termination/Duration of Employment
Term and Termination/Termination Conditions
Term and Termination/Notice Period
Non-Compete and Non-Solicit/Non-Compete Clauses
Non-Compete and Non-Solicit/Non-Solicit Clauses
Dispute Resolution/Arbitration
Dispute Resolution/Litigation
Miscellaneous/Amendments
Miscellaneous/Governing Law

Respond only in a the following structured format:\n
{{
    "expected_keyterm_categories": [\"Category/Sub_Category\", ...]
}}
'''


def construct_hypothetical_keyterms_assignment_prompt(synopsis_info, hypo_terms, key_term_str):
    return f'''\
Given the document:
{synopsis_info}

AND Given the hypothetical terms:
{hypo_terms}

AND Given the key terms extracted from the document:
title = src_text_snippet
{key_term_str}

Provide an assignment for each key term by title with the appropriate hypothetical category/sub-category.
ALSO if a term is not a key term i.e. was extracted from a table of contents indicate its category as:
"Not A KeyTerm/Reason" # Reason should be a short descriptive reason
for example
"Not A KeyTerm/Table of contents" # Reason should be a short descriptive reason

Respond only in a the following structured format:\n
{{
    "keyterm_category_assignment": [ {{\"title\": \"keyterm_title_1\", \"assignment\": \"category/sub_category\"}}, ...]
}}
'''

def construct_post_process_prompt(synopsis_info, key_term_str):
    return f'''\
Given the document:
{synopsis_info}

AND Given the key terms extracted from the document:
{key_term_str}

FOR EACH KEY TERM PROVIDE A CONFIDENCE SCORE 1-10 WITH LOWER SCORES REPRESENTING KEY TERMS WHICH WERE EXTRACTED FROM 
TEXT THAT ARE NOT IN FACT KEY TERMS (EXAMPLES MIGHT INCLUDE A TABLE OF CONTENTS WHICH HAS CATEGORICALLY IMPORTANT 
INFORMATION BUT NO ACTUAL KEY TERMS IN IN IT) 10 REPRESENTS HIGHLY DETAILED KEY TERMS THESE ARE TYPICALLY EXTRACTED 
FROM TEXT WITH DETAILED QUANTITATIVE INFORMATION
ALSO PROVIDE MORE GENERALIZED TITLES FOR EACH OF THE KEY TERMS EXTRACTED, RENAME THEM TO TERMS YOU WOULD EXPECT TO FIND 
IN ANY SIMILAR DOCUMENT.
ALSO PROVIDE MORE GENERIC NAMES FOR THE RELEVANT PARTIES
for example an agreement between "Honda" and "James Donahue" would become "Company", "Individual"
respectively
ALSO PROVIDE A CATEGORY FOR EACH TITLE UNDER THIS CONTRACT TYPE WHICH THE KEY TERM FITS INTO

Respond only in a the following structured format:\n
{{
    "keyterm_confidence": [{{"current_title":"title_1", "confidence": 7}}, ...]
    "keyterm_category": [{{"current_title":"title_1", "category": "..."}}, ...]
    "generic_relevant_parties": [{{"current_name":"name_1", "generic_name": "..."}}, ...]
    "improved_titles": [{{"current_title":"title_1", "improved_title": "..."}}, ...]
}}
\n\n'
        '''
def construct_prompt_0(text_chunk):
    return f'Given the text:\n' \
           f'{text_chunk}\n\n' \
           f'Extract a list of key terms from the text above.\n\n' \
           f'{PROMPT_0_INITIAL_KEY_TERM_EXTRACTION}'

def construct_prompt_1():
    return PROMPT_1_ITERATIVE_KEY_TERM_EXTRACTION