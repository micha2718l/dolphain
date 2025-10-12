#!/usr/bin/env python3
"""
Quick verification that the testing/experiment framework is properly set up.
Run this after installing dependencies to verify the framework.
"""

print("=" * 70)
print("Dolphain Testing Framework Verification")
print("=" * 70)

# Check file structure
from pathlib import Path

base_dir = Path(__file__).parent
required_files = [
    "dolphain/experiments.py",
    "tests/test_batch.py",
    "examples/experiment_templates.ipynb",
    "TESTING_FRAMEWORK.md",
    "TESTING_QUICK_START.md",
    "FRAMEWORK_COMPLETE.md",
]

print("\n1. Checking file structure...")
all_present = True
for filepath in required_files:
    full_path = base_dir / filepath
    if full_path.exists():
        print(f"   ✓ {filepath}")
    else:
        print(f"   ✗ {filepath} MISSING")
        all_present = False

if all_present:
    print("\n   All required files present!")
else:
    print("\n   Some files are missing!")
    exit(1)

# Check module structure
print("\n2. Checking module structure...")
try:
    import sys

    sys.path.insert(0, str(base_dir))

    # Check if experiments module exists
    from dolphain import experiments

    print("   ✓ experiments module found")

    # Check for key classes
    required_classes = [
        "BasicMetricsPipeline",
        "WhistleDetectionPipeline",
        "DenoisingComparisonPipeline",
        "SpectralAnalysisPipeline",
    ]

    for cls_name in required_classes:
        if hasattr(experiments, cls_name):
            print(f"   ✓ {cls_name}")
        else:
            print(f"   ✗ {cls_name} MISSING")
            all_present = False

    # Check for key functions
    required_funcs = ["run_experiment", "compare_methods"]
    for func_name in required_funcs:
        if hasattr(experiments, func_name):
            print(f"   ✓ {func_name}()")
        else:
            print(f"   ✗ {func_name}() MISSING")
            all_present = False

except ImportError as e:
    print(f"   ✗ Cannot import module: {e}")
    print("\n   Note: Install dependencies first: pip install -r requirements.txt")
    all_present = False

# Check test file structure
print("\n3. Checking test structure...")
test_file = base_dir / "tests" / "test_batch.py"
if test_file.exists():
    content = test_file.read_text()
    test_classes = [
        "TestDataDiscovery",
        "TestTimer",
        "TestResultCollector",
        "TestBatchProcessor",
        "TestIntegration",
    ]
    for test_cls in test_classes:
        if f"class {test_cls}" in content:
            print(f"   ✓ {test_cls}")
        else:
            print(f"   ✗ {test_cls} MISSING")
            all_present = False
else:
    print("   ✗ test_batch.py not found")
    all_present = False

# Summary
print("\n" + "=" * 70)
if all_present:
    print("✅ VERIFICATION PASSED")
    print("\nThe testing and experiment framework is properly set up!")
    print("\nNext steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run tests: pytest tests/test_batch.py -v")
    print("  3. Try tutorial: jupyter notebook examples/experiment_templates.ipynb")
    print("  4. Read docs: TESTING_QUICK_START.md")
else:
    print("⚠️  VERIFICATION INCOMPLETE")
    print("\nSome components are missing or not properly configured.")
    print("Check the output above for details.")

print("=" * 70)
