"""
Wellness Pulse - Mock Raw Data Generator

Generates 3 realistic raw datasets:
1) user_events
2) health_content
3) marketing_events

Outputs CSV files into:
data/raw/user_events/
data/raw/health_content/
data/raw/marketing_events/

Run:
  python scripts/generate_mock_data.py

Optional flags:
  python scripts/generate_mock_data.py --days 14 --users 8000 --events 120000 --seed 42
"""

from __future__ import annotations

import argparse
import os
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict

import pandas as pd
from faker import Faker


# ---------- Helpers ----------

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_z(dt: datetime) -> str:
    # Example: 2026-02-02T17:22:11Z
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class Config:
    days: int
    users: int
    events: int
    seed: int


# ---------- Data Generation ----------

def generate_health_content(fake: Faker, num_content: int, now: datetime) -> pd.DataFrame:
    """
    Simulates a health content catalog (articles/videos).
    This is reference data used in personalization/recommendations.
    """
    categories = [
        "nutrition", "fitness", "mental_health", "sleep", "heart_health",
        "diabetes", "women_health", "men_health", "skin_care", "covid19",
        "cold_flu", "digestive_health", "stress", "weight_loss"
    ]
    content_types = ["article", "video", "quiz"]
    difficulty = ["beginner", "intermediate", "advanced"]

    rows: List[Dict] = []
    for i in range(num_content):
        publish_days_ago = random.randint(0, 365)
        publish_dt = now - timedelta(days=publish_days_ago, hours=random.randint(0, 23))

        rows.append({
            "content_id": f"c_{i+1:06d}",
            "title": fake.sentence(nb_words=random.randint(4, 10)).rstrip("."),
            "category": random.choice(categories),
            "content_type": random.choice(content_types),
            "difficulty": random.choice(difficulty),
            "author": fake.name(),
            "publish_ts": isoformat_z(publish_dt),
            "reading_time_sec": random.randint(60, 900),  # 1–15 minutes
            "tags": ",".join(fake.words(nb=random.randint(2, 6), unique=True)),
        })

    return pd.DataFrame(rows)


def generate_users(fake: Faker, num_users: int) -> pd.DataFrame:
    """
    Simulates a user dimension table.
    We keep PII minimal; in real systems you'd hash/anonymize more aggressively.
    """
    genders = ["female", "male", "nonbinary", "prefer_not_say"]
    locales = ["en-US", "en-IN", "en-GB", "es-US", "fr-FR"]
    devices = ["ios", "android", "web"]
    states = ["CA", "NY", "TX", "FL", "IL", "MO", "WA", "MA", "GA", "PA"]

    rows: List[Dict] = []
    for i in range(num_users):
        rows.append({
            "user_id": f"u_{i+1:06d}",
            "age": random.randint(18, 65),
            "gender": random.choice(genders),
            "state": random.choice(states),
            "locale": random.choice(locales),
            "primary_device": random.choice(devices),
            "signup_source": random.choice(["organic", "paid_search", "referral", "social"]),
        })

    return pd.DataFrame(rows)


def generate_user_events(
    users_df: pd.DataFrame,
    content_df: pd.DataFrame,
    now: datetime,
    days: int,
    num_events: int,
) -> pd.DataFrame:
    """
    Simulates web/mobile behavioral events:
    view_content, search, click_recommendation, bookmark, share, email_open, app_open
    """
    event_types = [
        "app_open",
        "view_content",
        "search",
        "click_recommendation",
        "bookmark",
        "share",
        "email_open",
    ]
    devices = ["ios", "android", "web"]
    traffic_sources = ["direct", "seo", "email", "push", "social", "paid"]

    user_ids = users_df["user_id"].tolist()
    content_ids = content_df["content_id"].tolist()

    rows: List[Dict] = []
    start_dt = now - timedelta(days=days)

    for i in range(num_events):
        user_id = random.choice(user_ids)
        event_type = random.choice(event_types)
        device = random.choice(devices)

        # random timestamp in the last N days
        seconds_range = int((now - start_dt).total_seconds())
        event_dt = start_dt + timedelta(seconds=random.randint(0, seconds_range))

        session_id = f"s_{random.randint(1, 10_000_000):08d}"

        # some events tie to content; others don't
        content_id = None
        if event_type in ["view_content", "click_recommendation", "bookmark", "share"]:
            content_id = random.choice(content_ids)

        # searches have query text
        search_query = None
        if event_type == "search":
            search_query = random.choice([
                "healthy breakfast ideas",
                "how to sleep better",
                "lower blood pressure",
                "stress management tips",
                "weight loss plan",
                "workout for beginners",
                "high protein foods",
                "diabetes symptoms",
            ])

        # pseudo engagement
        dwell_time_sec = None
        if event_type in ["view_content", "app_open"]:
            dwell_time_sec = random.randint(5, 600)

        rows.append({
            "event_id": f"e_{i+1:09d}",
            "event_ts": isoformat_z(event_dt),
            "user_id": user_id,
            "session_id": session_id,
            "event_type": event_type,
            "device": device,
            "traffic_source": random.choice(traffic_sources),
            "content_id": content_id,
            "search_query": search_query,
            "dwell_time_sec": dwell_time_sec,
        })

    return pd.DataFrame(rows)


def generate_marketing_events(
    users_df: pd.DataFrame,
    now: datetime,
    days: int,
    num_events: int,
) -> pd.DataFrame:
    """
    Simulates CRM/marketing events: email/push sends and engagements
    Useful for attribution + personalization.
    """
    channels = ["email", "push", "sms"]
    event_types = ["sent", "delivered", "opened", "clicked", "unsubscribed"]
    campaigns = [
        "weekly_digest",
        "sleep_challenge",
        "heart_health_month",
        "new_content_alert",
        "weight_loss_series",
        "stress_relief_program",
    ]

    user_ids = users_df["user_id"].tolist()
    start_dt = now - timedelta(days=days)

    rows: List[Dict] = []
    seconds_range = int((now - start_dt).total_seconds())

    for i in range(num_events):
        user_id = random.choice(user_ids)
        channel = random.choice(channels)
        campaign_id = random.choice(campaigns)

        event_dt = start_dt + timedelta(seconds=random.randint(0, seconds_range))

        # Engagement probability chain (sent -> delivered -> opened -> clicked)
        base_event = random.random()
        if base_event < 0.60:
            event_type = "sent"
        elif base_event < 0.80:
            event_type = "delivered"
        elif base_event < 0.93:
            event_type = "opened"
        elif base_event < 0.99:
            event_type = "clicked"
        else:
            event_type = "unsubscribed"

        rows.append({
            "mkt_event_id": f"m_{i+1:09d}",
            "event_ts": isoformat_z(event_dt),
            "user_id": user_id,
            "channel": channel,
            "campaign_id": campaign_id,
            "event_type": event_type,
        })

    return pd.DataFrame(rows)


# ---------- Output ----------

def write_partitioned_csv(df: pd.DataFrame, base_dir: Path, dataset: str, now: datetime) -> Path:
    """
    Writes one raw file per run, like real ingestion drops.
    Filename includes timestamp.
    """
    ensure_dir(base_dir)
    filename = f"{dataset}_{now.strftime('%Y%m%dT%H%M%SZ')}.csv"
    out_path = base_dir / filename
    df.to_csv(out_path, index=False)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7, help="How many days of data to simulate.")
    parser.add_argument("--users", type=int, default=5000, help="Number of unique users.")
    parser.add_argument("--events", type=int, default=80000, help="Number of user events to generate.")
    parser.add_argument("--seed", type=int, default=123, help="Random seed for repeatable results.")
    args = parser.parse_args()

    cfg = Config(days=args.days, users=args.users, events=args.events, seed=args.seed)

    # Seed everything for reproducibility
    random.seed(cfg.seed)
    fake = Faker()
    Faker.seed(cfg.seed)

    now = utc_now()

    project_root = Path(__file__).resolve().parents[1]
    raw_root = project_root / "data" / "raw"

    user_events_dir = raw_root / "user_events"
    content_dir = raw_root / "health_content"
    marketing_dir = raw_root / "marketing_events"

    # Create reference + dimension tables
    content_df = generate_health_content(fake, num_content=1500, now=now)
    users_df = generate_users(fake, num_users=cfg.users)

    # Generate fact/event tables
    user_events_df = generate_user_events(users_df, content_df, now=now, days=cfg.days, num_events=cfg.events)

    # marketing events: smaller than user events usually
    marketing_events_df = generate_marketing_events(users_df, now=now, days=cfg.days, num_events=max(5000, cfg.users * 2))

    # Write outputs (raw drops)
    out1 = write_partitioned_csv(user_events_df, user_events_dir, "user_events", now)
    out2 = write_partitioned_csv(content_df, content_dir, "health_content", now)
    out3 = write_partitioned_csv(marketing_events_df, marketing_dir, "marketing_events", now)

    print("✅ Generated raw datasets:")
    print(f" - {out1}")
    print(f" - {out2}")
    print(f" - {out3}")
    


if __name__ == "__main__":
    main()
