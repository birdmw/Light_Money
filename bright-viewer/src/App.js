import React, { Component } from 'react';
import './App.css';
import Header from "./components/Header.js";
import Profile from "./components/Profile.js";

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header />
        <Profile />
      </div>
    );
  }
}

export default App;
