import './App.css';
import PlotterApp from './plotter'
import Config from './config';

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

// TODO: proper passing-through of error messages
// TODO: don't forget unit tests, docstrings, comments
// TODO: tidy up plotting legends etc
// TODO: move to using react-router for navigation
// TODO: add page on mathematical background
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
