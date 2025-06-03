"""
Dutch prompting system for T5 model evaluation
Adapted from original RUFF prompting methodology
"""

import torch
from transformers import GenerationConfig
from dutch_templates import dutch_mapping

# Dutch T5 model family
dutch_t5_family = ['yhavinga/t5-base-dutch', 'yhavinga/t5-small-dutch', 'yhavinga/t5-large-dutch']

# Other Dutch models that might be relevant
dutch_bert_family = ['GroNLP/bert-base-dutch-cased', 'wietsedv/bert-base-dutch-cased']

# Model families that need different instruction templates
only_pre_trained_family = ['yhavinga/t5-base-dutch', 'yhavinga/t5-small-dutch', 'yhavinga/t5-large-dutch']

class DutchT5InstructionTemplate:
    """Instruction template for Dutch T5 models"""
    def __init__(self):
        # T5 models expect specific task prefixes
        self.instruction_template = "{user_message}"

    def add_prompt_template(self, text):
        return self.instruction_template.format(user_message=text)

class RawLanguageModelInstructionTemplate:
    """Raw template for models without special formatting"""
    def __init__(self):
        self.instruction_template = ""

    def add_prompt_template(self, text):
        return text

def get_dutch_pronoun_templates():
    """Generate Dutch-specific pronoun resolution templates"""
    all_templates = []
    
    # Base Dutch templates
    base_templates = [
        "{task}\n\nWelk voornaamwoord moet gebruikt worden om de lege plek in te vullen?",
        "{task}\n\nHet beste voornaamwoord om de lege plek in te vullen is",
        "Vul de lege plek in met het juiste voornaamwoord.\n\n{task}",
        "Welk voornaamwoord moet gebruikt worden om de lege plek in te vullen?\n\n{task}",
        "Vervolledig de zin met het juiste voornaamwoord.\n\n{task}",
        "Kies het passende voornaamwoord voor de lege plek.\n\n{task}",
    ]

    for t in base_templates:
        all_templates.append(t)
        # Add variations
        if 'het juiste voornaamwoord' in t:
            a = t.replace('het juiste voornaamwoord', 'het passende voornaamwoord')
            all_templates.append(a)
        if 'het beste voornaamwoord' in t:
            a = t.replace('het beste voornaamwoord', 'het meest geschikte voornaamwoord')
            all_templates.append(a)

    # Add versions with explicit options
    for t in [t for t in all_templates]:
        all_templates.append(t + '\n{options}')

    return all_templates

def get_dutch_instruction_template_fns(model_signature):
    """Get appropriate instruction template for Dutch models"""
    if model_signature in dutch_t5_family:
        return DutchT5InstructionTemplate()
    elif model_signature in dutch_bert_family or model_signature in only_pre_trained_family:
        return RawLanguageModelInstructionTemplate()
    else:
        # Default to raw template for unknown Dutch models
        return RawLanguageModelInstructionTemplate()

def prompt_dutch_model(sentence, pronoun_type, pronouns, word, tokenizer, model, model_type, model_name):
    """
    Prompt Dutch model for pronoun resolution
    Adapted from original prompt_model function
    """
    # Create sentence with blank
    sentence_with_blank = sentence.replace(pronoun_type, '___')
    
    # Get appropriate instruction template
    instruction_template = get_dutch_instruction_template_fns(model_name)
    
    # Get Dutch pronoun templates
    all_pronoun_templates = get_dutch_pronoun_templates()

    # Format options for Dutch
    options = pronouns
    options_ = 'OPTIES:\n' + '\n'.join(['- ' + o for o in options])
    
    # Generation configuration for Dutch T5
    gen_config_args = {
        'max_new_tokens': 10,  # Dutch pronouns are typically short
        'num_beams': 1,
        'do_sample': False,
        'eos_token_id': tokenizer.eos_token_id,
        'pad_token_id': tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    }
    
    # Adjust for T5 models
    if 't5' in model_name.lower():
        gen_config_args['max_new_tokens'] = 5  # T5 typically generates shorter responses
    
    gen_config = GenerationConfig(**gen_config_args)

    # Test each template
    for i, pronoun_template in enumerate(all_pronoun_templates):
        try:
            # Fill template
            filled = pronoun_template.format(task=sentence_with_blank, options=options_)
            filled_with_instruction = instruction_template.add_prompt_template(filled)
            
            # Tokenize
            inputs = tokenizer(filled_with_instruction, return_tensors="pt", padding=True, truncation=True)
            
            # Move to device
            device = next(model.parameters()).device
            input_ids = inputs.input_ids.to(device)
            attention_mask = inputs.attention_mask.to(device) if 'attention_mask' in inputs else None
            
            # Generate
            with torch.no_grad():
                if attention_mask is not None:
                    outputs = model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        generation_config=gen_config
                    )
                else:
                    outputs = model.generate(
                        input_ids=input_ids,
                        generation_config=gen_config
                    )
                
                # Decode output
                if 't5' in model_name.lower():
                    # T5 models generate from scratch
                    decoded_tokens = tokenizer.decode(outputs[0], skip_special_tokens=True)
                else:
                    # For other models, remove input tokens
                    input_length = input_ids.shape[1]
                    decoded_tokens = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
                
                decoded_tokens = decoded_tokens.strip().replace("\n", " ")

            yield i, decoded_tokens
            
        except Exception as e:
            print(f"Error processing template {i}: {e}")
            yield i, f"ERROR: {str(e)}"

def evaluate_dutch_pronoun_choice(generated_text, target_pronouns):
    """
    Evaluate if generated text contains correct Dutch pronoun
    """
    generated_lower = generated_text.lower().strip()
    
    # Direct matches
    for pronoun in target_pronouns:
        if pronoun.lower() in generated_lower:
            return pronoun, True
    
    # Check for common variations or partial matches
    pronoun_variations = {
        'hij': ['hij', 'he'],
        'zij': ['zij', 'ze', 'she'],
        'die': ['die', 'they', 'hen', 'hun']
    }
    
    for target_pronoun in target_pronouns:
        if target_pronoun in pronoun_variations:
            for variation in pronoun_variations[target_pronoun]:
                if variation.lower() in generated_lower:
                    return target_pronoun, True
    
    # Return first pronoun as default with False
    return target_pronouns[0] if target_pronouns else "unknown", False

# Dutch-specific model configuration
dutch_model_configs = {
    'yhavinga/t5-base-dutch': {
        'model_type': 'enc-dec',
        'max_length': 512,
        'generation_config': {
            'max_new_tokens': 5,
            'num_beams': 1,
            'do_sample': False
        }
    },
    'yhavinga/t5-small-dutch': {
        'model_type': 'enc-dec', 
        'max_length': 512,
        'generation_config': {
            'max_new_tokens': 5,
            'num_beams': 1,
            'do_sample': False
        }
    }
}
