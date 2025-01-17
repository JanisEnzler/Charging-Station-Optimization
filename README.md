
# Optimizing Charging Station Turnover During Peak Demand

This project examines the optimization of turnover during peak times through various business models

## Customer Generation

A customer dataset is required before running the simulation, which can be created automatically by running the customer generator under /CustomerGeneration.

To customise the type of customers generated, different profiles can be created in /CustomerGereration/customer_profiles.json, which also contains information about the different cars used in the simulation. Alternatively, the dataset can be created using another tool, as the generation is independent of the actual simulation.

If the aim is to evaluate the business models for a specific charging station, it is a great advantage to have data and customer profiles collected at that specific charging station, as there can be a great deal of variation between different charging stations.
## Config

The config file can be used to configure various parameters of the simulation, such as the power output of the station or the number of days to be simulated.


## Running the simulation

Once the dataset has been created, the simulation can be run by running simulation.py, which will simulate the baseline and the three different business models in sequence. 
## Evaluation

To evaluate the results, there is a small script in the /evaluation folder that shows some basic percentage deviations at some data points between the simulated models compared to the baseline.

For further and deeper analysis, a process mixing tool such as Disco is recommended.

### Import into Disco

In order for the data to be imported correctly into disco, the columns must be configured correctly.

- The Timestamp column needs to be set as disco timestamp with the pattern 'm'.

- The agent column must be set as the case ID.

- And the Action column is to be set as the Activity.

- The rest of the columns need to be set to other.
