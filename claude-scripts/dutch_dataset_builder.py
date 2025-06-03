"""
Build Dutch pronoun fidelity dataset
Adapted from the original RUFF methodology with Dutch templates
"""

import csv
import sys
import itertools
from pathlib import Path
import pandas as pd
from dutch_templates import dutch_mapping, dutch_occupation_to_participant, dutch_context_templates, dutch_task_templates

def instantiate_template(template, occupation, participant, pronoun_type, pronoun):
    """Replace placeholders in template with actual values"""
    return (template
            .replace('$OCCUPATION', occupation)
            .replace('$PARTICIPANT', participant)
            .replace('$OCCUPATION/PARTICIPANT', occupation)  # Default to occupation for context
            .replace(pronoun_type, pronoun))

def build_pronoun_type_template_mapping():
    """Build mapping of pronoun types to templates with polarity"""
    pronoun_type_template_mapping = {
        'explicit_template': {pronoun_type: [] for pronoun_type in dutch_mapping},
        'implicit_template': {pronoun_type: [] for pronoun_type in dutch_mapping},
    }
    
    # Convert templates to required format
    for pronoun_type in dutch_mapping:
        for template, polarity in dutch_context_templates[pronoun_type]['explicit']:
            pronoun_type_template_mapping['explicit_template'][pronoun_type].append((template, polarity))
        for template, polarity in dutch_context_templates[pronoun_type]['implicit']:
            pronoun_type_template_mapping['implicit_template'][pronoun_type].append((template, polarity))
    
    return pronoun_type_template_mapping

def create_base_dataset():
    """Create base dataset with occupation-participant pairs and task templates"""
    base_data = []
    
    for occupation, participant in dutch_occupation_to_participant.items():
        for pronoun_type, task_templates in dutch_task_templates.items():
            for task_template in task_templates:
                for pronoun in dutch_mapping[pronoun_type]:
                    # Create the task sentence with the target pronoun as placeholder
                    task_sentence = task_template.replace('$OCCUPATION', occupation)
                    
                    base_data.append({
                        'occupation': occupation,
                        'participant': participant,
                        'sentence': task_sentence,
                        'pronoun_type': pronoun_type,
                        'word': occupation,  # The word being referred to
                        'target_pronoun': pronoun
                    })
    
    return base_data

def get_output_line(row, context, pronoun1, uid, confuse=''):
    """Format output line for dataset"""
    if isinstance(context, list):
        capitalized = [c.capitalize() for c in context]
        template = ' '.join((*capitalized, row['sentence']))
    else:
        template = f"{context.capitalize()} {row['sentence']}"
    
    return '\t'.join([
        row['occupation'],
        row['participant'], 
        template,
        row['pronoun_type'],
        row['word'],
        pronoun1,
        uid,
        confuse
    ]) + '\n'

def add_dutch_context(base_data, pronoun_type_template_mapping, occupation_focus=True):
    """Add context to base dataset following original methodology"""
    
    # Determine file naming
    f = 'o' if occupation_focus else 'p'  # first entity focus
    s = 'p' if occupation_focus else 'o'  # second entity focus
    
    # Create output files
    output_files = {}
    file_patterns = [
        f'e{f}_dutch_base.tsv',
        f'e{f}_e{s}_dutch_base.tsv', 
        f'e{f}_e{s}_i{s}_dutch_base.tsv',
        f'e{f}_e{s}_i{s}_i{s}_dutch_base.tsv',
        f'e{f}_e{s}_i{s}_i{s}_i{s}_dutch_base.tsv',
        f'e{f}_e{s}_i{s}_i{s}_i{s}_i{s}_dutch_base.tsv'
    ]
    
    for pattern in file_patterns:
        output_files[pattern] = open(pattern, 'w', encoding='utf-8')
    
    # Write headers
    header = 'occupation\tparticipant\tsentence\tpronoun_type\tword\tpronoun\tuid\tconfuse_pronoun\n'
    for f_obj in output_files.values():
        f_obj.write(header)
    
    try:
        first = 'occupation' if occupation_focus else 'participant'
        second = 'participant' if occupation_focus else 'occupation'
        
        for row in base_data:
            pronoun_type = row['pronoun_type']
            pronouns = dutch_mapping[pronoun_type]
            
            # Generate contexts with different complexity levels
            for i, (e1, s1) in enumerate(pronoun_type_template_mapping['explicit_template'][pronoun_type]):
                for pronoun1 in pronouns:
                    # Single explicit context
                    intro1 = instantiate_template(e1, row['occupation'], row['participant'], pronoun_type, pronoun1)
                    output_files[f'e{f}_dutch_base.tsv'].write(
                        get_output_line(row, [intro1], pronoun1, f'e{f}{i}'))
                    
                    # Two explicit contexts with different sentiment
                    for j, (e2, s2) in enumerate(pronoun_type_template_mapping['explicit_template'][pronoun_type]):
                        if (j % 5) == (i % 5):  # Different content
                            continue
                        if s2 == s1:  # Different sentiment
                            continue
                            
                        for pronoun2 in pronouns:
                            if pronoun1 == pronoun2:  # Different pronouns
                                continue
                                
                            # Use second entity for second context
                            second_entity = row['participant'] if occupation_focus else row['occupation']
                            intro2 = instantiate_template(e2, second_entity, second_entity, pronoun_type, pronoun2)
                            
                            output_files[f'e{f}_e{s}_dutch_base.tsv'].write(
                                get_output_line(row, [intro1, intro2], pronoun1, f'e{f}{i}_e{s}{j}', pronoun2))
                            
                            # Add implicit continuations
                            implicit_continuations = []
                            for k, (it, st) in enumerate(pronoun_type_template_mapping['implicit_template'][pronoun_type]):
                                if k == j or k == i:
                                    continue
                                if st != s2:  # Same sentiment as last explicit
                                    continue
                                    
                                implicit = instantiate_template(it, second_entity, second_entity, pronoun_type, pronoun2)
                                implicit_continuations.append((k, implicit))
                            
                            if len(implicit_continuations) >= 4:
                                implicit_continuations = implicit_continuations[:4]  # Take first 4
                                
                                # Single implicit
                                for perm in itertools.permutations(implicit_continuations, 1):
                                    k1, i1 = perm[0]
                                    output_files[f'e{f}_e{s}_i{s}_dutch_base.tsv'].write(
                                        get_output_line(row, [intro1, intro2, i1], pronoun1,
                                                       f'e{f}{i}_e{s}{j}_i{s}{k1}', pronoun2))
                                
                                # Two implicit
                                for perm in itertools.permutations(implicit_continuations, 2):
                                    k1, i1 = perm[0]
                                    k2, i2 = perm[1]
                                    output_files[f'e{f}_e{s}_i{s}_i{s}_dutch_base.tsv'].write(
                                        get_output_line(row, [intro1, intro2, i1, i2], pronoun1,
                                                       f'e{f}{i}_e{s}{j}_i{s}{k1}_i{s}{k2}', pronoun2))
                                
                                # Three and four implicit (using all 4)
                                for perm in itertools.permutations(implicit_continuations, 4):
                                    k1, i1 = perm[0]
                                    k2, i2 = perm[1] 
                                    k3, i3 = perm[2]
                                    k4, i4 = perm[3]
                                    
                                    output_files[f'e{f}_e{s}_i{s}_i{s}_i{s}_dutch_base.tsv'].write(
                                        get_output_line(row, [intro1, intro2, i1, i2, i3], pronoun1,
                                                       f'e{f}{i}_e{s}{j}_i{s}{k1}_i{s}{k2}_i{s}{k3}', pronoun2))
                                    
                                    output_files[f'e{f}_e{s}_i{s}_i{s}_i{s}_i{s}_dutch_base.tsv'].write(
                                        get_output_line(row, [intro1, intro2, i1, i2, i3, i4], pronoun1,
                                                       f'e{f}{i}_e{s}{j}_i{s}{k1}_i{s}{k2}_i{s}{k3}_i{s}{k4}', pronoun2))
    
    finally:
        # Close all files
        for f_obj in output_files.values():
            f_obj.close()

def main():
    """Main function to build Dutch dataset"""
    print("Building Dutch pronoun fidelity dataset...")
    
    # Create base dataset
    base_data = create_base_dataset()
    print(f"Created {len(base_data)} base examples")
    
    # Build template mapping
    pronoun_type_template_mapping = build_pronoun_type_template_mapping()
    
    # Add context (focusing on occupation first)
    add_dutch_context(base_data, pronoun_type_template_mapping, occupation_focus=True)
    
    print("Dataset creation complete!")
    print("Generated files:")
    for pattern in ['eo_dutch_base.tsv', 'eo_ep_dutch_base.tsv', 'eo_ep_ip_dutch_base.tsv', 
                   'eo_ep_ip_ip_dutch_base.tsv', 'eo_ep_ip_ip_ip_dutch_base.tsv', 'eo_ep_ip_ip_ip_ip_dutch_base.tsv']:
        if Path(pattern).exists():
            size = len(pd.read_csv(pattern, sep='\t'))
            print(f"  {pattern}: {size} examples")

if __name__ == '__main__':
    main()
