import './App.css';
import {PlotterApp} from './plotter'
import Config from './config';

/**
 * The application element
 */
function App() {
  const config = new Config();

  return (
    <div className="App">
      <header className="App-header">
        <h1>Impact Oscillator</h1>
        <small>(For background information click <a className="App-link" target="_blank" rel="noreferrer" href={config.infoURL()}>here</a>)</small>
      </header>
      <PlotterApp 
        url = {config.plotterURL()}
      />
    </div>
  );
}

export default App;
