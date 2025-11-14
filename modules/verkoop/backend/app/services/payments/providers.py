
from dataclasses import dataclass

@dataclass
class PaymentResult:
    intent_id: str
    status: str
    payment_url: str | None = None

class StripeProvider:
    def create_intent(self, amount: float, currency: str = "MXN") -> PaymentResult:
        # stub
        return PaymentResult(intent_id="pi_stub_"+str(int(amount*100)), status="requires_payment_method", payment_url="https://example.com/pay/stripe")

    def handle_webhook(self, payload: dict) -> dict:
        return {"ok": True}

class ProviderFactory:
    @staticmethod
    def get(name: str):
        return StripeProvider()
