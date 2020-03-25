import random
from venture_fund import VentureCapitalFund, Company, RiskModel
from util import InvestmentRound as IR, CompanyState as CS, Time

CAPITAL_RANGE_1 = [15e6, 25e6]
CAPITAL_RANGE_2 = [25e6, 50e6]
INVESTMENT_DEALS_AMOUNT = [3, 9]
SALES_AMOUNT = [1, 4]
BANS_AMOUNT = [1, 5]

INVESTMENT_MONEY_RANGE_BY_STAGE = {
    IR.Seed: [0.1e6, 0.2e6],
    IR.Round_A: [0.1e6, 0.2e6],
    IR.Round_B: [0.1e6, 0.2e6],
    IR.Round_C: [0.1e6, 0.2e6],
    IR.Round_D: [0.1e6, 0.2e6],
    IR.Round_E: [0.1e6, 0.2e6],
}
COMPANY_VALUE_RANGE_BY_STAGE = {
    IR.Seed: [0.01e6, 0.02e6],
    IR.Round_A: 2 * [0.01e6, 0.02e6],
    IR.Round_B: 4 * [0.01e6, 0.02e6],
    IR.Round_C: 8 * [0.01e6, 0.02e6],
    IR.Round_D: 16 * [0.01e6, 0.02e6],
    IR.Round_E: 32 * [0.01e6, 0.02e6],
}
INVESTOR_SHARE_RANGE_BY_STAGE = {
    IR.Seed: [0.05, 0.15],
    IR.Round_A: [0.15, 0.25],
    IR.Round_B: [0.25, 0.35],
    IR.Round_C: [0.35, 0.45],
    IR.Round_D: [0.45, 0.55],
    IR.Round_E: [0.55, 0.65],
}

TRANSITION_RANGE_BY_STAGE = {
    IR.Seed: {
        CS.NewInvestmentRound: 0.47,
        CS.Sale: 0.14,
        CS.Death: 0.39
    },
    IR.Round_A: {
        CS.NewInvestmentRound: 0.63,
        CS.Sale: 0.15,
        CS.Death: 0.22
    },
    IR.Round_B: {
        CS.NewInvestmentRound: 0.52,
        CS.Sale: 0.19,
        CS.Death: 0.29
    },
    IR.Round_C: {
        CS.NewInvestmentRound: 0.56,
        CS.Sale: 0.13,
        CS.Death: 0.31
    },
    IR.Round_D: {
        CS.NewInvestmentRound: 0.31,
        CS.Sale: 0.16,
        CS.Death: 0.53
    }
}
WAIT_TIME_BY_STAGE = {
    IR.Seed: [0.5 * Time.Year, 0.8 * Time.Year],
    IR.Round_A: [0.5 * Time.Year, 0.8 * Time.Year],
    IR.Round_B: [0.5 * Time.Year, 0.8 * Time.Year],
    IR.Round_C: [0.5 * Time.Year, 0.8 * Time.Year],
    IR.Round_D: [0.5 * Time.Year, 0.8 * Time.Year],
    IR.Round_E: [0.5 * Time.Year, 0.8 * Time.Year],
}


# Fixed parameters
INVESTMENT_PHASE = 4 * Time.Year
POST_INVESTMENT_PHASE = 3 * Time.Year
WORK_COST_1 = 0.035
WORK_COST_2 = 0.025
WORK_COST_POST = 0.02
GUARANTEED_IRR = 0.05
LAWYER_COST = 0.01e6
BENEFIT_DISTRIBUTION = 0.75, 0.25

COMPANY_NUMBERS = 111


def create_random_company(i):
    
    config = {
        "name": str(i),
        "value": random.uniform(0.01e6, 0.1e6),
        "investor_share": 0,
        "stage": IR.Seed,
        "risk_model": RiskModel()
    }
    return Company(config)


def scenario(n):
    capital = random.uniform(*CAPITAL_RANGE_1)
    investment_deals_amount = random.randrange(*INVESTMENT_DEALS_AMOUNT)
    sales_amount = random.randrange(*SALES_AMOUNT)
    death_amount = random.randrange(*BANS_AMOUNT)
    investment_money_pp_by_stage = INVESTMENT_MONEY_RANGE_BY_STAGE
    company_value_range_by_stage = COMPANY_VALUE_RANGE_BY_STAGE
    investor_share_range_by_stage = INVESTOR_SHARE_RANGE_BY_STAGE
    transition_range_by_stage = TRANSITION_RANGE_BY_STAGE
    wait_time_by_stage = WAIT_TIME_BY_STAGE
    
    config = {
        "capital": capital,
        "investments_number_per_year": investment_deals_amount,
        "sales_number_per_year": sales_amount,
        "death_number_per_year": death_amount,
        "investment_money_pp_by_stage": investment_money_pp_by_stage,
        "company_value_range_by_stage": company_value_range_by_stage,
        "investments_value_by_stage": 0,
        "investor_share_range_by_stage": investor_share_range_by_stage,
        "transition_range_by_stage": transition_range_by_stage,
        "wait_time_by_stage": wait_time_by_stage,
        "outcome_probability_by_project_by_stage": None,
        
        # fixed parameter
    
        "investment_phase": INVESTMENT_PHASE,
        "post_investment_phase": POST_INVESTMENT_PHASE,
        "work_cost": WORK_COST_1,
        "work_cost_in_post_investment_phase": WORK_COST_POST,
        "g_irr": GUARANTEED_IRR,
        "distribution_rate": BENEFIT_DISTRIBUTION,
        "lawyer_cost": LAWYER_COST,
    }
    
    i = 0
    while i < n:
        yield VentureCapitalFund(config), [create_random_company(i) for i in range(COMPANY_NUMBERS)]
        i += 1
