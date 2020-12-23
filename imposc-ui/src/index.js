import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class PlotterInput extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const step = this.props.type === 'integer' ? 1 : 0.01;
    let min = '';
    let max = '';

    switch (this.props.range)
    {
      case 'non-negative': {
        min = 0;
        break;
      }
      case 'negative': {
        max = -step;
        break;
      }
      case 'non-positive': {
        max = 0;
        break;
      }
      case 'positive': {
        min = step;
        break;
      }
      case 'circle' : {
        min = 0;
        max = 1;
        break;
      }
    }

    return (
      <label>
        {this.props.label}: <input 
          name={this.props.name}
          type="number"
          value={this.props.value}
          onChange={this.props.onChange}
          step = {step}
          min = {min}
          max = {max}
        />
      </label>
    )
  }
}

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
        throw new Error('Network response failed');
      }
      return response.blob();
    })
    .then(blob => {
      this.setState( {blob: blob, src: URL.createObjectURL(blob), result: "Done"});
    })
    .catch(error => {
      console.error('Fetch operation failed:', error);
      this.setState({result: error.toString()});
    });
    event.preventDefault();
  }

  renderInput(name, label, value, range, type)
  {
    return (
      <PlotterInput 
        name = {name}
        label = {label}
        value = {value}
        range = {range}
        type = {type}
        onChange={this.handleInputChange}
      />
    )
  }

  render() {
    return (
      <div>
      <form onSubmit={this.handleSubmit}>
      {this.renderInput('omega', 'Forcing frequency', this.state.args.omega, 'positive')}
      {this.renderInput('sigma', 'Obstacle offset', this.state.args.sigma)}
      {this.renderInput('r', 'Coefficient of restitution', this.state.args.r, 'non-negative')}
      {this.renderInput('phi', 'Initial phase', this.state.args.phi, 'circle')}
      {this.renderInput('v', 'Initial velocity', this.state.args.v, 'non-negative')}
      {this.renderInput('max_periods', 'Max forcing periods between impacts', this.state.args.max_periods, 'positive', 'integer')}
      {this.renderInput('num_impacts', 'Number of impacts to plot', this.state.args.num_impacts, 'positive', 'integer')}
      <input type="submit" value="Update" />
      </form>
      <div align="center" ><img src={this.state.src} alt="" width="50%" align="center" /></div>
      </div>
    )
  }

};

ReactDOM.render(
  <PlotterForm 
  url = 'http://127.0.0.1:5000/impacts'
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

// TODO: Make imposc service self-documenting via JSON (actions, descriptions, variable lists, with descriptions - try to follow same structure as Elixir project)
// TODO: Construct form element from actions JSON
// TODO: arrange SPA with form and display elements
// TODO: make imposc service address and port number configurable
// TODO: don't forget unit tests, docstrings, comments
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
