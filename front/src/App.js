import './App.css';
import { useRef, useState } from 'react';

function App() {
  const [image, setimage] = useState(null);
  const fileInput = useRef(null);
  const inputRef = useRef(null);
  const [tablas, setTablas] = useState([]); // Estado para almacenar las tablas generadas
  const Tabla = ({ datos }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Imagen</th>
          <th>Distancia</th>
        </tr>
      </thead>
      <tbody>
        {datos.map((tupla) => (
          <tr key={tupla[0]}>
            <td>{tupla[0]}</td>
            <td>{tupla[1]}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

  const handleImage = async () => {
    const file = fileInput.current.files[0];
    const k = inputRef.current.value || '1';

    const formData = new FormData();
    formData.append('image', file);
    formData.append('k',k);

    try {
      const response = await fetch('http://localhost:8000/sequential', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const {responseData : data} = await response.json();
        const nuevasTablas = data.map((lista) => (
          <Tabla key={lista[0][0]} datos={lista} />
        ));
        setTablas(nuevasTablas);
        /*
        data.forEach(element => {
          element.forEach(tupla =>{
            console.log(tupla);
          });
        });
        */
       
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
      <div className='input-div'>
      <input type="file" ref={fileInput} />
      <input type="text" placeholder="K" ref={inputRef} />
      </div>
      <button onClick={handleImage}>Enviar</button>
      {image && (
        <div>
          <img src={image} alt="imagen-seleccionada" />
        </div>
      )}
      {tablas.length > 0 && tablas}

    </div>
  );
}

export default App;
