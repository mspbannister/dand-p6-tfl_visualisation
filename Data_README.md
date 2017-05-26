# Notes on the data used

The data supporting this visualisation ('March_Cycle_Hire_Summary.csv') is a summary of every Santander Cycles journey made in the period 1-28 March 2017 inclusive. This was compiled using raw data from [TfL](http://cycling.data.tfl.gov.uk/), and cleaned using a Python script ('Prepare_TfL_bike_data.py').

Note, some stations do not return geographic data via the TfL API and hence have been excluded from the visualisation, as follows:
- Eccleston Place, Victoria (id 167)  
- Wardour Street, Soho (id 192)  
- Union Street, The Borough (id 196)  
- Frampton Street, Paddington (id 238)  
- Clifford Street, Mayfair (id 391)  
- Chelsea Bridge, Pimlico (id 419)  
- Southerton Road, Hammersmith (id 598)