import json
import simpy
import numpy as np
import random
from enum import Enum, IntEnum


class InvestmentPhase(Enum):
    Current = 1
    Post = 2


class InvestmentRound(Enum):
    Seed = 1
    Round_A = 2
    Round_B = 3
    Round_C = 4
    Round_D = 5
    Round_E = 6


class CompanyState(Enum):
    Death = 1
    NewInvestmentRound = 2
    Sale = 3
    Dividends = 4


class Time(IntEnum):
    Day = 1
    Month = 30 * Day
    Quarter = 3 * Month
    Year = 12 * Month
    

def create_random_range_map(custom_dict):
    new_dict = {}
    for key in custom_dict:
        interval = custom_dict[key]
        new_dict[key] = random.uniform(*interval)
    return new_dict


def get_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


def combine_income_outcome_flows(a, b):
    a = -np.array(a)
    res = [None]*(len(a)+len(b))
    res[::2] = a
    res[1::2] = b
    return res
