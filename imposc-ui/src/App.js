import './App.css';
import PlotterApp from './plotter'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Impact Oscillator</h1>
      </header>
      <body>
      <PlotterApp 
        url = 'http://127.0.0.1:5000'
      />
      </body>
    </div>
  );
}

export default App;

// TODO: make imposc service address and port number configurable
// TODO: proper passing-through of error messages
// TODO: don't forget unit tests, docstrings, comments
// TODO: tidy up plotting legends etc
// TODO: move to using react-router for navigation
// TODO: add page on mathematical background
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
