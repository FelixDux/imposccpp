import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class PlotterForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      blob: null,
      src: "",
      args: {omega: 5.2, sigma: 0.0, r: 0.8, phi: 0.2, v: 0.01, max_periods: 100, num_impacts: 5000}
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {    
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    let args = this.state.args
    args[name] = value;
    this.setState({ args: args });
  }

  handleSubmit(event) {
    fetch(this.props.url,
      {
        method: 'POST',
        headers: {
            Accept: 'application/json',
                    'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.state.args)
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
    event.preventDefault();
  }

  render() {
    return (
      <div>
      <form onSubmit={this.handleSubmit}>
      <label>Omega: <input 
        name="omega"
        type="number"
        value={this.state.args.omega}
        onChange={this.handleInputChange} />
      </label>
      <label>Sigma: <input 
        name="sigma"
        type="number"
        value={this.state.args.sigma}
        onChange={this.handleInputChange}
        />
      </label>
      <label>r: <input 
        name="r"
        type="number"
        value={this.state.args.r}
        onChange={this.handleInputChange}
        />
      </label>
      <label>phi: <input 
        name="phi"
        type="number"
        value={this.state.args.phi}
        onChange={this.handleInputChange}
        />
      </label>
      <label>v: <input 
        name="v"
        type="number"
        value={this.state.args.v}
        onChange={this.handleInputChange}
        />
      </label>
      <label>max_periods: <input 
        name="max_periods"
        type="number"
        value={this.state.args.max_periods}
        onChange={this.handleInputChange}
        />
      </label>
      <label>num_impacts: <input 
        name="num_impacts"
        type="number"
        value={this.state.args.num_impacts}
        onChange={this.handleInputChange}
        />
      </label>
      <input type="submit" value="Update" />
      </form>
      <div><img src={this.state.src} alt="" /></div>
      </div>
    )
  }

};

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

ReactDOM.render(
  <PlotterForm 
  url = 'http://127.0.0.1:5000/impacts'
  // args = {{
  //   omega: 5.2, sigma: 0.0, r: 0.8, phi: 0.2, v: 0.01, max_periods: 100, num_impacts: 5000,
  // }}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

// TODO: arrange SPA with form and display elements
// TODO: make imposc service address and port number configurable
// TODO: Make imposc service self-documenting via JSON (actions, descriptions, variable lists, with descriptions - try to follow same structure as Elixir project)
// TODO: Construct form element from actions JSON
// TODO: don't forget unit tests, docstrings, comments
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
