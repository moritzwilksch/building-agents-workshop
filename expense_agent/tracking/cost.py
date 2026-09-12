"""Token-cost accounting for agent trajectories.

Prices each model response using the cost the provider reported on
`RequestUsage.cost` when present, falling back to genai-prices for
models that do not report one.
"""

from __future__ import annotations

from decimal import Decimal

from genai_prices import calc_price
from pydantic_ai.messages import ModelMessage, ModelResponse

ZERO = Decimal("0")


def response_cost(response: ModelResponse) -> Decimal:
    """Price one model response, preferring the cost the provider reported."""
    if response.usage.cost is not None:
        return response.usage.cost
    try:
        return calc_price(response.usage, response.model_name or "", provider_id=response.provider_name).total_price
    except Exception:  # unknown model or provider: cost stays unpriced
        return ZERO


def messages_cost(messages: list[ModelMessage]) -> Decimal:
    """Total token cost of a message trajectory."""
    return sum((response_cost(m) for m in messages if isinstance(m, ModelResponse)), ZERO)


def messages_tokens(messages: list[ModelMessage]) -> int:
    """Total input plus output tokens of a message trajectory."""
    return sum(m.usage.input_tokens + m.usage.output_tokens for m in messages if isinstance(m, ModelResponse))
