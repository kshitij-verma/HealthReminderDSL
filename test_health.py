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