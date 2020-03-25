from enum import Enum, IntEnum
from collections import defaultdict, namedtuple
import random
import simpy
from util import CompanyState, InvestmentRound


class Deal:
    def __init__(self, ccb, investment):
        """
        
        :param ccb: cost of company before deal
        :param investment: investment in company
        """
        self.company_cost_before = ccb
        self.investment = investment
        self.share = (self.company_cost_before, self.investment)


class Company:
    def __init__(self, config):
        self.name = config["name"]
        self.value = config["value"]
        self.stage = config["stage"]
        self.investor_share = config["investor_share"]
        
        self.risk_model = config["risk_model"]


class RiskModel:
    def __init__(self):
        cs = CompanyState
        self.states = [cs.Death, cs.NewInvestmentRound, cs.Sale, cs.Dividends]
        self.ProbType = namedtuple("RiskModel", ["death", "new_investment_round", "sale", "dividend"])
        
        self.weights = self.ProbType(0.25, 0.25, 0.25, 0.25)
    
    def get_next_state(self):
        return random.choices(self.states, weights=self.weights, k=1)[0]
    
    def update(self):
        pass
    
    
class VentureCapitalFund:
    def __init__(self, config):
        self.available_capital = config["capital"]
        self.start_capital = config["capital"]
        self.investments_number_per_year = config["investments_number_per_year"]  # [3, 8]
        self.sales_number_per_year = config["sales_number_per_year"]
        self.death_number_per_year = config["death_number_per_year"]
        self.investment_money_pp_by_stage = config["investment_money_pp_by_stage"]  # map Stage --> [min, max]
        self.company_value_range_by_stage = config["company_value_range_by_stage"]
        self.investments_value_by_stage = config["investments_value_by_stage"]
        self.investor_share_range_by_stage = config["investor_share_range_by_stage"]
        self.transition_range_by_stage = config["transition_range_by_stage"]
        self.wait_time_by_stage = config["wait_time_by_stage"]
        self.outcome_probability_by_project_by_stage = config["outcome_probability_by_project_by_stage"]
        
        # fixed parameters
        self.investment_phase = config["investment_phase"]
        self.post_investment_phase = config["post_investment_phase"]
        self.work_cost = config["work_cost"]
        self.work_cost_in_post_investment_phase = config["work_cost_in_post_investment_phase"]
        self.g_irr = config["g_irr"]
        self.distribution_rate = config["distribution_rate"]
        self.lawyer_cost = config["lawyer_cost"]
        
        # custom parameters
        self.reserve_investment_capital = defaultdict(float)
        self.value_increase = 1.5
        self.income_flow = 0
        self.outcome_flow = 0
        self.companies = []
        
        self.income_outcome_flow = []

    # ===================================++=======================
    # Investment
    # ===================================++=======================
    def choose_company_to_invest(self, companies):
        """
        
        :param companies:
        :return:
        A choose is made in two steps
        """
        new_investment = CompanyState.NewInvestmentRound
        # I step
        candidates = []
        for company in companies:
            if company.risk_model.get_next_state() is new_investment:
                candidates.append(company)

        # II step c.risk_model.weights[1]
        # -- new investment round prob
        weights = [c.value * c.risk_model.weights.new_investment_round for c in candidates]
        company = random.choices(candidates, weights=weights, k=1)[0]
        return company

    def choose_investment_amount(self, company):
        return random.uniform(*self.investment_money_pp_by_stage[company.stage])

    def calculate_share(self, company, investment):
        return investment / company.value
    
    def invest(self, company, investment_money):
        ir = InvestmentRound
        # make a reserve
        if company.stage in [ir.Seed, ir.Round_A]:
            self.available_capital -= company.value
            self.reserve_investment_capital[company.name] += company.value
    
        reserve_money = self.reserve_investment_capital[company.name]
        if reserve_money >= investment_money:
            # pay from reserve
            self.reserve_investment_capital[company.name] -= investment_money
        else:
            # pay from
            remains = investment_money - reserve_money
            self.available_capital -= remains
            self.reserve_investment_capital[company.name] = 0
        
        company.investor_share += self.calculate_share(company, investment_money)
        self.companies.append(company)
        
        self.outcome_flow += investment_money

    def increase_value(self, company, money):
        company.value += self.value_increase * money
    
    # ===================================++=======================
    # SALE
    # ===================================++=======================
    def choose_company_to_sale(self):
        weights = [c.risk_model.weights.sale for c in self.companies]
        company = random.choices(self.companies, weights=weights, k=1)[0]
        return company
    
    def sale(self, company):
        self.companies.remove(company)

        money = company.value
        self.available_capital += money
        self.income_flow += money
        return money
    
    # ===================================++=======================
    # Bankruptcy
    # ===================================++=======================
    def choose_company_to_ban(self):
        weights = [c.risk_model.weights.death for c in self.companies]
        company = random.choices(self.companies, weights=weights, k=1)[0]
        return company
    
    def ban_company(self, company):
        self.companies.remove(company)
        return
    
    # ===================================++=======================
    # SALARY
    # ===================================++=======================
    def pay_salary_yearly(self):
        salary = self.work_cost * \
                 self.available_capital
        self.available_capital -= salary
        
        self.outcome_flow += salary
    
    def pay_salary_quarterly(self):
        quarter_cost = self.work_cost / 4
        salary = quarter_cost * self.start_capital
        self.available_capital -= salary
        
        self.outcome_flow += salary

    def pay_lawyer(self):
        self.available_capital -= self.lawyer_cost
        
        self.outcome_flow += self.lawyer_cost

