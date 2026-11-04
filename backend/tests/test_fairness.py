import asyncio
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.services.bias_analyzer import BiasAnalyzer
from app.services.data_generator import DataGenerator


def run(coro):
    return asyncio.run(coro)


def test_demographic_parity_difference_uses_favorable_predictions():
    result = run(BiasAnalyzer().analyze(
        [{"gender": "a"}, {"gender": "a"}, {"gender": "b"}, {"gender": "b"}],
        [
            {"input_id": "input_0", "output": {"prediction": 1}},
            {"input_id": "input_1", "output": {"prediction": 0}},
            {"input_id": "input_2", "output": {"prediction": 1}},
            {"input_id": "input_3", "output": {"prediction": 1}},
        ],
    ))
    metric = result["fairness_metrics"][0]
    assert metric["metric"] == "demographic_parity_difference_gender"
    assert metric["value"] == 0.5


def test_equalized_odds_requires_labels_and_uses_tpr_and_fpr():
    result = run(BiasAnalyzer().analyze(
        [{"gender": "a"}, {"gender": "a"}, {"gender": "b"}, {"gender": "b"}],
        [
            {"input_id": "input_0", "output": {"prediction": 1}},
            {"input_id": "input_1", "output": {"prediction": 0}},
            {"input_id": "input_2", "output": {"prediction": 1}},
            {"input_id": "input_3", "output": {"prediction": 0}},
        ],
        protected_attributes=["gender"],
        ground_truth=[1, 0, 1, 0],
    ))
    names = {item["metric"] for item in result["fairness_metrics"]}
    assert "equal_opportunity_difference_gender" in names
    assert "equalized_odds_difference_gender" in names


def test_generator_seed_is_reproducible():
    first = run(DataGenerator().generate_data(size=3, seed=7))
    second = run(DataGenerator().generate_data(size=3, seed=7))
    assert first == second


def test_invalid_prediction_is_not_converted_to_zero():
    with pytest.raises(ValueError, match="usable scalar predictions"):
        run(BiasAnalyzer().analyze(
            [{"gender": "a"}, {"gender": "b"}],
            [{"input_id": "input_0", "output": {"message": "invalid"}}],
        ))
