import { useState } from "react";

function LoginForm({ onLogin }) {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(credentials);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username</label>
        <input
          type="text"
          value={credentials.username}
          onChange={(e) =>
            setCredentials({ ...credentials, username: e.target.value })
          }
        />
      </div>
      <div>
        <label>Password</label>
        <input
          type="password"
          value={credentials.password}
          onChange={(e) =>
            setCredentials({ ...credentials, password: e.target.value })
          }
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginForm;
