import pandas as pd
import statsmodels.api as sm
import numpy as np



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Read the CSV file into a DataFrame
    df = pd.read_csv('WCCData.csv')
    print(df.dtypes)


    #Place unknown into the School Location empty blocks
    df['School'].fillna('Unknown', inplace=True)

    #Placing 'U' for unknown gender
    df['M/F'].fillna('U', inplace=True)

    #Placing 'U' for Unknown Ethnicity
    df['Ethnicity'].fillna('U', inplace=True)

    # Convert 'M/F' column to numeric (assuming it contains binary values)
    df['M/F'] = df['M/F'].map({'M': 0, 'F': 1})

    # Fill missing values in 'Discharged To' with "Pending"
    df['Discharged To'] = df['Discharged To'].fillna("Pending")

    # Replace NaN values in 'Placement Date' with the minimum date in the column
    df['Placement Date'].fillna(df['Placement Date'].min(), inplace=True)

    # Convert 'Placement Date' to datetime
    df['Placement Date'] = pd.to_datetime(df['Placement Date'], errors='coerce', format='%m/%d/%Y')

    # Convert categorical variables to dummy/indicator variables
    df = pd.get_dummies(df, columns=['Month', 'M/F', 'Placement Code', 'Placed From', 'Ethnicity', 'Placing County',
                                     'School'])

    # Convert 'Discharge Date' to datetime, filling invalid values with NaT
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce', format='%m/%d/%Y')

    # Replace NaT (Not a Time) values in 'Discharge Date' with the minimum date in the column
    df['Discharge Date'].fillna(df['Discharge Date'].min(), inplace=True)

    # Calculate the average time between 'Placement Date' and 'Discharge Date'
    average_time = (df['Discharge Date'] - df['Placement Date']).mean()

    # Fill missing 'Discharge Date' with the calculated average
    df['Discharge Date'] = df.apply(
        lambda row: row['Placement Date'] + pd.Timedelta(days=int(average_time.days)) if pd.isna(
            row['Discharge Date']) else row['Discharge Date'],
        axis=1
    )

    df.to_csv('exported_data.csv', index=False)
    print("Data sent to CSV")
    
    arrayData = np.asarray(df)
    print(arrayData.dtype)
    print()
    print(arrayData)
    
"""   
    # Iterate over each column as the dependent variable
    for dependent_variable in df.columns:
        if dependent_variable != 'target_variable' and dependent_variable in df.columns:
            # Define the dependent variable
            y = df[dependent_variable]

            # Define the independent variables
            X = df.drop([dependent_variable], axis=1, errors='ignore')

            # Add a constant term to the features (required for statsmodels)
            X = sm.add_constant(X)

            # Assuming df is your DataFrame
            for column in df.columns:
                if pd.api.types.is_categorical_dtype(df[column]):
                    print(f"{column} is categorical.")
                elif pd.api.types.is_object_dtype(df[column]) and len(df[column].unique()) <= 10:
                    # Assuming a variable is considered categorical if it has fewer than or equal to 10 unique values
                    print(f"{column} is categorical.")
                else:
                    print(f"{column} is not categorical.")
                    # Fit the regression model
                    model = sm.OLS(y, X).fit()
                    # Print the results
                    print(f"Dependent Variable: {dependent_variable}")
                    print(model.summary())
                    print("\n" + "=" * 80 + "\n")
"""            
            

            

