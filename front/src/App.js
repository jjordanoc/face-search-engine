import './App.css';
import { useRef, useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import normalize from 'normalize-path';

function App() {
  const [image, setimage] = useState(null);
  const fileInput = useRef(null);
  const inputRef = useRef(null);
  const [tabla_secuencial, setTabla_secuencial] = useState([]); // Estado para almacenar las tablas generadas
  const [tabla_rtree, setTabla_rtree] = useState([]); // Estado para almacenar las tablas generadas
  const [tabla_highD, setTabla_highD] = useState([]); // Estado para almacenar las tablas generadas
  const [time_secuential, settime_secuential] = useState(0)
  const [time_rtree, settime_rtree] = useState(0)
  const [time_highD, settime_highD] = useState(0)
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
          <tr key={uuidv4()}>
            <td>{<img src={require("./" + normalize(tupla[0]))} alt={uuidv4()} key={uuidv4()} id={uuidv4()}/>}</td>
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
    formData.append('file', file);
    formData.append('k',k);
    setimage(URL.createObjectURL(file));

    try {
      const start_time = Date.now();
      const response = await fetch('http://localhost:8000/sequential', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const end_secuential_time = Date.now();
        settime_secuential(end_secuential_time-start_time);
        const {result: data} = await response.json();
        const arr = JSON.parse(data);
        const tabla_secuencial = arr.map((lista) => (
          <Tabla key={uuidv4()} datos={lista} />
        ));
        setTabla_secuencial(tabla_secuencial);       
      } else {
        console.log('Error Secuencial');
      }
    } catch (error) {
      console.log(error);
    }

    try {
      const start_time = Date.now();
      const response = await fetch('http://localhost:8000/rtree', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const end_rtree_time= Date.now();
        settime_rtree(end_rtree_time-start_time);
        const {result: data} = await response.json();
        const arr = JSON.parse(data);
        const tabla_secuencial = arr.map((lista) => (
          <Tabla key={uuidv4()} datos={lista} />
        ));
        setTabla_rtree(tabla_secuencial);       
      } else {
        console.log('Error RTree');
      }
    } catch (error) {
      console.log(error);
    }

    try {
      const start_time = Date.now();
      const response = await fetch('http://localhost:8000/highd', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const end_highD_time= Date.now();
        settime_highD(end_highD_time-start_time);
        const {result: data} = await response.json();
        const arr = JSON.parse(data);
        const tabla_secuencial = arr.map((lista) => (
          <Tabla key={uuidv4()} datos={lista} />
        ));
        setTabla_highD(tabla_secuencial);       
      } else {
        console.log('Error HighD');
      }
    } catch (error) {
      console.log(error);
    }

  };

  return (
    <div className="App">
      <h3>Proyecto 3</h3>
      <div className='input-div'>
      <input type="file" ref={fileInput} id='file'/>
      <input type="text" placeholder="K" ref={inputRef} />
      </div>
      <button onClick={handleImage}>Enviar</button>
      {image && (
        <div>
          <p>Imagen Escaneada:</p>
          <img src={image} alt="imagen-seleccionada" />
        </div>
      )}
      <section className='resultados'>
        <div className='secuential'>
          {tabla_secuencial.length > 0 && <h4>KNN Secuencial</h4>}
        {tabla_secuencial.length > 0 && tabla_secuencial}
        {time_secuential > 0 && <p>Tiempo Secuencial: {time_secuential} ms</p>}
        </div>
        <div className='rtree'>
          {tabla_rtree.length > 0 && <h4>KNN RTree</h4>}
        {tabla_rtree.length > 0 && tabla_rtree}
        {time_rtree> 0 && <p>Tiempo Rtree: {time_rtree} ms</p>}
        </div>
        <div className='highD'>
        {tabla_highD.length > 0 && <h4>KNN HighD</h4>} 
        {tabla_highD.length > 0 && tabla_highD}
        {time_highD> 0 && <p>Tiempo HighD: {time_highD} ms</p>}
        </div>
      </section>
    </div>
  );
}

export default App;
