import React, { useEffect, useState } from 'react';

function App() {
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    fetch('/posts')
      .then(res => res.json())
      .then(setPosts);
  }, []);

  return (
    <div>
      <h1>Uni-One</h1>
      <ul>
        {posts.map(p => (
          <li key={p.id}>{p.content} - {p.author}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
