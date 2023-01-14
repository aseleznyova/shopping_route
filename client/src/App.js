import './App.css';
import {useEffect, useState} from "react";
function App() {
  const [msg, msgState] = useState('[]')
  useEffect(()=>{
    fetch('/api').then(response=>response.json())
        .then((json) => {
        msgState(json.msg)
    })
  },[]);
  return (
    <div className="App">
      
      {msg}
    </div>
  );
}
  
export default App;
