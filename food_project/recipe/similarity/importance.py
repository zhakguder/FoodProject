#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod

class ImportanceCalculator:
    def _create_ranker(self):
        '''Return an importance ranker'''
        return EntropyRanker()
    def calculate_importances(self, mask, mask_type):
        ranker = self._create_ranker(mask_type)
        return ranker.get_ranks(mask)

class Ranker(ABCMeta):
    @abstractmethod
    def get_ranks(self, mask):
        pass

class EntropyRanker(Ranker):
    def get_ranks(self, mask):
        breakpoint()
