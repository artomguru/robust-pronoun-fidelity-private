"""
Dutch model evaluation script
Adapted from the original score_models.py for Dutch language models
"""

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoModelForCausalLM, T5ForConditionalGeneration
import numpy as np
import torch.nn.functional as F
from collections import defaultdict
from pathlib import Path
from dutch_templates import dutch_mapping
from dutch_prompt import prompt_dutch_model, evaluate_dutch_pronoun_choice, dutch_model_configs
from minicons import scorer
import csv
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Dutch models to evaluate (ordered by size)
dutch_models = [
    ('yhavinga/t5-small-dutch', 'enc-dec'),
    ('yhavinga/t5-base-dutch', 'enc-dec'),
    ('GroNLP/bert-base-dutch-cased', 'encoder'),
    ('wietsedv/bert-base-dutch-cased', 'encoder'),
]

def get_dutch_model(model_name, model_type):
    """Load Dutch model based on type"""
    logger.info(f"Loading model: {model_name}")
    
    try:
        if model_type == 'encoder':