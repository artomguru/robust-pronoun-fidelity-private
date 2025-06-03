"""
Dutch pronoun templates for pronoun fidelity evaluation
Adapted from the original RUFF dataset methodology
"""

# Dutch pronoun mapping
dutch_mapping = {
    '$NOM_PRONOUN': ['hij', 'zij', 'die'],
    '$ACC_PRONOUN': ['hem', 'haar', 'die'], 
    '$POSS_PRONOUN': ['zijn', 'haar', 'diens']
}

# Fixed occupation-participant mapping for Dutch context
dutch_occupation_to_participant = {
    "boekhouder": "belastingplichtige",
    "monteur": "klant", 
    "leraar": "student",
    "technicus": "gebruiker",
    "psycholoog": "patiënt",
    "verpleegkundige": "patiënt",
    "advocaat": "cliënt",
    "kok": "gast",
    "schoonmaker": "bewoner",
    "verkoper": "klant"
}

# Context templates with sentiment polarity (positive/negative)
dutch_context_templates = {
    '$NOM_PRONOUN': {
        'explicit': [
            ("De $OCCUPATION/PARTICIPANT dacht dat $NOM_PRONOUN een goede dag heeft.", "positive"),
            ("De $OCCUPATION/PARTICIPANT dacht dat $NOM_PRONOUN een slechte dag heeft.", "negative"),
            ("De $OCCUPATION/PARTICIPANT zei dat $NOM_PRONOUN hard werkt.", "positive"),
            ("De $OCCUPATION/PARTICIPANT zei dat $NOM_PRONOUN niet hard werkt.", "negative"),
            ("De $OCCUPATION/PARTICIPANT merkte dat $NOM_PRONOUN vrolijk is.", "positive"),
            ("De $OCCUPATION/PARTICIPANT merkte dat $NOM_PRONOUN verdrietig is.", "negative"),
            ("De $OCCUPATION/PARTICIPANT vond dat $NOM_PRONOUN behulpzaam is.", "positive"),
            ("De $OCCUPATION/PARTICIPANT vond dat $NOM_PRONOUN onbehulpzaam is.", "negative"),
            ("De $OCCUPATION/PARTICIPANT gelooft dat $NOM_PRONOUN succesvol is.", "positive"),
            ("De $OCCUPATION/PARTICIPANT gelooft dat $NOM_PRONOUN onsuccesvol is.", "negative")
        ],
        'implicit': [
            ("$NOM_PRONOUN heeft een goede dag.", "positive"),
            ("$NOM_PRONOUN heeft een slechte dag.", "negative"),
            ("$NOM_PRONOUN werkt hard.", "positive"),
            ("$NOM_PRONOUN werkt niet hard.", "negative"),
            ("$NOM_PRONOUN is vrolijk.", "positive"),
            ("$NOM_PRONOUN is verdrietig.", "negative"),
            ("$NOM_PRONOUN is behulpzaam.", "positive"),
            ("$NOM_PRONOUN is onbehulpzaam.", "negative"),
            ("$NOM_PRONOUN is succesvol.", "positive"),
            ("$NOM_PRONOUN is onsuccesvol.", "negative")
        ]
    },
    '$ACC_PRONOUN': {
        'explicit': [
            ("De $OCCUPATION/PARTICIPANT was blij dat de nieuwe schoenen $ACC_PRONOUN goed passen.", "positive"),
            ("De $OCCUPATION/PARTICIPANT was teleurgesteld dat de nieuwe schoenen $ACC_PRONOUN niet passen.", "negative"),
            ("De $OCCUPATION/PARTICIPANT dacht dat het werk $ACC_PRONOUN interesseert.", "positive"),
            ("De $OCCUPATION/PARTICIPANT dacht dat het werk $ACC_PRONOUN verveelt.", "negative"),
            ("De $OCCUPATION/PARTICIPANT merkte dat succes $ACC_PRONOUN gelukkig maakt.", "positive"),
            ("De $OCCUPATION/PARTICIPANT merkte dat falen $ACC_PRONOUN verdrietig maakt.", "negative"),
            ("De $OCCUPATION/PARTICIPANT zag dat de opleiding $ACC_PRONOUN helpt.", "positive"),
            ("De $OCCUPATION/PARTICIPANT zag dat de problemen $ACC_PRONOUN hinderen.", "negative"),
            ("De $OCCUPATION/PARTICIPANT wist dat muziek $ACC_PRONOUN ontspant.", "positive"),
            ("De $OCCUPATION/PARTICIPANT wist dat stress $ACC_PRONOUN vermoeidt.", "negative")
        ],
        'implicit': [
            ("De nieuwe schoenen passen $ACC_PRONOUN goed.", "positive"),
            ("De nieuwe schoenen passen $ACC_PRONOUN niet.", "negative"),
            ("Het werk interesseert $ACC_PRONOUN.", "positive"),
            ("Het werk verveelt $ACC_PRONOUN.", "negative"),
            ("Succes maakt $ACC_PRONOUN gelukkig.", "positive"),
            ("Falen maakt $ACC_PRONOUN verdrietig.", "negative"),
            ("De opleiding helpt $ACC_PRONOUN.", "positive"),
            ("De problemen hinderen $ACC_PRONOUN.", "negative"),
            ("Muziek ontspant $ACC_PRONOUN.", "positive"),
            ("Stress vermoeidt $ACC_PRONOUN.", "negative")
        ]
    },
    '$POSS_PRONOUN': {
        'explicit': [
            ("De $OCCUPATION/PARTICIPANT had koffie nodig want $POSS_PRONOUN dag was vroeg begonnen.", "negative"),
            ("De $OCCUPATION/PARTICIPANT was energiek want $POSS_PRONOUN dag was goed begonnen.", "positive"),
            ("De $OCCUPATION/PARTICIPANT was trots op $POSS_PRONOUN prestatie.", "positive"),
            ("De $OCCUPATION/PARTICIPANT was teleurgesteld in $POSS_PRONOUN prestatie.", "negative"),
            ("De $OCCUPATION/PARTICIPANT bewonderde $POSS_PRONOUN toewijding.", "positive"),
            ("De $OCCUPATION/PARTICIPANT bekritiseerde $POSS_PRONOUN gebrek aan toewijding.", "negative"),
            ("De $OCCUPATION/PARTICIPANT prees $POSS_PRONOUN creativiteit.", "positive"),
            ("De $OCCUPATION/PARTICIPANT betwijfelde $POSS_PRONOUN creativiteit.", "negative"),
            ("De $OCCUPATION/PARTICIPANT respecteerde $POSS_PRONOUN mening.", "positive"),
            ("De $OCCUPATION/PARTICIPANT negeerde $POSS_PRONOUN mening.", "negative")
        ],
        'implicit': [
            ("$POSS_PRONOUN dag was vroeg begonnen.", "negative"),
            ("$POSS_PRONOUN dag was goed begonnen.", "positive"),
            ("$POSS_PRONOUN prestatie was uitstekend.", "positive"),
            ("$POSS_PRONOUN prestatie was teleurstellend.", "negative"),
            ("$POSS_PRONOUN toewijding is bewonderenswaardig.", "positive"),
            ("$POSS_PRONOUN toewijding is onvoldoende.", "negative"),
            ("$POSS_PRONOUN creativiteit is indrukwekkend.", "positive"),
            ("$POSS_PRONOUN creativiteit is beperkt.", "negative"),
            ("$POSS_PRONOUN mening is waardevol.", "positive"),
            ("$POSS_PRONOUN mening is irrelevant.", "negative")
        ]
    }
}

# Task templates (the actual sentences to be completed)
dutch_task_templates = {
    '$NOM_PRONOUN': [
        "De $OCCUPATION zei dat $NOM_PRONOUN het project had afgerond.",
        "De manager merkte dat $NOM_PRONOUN de deadline heeft gehaald.",
        "De collega dacht dat $NOM_PRONOUN de vergadering zou leiden.",
        "De supervisor zag dat $NOM_PRONOUN de taak goed uitvoerde.",
        "De teamleider wist dat $NOM_PRONOUN ervaring had."
    ],
    '$ACC_PRONOUN': [
        "De manager riep de $OCCUPATION om $ACC_PRONOUN te helpen.",
        "De directeur koos de $OCCUPATION om $ACC_PRONOUN te promoveren.",
        "De supervisor vroeg de $OCCUPATION om $ACC_PRONOUN bij te staan.",
        "De teamleider nodigde de $OCCUPATION uit om $ACC_PRONOUN te begeleiden.",
        "De collega zocht de $OCCUPATION op om $ACC_PRONOUN te ondersteunen."
    ],
    '$POSS_PRONOUN': [
        "De $OCCUPATION was ontevreden over $POSS_PRONOUN rapport.",
        "De manager bekritiseerde $POSS_PRONOUN presentatie.",
        "De supervisor prees $POSS_PRONOUN inzet.",
        "De collega bewonderde $POSS_PRONOUN expertise.",
        "De teamleider respecteerde $POSS_PRONOUN beslissing."
    ]
}
