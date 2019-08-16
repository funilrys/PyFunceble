File generation while using the API
===================================

You may want to test using the API but still want the result structured normally like a CLI usage.
For that case simply add the following.

Global configuration load
-------------------------

::

    from PyFunceble import load_config

    OUR_CUSTOM_PYFUNCEBLE_CONFIGURATION = {
        "api_file_generation": True
    }

    load_config(generate_directory_structure=True, custom=OUR_CUSTOM_PYFUNCEBLE_CONFIGURATION)

    # The output directory is then generated, and the file(s) too.

    # You logic or whatever you want.

Local configuration load
------------------------

::

    from PyFunceble import test as PyFunceble

    OUR_CUSTOM_PYFUNCEBLE_CONFIGURATION = {
        "api_file_generation": True
    }

    print(f"google.com is {PyFunceble("google.com", config=OUR_CUSTOM_PYFUNCEBLE_CONFIGURATION)}")

    # The output directory is then generated, and the file(s) too.