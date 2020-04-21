import math
import random
import datetime as dt
from google.appengine.api import urlfetch
from util.custom_requests import get_request_content

urlfetch.set_default_fetch_deadline(45)

GOOGLE_URL = "http://finance.google.com/finance/historical?q=BMV:{symbol}&startdate={startdate}&enddate={enddate}&output=csv"
N_YEARS = 2


def get_dates():
    now = dt.datetime.now()
    year, month, day = now.year, now.month, now.day
    startdate = str(day).zfill(2) + str(month).zfill(2) + str(year-N_YEARS)
    enddate = now.strftime("%d%m%Y")
    return startdate, enddate


#def get_request_content(url):
#    r = urlfetch.fetch(url=url, method='GET', deadline=45)
#    return r.content


def get_symbol_data(symbol):
    def float_or_nan(x):
        try:
            return float(x)
        except:
            return float("nan")
    startdate, enddate = get_dates()
    try:
        string_data = get_request_content(GOOGLE_URL.format(
            symbol=symbol,
            startdate=startdate,
            enddate=enddate
        ))

        return [(row.split(",")[0], float_or_nan(row.split(",")[-2])) for row in string_data.split("\n") if len(row) and "Close" not in row]
    except:
        return []


def sort_symbol_data(xs):
    def str_to_datetime(x):
        return dt.datetime.strptime(x, "%d-%b-%y")
    return sorted(xs, key=lambda x: str_to_datetime(x[0]))


def extract_sorted_price(xs):
   return [x[1] for x in sort_symbol_data(xs)]


def extract_sorted_date(xs):
   return [x[0] for x in sort_symbol_data(xs)]


def calculate_returns(xs):
    def get_returns(vs, ws):
        def divide(a, b):
            try:
                return a/b
            except:
                return float("nan")
        return [divide(v, w) - 1 for v, w in zip(vs, ws)]
    price_data = extract_sorted_price(xs)
    return get_returns(price_data[1:], price_data[:-1])


def create_markov_chain(xs):
    def assign_state(x, mu, sigma):
        if x > mu + sigma:
            return "increasing"
        if x > mu - sigma:
            return "stable"
        return "decreasing"
    returns = calculate_returns(xs)
    state_table = {}
    mu = sum(returns) / len(returns)
    sigma = math.sqrt(sum([(r-mu)**2 for r in returns]) / len(returns))
    states = [assign_state(r, mu, sigma) for r in returns]
    for s in zip(states[:-1], states[1:]):
        if not state_table.get(s[0]):
            state_table[s[0]] = {}
        if not state_table[s[0]].get(s[1]):
            state_table[s[0]][s[1]] = 0
        state_table[s[0]][s[1]] += 1
    for prev_state in state_table:
        total = sum([state_table[prev_state][k] for k in state_table[prev_state]])
        for next_state in state_table[prev_state]:
            state_table[prev_state][next_state] = state_table[prev_state][next_state] / total
    return state_table, states[-1], states


def generate_suggestions(xs, state_of_interest=None, state_table=None):
    if (not state_table) or (not state_of_interest):
        state_table, last_state, all_states = create_markov_chain(xs)
        if not state_of_interest:
            state_of_interest = last_state
    prob_accum = random.random()
    accum = 0
    for next_state in state_table[state_of_interest]:
        prob = state_table[state_of_interest][next_state]
        accum += prob
        if accum > prob_accum:
            break
    return {"decreasing": "sell", "increasing": "buy", "stable": "hold"}[next_state]


def suggestion_strategy(xs):
    def points(action, state):
        if (action == "buy" and state == "increasing") or (action == "sell" and state == "decreasing"):
            return "gain"
        if (action == "buy" and state == "decreasing") or (action == "sell" and state == "increasing"):
            return "loss"
        return "neutral"

    def get_probs(results):
        probs = {}
        probs["gains"] = float(len(list(filter(lambda x: x == "gain", results)))) / float(len(results))
        probs["losses"] = float(len(list(filter(lambda x: x == "loss", results)))) / float(len(results))
        probs["neutral"] = float(len(list(filter(lambda x: x == "neutral", results)))) / float(len(results))
        return probs

    def procedure(sum_probs={"gains": 0, "losses": 0, "neutral": 0}, sugg=[], nmax=10, n=0):
        state_table, last_state, all_states = create_markov_chain(xs)
        suggestions = [generate_suggestions(xs, s, state_table) for s in all_states]
        result = [points(action, state) for action, state in zip(suggestions[:-1], all_states[1:])]
        probs = get_probs(result)
        if n == nmax-1:
            sum_probs["gains"] = (sum_probs["gains"] + probs["gains"]) / nmax
            sum_probs["losses"] = (sum_probs["losses"] + probs["losses"]) / nmax
            sum_probs["neutral"] = (sum_probs["neutral"] + probs["neutral"]) / nmax
            return sum_probs, sugg
        sum_probs["gains"] = sum_probs["gains"] + probs["gains"]
        sum_probs["losses"] = sum_probs["losses"] + probs["losses"]
        sum_probs["neutral"] = sum_probs["neutral"] + probs["neutral"]
        return procedure(sum_probs, sugg+[suggestions[-1]], nmax, n+1)#if sum_probs["losses"] != 0.0 else n-1)

    def most_common(lst):
        return max(set(lst), key=lst.count)

    probs, suggs = procedure(nmax=75)
    if probs["losses"] > 0.00001:
        ratio = "probability of gaining that is {:.2f} % greater than the probability of loss.".format(
            (probs["gains"] - probs["losses"]) * 100 / probs["losses"])
    else:
        ratio = " < undefined >"
    return probs, most_common(suggs), ratio
