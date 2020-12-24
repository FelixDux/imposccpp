import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class PlotterInput extends React.Component {
  constructor(props) {
    super(props);
  };

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
      // <label>
        <tr>
        <td className = "inputGroup" >{this.props.label}</td>
        <td className = "inputGroup" ><input 
          name={this.props.name}
          type="number"
          value={this.props.value}
          onChange={this.props.onChange}
          step = {step}
          min = {min}
          max = {max}
        /></td></tr>
      // </label>
    )
  }
};

class PlotterInputGroup extends React.Component {
  constructor(props) {
    super(props);
  };

  render() {
    const inputs = this.props.inputs.map(
      (record) =>
      {
        return (
          <PlotterInput 
            name = {record.name}
            label = {record.label}
            value = {record.value}
            range = {record.range}
            type = {record.type}
            onChange={this.props.onChange}
          />
        );
      }
    )

    return (
      <table className = "inputGroup" >
        <tr className = "inputGroup" >
          <th className = "inputGroup" span="2">{this.props.groupName}</th>
          {inputs}
        </tr>
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
    
    const groups = Object.entries(this.props.groups).map(([groupName,group]) => {
      return (
        <PlotterInputGroup 
          name = {groupName}
          inputs = {group}
          onChange={this.handleInputChange}
        />
      );
    });

    return (
      <div>
        <table className = "spaLayout" >
          <tr>
          <td className = "spaInputs" >
      <form onSubmit={this.handleSubmit}>
        {groups}
      <input type="submit" value="Update" />
      </form>
      </td>
      <td className = "spaImage" >
      <div align="center" ><img src={this.state.src} alt="" width="90%" align="center" /></div>
      </td>
      </tr>
      </table>
      </div>
    )
  }
};

const groups = {
  Parameters : [
    {name: 'omega', label: 'Forcing frequency', value: 5.2, range: 'positive', type: 'float'},
    {name: 'sigma', label: 'Obstacle offset', value: 0, range: '', type: 'float'},
    {name: 'r', label: 'Coefficient of restitution', value: 0.8, range: 'non-negative', type: 'float'}
  ],
  Initial : [
    {name: 'phi', label: 'Phase', value: 0.5, range: 'circle', type: 'float'},
    {name: 'v', label: 'Velocity', value: 0, range: 'non-negative', type: 'float'}
  ],
  Options : [
    {name: 'max_periods', label: 'Max forcing periods between impacts', value: 100, range: 'positive', type: 'integer'},
    {name: 'num_impacts', label: 'Number of impacts to plot', value: 1000, range: 'positive', type: 'integer'}
  ]
};

var element = <React.StrictMode><App /></React.StrictMode>;

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
// TODO: Construct form element from actions JSON
// TODO: make imposc service address and port number configurable
// TODO: don't forget unit tests, docstrings, comments
// TODO: Dockerise
// TODO: Orchestrate with K8s?
// TODO: Pull Elixir project into same structure
// TODO: create alternate imposc services in Rust, Golang, Haskell, Java
