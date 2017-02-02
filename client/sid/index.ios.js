'use strict';

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  TextInput,
  Button,
  AlertIOS
} from 'react-native';

export default class sid extends Component {

  constructor() {
    super();
    this.state = {
      email: '',
      password: ''
    }

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
     // now we push this state to our Flask API
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/student/login', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function() {

      if(xhr.readyState == 4) {
        try {
          var resp_obj = JSON.parse(xhr.response);
        } catch(e) {
          alert(e);
        }
        if (xhr.status == 200) {
          alert(xhr.response);
        } else {
          try {
            var error = resp_obj['error'];
          } catch(e) {
            alert(e);
          }
          alert(error);
        }
      }
    }
    xhr.send(JSON.stringify({'email': this.state.email, 'password': this.state.password}));
  }

  handleForgotPassword(text) {
     // now we push this state to our Flask API
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/student/login', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function() {

      if(xhr.readyState == 4) {
        try {
          var resp_obj = JSON.parse(xhr.response);
        } catch(e) {
          alert(e); // bad
        }
        if (xhr.status == 200) {
          // successful response

        } else {
          try {
            var error = resp_obj['error'];
          } catch(e) {
            alert(e);
          }
          alert(error); // bad
        }
      }
    }
    xhr.send(JSON.stringify({'email': this.state.email, 'password': this.state.password}));

  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>
          Student ID
        </Text>
        <View style={styles.instructions}>
        <Text>
        Please enter your email and password.
        </Text>
        <TextInput style={{height: 40}} placeholder="Email" autoCorrect={false} spellCheck={false}
        onChangeText={(email) => this.setState({'email':email})} />
        <TextInput style={{height: 40}} placeholder="Password" secureTextEntry={true} autoCorrect={false} spellCheck={false}
        onChangeText={(password) => this.setState({'password':password})}/>
        <Button title="Submit" onPress={this.handleSubmit} />
        <Button title="Forgot Password" onPress={() =>
            AlertIOS.prompt('Forgot Password', 'Please enter your email so that a password reset form may be sent.',
                (text) => handleForgotPassword(text), 'plain-text', '')
            }
        />
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    justifyContent: 'center',
    height: 250,
  },
  instructions: {
    justifyContent: 'center',
    height: 150,
  }
});

AppRegistry.registerComponent('sid', () => sid);
