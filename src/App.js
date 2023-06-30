import './App.css';
import { useRef, useState } from 'react';
function App() {

  const [image, setimage] = useState(null)
  const fileInput = useRef(null)

  const handleImage = async() => {
    const file = fileInput.current.files[0] 

    const formData = new FormData()
    formData.append('image', file)

    try{
      const response = await fetch('http://localhost:8000/procesar_imagen',{
        method :'POST',
        body : formData, 
        headers : {
        }
      })
    if (response.ok) {
      const data = await response.json();
      console.log(data.message); // Imprime el mensaje recibido en la consola
    } else {
      console.log("Error");
    }
  } catch (error) {
    console.log(error);
  }
    setimage(URL.createObjectURL(file))
  }



  return (
    <div className="App">
      <h3>Proyecto 3</h3>
      <input type='file' ref={fileInput} /> 
      {image && (
        <div>
          <img src={image} alt='imagen-seleccionada'/>
          </div>
      )} 
      <button onClick={handleImage}>Enviar</button>
    </div>
  );
}

export default App;
