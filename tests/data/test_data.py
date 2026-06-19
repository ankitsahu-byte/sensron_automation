class DasInterrogatorData:
    # We store the data as a list of tuples, exactly how Pytest expects it
    
    EDFA_BOUNDARIES = [
        ("-1", False, "Pulse EDFA Current Reading must be at least 0 mA"),
        ("0", True, None),
        ("110", True, None),
        ("1801", False, "Pulse EDFA Current Reading must not exceed 1800 mA"),
    ]

    VOA_BOUNDARIES = [
        ("-1", False, "VOA Voltage Value must be at least 0 V"), 
        ("0", True, None),
        ("2000", True, None),
        ("4000", True, None),
        ("4001", False, "VOA Voltage Value must not exceed 4000 V"), 
    ]

    DAQ_PULSE_BOUNDARIES = [
          ("49", False, "Pulse Width must be between 50 and 500 nanoseconds"),
          ("50", True, None),
          ("250", True, None),
          ("500", True, None),
          ("501", False, "Pulse Width must be between 50 and 500 nanoseconds")
    ]

    DAQ_PULSE_FREQUENCY = [
          ("-1", False, "Pulse Frequency must be between 100 and 100000 Hz"),
          ("0", True, None),#Pulse Frequency must be between 100 and 100000 Hz
          ("1200", True, None),
          ("2000", True, None),
          ("2441.41", True, None),#Pulse Frequency must be less than 2441.41 Hz for the current Resolution and Sample Number
          ("2442", False, "Pulse Frequency must be less than 2441.41 Hz for the current Resolution and Sample Numbe")
    ]

    DAQ_SAMPLE_NUMBER = [
          ("-1", False, "Sample Number must be at least 256"),
          ("255", False, "Sample Number must be at least 256"),
          ("256", True, None),
          ("51200", True, None),
          ("65536", True, None),
          ("65537", False, "Sample Number must not exceed 65536")
    ]

    DAQ_PULSE_NUMBER = [
        (9, False, "Pulse Number must be at least 10"),       
        (101, False, "Pulse Number must not exceed 100"),       
        (-1, False, "Pulse Number must be at least 10"),  
        (10, True, None),                              
        (55, True, None),                              
        (100, True, None),
    ]

class DatabaseData:
    DATABASE_DATA = [
        ("Username", "Username is required"),
        ("Password", "Password is required"),
        ("Database", "Database is required"),
        # ("Port", "Port is required"), # Kept commented out as requested
        ("Host", "Host is required"),
        ("postgres", "Dialect is required")
    ]

class AnomalyServerData:
    ANOMOLY_SERVER_DATA = [
        ("Topic", "Topic is required"),
        ("Group id", "Group id is required"),
        ("Host", "Host is required")
    ]