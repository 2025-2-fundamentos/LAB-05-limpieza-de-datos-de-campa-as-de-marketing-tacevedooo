"""
Escriba el codigo que ejecute la accion solicitada.
"""

import os
import glob
import pandas as pd

def clean_campaign_data():
    #Create output directory if it doesn't exist
    os.makedirs("files/output", exist_ok=True)

    # Read and concatenate all zip files
    zip_files = glob.glob("files/input/bank-marketing-campaing-*.csv.zip")

    dataframes = []
    for zip_file in zip_files:
        df = pd.read_csv(zip_file, compression='zip')
        dataframes.append(df)

    # Concatenate all dataframes
    data = pd.concat(dataframes, ignore_index=True)

    # CLIENT CSV
    client_data = data[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()

    # Clean job column: replace "." with "" and "-" with "_"
    client_data['job'] = client_data['job'].str.replace('.', '', regex=False)
    client_data['job'] = client_data['job'].str.replace('-', '_', regex=False)

    # Clean education column: replace "." with "_" and "unknown" with pd.NA
    client_data['education'] = client_data['education'].str.replace('.', '_', regex=False)
    client_data['education'] = client_data['education'].replace('unknown', pd.NA)

    # Convert credit_default and mortgage columns (they're already in the right format based on the data)
    # Just ensure they are in the right format: "yes" to 1, anything else to 0
    client_data['credit_default'] = (client_data['credit_default'] == 'yes').astype(int)
    client_data['mortgage'] = (client_data['mortgage'] == 'yes').astype(int)

    # Select final columns for client
    client_final = client_data[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']]

    # CAMPAIGN CSV
    campaign_data = data[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()

    # Convert previous_outcome: "success" to 1, anything else to 0
    campaign_data['previous_outcome'] = (campaign_data['previous_outcome'] == 'success').astype(int)

    # Convert campaign_outcome: "yes" to 1, anything else to 0
    campaign_data['campaign_outcome'] = (campaign_data['campaign_outcome'] == 'yes').astype(int)

    # Create last_contact_date in YYYY-MM-DD format using day, month, and year 2022
    campaign_data['last_contact_date'] = pd.to_datetime(
        '2022-' + campaign_data['month'].astype(str) + '-' + campaign_data['day'].astype(str),
        format='%Y-%b-%d'
    ).dt.strftime('%Y-%m-%d')

    # Select final columns for campaign
    campaign_final = campaign_data[['client_id', 'number_contacts', 'contact_duration', 
                                    'previous_campaign_contacts', 'previous_outcome', 
                                    'campaign_outcome', 'last_contact_date']]

    # ECONOMICS CSV
    economics_data = data[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()

    # Write output files
    client_final.to_csv("files/output/client.csv", index=False)
    campaign_final.to_csv("files/output/campaign.csv", index=False)
    economics_data.to_csv("files/output/economics.csv", index=False)