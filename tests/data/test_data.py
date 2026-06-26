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

class MoniteringServerData:
    MONITERING_SERVER_DATA = [
        ("Topic", "Topic is required"),
        ("Group id", "Group id is required"),
        ("Host", "Host is required")
    ]

class AnomalyData:
    LOCTION_OFFSET_DATA=[
          (-40001, False, "Value must be at least -40000"), 
          (-40000, True, None),          
          (40000, True, None),
          (0, True, None),
          (40001, False, "Value must be between -40000 and 40000")
    ]

    PROCESS_ANOMALY_INTERVAL_DATA =[
          ("999", False, "Value must be at least 1000"), 
          ("1000", True, None),                                            
          ("30000", True, None),                                         
          ("60000", True, None),
          ("1300", True, None),                                        
          ("60001", False, "Value must be between 1000 and 60000")
    ]

    MAX_ANOMALY_LIMIT_DATA =[
          ("9", False, "Value must be at least 10"),
          ("10", True, None),
          ("1000", True, None),
          ("1001", False, "Value must be between 10 and 1000")
    ]

    SYSTEM_IDLE_TIME_THRESOLD_DATA =[
          ("-1", False, "The Minimum value is greater than 1"),
          ("0", False, "The Minimum value is greater than 1"),
          ("300", True, None),
          ("1", True, None),
          ("301", False, "Value must be between 1 and 300")
    ]

    AUOT_ACT_TIMEOUT_DATA = [
          ("0", False, "The Minimum value is greater than 1"),
          ("1440", True, None),
          ("10", True, None),
          ("1441", False, "Value must be between 1 and 1440")
    ]

class MapData:
    HIGH_PROXIMITY_THRESHOLD_DATA = [
          (-1, False, "Value must be greater than or equal to 0"),        
          (1, True, None),
          (0,True, None)

        ]
    HIGHER_CONFIDENCE_THRESHOLD_DATA = [
          (-1, False, "Value must be greater than or equal to 0"),        
          (1, True, None),
          (0,True, None)
    ]
    
    MAP_TOGGLES = [
        "Enable Offline Map",
        "Allow Look Forward",
        "kilometer Marker",
        "Merge Type"
    ]

class RbacData:
    SESSION_TIME_DATA = [
        ("0", False, "The Minimum value is greater than 1"),   
        ("1", True, None),                          
        ("1440", True, None),                          
        ("60", True, None),                        
        ("1441", False, "Value must be between 1 and 1440"),  
        ("-10", False, "The Minimum value is greater than 1"),  
    ]

    RBAC_TOGGLES = [
        "Session Time Out"
    ]
    
class LoggerData:
    RETENTION_TIME_DATA = [
        ("0", False, "The Minimum value is greater than 1"),   
        ("1", True, None),                          
        ("15", True, None),                          
        ("30", True, None),                        
        ("31", False, "Value must be between 1 and 30"),  
        ("-1", False, "The Minimum value is greater than 1"),  
    ]

    LOGGER_TOGGLES = [
        "logger status"
    ]

class JetsonDeviceData:
    REQUEST_TIMEOUT_DATA = [
        ("100", False, "Value must be at least 1000"),   
        ("999", False, "Value must be at least 1000"),   
        ("1000", True, None),                          
        ("60000", True, None),
        ("10000", True, None),                          
        ("60001", False, "Value must be between 1000 and 60000"),                        
        ("-1", False, "The Minimum value is greater than 1000")  
    ]

    RETRY_DELAY_DATA = [
        ("100", False, "Value must be at least 500"),   
        ("499", False, "Value must be at least 500"),   
        ("500", True, None),                          
        ("10000", True, None),
        ("1000", True, None),                          
        ("10001", False, "Value must be between 500 and 10000"),                        
        ("-1", False, "The Minimum value is greater than 500")  
    ]

    MAX_RETRY_ATTEMPTS_DATA = [
        ("0", False, "The Minimum value is greater than 1"),   
        ("1", True, None),   
        ("10", True, None),                          
        ("3", True, None),                          
        ("11", False, "Value must be between 1 and 10"),                        
        ("-1", False, "The Minimum value is greater than 1")  
    ]

class LogConfigData:
    TABS_TO_TEST = ["DAS", "DAQ", "Alarm", "Anomaly"]

class TempMonitoringData:
    FIELDS_TO_TEST = [
        "Chassis Sample Frequency",
        "Jetson Sample Frequency",
        "SBC Sample Frequency",
        "DAS Sample Frequency",
        "SBC Setpoint",
        "Jetson Setpoint",
        "DAS Setpoint",
        "Chassis Setpoint"
    ]