## TODO
- consolidate `combine_data.py` and `combine_data_with_2021.py`

### Flow:


- start by running `download_epa_data` TWICE, once for 2021 and once for 2022
- run the Google Earth Engine scripts to download 2021-2022 daily data for the gridded datasets

#### Notes on GEE scripts:
- coming soon!

#### okay, at this point you've got all the data downloaded in local folders -- back to the python!

- run `combine_data.py` and `combine_data_with_2021.py` afterwards -- this will be combined into just `combine_data.py` soon :)

- run add_vcd, add_vcd_with_2021, and add_vcd_with_2021.py

#### organize your files such that you now have the final input dataset in the add_vcd_with_vocs.py (i should really write that somewhere shouldn't i)

- run `analysis_with_output_df.py`

#### now, you've got a trained model that has evaluated accuracy at the test data points!

#### To generate the output maps:

- run GEE scripts to download all input data for ROI, which can be changed by modifying `socal_roi`
** NOTE -- due to Google Earth Engine computation limits, the platform may time out/crash if downloading too large of a study area's data

- run `combine_data_socal.py` to get output dataframe
- run `mapped_outputs.py` to see the output map!
