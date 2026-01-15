#!/usr/bin/env python3
"""Monitor the running SPACEV1B benchmark"""

import time
from pymilvus import MilvusClient
import sys

def monitor_collection(collection_name="spacev1b_benchmark", interval=10):
    """Monitor collection growth"""
    client = MilvusClient(uri="http://localhost:19530")

    print(f"Monitoring collection '{collection_name}'...")
    print(f"Press Ctrl+C to stop\n")

    last_count = 0
    last_time = time.time()

    try:
        while True:
            if client.has_collection(collection_name):
                stats = client.get_collection_stats(collection_name)
                current_count = int(stats['row_count'])
                current_time = time.time()

                # Calculate rate
                if last_count > 0:
                    elapsed = current_time - last_time
                    added = current_count - last_count
                    rate = added / elapsed if elapsed > 0 else 0

                    progress_50m = (current_count / 50_000_000) * 100
                    eta_seconds = (50_000_000 - current_count) / rate if rate > 0 else 0
                    eta_minutes = eta_seconds / 60

                    print(f"Vectors: {current_count:>12,} | "
                          f"Rate: {rate:>8,.0f} vec/s | "
                          f"Progress: {progress_50m:>5.2f}% | "
                          f"ETA: {eta_minutes:>5.1f} min")
                else:
                    print(f"Vectors: {current_count:>12,}")

                last_count = current_count
                last_time = current_time
            else:
                print(f"Collection '{collection_name}' not found yet...")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        if last_count > 0:
            print(f"Final count: {last_count:,} vectors")

if __name__ == "__main__":
    collection = sys.argv[1] if len(sys.argv) > 1 else "spacev1b_benchmark"
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    monitor_collection(collection, interval)
