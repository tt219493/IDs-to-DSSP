import unittest
from ids_to_dssp.processing.df import *
import os
import polars as pl


class TestIDsToDF(unittest.TestCase):
    def test_ids_to_df(self):
        self.assertEqual(type(ids_to_df(os.path.join("..", "data", "train-tsv"))), pl.LazyFrame)


unittest.main()