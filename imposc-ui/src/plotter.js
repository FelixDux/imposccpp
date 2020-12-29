import React from 'react';
import './plotter.css';

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
        default : {
          min = '';
          max = '';
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
              value={this.props.value}
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
      if (this.props.inputs.length > 0)  {
  
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
          ) : [];
          
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
      else {
        return ( <table className = "inputGroup" ></table> )
      }
    }
  };
  
  class PlotterForm extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        blob: null,
        src: "",
        args: {},
      };
  
      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.argsToSubmit = this.argsToSubmit.bind(this);
    }
  
    handleInputChange(event) {    
      const target = event.target;
      const value = target.type === 'checkbox' ? target.checked : target.value;
      const name = target.name;
      let args = this.state.args;
      args[name] = value;
      this.setState({ args: args });
    }
  
    argsToSubmit () {
      var groups = Object.values(this.props.groups);
  
      var records = groups.flat();
      
      var args = records.reduce(
        function (r, record) {
          return Object.assign(r, {
            [record.name]: !(record.name in r) || r[record.name] === null ? record.defaultValue : r[record.name]
          });
        }, 
        this.state.args
      );
  
      return args;
    }
  
    updateFields() {
  
      for (var name in this.state.args) {
        document.getElementById(name).setAttribute('value', this.state.args[name]);
      }
    }
  
    handleSubmit(event) {
      const args = this.argsToSubmit();
  
      fetch(this.props.url,
        {
          method: 'POST',
          headers: {
              Accept: 'application/json',
                      'Content-Type': 'application/json',
          },
          body: JSON.stringify(args)
        })
      .then(response => {
        if (!response.ok) {
            response.json().then((json) => {                    
                if ('error' in json) {
                    this.setState({result: json['error']});
                }
                else {
                    this.setState({result: 'Unknown error'});
                }
            });
        }
        return response.blob();
      })
      .then(blob => {
          if (blob) {
              this.setState( {blob: blob, src: URL.createObjectURL(blob), result: "Done"});
          }
      })
      .catch((error) => {
        console.error('Fetch operation failed:', error);
        this.setState({result: error.toString()});
      });
      event.preventDefault();
    }
  
    render() {
      
      const groups = Object.entries(this.props.groups).map(([groupName,group]) => {
        const values = Object.assign({}, ...group.map((record) => ({
          [record.name]: this.state.args[record.name] == null ? record.defaultValue : this.state.args[record.name]
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

      const submitType = groups.length > 0 ? "submit" : "hidden"
  
      return (
        <div className="row">
          <div className="column left"><p /></div>
          <div className="column">
        <form onSubmit={this.handleSubmit}>
          {groups}
        <input type={submitType} value="Show" />
        </form></div>      
        <div className="column right" ><img src={this.state.src} alt={this.state.result} width="80%" align="center" /></div>
        </div>
      )
    }
  };
  
  class ActionSelector extends React.Component {
    constructor(props) {
      super(props);
      const activeClass = this.props.active ? 'active' : '';
  
      this.state = {
        activeClass: activeClass
      };
    }
  
    render() {
      return (
        <div class="tooltip">
        <a id={this.props.action} href={'#'+this.props.action} class={this.state.activeClass} onClick={this.props.onClick}>{this.props.label}</a>
        <span class="tooltiptext">{this.props.description}</span>
        </div>
      )
    }
  }
  
  class PlotterApp extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        action: "",
        actions: {},
      };
  
      this.populate();
  
      this.handleActionChange = this.handleActionChange.bind(this);
    };
  
    populate() {
  
      fetch(this.props.url)
      .then(response => {
        if (!response.ok) {
            response.json().then((json) => {                    
                if ('error' in json) {
                    this.setState({result: json['error']});
                }
                else {
                    this.setState({result: 'Unknown error'});
                }
            });
        }
        return response.json();
      })
      .then(actions => {
        this.setState( {actions: actions});
      })
      .catch(error => {
        console.error('Fetch operation failed:', error);
      });
    };
  
    handleActionChange(event) {
      const target = event.target;
  
      const action = target.id;
  
      this.setState({action: action});
  
      event.preventDefault();
    }
  
    render() {
  
      const actionUrl = this.props.url + '/' + this.state.action;
      const actionGroups = (this.state.action in this.state.actions) ? this.state.actions[this.state.action]["groups"] : {};
  
      const actionLinks = Object.entries(this.state.actions).map(
        ([actionName, actionInfo]) => {
          return (
            <ActionSelector 
            action={actionName}
            active={this.state.action == actionName}
            description={actionInfo.description}
            label={actionInfo.label}
            onClick={this.handleActionChange}
            />
          );
        }
      );
  
      return (
        <div>
          <div className="topnav">
            {actionLinks}
          </div>
          <PlotterForm
          url={actionUrl}
          groups={actionGroups}
          />
        </div>
      );
    }
  };

  export default PlotterApp;
  