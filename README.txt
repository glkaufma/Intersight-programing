    
    
The get_dimm_sn.py script was created to support Field Notice (FN): FN - 72368 - Some DIMMs Might Fail Prematurely Due
to a Manufacturing Deviation - Hardware Upgrade Available. https://www.cisco.com/c/en/us/support/docs/field-notices/723/fn72368.html

This script makes API calls to obtian Serial Numbers (SNs), hostname, location and DN for all DIMMs from servers being managed by Intersight.

The script leverages "intersight_auth.py" from the DevNet learning labs to handle authentication, thanks Chris Gascoigne!

You will need to setup an Intresight API key in order to access your instance of Intersight.  Instructions on how to do so are here:
https://intersight.com/apidocs/introduction/security/%23generating-api-keys&sa=D&ust=1612024909729000&usg=AOvVaw362rkbFxqhX_Mo8w0xkDJG/#benefits-of-using-api-keys     

Once you have a secret key created copy your key into a file called SecretKey.txt

Copy the API key and paste it to the variable 'api_key_id'

The script will pull all DIMM slot information from Intersight, remove all null entries (empty DIMMs), output a serial.txt file
and output a serial_all.xls file.

Use the 'serial.txt' file to upload into the Serial Number Validation tool for the FN:
https://snvui.cisco.com/snv/FN72368

Once you upload 'serial.txt' a new file with the DIMM SN identfied as 'impacted' or 'not impacted' will be created.  Use this file to identify
what SN's are impacted from 'serial_all.xlsx' (you can use vlookup in excel) so that you now the hostname, locations and 'DN' of the DIMMs that
are impacted.

author: Glen Kaufman (glkaufma@cisco.com)