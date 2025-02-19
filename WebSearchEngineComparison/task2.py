import json
import csv
import numpy as np
from urllib.parse import urlparse

# Load Google and Bing results from JSON files
with open('googleResults.json', 'r') as f:
    google_results = json.load(f)

with open('hw1.json', 'r') as f:
    bing_results = json.load(f)

# Function to normalize URLs based on the updated rules
def normalize_url(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip('/')
    if netloc.startswith('www.'):
        netloc = netloc[4:]  # Remove 'www.' prefix

    return f'{netloc}{path}'

def spearman_calculation(rank1, rank2):
    if len(rank1) != len(rank2):
        raise ValueError("Rank lists must be the same length")
    n = len(rank1)
    if n == 0 or n == 1:  # Return None if no valid comparison can be made
        return None
    rank_diff = [rank1[i] - rank2[i] for i in range(n)]
    d_squared = [d ** 2 for d in rank_diff]
    numerator = 6 * sum(d_squared)
    denominator = n * (n ** 2 - 1)
    return 1 - (numerator / denominator)

# Function to calculate overlap and Spearman correlation
def calculate_overlap_and_spearman(google_urls, bing_urls):
    google_urls_normalized = [normalize_url(url) for url in google_urls]
    bing_urls_normalized = [normalize_url(url) for url in bing_urls]
    overlap_urls = set(google_urls_normalized) & set(bing_urls_normalized)
    
    if len(overlap_urls) == 0:
        # No overlap
        return 0, 0, 0
    
    google_ranks = []
    bing_ranks = []
    
    for url in overlap_urls:
        google_rank = google_urls_normalized.index(url) + 1
        bing_rank = bing_urls_normalized.index(url) + 1
        google_ranks.append(google_rank)
        bing_ranks.append(bing_rank)
    
    if len(overlap_urls) == 1:
        # Handle the case of one result matching
        if google_ranks[0] == bing_ranks[0]:
            return len(overlap_urls), len(overlap_urls) / len(google_urls) * 100, 1
        else:
            return len(overlap_urls), len(overlap_urls) / len(google_urls) * 100, 0
    
    # Multiple overlaps
    percent_overlap = len(overlap_urls) / len(google_urls) * 100
    spearman_corr = spearman_calculation(google_ranks, bing_ranks) if overlap_urls else None
    return len(overlap_urls), percent_overlap, spearman_corr


# Prepare CSV file to write results
output_file = 'hw1.csv'

# Track sums for calculating averages
total_overlap = 0
total_percent_overlap = 0
total_spearman = []


with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write header
    csvwriter.writerow(['Queries'.ljust(30), 'Number of Overlapping Results'.ljust(30), 'Percent Overlap'.ljust(30), 'Spearman Coefficient'.ljust(30)])
    
    # Add a line under the titles
    csvwriter.writerow(['-' * 30, '-' * 30, '-' * 30, '-' * 30])
    
    # Iterate over each query in Google results
    for i, (query, google_urls) in enumerate(google_results.items()):
        bing_urls = bing_results.get(query, [])
        num_overlap, percent_overlap, spearman_corr = calculate_overlap_and_spearman(google_urls[:10], bing_urls[:10])
        
        # Write results to CSV
        csvwriter.writerow([
            f'Query {i+1}'.ljust(30),
            str(num_overlap).ljust(30),
            f'{percent_overlap:.2f}%'.ljust(30),
            spearman_corr if spearman_corr is not None else 'None'.ljust(30)
        ])
        
        total_overlap += num_overlap
        total_percent_overlap += percent_overlap
        if spearman_corr is not None:
            total_spearman.append(spearman_corr)

    # Calculate averages
    avg_overlap = total_overlap / len(google_results)
    avg_percent_overlap = total_percent_overlap / len(google_results)
    avg_spearman = np.mean(total_spearman) if total_spearman else None
    
    # Write averages to CSV
    csvwriter.writerow(['Averages'.ljust(30), str(avg_overlap).ljust(30), f'{avg_percent_overlap:.2f}%'.ljust(30), avg_spearman if avg_spearman is not None else 'None'.ljust(30)])

print(f"Results saved to {output_file}")
