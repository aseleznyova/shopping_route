import './App.css';
import './index.css'
import { useEffect, useState, useRef} from "react";
import DataInputComponent from "./components/DataInputComponent";
import ResultComponent from "./components/ResultComponent";
import {useDispatch, useSelector} from "react-redux";
//import {result} from "./redux/actions/resultState.action";
import { YMaps, Map,Placemark} from '@pbe/react-yandex-maps';
import {api_key} from './conf'
function App() {
    const [dataProducts, dataProductsSet] = useState(null)
    const map = useRef(null);
    const shoppingCart = useSelector(state => state.shoppingCartReducer.shoppingCart)
    const resState = useSelector(state=>state.resultStateReducer.resultState)
    //const dispatch = useDispatch()
    const [resultProducts, resultProductsSet] = useState(null)
    let points = null;
    const ymaps = useRef(null)
    let geoObj = null;
    let multiRoute = null;
    useEffect(()=>{
        console.log(api_key)
      dataProductsSet([{
               "name" : "молоко",
               "id" : 1
          },
          {
              "name" : "пиво",
              "id" : 2
          },
          {
              "name" : "шоколад",
              "id" : 3
          },
          {
              "name" : "печенье",
              "id" : 4
          },
          {
              "name" : "пельмени",
              "id" : 5
          },
          {
              "name" : "бульмени",
              "id" : 6
          },
          {
              "name" : "сникерс",
              "id" : 7
          },
          {
              "name" : "хлеб",
              "id" : 8
          },
          {
              "name" : "хлопья",
              "id" : 9
          },
          {
              "name" : "йогурт",
              "id" : 10
          },
          {
              "name" : "кола",
              "id" : 11
          },
          {
              "name" : "шоколад",
              "id" : 12
          },
      ])
        resultProductsSet({
            cart : [{
                name : "Колбаски Grizzly, сырокопчёные, Ремит, 40 г",
                address : "Ленинградская ул., 10",
                count : "2",
                price: "59.99",
            },],
            sumPrice: 119.98,
            time: 22,
        })

  },[])
    const addObserverClick = (ym) => {
        ymaps.current = ym;

        map.current.events.add('click', (ev)=>{
            points = ev.get('coords');
            if(geoObj){
                map.current.geoObjects.remove(geoObj)
            }
            geoObj = new ym.Placemark(points, {}, {
                preset: "islands#circleDotIcon",
                iconColor: '#ff0000'
            });
            map.current.geoObjects.add(geoObj);
        })
    }
    const mapState =  { center: [59.904883, 30.513427], zoom: 1 ,
        controls: ["zoomControl"]};
    const RESTRICT_AREA = [
        [59.921955, 30.498686],
        [59.890619, 30.528230],

    ];

    const addRoute = () => {
        const pointA = [59.907659, 30.508591];
        const pointB = [59.908500, 30.521122];

        multiRoute = new ymaps.current.multiRouter.MultiRoute(
            {
                referencePoints: [pointA, pointB , [59.910202, 30.515672]],
                params: {
                    routingMode: "pedestrian"
                }
            },
            {
                boundsAutoApply: true
            }
        );
        map.current.geoObjects.add(multiRoute);

    };
    const deleteRoute = ()=>{
        map.current.geoObjects.removeAll();
    }
    function getCurState(){
        if(resState){
            return <ResultComponent resultData={resultProducts} deleteRoute={deleteRoute}/>
        }
        return <DataInputComponent dataProducts={dataProducts} addRoute={addRoute}/>
    }
  return (
    <div className="App">
        <div>
            <div className="right">
                {
                    getCurState()
                }
            </div>
            <div align="center">
                <div className="table">
                    <div className="row">
                        <div className="cell">
                            <YMaps  query={{apikey: api_key,
                                ns: "use-load-option",
                                load: "Map,Placemark,control.ZoomControl,control.FullscreenControl,geoObject.addon.balloon",
                            }}>
                                <Map className="map"
                                     modules={["multiRouter.MultiRoute", "control.ZoomControl"]}
                                     state={mapState}
                                     options={{restrictMapArea : RESTRICT_AREA}}
                                     instanceRef={map}
                                     onLoad={addObserverClick}
                                >
                                </Map>
                            </YMaps>
                           </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
  );
}

export default App;
