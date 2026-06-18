#!/usr/bin/env python3
"""PayHere hash/signature helpers."""

from __future__ import annotations

import argparse
import base64
import hashlib
from decimal import Decimal, ROUND_HALF_UP


def md5_upper(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest().upper()


def format_amount(value: str) -> str:
    amount = Decimal(str(value).replace(",", "")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{amount:.2f}"


def request_hash(merchant_id: str, order_id: str, amount: str, currency: str, merchant_secret: str) -> str:
    formatted_amount = format_amount(amount)
    hashed_secret = md5_upper(merchant_secret)
    return md5_upper(f"{merchant_id}{order_id}{formatted_amount}{currency.upper()}{hashed_secret}")


def notification_sig(
    merchant_id: str,
    order_id: str,
    payhere_amount: str,
    payhere_currency: str,
    status_code: str,
    merchant_secret: str,
) -> str:
    hashed_secret = md5_upper(merchant_secret)
    return md5_upper(
        f"{merchant_id}{order_id}{payhere_amount}{payhere_currency.upper()}{status_code}{hashed_secret}"
    )


def oauth_basic(app_id: str, app_secret: str) -> str:
    raw = f"{app_id}:{app_secret}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate PayHere request hashes and callback signatures.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    request = subparsers.add_parser("request-hash", help="Generate hosted checkout/preapproval/authorize hash")
    request.add_argument("--merchant-id", required=True)
    request.add_argument("--order-id", required=True)
    request.add_argument("--amount", required=True)
    request.add_argument("--currency", required=True)
    request.add_argument("--merchant-secret", required=True)

    sig = subparsers.add_parser("notification-sig", help="Generate callback md5sig for verification")
    sig.add_argument("--merchant-id", required=True)
    sig.add_argument("--order-id", required=True)
    sig.add_argument("--payhere-amount", required=True)
    sig.add_argument("--payhere-currency", required=True)
    sig.add_argument("--status-code", required=True)
    sig.add_argument("--merchant-secret", required=True)

    basic = subparsers.add_parser("oauth-basic", help="Generate Base64 app_id:app_secret authorization code")
    basic.add_argument("--app-id", required=True)
    basic.add_argument("--app-secret", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "request-hash":
        print(request_hash(args.merchant_id, args.order_id, args.amount, args.currency, args.merchant_secret))
    elif args.command == "notification-sig":
        print(
            notification_sig(
                args.merchant_id,
                args.order_id,
                args.payhere_amount,
                args.payhere_currency,
                args.status_code,
                args.merchant_secret,
            )
        )
    elif args.command == "oauth-basic":
        print(oauth_basic(args.app_id, args.app_secret))


if __name__ == "__main__":
    main()
