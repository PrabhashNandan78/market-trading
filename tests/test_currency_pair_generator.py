"""Offline tests for CurrencyPairGenerator.

The generator module is pure stdlib logic, so it is loaded directly from
its file path. Importing it through the ``market_dashboard`` package would
execute the package ``__init__``, which pulls in pandas / TA-Lib / yfinance
via the data-processor and dashboard modules; those heavy dependencies are
not needed to test pair generation and are not available in every
environment (TA-Lib needs its C library).
"""

import importlib.util
from pathlib import Path

import pytest

_MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "market_dashboard"
    / "currency_pair_generator.py"
)
_spec = importlib.util.spec_from_file_location("currency_pair_generator", _MODULE_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
CurrencyPairGenerator = _module.CurrencyPairGenerator


@pytest.fixture()
def gen():
    return CurrencyPairGenerator()


def test_format_pair_keeps_hierarchy_order(gen):
    # EUR outranks USD, so EUR is the base regardless of argument order.
    assert gen.format_pair("EUR", "USD") == "EUR/USD"
    assert gen.format_pair("USD", "EUR") == "EUR/USD"


def test_format_pair_usd_jpy(gen):
    # USD outranks JPY.
    assert gen.format_pair("USD", "JPY") == "USD/JPY"
    assert gen.format_pair("JPY", "USD") == "USD/JPY"


def test_get_yahoo_symbol(gen):
    assert gen.get_yahoo_symbol("EUR/USD") == "EURUSD=X"
    assert gen.get_yahoo_symbol("USD/JPY") == "USDJPY=X"


def test_major_pairs_are_well_formed(gen):
    majors = gen.generate_major_pairs()
    assert "EUR/USD" in majors
    assert "USD/JPY" in majors
    for pair, symbol in majors.items():
        base, quote = pair.split("/")
        assert base in gen.major_currencies
        assert quote in gen.major_currencies
        assert base != quote
        assert symbol == f"{base}{quote}=X"


def test_minor_pairs(gen):
    minors = gen.generate_minor_pairs()
    # 5 minor currencies quoted against USD and EUR.
    assert len(minors) == 2 * len(gen.minor_currencies)
    for pair in minors:
        base, quote = pair.split("/")
        assert base in ("USD", "EUR")
        assert quote in gen.minor_currencies


def test_emerging_pairs(gen):
    emerging = gen.generate_emerging_pairs()
    # 10 emerging currencies quoted against USD and EUR.
    assert len(emerging) == 2 * len(gen.emerging_currencies)
    for pair in emerging:
        base, quote = pair.split("/")
        assert base in ("USD", "EUR")
        assert quote in gen.emerging_currencies


def test_cross_rates_exclude_usd(gen):
    crosses = gen.generate_cross_rates()
    assert crosses, "expected at least one cross rate"
    for pair in crosses:
        assert "USD" not in pair.split("/")


def test_generate_all_pairs_structure(gen):
    result = gen.generate_all_pairs()
    assert set(result.keys()) == {"forex_pairs"}
    categories = result["forex_pairs"]
    assert set(categories.keys()) == {
        "major_pairs",
        "minor_pairs",
        "emerging_pairs",
        "cross_rates",
    }
    for pairs in categories.values():
        for pair, symbol in pairs.items():
            assert symbol == gen.get_yahoo_symbol(pair)
