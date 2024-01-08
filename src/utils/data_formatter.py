import json

def format_quantities(quantities):
    """
    Formats quantities list into a JSON string.

    Args:
    quantities (list of dict): List of quantities, each as a dictionary.

    Returns:
    str: JSON string representing the list of quantities.
    """
    return json.dumps(quantities) if quantities else "[]"

def format_key_terms(key_terms):
    """
    Formats key terms data for CSV output.

    Args:
    key_terms (list of dict): List of key terms, each as a dictionary.

    Returns:
    list of dict: Formatted key terms data.
    """
    formatted_data = []
    for term in key_terms:
        formatted_term = {
            'contract_type': term.get('contract_type', ''),
            'contract_synopsis': term.get('contract_synopsis', ''),
            'id': term.get('id', ''),
            'title': term.get('title', ''),
            'description': term.get('description', ''),
            'quantities': format_quantities(term.get('quantities', [])),
            'relevant_party': term.get('relevant_party', ''),
            'key_term_importance': term.get('key_term_importance', 0),
            'total_cost': term.get('total_cost', 0)
        }
        formatted_data.append(formatted_term)
    return formatted_data