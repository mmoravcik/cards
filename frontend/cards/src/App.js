import React, { Component } from 'react';
import './App.css';
import InputForm from "./components/InputForm";

class App extends Component {
  render() {
    return (
      <div className="App">
        <h1>Cards</h1>
        <InputForm />


      </div>
    );
  }
}

export default App;