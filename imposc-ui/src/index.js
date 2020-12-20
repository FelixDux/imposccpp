import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

var element = React.createElement('h1', { className: 'greeting' }, 'Hello, world!'); // <React.StrictMode><App /></React.StrictMode>;

ReactDOM.render(
  element,
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
