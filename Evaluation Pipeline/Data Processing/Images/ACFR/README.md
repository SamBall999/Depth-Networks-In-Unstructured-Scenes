## Extracting ACFR Image Data

The ACFR image files were made available in binary format for optimisation purposes. To transform the images to png format, the ACFR custom-built libraries
comma and snark were installed. The [comma](https://github.com/acfr/comma) and [snark](https://github.com/acfr/snark) libraries built by the Australian Centre for Field Robotics (ACFR) provide a suite of C++ functionality for robotics applications. 

The following steps were followed for the extraction:

- The comma and snark libraries were built from the source on a Linux Mint operating system.

- In order for a fair comparison with the FieldSafe dataset, only the front view from the panospheric Ladybug camera was extracted for analysis.

- Images from the almond subset were extracted from binary to png format through the bash commands and relevant library utilities as outlined in ...