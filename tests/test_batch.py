#!/usr/bin/env python3
"""
Test suite for batch processing functionality.

Run with pytest:
    pytest tests/test_batch.py -v
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import dolphain


class TestDataDiscovery:
    """Test data file discovery functions."""

    def test_find_data_files(self):
        """Test finding data files."""
        files = dolphain.find_data_files("data/Buoy210_100300_100399", "*.210")
        assert len(files) > 0
        assert all(f.suffix == ".210" for f in files)
        assert all(f.exists() for f in files)

    def test_find_data_files_recursive(self):
        """Test recursive file finding."""
        files = dolphain.find_data_files("data", "**/*.210")
        assert len(files) > 0

    def test_select_random_files(self):
        """Test random file selection with reproducibility."""
        all_files = dolphain.find_data_files("data", "**/*.210")

        # Test reproducibility with seed
        subset1 = dolphain.select_random_files(all_files, n=5, seed=42)
        subset2 = dolphain.select_random_files(all_files, n=5, seed=42)
        assert subset1 == subset2

        # Test different seed gives different results
        subset3 = dolphain.select_random_files(all_files, n=5, seed=123)
        assert subset1 != subset3

    def test_select_random_files_size(self):
        """Test that selection returns correct number of files."""
        all_files = dolphain.find_data_files("data", "**/*.210")

        for n in [1, 5, 10]:
            subset = dolphain.select_random_files(all_files, n=n, seed=42)
            assert len(subset) == min(n, len(all_files))


class TestTimer:
    """Test timing context manager."""

    def test_timer_basic(self):
        """Test timer measures elapsed time."""
        import time

        with dolphain.timer("Test", verbose=False) as t:
            time.sleep(0.1)

        assert t.elapsed >= 0.1
        assert t.elapsed < 0.2

    def test_timer_verbose(self, capsys):
        """Test timer prints when verbose=True."""
        with dolphain.timer("Test operation", verbose=True):
            pass

        captured = capsys.readouterr()
        assert "Test operation" in captured.out
        assert "seconds" in captured.out


class TestResultCollector:
    """Test result collection and summarization."""

    def test_add_result(self):
        """Test adding results."""
        collector = dolphain.ResultCollector()
        collector.add_result("file1.210", {"metric1": 10.0, "metric2": 20.0})

        assert len(collector.results) == 1
        assert collector.results[0]["file"] == "file1.210"
        assert collector.results[0]["metric1"] == 10.0

    def test_add_error(self):
        """Test recording errors."""
        collector = dolphain.ResultCollector()
        collector.add_error("file1.210", ValueError("Test error"))

        assert len(collector.errors) == 1
        assert collector.errors[0]["file"] == "file1.210"
        assert collector.errors[0]["error_type"] == "ValueError"

    def test_add_timing(self):
        """Test recording timing information."""
        collector = dolphain.ResultCollector()
        collector.add_timing("operation1", 1.5)
        collector.add_timing("operation1", 2.0)

        assert "operation1" in collector.timings
        assert len(collector.timings["operation1"]) == 2

    def test_summarize_empty(self):
        """Test summarizing empty collector."""
        collector = dolphain.ResultCollector()
        summary = collector.summarize()

        assert summary["total_files"] == 0
        assert summary["successful"] == 0
        assert summary["failed"] == 0

    def test_summarize_with_results(self):
        """Test summarizing with results."""
        collector = dolphain.ResultCollector()
        collector.add_result("file1.210", {"snr": 15.0, "duration": 30.0})
        collector.add_result("file2.210", {"snr": 20.0, "duration": 30.0})
        collector.add_timing("processing", 1.0)
        collector.add_timing("processing", 2.0)

        summary = collector.summarize()

        assert summary["total_files"] == 2
        assert summary["successful"] == 2
        assert summary["success_rate"] == 100.0
        assert "metrics" in summary
        assert "snr" in summary["metrics"]
        assert summary["metrics"]["snr"]["mean"] == 17.5
        assert "timings" in summary
        assert summary["timings"]["processing"]["mean"] == 1.5

    def test_print_summary(self, capsys):
        """Test printing summary."""
        collector = dolphain.ResultCollector()
        collector.add_result("file1.210", {"snr": 15.0})
        collector.print_summary()

        captured = capsys.readouterr()
        assert "BATCH PROCESSING SUMMARY" in captured.out
        assert "Total files processed: 1" in captured.out


class TestBatchProcessor:
    """Test batch processing."""

    @pytest.fixture
    def sample_files(self):
        """Get sample files for testing."""
        files = dolphain.find_data_files("data", "**/*.210")
        return dolphain.select_random_files(files, n=3, seed=42)

    @pytest.fixture
    def simple_pipeline(self):
        """Simple pipeline for testing."""

        def pipeline(filepath):
            data = dolphain.read_ears_file(filepath)
            return {
                "duration": data["duration"],
                "n_samples": data["n_samples"],
                "rms": float(np.sqrt(np.mean(data["data"] ** 2))),
            }

        return pipeline

    def test_process_file_success(self, sample_files, simple_pipeline):
        """Test processing a single file successfully."""
        processor = dolphain.BatchProcessor(verbose=False)
        result = processor.process_file(sample_files[0], simple_pipeline)

        assert result is not None
        assert "duration" in result
        assert "rms" in result

    def test_process_file_error(self):
        """Test handling errors in processing."""
        processor = dolphain.BatchProcessor(verbose=False)

        def bad_pipeline(filepath):
            raise ValueError("Test error")

        result = processor.process_file(Path("test.210"), bad_pipeline)
        assert result is None
        assert len(processor.collector.errors) == 1

    def test_process_files(self, sample_files, simple_pipeline):
        """Test processing multiple files."""
        processor = dolphain.BatchProcessor(verbose=False)
        collector = processor.process_files(sample_files, simple_pipeline)

        assert collector.successful > 0
        assert len(collector.results) > 0
        assert "total_batch" in collector.timings

    def test_process_files_max_limit(self, sample_files, simple_pipeline):
        """Test max_files parameter."""
        processor = dolphain.BatchProcessor(verbose=False)
        collector = processor.process_files(sample_files, simple_pipeline, max_files=2)

        total = collector.successful + collector.failed
        assert total <= 2


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow(self):
        """Test a complete batch processing workflow."""
        # 1. Find files
        all_files = dolphain.find_data_files("data", "**/*.210")
        assert len(all_files) > 0

        # 2. Select subset
        subset = dolphain.select_random_files(all_files, n=3, seed=42)
        assert len(subset) <= 3

        # 3. Define pipeline
        def pipeline(filepath):
            data = dolphain.read_ears_file(filepath)
            return {
                "duration": data["duration"],
                "peak": float(np.max(np.abs(data["data"]))),
            }

        # 4. Process
        processor = dolphain.BatchProcessor(verbose=False)
        collector = processor.process_files(subset, pipeline)

        # 5. Verify results
        assert collector.successful > 0
        summary = collector.summarize()
        assert "metrics" in summary
        assert summary["success_rate"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
