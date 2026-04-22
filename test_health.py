import pytest
from textx import metamodel_from_file

def test_medication_parsing():
    # 1. Load your grammar
    meta_model = metamodel_from_file('health.tx')
    
    # 2. Provide a simple input
    example = "medication Aspirin"
    
    # 3. Parse it
    model = meta_model.model_from_str(example)
    
    # 4. ASSERT (The actual test)
    # We expect the first medication in the list to be named "Aspirin"
    assert model.medications[0].name == "Aspirin"

def test_dynamic_conflict_parsing():
    meta_model = metamodel_from_file('health.tx')
    example = "medication A medication B conflict A with B within 45 min message 'Danger'"
    model = meta_model.model_from_str(example)
    
    # This verifies your new grammar logic works!
    assert model.conflicts[0].time == 45
    assert model.conflicts[0].medA.name == "A"
