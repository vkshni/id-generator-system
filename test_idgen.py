"""
Basic tests for ID Generator System
Run with: python test_idgen.py
"""

import os
from pathlib import Path
from engine import IDGenerator
from exceptions import *

def cleanup_files():
    """Remove config and counter files"""
    files = ['config.json', 'counter.json']
    for f in files:
        if Path(f).exists():
            os.remove(f)

def test_generate_id():
    """Test basic ID generation"""
    print("Test 1: Generate ID... ", end="")
    cleanup_files()  # Clean before test
    
    gen = IDGenerator()
    id1 = gen.generate("order")
    id2 = gen.generate("order")
    
    assert id1 != id2, "IDs should be unique"
    assert "ORD-" in id1, "Should have prefix"
    print("✓ PASSED")

def test_add_id_type():
    """Test adding new ID type"""
    print("Test 2: Add ID type... ", end="")
    # Don't cleanup - continue from previous test
    
    gen = IDGenerator()
    result = gen.add_id_type("product", 5000, 1, "PROD-", 8)
    
    assert result == True
    id_types = gen.list_id_types()
    names = [it['name'] for it in id_types]
    assert "product" in names
    print("✓ PASSED")

def test_duplicate_id_type():
    """Test adding duplicate ID type fails"""
    print("Test 3: Duplicate ID type... ", end="")
    
    gen = IDGenerator()
    
    try:
        gen.add_id_type("order", 1000, 1, "ORD-", 6)
        assert False, "Should have raised IDTypeExistsError"
    except IDTypeExistsError:
        print("✓ PASSED")

def test_invalid_id_name():
    """Test invalid ID type name"""
    print("Test 4: Invalid ID name... ", end="")
    
    gen = IDGenerator()
    
    try:
        gen.add_id_type("my order", 1000, 1, "ORD-", 6)
        assert False, "Should have raised InvalidIDTypeNameError"
    except InvalidIDTypeNameError:
        print("✓ PASSED")

def test_update_id_type():
    """Test updating ID type"""
    print("Test 5: Update ID type... ", end="")
    
    gen = IDGenerator()
    gen.update_id_type("order", prefix="ORDER-", padding=12)
    
    # Verify update
    id_types = gen.list_id_types()
    order_type = [it for it in id_types if it['name'] == 'order'][0]
    
    assert order_type['prefix'] == "ORDER-", "Prefix should be updated"
    assert order_type['padding'] == 12, "Padding should be updated"
    print("✓ PASSED")

def test_delete_id_type():
    """Test deleting ID type"""
    print("Test 6: Delete ID type... ", end="")
    
    gen = IDGenerator()
    gen.add_id_type("temp", 1, 1, "TMP-", 4)
    gen.delete_id_type("temp", force=True)
    
    # Verify deleted
    id_types = gen.list_id_types()
    names = [it['name'] for it in id_types]
    assert "temp" not in names, "Temp should be deleted"
    print("✓ PASSED")

def test_reset_counter():
    """Test counter reset"""
    print("Test 7: Reset counter... ", end="")
    
    gen = IDGenerator()
    
    # Generate some IDs
    gen.generate("order")
    gen.generate("order")
    gen.generate("order")
    
    # Reset
    gen.reset_counter("order", force=True)
    
    # Check counter is back to start_value
    id_types = gen.list_id_types()
    order_type = [it for it in id_types if it['name'] == 'order'][0]
    
    assert order_type['counter'] == order_type['start_value'], "Counter should be reset"
    print("✓ PASSED")

def test_list_id_types():
    """Test listing ID types"""
    print("Test 8: List ID types... ", end="")
    
    gen = IDGenerator()
    id_types = gen.list_id_types()
    
    assert len(id_types) > 0, "Should have at least one ID type"
    assert 'name' in id_types[0], "Should have name field"
    assert 'counter' in id_types[0], "Should have counter field"
    print("✓ PASSED")

def test_persistence():
    """Test that counter persists across restarts"""
    print("Test 9: Persistence... ", end="")
    
    # First instance
    gen1 = IDGenerator()
    id1 = gen1.generate("order")
    counter1 = gen1.list_id_types()[0]['counter']
    
    # Second instance (simulates restart)
    gen2 = IDGenerator()
    id2 = gen2.generate("order")
    counter2 = gen2.list_id_types()[0]['counter']
    
    assert counter2 > counter1, "Counter should continue from previous value"
    print("✓ PASSED")

def run_all_tests():
    print("\n" + "="*50)
    print("Running ID Generator Tests")
    print("="*50 + "\n")
    
    tests = [
        test_generate_id,
        test_add_id_type,
        test_duplicate_id_type,
        test_invalid_id_name,
        test_update_id_type,
        test_delete_id_type,
        test_reset_counter,
        test_list_id_types,
        test_persistence
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    # Optional: cleanup after all tests
    # cleanup_files()

if __name__ == "__main__":
    run_all_tests()