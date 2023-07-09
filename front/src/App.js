import './App.css';
import { useRef, useState } from 'react';

function App() {
  const [image, setimage] = useState(null);
  const fileInput = useRef(null);
  const inputRef = useRef(null);

  const handleImage = async () => {
    const file = fileInput.current.files[0];
    const k = inputRef.current.value || '1';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('k',k);

    try {
      const response = await fetch('http://localhost:8000/sequential', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log(responseData.message); // Imprime el mensaje recibido en la consola
      } else {
        console.log('Error');
      }
    } catch (error) {
      console.log(error);
    }

    setimage(URL.createObjectURL(file));
  };

  return (
    <div className="App">
      <h3>Proyecto 3</h3>
      <input type="file" ref={fileInput} />
      <input type="text" placeholder="K" ref={inputRef} />
      <button onClick={handleImage}>Enviar</button>
      {image && (
        <div>
          <img src={image} alt="imagen-seleccionada" />
        </div>
      )}
    </div>
  );
}

export default App;
