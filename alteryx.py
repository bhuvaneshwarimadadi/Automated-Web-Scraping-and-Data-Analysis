from ayx import Package
import pandas as pd
import re  # For regex pattern matching
from ayx import Alteryx

# Step 1: Read input data from Alteryx
df = Alteryx.read("#1")  # Reads the data passed to the Python Tool
print("Columns in the DataFrame:", df.columns)  # Prints columns for verification

# Step 2: Define a function to extract author, price, and type from the 'details' column
def extract_details(details):
    """
    Extracts 'Author', 'Price', and 'Type' using regex patterns from a combined 'details' field.
    - details: A string containing book details.

    Returns:
        A Pandas Series containing the extracted 'Author', 'Price', and 'Type'.
    """
    # Regex pattern to extract the author
    author_match = re.match(r"([A-Za-z\s]+)(?=\$\d+(\.\d{1,2})?)", details)
    # Regex pattern to extract the price (e.g., $12.99)
    price_match = re.search(r"(\$\d+(\.\d{1,2})?)", details)
    # Regex pattern to extract the type (alphabetic characters after the price)
    type_match = re.search(r"(\D+)$", details)

    # Extract values or set to 'Null' if no match found
    author = author_match.group(1) if author_match else "Null"
    price = price_match.group(1) if price_match else "Null"
    book_type = type_match.group(1).strip() if type_match else "Null"

    return pd.Series([author, price, book_type])

# Step 3: Apply the function to split the 'details' column
df[['Author', 'Price', 'Type']] = df['details'].apply(extract_details)

# Step 4: Drop the old 'details' column (optional)
df.drop(columns=['details'], inplace=True)

# Step 5: Print and verify the updated DataFrame
print("Updated DataFrame:")
print(df.head())

# Step 6: Write the processed data back to Alteryx
Alteryx.write(df, 1)  # Sends the data to the first output anchor
