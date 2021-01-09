import Config from './config';

const mockUrl = 'http://mocked.url';
const mockPort = '123467';
const OLD_ENV = process.env;
{
  
    beforeEach(() => {
      jest.resetModules() // most important - it clears the cache
      process.env = { ...OLD_ENV }; // make a copy
    });

    const mockConfig = new Config({
        IMPOSC_URL: mockUrl,
        IMPOSC_PORT: mockPort
    });

    test('Correct config URL', () => {
        const url = mockConfig.plotterURL();

        const expected = expect.stringMatching(/^http:/);

        expect(url).toEqual(expected);
        expect(url).toEqual(expect.stringMatching(/:[0-9]*/));
        expect(url).toBe(mockUrl + ':' + mockPort);
    });

    test('Config value returns default', () => {
        const defaultValue = '999';

        const key = 'SILLY_KEY';

        const value = mockConfig.value(key, defaultValue);

        expect(value).toBe(defaultValue);
    });

    test('Config value returns JSON setting', () => {
        expect(mockConfig.value('IMPOSC_PORT')).toEqual(mockPort);
    });

    test('Config value overrides with environment variable', () => {
        process.env.REACT_APP_IMPOSC_PORT = '142857';

        expect(mockConfig.value('IMPOSC_PORT')).toEqual(process.env.REACT_APP_IMPOSC_PORT);
    });

    test('Config value overrides correctly with environment variables for docker-compose', () => {
        process.env.REACT_APP_IMPOSC_PORT = '';
        process.env.REACT_APP_IMPOSC_URL = 'service';

        expect(mockConfig.plotterURL()).toEqual(process.env.REACT_APP_IMPOSC_URL);
    });
}