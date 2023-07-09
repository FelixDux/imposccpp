import configData from "./config.json";

/**
 * Provides access to configuration settings from a JSON configuration file and/or environment variables
 */
class Config {
    /**
     * 
     * @param {*} data A dictionary of settings loaded from a JSON file
     */
    constructor(data = configData) {
        this.data = data;
    };

    /**
     * Returns a named setting
     * 
     * @public
     * 
     * @param {string} key The name of the setting to retrieve
     * @param {string} defaultValue The value to use of there is no setting in either the JSON or an environment variable
     */
    value(key, defaultValue='') {
        let result = defaultValue;
    
        // Try to retrieve from config file
        if (key in this.data) {
            result = this.data[key];
        }
    
        // Override from environment variable
        const envKey = "REACT_APP_" + key;
        if (envKey in process.env && process.env[envKey] !== '') {
            result = process.env[envKey];
        }
    
        return result;
    }
    
    /**
     * Returns an address for the imposc service from the url and port number in the settings
     * 
     * @public
     */
    plotterURL() {
        if (this.value('IMPOSC_PORT') === '') {
            return  this.value('IMPOSC_URL');
        }
        else {
            return this.value('IMPOSC_URL') + ':' + this.value('IMPOSC_PORT');
        }
        
    }

    /**
     * @returns the URL for a page with background info about what the app does
     * 
     * @public
     */
    infoURL() {
        return this.value('MORE_INFO_LINK');
    }

    env() {
        return Object.entries(process.env).map(
            ([key, value]) => {
                return (
                    <p>{key+"='"+value+"'"}</p>
                );
            }
        );
    }
};

export default Config