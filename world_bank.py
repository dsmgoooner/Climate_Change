# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define a function to clean the World Bank data
def clean_data(filename):
    
    
    # Read the CSV file and set 'Country Name' and 'Indicator Name' as index
    df = pd.read_csv(filename, index_col=['Country Name', 'Indicator Name'])
    # Drop the unnecessary columns 'Country Code' and 'Indicator Code'
    df = df.drop(columns=['Country Code', 'Indicator Code'])
    # Convert the data to numeric type, and replace any missing values using forward and backward fill
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(method='ffill', axis=0).fillna(method='bfill', axis=0)
    # Reset the index of the DataFrame
    df = df.reset_index()
    return df



# Call the function to clean the data and store it in a variable
world_bank_data = clean_data('world_bank_data.csv')

# Transpose the data
transposed_data = world_bank_data.set_index(['Country Name', 'Indicator Name']).transpose()
print(transposed_data)

# Define the indicators of interest
population_growth = 'Population growth (annual %)'
co2_emissions = 'CO2 emissions (kt)'
electric_consumption = 'Electric power consumption (kWh per capita)'

# Get the statistics for the selected indicators
population_growth_stats = world_bank_data[world_bank_data['Indicator Name'] == population_growth]
emmision_stats = world_bank_data[world_bank_data['Indicator Name'] == co2_emissions]
electric_consumption_stats = world_bank_data[world_bank_data['Indicator Name'] == electric_consumption]

# Print the statistics for the selected indicators
print('population growth statistics:')
print(population_growth_stats.describe())
print('\nCO2 emissions statistics:')
print(emmision_stats.describe())
print('\nElectric Consumption statistics:')
print(electric_consumption_stats.describe())

# Plot the CO2 emissions over time for selected countries
countries = ['Australia', 'United Kingdom', 'Canada', 'India']
for country in countries:
   co2_stats_temp = world_bank_data[world_bank_data['Country Name'] == country]
   co_stats_temp = co2_stats_temp.describe()
   # Plot the CO2 emissions for the country
   co2_stats_temp.plot(label=country, legend=False)
   plt.title('CO2 emissions over time')
   plt.xlabel('Emission over years')
   plt.ylabel('CO2 emissions (in KT)')
   plt.show()
   
   # Concatenate the statistics for the selected indicators
combined_df = pd.concat([population_growth_stats.describe(), emmision_stats.describe(), electric_consumption_stats.describe()])
# Calculate the correlation matrix for the selected indicators
correlation_matrix = combined_df.corr()

# Print the correlation matrix
print('Correlation matrix:')
print(correlation_matrix)

# Plot scatter plots to visualize the relationship between CO2 emissions and the selected indicators
plt.scatter(emmision_stats.describe(), population_growth_stats.describe())
plt.title('CO2 emissions vs population growth')
plt.xlabel('CO2 emissions (in KT)')
plt.ylabel('population growth')
plt.show()

plt.scatter(emmision_stats.describe(), electric_consumption_stats.describe())
plt.title('CO2 emissions vs electric consumption')
plt.xlabel('CO2 emissions')
plt.ylabel('Electric power consumption (kWh per capita)')
plt.show()

# visualize the correlation matrix for each indicator for each country using a heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')


