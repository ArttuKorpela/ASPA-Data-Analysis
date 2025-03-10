#Library for functions
import pandas as pd

def categorize_error_type(violation_id):
    category = None
    match violation_id[:2]:
        case "PT":
            category = "basic"
        case "AR":
            category = "function"
        case "MR":
            category = "library"
        case "PK":
            category = "exception_handling"
        case "TK":
            category = "file_handling"
        case "TR":
            category = "data_structures"
        case _:
            category = None
    return category



def errors_per_return(data):
    entries = []

    for entry in data:
        entries.append({
                    'email': entry.get('email'),
                    'filenames': [],
                    'time' : pd.to_datetime(entry.get('createdAt'),format='mixed'),
                    'basic' : 0,
                    'function' : 0,
                    'library' : 0,
                    'exception_handling' : 0,
                    'file_handling' : 0,
                    'data_structures' : 0,
                    'total' : 0 
                })
        for file in entry.get('analysis_files', {}):
            ((entries[-1])['filenames']).append(file['file_name'])
        ((entries[-1])['filenames']).sort()
        (entries[-1])['filenames'] = ' '.join((entries[-1])['filenames'])
        for result in entry.get('analysis_result', {}).get('results', []):
            for analysis in result.get('analysis_results', []):
                if 'violation_id' in analysis:
                    category = categorize_error_type(analysis.get('violation_id'))
                    (entries[-1])[category] += 1
                    (entries[-1])['total'] += 1
    
    return entries

def extract_errors(data):
    errors = []

    for entry in data:
        for result in entry.get('analysis_result', {}).get('results', []):
            for analysis in result.get('analysis_results', []):
                if 'violation_id' in analysis:
                    errors.append({
                        'file_name': result.get('file_name'),
                        'id':entry.get('_id'),
                        'email':entry.get('email'),
                        'violation_id': analysis.get('violation_id'),
                        'severity': analysis.get('severity'),
                        'msg': analysis.get('msg'),
                        'category': categorize_error_type(analysis.get('violation_id')),
                        'time' : pd.to_datetime(entry.get('createdAt'),format = "mixed")
                    })
    return errors