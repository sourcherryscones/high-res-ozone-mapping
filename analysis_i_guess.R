library(tigris)
library(tidyverse)
library(sf)
library(terra)

setwd("C:/Users/purva/gis_stuff/")
getwd()

california <- states(cb = FALSE, year = 2021) %>% 
  filter(NAME == "California")

plot(st_geometry(california))

# Save the data
california %>% 
  st_write("data/california.shp")


# Load NDVI data
ndvi <- rast("gee/NDVI_California_Stacked.tif")
plot(ndvi)

tt <- rast("gee/Daymet_temp_image.tif")
plot(tt)
