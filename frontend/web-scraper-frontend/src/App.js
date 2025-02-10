import Button from '@mui/material/Button';
import React, { useState } from "react";
import Card from 'react-bootstrap/Card';
import axios from "axios";
import { TextField } from '@mui/material'
import './App.css';

function App() {
  const [ids, setIds] = useState([])
  const [posts, setPosts] = useState({})
  const [messages, setMessages] = useState([])
  const [keyword, setKeyword] = useState("")
  const [index, setIndex] = useState(0)
  const handleClick = async () => {
    console.log("click")
    try {
      if (!keyword) {
        alert("Enter a keyword!")
        return;
      }
      
      const response = await axios.get("http://127.0.0.1:5000/get_all_posts", {
        params: {keyword: keyword},
      })
      const data = response.data
      setPosts(data);
      setMessages(Object.values(data));
      setIds(Object.keys(data))
      alert("Post scraping successfull");
      console.log(posts);
      setIndex(0)
    }
    catch(error) {
      alert("Scraping not succesfull")
    }}

  const cardClick = () => {
    if (index < messages.length - 1) {
      setIndex(index + 1);
    }
  };
  const cardLast = () => {
    if (index > 0) {
      setIndex(index - 1);
    }
  };

  const saveToDb = async () => {
    try{
      const response = await axios.post("http://127.0.0.1:5000/add_to_db")
    }
    catch {
      console.log("Error")
    }
  }



  



  






  return (
    <div className="main">
      <div className="header1">
        <header>
          <h1>
            Ylis-scrape
          </h1>
        </header>
      </div>
      <div className="scrape_btn">
        <Button variant='contained' type="button" onClick={handleClick}>
          scrape posts containing your keyword
        </Button>
      </div>
      <div className="input">
        <TextField
          type="text"
          placeholder="Enter a keyword..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          />
      </div>
      <div className="Card_and_btn">
       
      
        <Card>
          <Card.Body>
            <Card.Title>{ids.length > 0 ? ids[index] : "No post Id to display"}</Card.Title>
            <Card.Text>{messages.length > 0 ? messages[index] : "No posts to display"}</Card.Text>
          </Card.Body>
        </Card>
        <Button variant='contained' type="button" onClick={cardClick}>
          Click for next post
        </Button>
        <Button variant='contained' type="button" onClick={cardLast}>
          Click for last post
        </Button>
      </div>
      <div className="db_btn">
        <Button variant='contained' type="button" onClick={saveToDb}>
          save posts
        </Button>
      </div>
    </div>
      
      
    
  );
}

export default App;
