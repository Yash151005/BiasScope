"""
Data Generator Service - Generate synthetic test data using Faker or CTGAN
"""

import pandas as pd
import numpy as np
from faker import Faker
from typing import List, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataGenerator:
    """Service for generating synthetic test data"""

    def __init__(self):
        self.faker = Faker()
        self.generator_type = settings.synthetic_data_generator

    async def generate_data(self) -> List[Dict[str, Any]]:
        """
        Generate synthetic data for bias testing
        Returns a list of dictionaries with features
        """
        if self.generator_type == "faker":
            return self._generate_with_faker()
        elif self.generator_type == "ctgan":
            return await self._generate_with_ctgan()
        else:
            logger.warning(f"Unknown generator type: {self.generator_type}, using Faker")
            return self._generate_with_faker()

    def _generate_with_faker(self) -> List[Dict[str, Any]]:
        """Generate synthetic data using Faker library"""
        data = []
        size = settings.synthetic_data_size

        for _ in range(size):
            # Generate diverse demographic and feature data
            record = {
                "age": np.random.randint(18, 80),
                "gender": np.random.choice(["male", "female", "other"], p=[0.48, 0.48, 0.04]),
                "race": np.random.choice(
                    ["white", "black", "asian", "hispanic", "other"],
                    p=[0.6, 0.13, 0.06, 0.18, 0.03],
                ),
                "education": np.random.choice(
                    ["high_school", "bachelor", "master", "phd"],
                    p=[0.3, 0.4, 0.25, 0.05],
                ),
                "income": np.random.normal(50000, 20000),
                "experience_years": np.random.randint(0, 40),
                "location": self.faker.city(),
                "credit_score": np.random.randint(300, 850),
            }
            # Ensure income is positive
            record["income"] = max(0, record["income"])
            data.append(record)

        logger.info(f"Generated {len(data)} synthetic records using Faker")
        return data

    async def _generate_with_ctgan(self) -> List[Dict[str, Any]]:
        """
        Generate synthetic data using CTGAN
        Note: This requires training data or a pre-trained model
        For now, falls back to Faker
        """
        # TODO: Implement CTGAN integration when training data is available
        logger.info("CTGAN not yet implemented, using Faker")
        return self._generate_with_faker()
