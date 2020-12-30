import React from 'react';
import './plotter.css';
import PropTypes from 'prop-types'


/**
 * Form field for inputting an action argument to pass to the imposc service
 */
class PlotterInput extends React.Component {

    static propTypes = {
        /** The (numeric) type of the argument */
        type: PropTypes.string,
        /** Rule for the permitted range of values for a numeric argument */
        range: PropTypes.string,
        /** The argument name that will be passed to the imposc service */
        name: PropTypes.string,
        /** The name to be displayed on the form */
        label: PropTypes.string,
        /** A description to be shown as a tooltip */
        tooltip: PropTypes.string,
        /** A current value used to initialise the field */
        value: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
        /** Handler for a change in value */
        onChange: PropTypes.func
    }

    render() {
      const step = (this.props.type === 'integer' || this.props.type === 'uint') ? 1 : 0.01;
      let min = '';
      let max = '';
  
      // Interpret the range
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
              <div className="tooltip">{this.props.label}
              <span className="tooltiptext">{this.props.tooltip}</span></div>
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
  
  /**
   * An expandable set of related input fields
   */
  class PlotterInputGroup extends React.Component {

    static propTypes = {
        /** An array of dictionaries defining the properties of the constituent input fields */
        inputs: PropTypes.array,
        /** The name of the group */
        name: PropTypes.string,
        /** A dictionary of current values used to initialise each field */
        values: PropTypes.object,
        /** Handler for a change in value for each input - passed down the the input fields */
        onChange: PropTypes.func
    }

    constructor(props) {
      super(props);
  
      this.handleToggleClick = this.handleToggleClick.bind(this);
  
      this.state = {isOpen: true};
    }
  
    /** Handler for expanding/hiding the fields in the group */
    handleToggleClick() {
      this.setState( {isOpen: !this.state.isOpen});
    }
  
    render() {
      if (this.props.inputs.length > 0)  {
  
        // Generate the field elements to display (none if hidden)
        const inputs = this.state.isOpen ? this.props.inputs.map(
          (record) =>
            {
              return (
                <PlotterInput 
                  key = {record.name}
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
            <tbody>
            <tr>
              <th className = "inputGroup">{this.props.name} 
                <button type = "button" className = "toggle" onClick = {this.handleToggleClick}>
                  {this.state.isOpen ? "-" : "+"}
                </button>
              </th>
            </tr>
            <tr className = "inputGroup"><td className = "inputGroup" >
            <table className = "inputGroup" >
            <tbody>
            {inputs}
            </tbody>
            </table>
            </td></tr>
            </tbody>
          </table>
        )
      }
      else {
        return ( <table className = "inputGroup" ></table> )
      }
    }
  };
  
  /**
   * A form which accepts the arguments for a specified action, submits them to the imposc service and displays the returned image
   */
  class PlotterForm extends React.Component {

    static propTypes = {
        /** The address of the imposc service with the endpoint for the selected action */
        url: PropTypes.string,
        /** A dictionary of arrays of input specifications keyed by group name */
        groups: PropTypes.object
    }
    constructor(props) {
      super(props);
  
      this.state = {
          /** The returned image as a binary object */
          blob: null,
          /** An object url for displaying the image */
          src: "",
          /** Current values of all the action arguments */
          args: {},
          /** Alt text for the image - used to display error messages from the imposc service */
          result: ""
      };
  
      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.argsToSubmit = this.argsToSubmit.bind(this);
    }
  
    /**
     * Handler for changes to an input field - stores the value in state
     * @param {*} event 
     */
    handleInputChange(event) {    
      const target = event.target;
      const value = target.type === 'checkbox' ? target.checked : target.value;
      const name = target.name;
      let args = this.state.args;
      args[name] = value;
      this.setState({ args: args });
    }
  
    /** Marshals arguments to submit, applying default values where necessary */
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
  
    /**
     * Submits the form data as a JSON request to the imposc service and displays the result
     * @param {*} event 
     */
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

      // If no action has been selected, there will be no fields, so hide the submit button
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
  
  /**
   * Allows an available action to be selected in the navigation bar. Each action is an endpoint in the imposc service
   */
  class ActionSelector extends React.Component {

    static propTypes = {
        /** The action (service endpoint) */
        action: PropTypes.string,
        /** Flags whether this is the currently selected action */
        active: PropTypes.bool,
        /** Short description of the action - what gets displayed */
        label: PropTypes.string,
        /** Explanatory text, displayed as a tooltip */
        description: PropTypes.string,
        /** Handler for selecting the action */
        onClick: PropTypes.func
    }
    
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
  
  /** Wraps everything needed for selecting and action, inputting the arguments and displaying the result */
  class PlotterApp extends React.Component {

    static propTypes = {
        /** The address of the imposc service */
        url: PropTypes.string
    }

    constructor(props) {
      super(props);
  
      this.state = {
        action: "",
        actions: {},
      };
  
      this.populate();
  
      this.handleActionChange = this.handleActionChange.bind(this);
    };
  
    /** Retrieves and stores the action definitions from the imposc service */
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
  
    /** Captures the selected action and uses to ensure the form displays the correct fields */
    handleActionChange(event) {
      const target = event.target;
  
      const action = target.id;
  
      this.setState({action: action});
  
      event.preventDefault();
    }
  
    render() {
  
      const actionUrl = this.props.url + '/' + this.state.action;
      const actionGroups = (this.state.action in this.state.actions) ? this.state.actions[this.state.action]["groups"] : {};
  
      // Links for the navigation bar
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

  export {PlotterApp, PlotterInput, PlotterInputGroup, PlotterForm, ActionSelector};
  