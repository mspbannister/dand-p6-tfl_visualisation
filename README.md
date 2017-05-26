# dand-p6-tfl_visualisation
Udacity DAND Project 6 - Make Effective Data Visualisation

This is my submission for Project 6 ('Make Effective Data Visualisation') on Udacity's Data Analyst Nanodegree. The project brief asked the student to create a data visualisation from a data set that tells a story or highlights trends or patterns in the data, using either dimple.js or d3.js.

## Summary 

As a regular user of London's cycle hire scheme, I know how frustrating it can be to arrive at a hire station and find there are no bikes left. This visualisation plots every docking station on an interactive map, with the relative number of average daily bike hires indicated by the station's size and colour saturation (based on data from 1-28 March 2017). As well as giving users a guide as to which stations to avoid on weekdays and weekends, the visualisation hints at commmuter and leisure trends in London: on weekdays the busiest stations can be found in the centre - near train stations and key commercial districts. On weekends, the number of bikes hired in these areas fall, while hires in park areas increase significantly.

## Design

### Chart type
I decided at the outset that I wanted to plot each station on an interactive map, rather than using a fixed image of London, for two reasons:
- There are over 750 bike docking stations spread over a large area within central London. Plotting these all at once causes a lot of overlap, which is alleviated when the user zooms in on specific areas; and  
- I wanted fellow bike scheme users to be able to zoom in on their local hire station to see how it compared with others nearby, rather than trying to gauge it from a distance.

### Data
I noticed that cycle hire patterns were significantly different on weekdays and weekends, which may reflect the different patterns of commmuter vs. leisure usage. I designed the visualisation to allow these different patterns to be viewed separately, accessible through the buttons on the upper right of the graphic. 

I designed the buttons themselves to match the map's native zoom buttons as closely as possible, to ensure the viewer intuitively understood these were clickable objects. The buttons change colour to denote the selected option, with the purple hue reflecting the colour of the bubble markers.

### Markers
I used bubble markers for each station because they allow additional information (in this case average daily cycle hires) to be clearly encoded through attributes like size and colour. Initially I planned only to encode the data using bubble size, but after receiving feedback from a friend, I decided to use double encoding (combining size with colour saturation) to make the patterns easier to see.

Another friend felt that my original colour scheme, red, was too aggressive, and that it made her not want to explore the data further. After experimenting with a few alternatives, I settled on purple because (unlike blue or green) it does not appear elsewhere on the map, reducing the potential for visual confusion.

### Labels
Rather than include a legend, which can be difficult to interpret accurately for these relatively small and similarly sized circles (with radii of 4-9 pixels), I decided to annotate each bubble with a tooltip. As the user moves the mouse over a station, they are shown the station name and average daily cycle hires for the chosen data (i.e. Overall, Weekdays or Weekends).

## Conclusion

I am satisfied that this visualisation accomplishes what I set out to achieve with it. I would be interested in improving it further by adding additional options, for example adding lines between stations to represent the most popular journeys.

## Resources

In creating this visualisation, I used the following resources:

- https://api.tfl.gov.uk/  
- http://cycling.data.tfl.gov.uk/  
- http://bl.ocks.org/d3noob/9267535  
- http://bl.ocks.org/d3noob/a22c42db65eb00d4e369  
- http://leafletjs.com/examples/quick-start/  
- http://stackoverflow.com/questions/17671252/  d3-create-a-continuous-color-scale-with-many-strings-inputs-for-the-range-and-d  
- https://github.com/d3/d3-scale-chromatic  
- https://github.com/d3/d3/blob/master/CHANGES.md#scales-d3-scale  