import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class PlotterInput extends React.Component {

  render() {
    const step = (this.props.type === 'integer' || this.props.type === 'uint') ? 1 : 0.01;
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
        <tr>
          <td className = "inputGroup" width="10%"></td>
          <td className = "inputGroup" >
            <div class="tooltip">{this.props.label}
            <span class="tooltiptext">{this.props.tooltip}</span></div>
            </td>
          <td className = "inputGroup" >
            <input 
            id={this.props.name}
            name={this.props.name}
            type="number"
            defaultValue={this.props.value}
            onChange={this.props.onChange}
            step = {step}
            min = {min}
            max = {max}
          />
          </td>
        </tr>
    )
  }
};

class PlotterInputGroup extends React.Component {
  constructor(props) {
    super(props);

    this.handleToggleClick = this.handleToggleClick.bind(this);

    this.state = {isOpen: true};
  }

  handleToggleClick() {
    this.setState( {isOpen: !this.state.isOpen});
  }

  render() {
    const inputs = this.state.isOpen ? this.props.inputs.map(
      (record) =>
      {
        return (
          <PlotterInput 
            name = {record.name}
            label = {record.label}
            tooltip = {record.description}
            value = {this.props.values[record.name]}
            range = {record.range}
            type = {record.type}
            onChange={this.props.onChange}
          />
        );
      }
    ) : null;

    return (
      <table className = "inputGroup" >
        <tr>
          <th className = "inputGroup">{this.props.name} 
            <button type = "button" className = "toggle" onClick = {this.handleToggleClick}>
              {this.state.isOpen ? "-" : "+"}
            </button>
          </th>
        </tr>
        <tr className = "inputGroup"><td className = "inputGroup" >
        <table className = "inputGroup" >
        {inputs}
        </table>
        </td></tr>
      </table>
    )
  }
};

class PlotterForm extends React.Component {
  constructor(props) {
    super(props);
    
    let args = {};
    Object.entries(props.groups).forEach(([groupName,group]) => {
      for (let record of group) {
        args[record.name] = record.value;
      }
    });

    this.state = {
      blob: null,
      src: "",
      args: args,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {    
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    let args = this.state.args;
    args[name] = value;
    this.setState({ args: args });
    
    // this.updateFields();
  }

  updateFields() {

    for (var name of this.state.args) {
      document.getElementById(name).setAttribute('value', this.state.args[name]);
    }
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

  render() {
    
    const groups = Object.entries(this.props.groups).map(([groupName,group]) => {
      const values = Object.assign({}, ...group.map((record) => ({
        [record.name]: this.state.args[record.name]
      })));
      return (
        <PlotterInputGroup 
          name = {groupName}
          inputs = {group}
          values = {values}
          onChange={this.handleInputChange}
        />
      );
    });

    return (
      <div className="row">
        <div className="column left"><p /></div>
        <div className="column">
      <form onSubmit={this.handleSubmit}>
        {groups}
      <input type="submit" value="Show" />
      </form></div>      
      <div className="column right" ><img src={this.state.src} alt="" width="90%" align="center" /></div>
      </div>
    )
  }
};

const groups = {
  Parameters : [
    {name: 'omega', description: 'Forcing frequency', value: 5.2, range: 'positive', type: 'float', label: 'ω'},
    {name: 'sigma', description: 'Obstacle offset', value: 0, range: '', type: 'float', label: 'σ'},
    {name: 'r', description: 'Coefficient of restitution', value: 0.8, range: 'non-negative', type: 'float', label: 'r'}
  ],
  Initial : [
    {name: 'phi', description: 'Phase (modulo 1)', value: 0.5, range: 'circle', type: 'float', label: 'φ'},
    {name: 'v', description: 'Velocity', value: 0, range: 'non-negative', type: 'float', label: 'v'}
  ],
  Options : [
    {name: 'max_periods', description: 'Max forcing periods between impacts', value: 100, range: 'positive', type: 'integer', label: 'P'},
    {name: 'num_impacts', description: 'Number of impacts to plot', value: 1000, range: 'positive', type: 'integer', label: 'N'}
  ]
};

// var element = <React.StrictMode><App /></React.StrictMode>;

ReactDOM.render(
  <PlotterForm 
    url = 'http://127.0.0.1:5000/impacts'
    groups = {groups}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

// TODO: Make imposc service self-documenting via JSON (actions, descriptions, variable lists, with descriptions - try to follow same structure as Elixir project)
// TODO: Include navigation bar for plot types
// TODO: Construct form element from actions JSON
// TODO: make imposc service address and port number configurable
// TODO: don't forget unit tests, docstrings, comments
// TODO: tidy up plotting legends etc
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
