#!/usr/bin/env python3
"""
Quick test to verify HuggingFace integration works.

Run this to test the new EARS class:
    python test_ears_class.py
"""

import sys
sys.path.insert(0, '/Users/mjhaas/code/dolphain')

print("Testing dolphain HuggingFace integration...")
print("=" * 70)

# Test 1: Import
print("\n1. Testing imports...")
try:
    import dolphain
    print("   ✓ dolphain imported successfully")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Check EARS class exists
print("\n2. Checking EARS class...")
try:
    assert hasattr(dolphain, 'EARS'), "EARS class not found"
    assert hasattr(dolphain, 'fetch_huggingface_file'), "fetch_huggingface_file not found"
    print("   ✓ EARS class available")
    print("   ✓ fetch_huggingface_file available")
except AssertionError as e:
    print(f"   ✗ {e}")
    sys.exit(1)

# Test 3: Check huggingface_hub
print("\n3. Checking huggingface_hub...")
try:
    import huggingface_hub
    print("   ✓ huggingface_hub is installed")
except ImportError:
    print("   ✗ huggingface_hub not installed")
    print("   Install with: pip install huggingface_hub")
    sys.exit(1)

# Test 4: Try loading a file (this will actually download!)
print("\n4. Testing EARS class (downloading from HuggingFace)...")
print("   This may take ~10 seconds for first download...")
try:
    ears = dolphain.EARS()
    print(f"   ✓ Successfully loaded: {ears.filename}")
    print(f"   ✓ Duration: {ears.duration:.2f}s")
    print(f"   ✓ Sampling rate: {ears.fs} Hz")
    print(f"   ✓ Data shape: {ears.data.shape}")
    print(f"   ✓ Source: {ears.metadata['source']}")
except Exception as e:
    print(f"   ✗ Failed to load file: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test EARS methods
print("\n5. Testing EARS methods...")
try:
    # Test denoise
    denoised = ears.denoise()
    print(f"   ✓ denoise() works: {denoised.shape}")
    
    # Test detect_whistles
    whistles = ears.detect_whistles()
    print(f"   ✓ detect_whistles() works: found {len(whistles)} whistles")
    
    print("   ✓ All methods working")
except Exception as e:
    print(f"   ✗ Method test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test repr
print("\n6. Testing object representation...")
try:
    repr_str = repr(ears)
    print(f"   {repr_str}")
    assert 'EARS(' in repr_str
    print("   ✓ __repr__ works")
except Exception as e:
    print(f"   ✗ Repr test failed: {e}")
    sys.exit(1)

# Success!
print("\n" + "=" * 70)
print("🎉 All tests passed! HuggingFace integration is working!")
print("=" * 70)
print("\nTry it yourself:")
print("  >>> import dolphain")
print("  >>> ears = dolphain.EARS()")
print("  >>> ears.plot('denoising', fmax=50000)")
print()
