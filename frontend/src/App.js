import * as React from "react";
import ReactDOM from "react-dom";
import logo from "./logo.svg";
import "./App.css";
import axios from "axios";
import TextField from "@mui/material/TextField";
import { Button } from "@mui/material";

function App() {
  const [inputValue, setInputValue] = React.useState("");
  const [results, setResults] = React.useState([]);
  const [error, setError] = React.useState({ status: false, content: "" });
  const queryWord = (word) => {
    axios.get(`http://127.0.0.1:9000/query/${word}`).then((res) => {
      console.log(res.data);
      setError({ status: false, content: "" });
      if (res.data[0].response === "error") {
        setError({ status: true, content: res.data[0].body });
      } else {
        setResults(res.data);
      }
    });
  };
  const handleChange = (e) => {
    setInputValue(e.target.value);
  };
  return (
    <div className="App">
      <div className="container">
        <div className="search-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1>Word_Searcher</h1>
        </div>
        <TextField
          id="demo-helper-text-misaligned-no-helper"
          label="Search Word"
          onChange={handleChange}
          fullWidth
        />
        <Button variant="contained" onClick={() => queryWord(inputValue)}>
          Search
        </Button>
      </div>
      <div className="results-container">
        {error.status ? (
          <div>{error.content}</div>
        ) : (
          results.map((result, index) => (
            <div>
              <a
                key={`results-${index}`}
                href={`https://storage.cloud.google.com/web-searcher-dump/${result.response}.txt`}
              >
                {result.response}
              </a>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
