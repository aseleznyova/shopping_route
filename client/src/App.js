import './App.css';
import './index.css'
import { useEffect, useState, useRef} from "react";
import DataInputComponent from "./components/DataInputComponent";
import ResultComponent from "./components/ResultComponent";
import {useDispatch, useSelector} from "react-redux";
import {result} from "./redux/actions/resultState.action";
import { YMaps, Map,Placemark} from '@pbe/react-yandex-maps';
import {api_key} from './conf'
function App() {
    const [dataProducts, dataProductsSet] = useState(null)
    const map = useRef(null);
    const shoppingCart = useSelector(state => state.shoppingCartReducer.shoppingCart)
    const resState = useSelector(state => state.resultStateReducer.resultState)
    const dispatch = useDispatch()
    const [resultProducts, resultProductsSet] = useState(null)
    const [points, pointsSet] = useState([]);
    const ymaps = useRef(null)
    const time_limit = useRef(null);
    const weight_limit = useRef(null);
    let geoObj = null;
    let multiRoute = null;
    const [mapCenter, mapCenterSet] =  useState([59.904883, 30.513427]);
    useEffect(()=>{
        if(!dataProducts){
            fetch('/products').then(response=>response.json())
            .then((json) => {
                dataProductsSet(json)
            })
        }
  },[])
    const addObserverClick = (ym) => {
        ymaps.current = ym;

        map.current.events.add('click', (ev)=>{
            const p = ev.get('coords')
            pointsSet(p);
            if(geoObj){
                map.current.geoObjects.remove(geoObj)
            }
            geoObj = new ym.Placemark(p, {}, {
                preset: "islands#circleDotIcon",
                iconColor: '#ff0000'
            });
            map.current.geoObjects.add(geoObj);
        })
        map.current.events.add('boundschange', (ev)=>{
            mapCenterSet(ev.get('newCenter'));
        })
    }
    const RESTRICT_AREA = [
        [59.921955, 30.498686],
        [59.890619, 30.528230],

    ];

    const addRoute = () => {
        fetch("/route", {
            method: 'POST',
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "time" : time_limit.current.value,
                "weight" : weight_limit.current.value,
                "coordinates": {
                    "longitude" : points[1],
                    "latitude" : points[0]
                },
                "list_products" : shoppingCart
            })
        })
        .then((responce)=>{
            if(responce.status != 201){
                return
            }
            return responce.json()
        }).then((json)=>{
            if(!json){
                return;
            }
            let route_points = []
            for(let i = 0; i < json.route.length; i++){
                route_points.push([json.route[i].latitude, json.route[i].longitude])
            }
            multiRoute = new ymaps.current.multiRouter.MultiRoute(
                {
                    referencePoints: route_points,
                    params: {
                        routingMode: "pedestrian"
                    }
                },
                {
                    boundsAutoApply: true
                }
            );
            resultProductsSet(json);
            dispatch(result());
            map.current.geoObjects.add(multiRoute);
        });
        

    };
    const deleteRoute = ()=>{
        map.current.geoObjects.removeAll();
    }
    function getCurState(){
        if(resState && resultProducts){
            return <ResultComponent resultData={resultProducts} deleteRoute={deleteRoute}/>
        }
        return <DataInputComponent dataProducts={dataProducts} addRoute={addRoute} time_limit={time_limit} weight_limit={weight_limit}/>
    }
  return (
    <div className="App">
        <div>
            <div className="right">
                {
                    getCurState()
                }
            </div>
            sss
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
                                     state={{ center: mapCenter, zoom: 1 ,
                                        controls: ["zoomControl"]}}
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
