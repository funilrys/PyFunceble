Logs Sharing
============

What do we share / collect?
---------------------------

We only collect when the following actions/events are encountered:

*   The script finds and generates logs into :code:`output/logs/no_referer/`

    *   Shared/posted information:

        *   The extension of the currently tested domain.

    *   Shared/posted to :code:`http://pyfunceble.funilrys.com/api/no-referer`

*   The script find and generate logs into :code:`output/logs/date_format/`

    *   Shared/posted information:

        *   The extracted date.
        *   The currently tested domain name.
        *   The matched whois server (from :code:`iana-domains-db.json`)

    *   Shared/posted to :code:`http://pyfunceble.funilrys.com/api/date-format`

How to share logs?
------------------

::
    
     _______ _                 _           __           
    |__   __| |               | |         / _|          
       | |  | |__   __ _ _ __ | | _____  | |_ ___  _ __
       | |  | '_ \ / _` | '_ \| |/ / __| |  _/ _ \| '__|
       | |  | | | | (_| | | | |   <\__ \ | || (_) | |   
       |_|  |_| |_|\__,_|_| |_|_|\_\___/ |_| \___/|_|   


         _                _                                      
        | |              (_)                                     
     ___| |__   __ _ _ __ _ _ __   __ _   _   _  ___  _   _ _ __
    / __| '_ \ / _` | '__| | '_ \ / _` | | | | |/ _ \| | | | '__|
    \__ \ | | | (_| | |  | | | | | (_| | | |_| | (_) | |_| | |   
    |___/_| |_|\__,_|_|  |_|_| |_|\__, |  \__, |\___/ \__,_|_|   
                                   __/ |   __/ |                 
                                  |___/   |___/                  
     _                   _
    | |                 | |
    | | ___   __ _ ___  | |
    | |/ _ \ / _` / __| | |
    | | (_) | (_| \__ \ |_|
    |_|\___/ \__, |___/ (_)
              __/ |        
             |___/


The logs sharing is now activated automatically with every configuration.

If you do not whish to share your logs simply change

::

   share_logs:                   True

to

::

   share_logs:                   False

into your personal `.PyFunceble.yaml`.

::
    
    _______ _                 _           __           
    |__  __| |               | |         / _|          
      | |  | |__   __ _ _ __ | | _____  | |_ ___  _ __
      | |  | '_ \ / _` | '_ \| |/ / __| |  _/ _ \| '__|
      | |  | | | | (_| | | | |   <\__ \ | || (_) | |   
      |_|  |_| |_|\__,_|_| |_|_|\_\___/ |_| \___/|_|   


                     _    _             
                    | |  (_)            
     _ __ ___   __ _| | ___ _ __   __ _
    | '_ ` _ \ / _` | |/ / | '_ \ / _` |
    | | | | | | (_| |   <| | | | | (_| |
    |_| |_| |_|\__,_|_|\_\_|_| |_|\__, |
                                   __/ |
                                  |___/
     _____       ______                    _     _              
    |  __ \     |  ____|                  | |   | |             
    | |__) |   _| |__ _   _ _ __   ___ ___| |__ | | ___    __ _
    |  ___/ | | |  __| | | | '_ \ / __/ _ \ '_ \| |/ _ \  / _` |
    | |   | |_| | |  | |_| | | | | (_|  __/ |_) | |  __/ | (_| |
    |_|    \__, |_|   \__,_|_| |_|\___\___|_.__/|_|\___|  \__,_|
            __/ |                                               
           |___/                                                
     _          _   _              _              _   _
    | |        | | | |            | |            | | | |
    | |__   ___| |_| |_ ___ _ __  | |_ ___   ___ | | | |
    | '_ \ / _ \ __| __/ _ \ '__| | __/ _ \ / _ \| | | |
    | |_) |  __/ |_| ||  __/ |    | || (_) | (_) | | |_|
    |_.__/ \___|\__|\__\___|_|     \__\___/ \___/|_| (_)
