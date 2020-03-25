import random
from scipy.stats import poisson
from util import Time
from config import scenario
import simpy


def investment(env, venture_fond, companies):
    while True:
        number = venture_fond.investments_number_per_year
        deal_times = poisson.rvs(Time.Year / number, size=number)
        
        for i in range(number):
            yield env.timeout(deal_times[i])
            company = venture_fond.choose_company_to_invest(companies)
            investment_money = venture_fond.choose_investment_amount(company)
            venture_fond.invest(company, investment_money)
            venture_fond.increase_value(company, investment_money)
            venture_fond.pay_lawyer()


def sale(env, venture_fond):
    while True:
        number = venture_fond.sales_number_per_year
        sale_times = poisson.rvs(Time.Year / number, size=number)
        
        for i in range(number):
            yield env.timeout(sale_times[i])
            company = venture_fond.choose_company_to_sale()
            money = venture_fond.sale(company)
            venture_fond.pay_lawyer()


def bankruptcy(env, venture_fond):
    while True:
        number = venture_fond.death_number_per_year
        ban_times = poisson.rvs(Time.Year / number, size=number)
        for i in range(number):
            yield env.timeout(ban_times[i])
            company = venture_fond.choose_company_to_ban()
            venture_fond.ban_company(company)
            venture_fond.pay_lawyer()
            
            
def pay_salary(env, venture_fond):
    while True:
        yield env.timeout(Time.Quarter)
        venture_fond.pay_salary_quarterly()


def investor_money_flow(env, venture_fond):
    while True:
        yield env.timeout(Time.Month)
        venture_fund.income_outcome_flow.append([venture_fond.income_flow, venture_fond.outcome_flow])
        venture_fond.income_flow = 0
        venture_fond.outcome_flow = 0


if __name__ == '__main__':
    SEED = 1234
    random.seed(SEED)
    env = simpy.Environment()
    
    for venture_fund, companies in scenario(1):
        env.process(investment(env, venture_fund, companies))
        env.process(sale(env, venture_fund))
        env.process(bankruptcy(env, venture_fund))
        env.process(pay_salary(env, venture_fund))
        env.process(investor_money_flow(env, venture_fund))
        
    env.run(until=10 * Time.Year)
