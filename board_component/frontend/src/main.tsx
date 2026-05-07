import React from "react";
import ReactDOM from "react-dom/client";
import MyComponent from "./MyComponent";
import { withStreamlitConnection } from "streamlit-component-lib";

const Connected = withStreamlitConnection(MyComponent);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Connected />
  </React.StrictMode>
);