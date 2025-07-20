from portfolio_convert.models.convert import PortfolioStateInr, PortfolioStateGeneral, Currency



def calculate_linear_graph(state: PortfolioStateInr):
    state.total_usd = state.amount_usd * 1.1
    return state

###### INR to USD ######
def usd_to_inr(state: PortfolioStateInr):
    state.total_inr = state.total_usd * 85
    return state



def calculate_linear_graph_general(state: PortfolioStateGeneral):
    state.total_usd = state.amount_usd * 1.1
    return state

###### USD to EUR ######
def calculate_usd_to_eur(state: PortfolioStateGeneral):
    state.total_amount = state.total_usd * 0.85
    return state

###### USD to INR ######
def calculate_usd_to_inr(state: PortfolioStateGeneral):
    state.total_amount = state.total_usd * 85
    return state


def choose_path_currency(state: PortfolioStateGeneral):
    return state.target_currency.value 