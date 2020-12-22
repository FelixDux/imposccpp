import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

function Plot(props) {
  return (
    <img src={props.url} />
  );
}

class Plotter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      blob: null,
      src: "",
      result: "Waiting"
    };
  }

  handleButtonClick = () => {
    fetch(this.props.url,
      {
        method: 'POST',
        headers: {
            Accept: 'application/json',
                    'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.props.args)
      })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.blob();
    })
    .then(blob => {
      this.setState( {blob: blob, src: URL.createObjectURL(blob), result: "Done"});
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
      this.setState({result: error.toString()});
    });
  };

  render() {
    return (
      <div><div><h1>{this.state.result}</h1><button onClick={this.handleButtonClick}>Update</button></div><div><img src={this.state.src} alt="" /></div></div>
    );
  }
};

var element = React.createElement('h1', { className: 'greeting' }, 'Impact Oscillator'); // <React.StrictMode><App /></React.StrictMode>;

ReactDOM.render(
  // element,
  <Plotter
  url = 'http://127.0.0.1:5000/impacts'
  args = {{
    omega: 5.2, sigma: 0.0, r: 0.8, phi: 0.2, v: 0.01, max_periods: 100, num_impacts: 5000,
  }}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

// TODO: comms to imposc service
// TODO: display imposc response
// TODO: form element to send imposc request
// TODO: arrange SPA with form and display elements
// TODO: make imposc service address and port number configurable
// TODO: Make imposc service self-documenting via JSON (actions, descriptions, variable lists, with descriptions - try to follow same structure as Elixir project)
// TODO: Construct form element from actions JSON
// TODO: don't forget unit tests, docstrings, comments
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
