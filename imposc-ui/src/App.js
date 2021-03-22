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
      </header>
      <PlotterApp 
        url = {config.plotterURL()}
      />
    </div>
  );
}

export default App;
