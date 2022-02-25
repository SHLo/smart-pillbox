import logo from "./logo.svg";
import "./App.css";
import User from "./User.js";
import "bootstrap/dist/css/bootstrap.min.css";
import { getUsers } from "./db.js";
import { useState, useEffect } from "react";

function App() {
  const [topUser, setTopUser] = useState({});
  const [bottomUser, setBottomUser] = useState({});

  useEffect(() => {
    async function init() {
      const users = await getUsers();
      // console.log(users);
      setTopUser(users.top);
      setBottomUser(users.bottom);
    }
    init();
  }, []);

  return (
    <>
      <User user={topUser} />
      <User user={bottomUser} />
    </>
  );
}

export default App;
