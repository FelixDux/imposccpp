import configData from "./config.json";

class Config {
    constructor(data = configData) {
        this.data = data;
    };

    value(key, defaultValue='') {
        let result = defaultValue;
    
        // Try to retrieve from config file
        if (key in this.data) {
            result = this.data[key];
        }
    
        // Override from environment variable
        const envKey = "REACT_APP_" + key;
        if (envKey in process.env) {
            result = process.env[envKey];
        }
    
        return result;
    }
    
    plotterURL() {
        return this.value('IMPOSC_URL') + ':' + this.value('IMPOSC_PORT');
    }
};

export default Config